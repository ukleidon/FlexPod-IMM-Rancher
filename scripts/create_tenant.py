#!/usr/bin/env python3
"""Create a new FlexPod tenant from an existing tenant directory.

Tenant vars are the source of truth. For virtual tenants, the script can also
update the registry-owning tenant vars files that consume the vNN_* values.
Run with --dry-run first to review the plan.
"""

from __future__ import annotations

import argparse
import copy
import ipaddress
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_MARKERS = ("TENANT.yml", "tenants")
VIRTUAL_INDEX_RE = re.compile(r"^v(?P<num>\d+)_name$")


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data: Any) -> bool:
        return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a FlexPod tenant directory and update virtual tenant vars when requested."
    )
    parser.add_argument("--name", required=True, help="New tenant name, for example kastanie.")
    parser.add_argument("--tid", required=True, help="Tenant ID used by the playbooks.")
    parser.add_argument("--access-vlan", type=int, required=True, help="Access/management VLAN ID.")
    parser.add_argument("--access-prefix", required=True, help="Access CIDR prefix without host part, for example 198.51.100.")
    parser.add_argument("--nfs-vlan", type=int, required=True, help="NFS/storage VLAN ID.")
    parser.add_argument("--nfs-prefix", required=True, help="NFS/storage CIDR prefix without host part, for example 203.0.113.")
    parser.add_argument("--source", default="tenant_template", help="Source tenant to clone. Default: tenant_template.")
    parser.add_argument("--tenant-type", default="virtual", help="Tenant type. Default: virtual.")
    parser.add_argument("--ib-vlan", type=int, help="Infrastructure/back-end VLAN ID. Defaults to access VLAN.")
    parser.add_argument("--ib-prefix", help="Infrastructure/back-end CIDR prefix. Defaults to access prefix.")
    parser.add_argument("--iscsi-a-vlan", type=int, help="iSCSI-A VLAN ID. Defaults to NFS VLAN.")
    parser.add_argument("--iscsi-a-prefix", help="iSCSI-A CIDR prefix. Defaults to NFS prefix.")
    parser.add_argument("--iscsi-b-vlan", type=int, help="iSCSI-B VLAN ID. Defaults to NFS VLAN.")
    parser.add_argument("--iscsi-b-prefix", help="iSCSI-B CIDR prefix. Defaults to NFS prefix.")
    parser.add_argument("--mask", type=int, default=24, help="CIDR mask for generated networks. Default: 24.")
    parser.add_argument("--netmask", default="255.255.255.0", help="Dotted netmask for generated networks.")
    parser.add_argument("--api-key-id", help="Tenant Intersight API key id/reference.")
    parser.add_argument("--api-private-key", help="Tenant Intersight private key path.")
    parser.add_argument("--org-name", help="Intersight organization expression/name.")
    parser.add_argument("--num-profiles", type=int, help="Number of server profiles for this tenant.")
    parser.add_argument("--virtual-index", type=int, help="Override the generated vNN index in virtual tenant registry vars.")
    parser.add_argument(
        "--virtual-registry-target",
        action="append",
        help="Tenant vars file to update with vNN data, for example tenant-hub. No registry is updated unless this option is provided.",
    )
    parser.add_argument("--no-virtual-registry", action="store_true", help="Do not update any vNN registry vars files.")
    parser.add_argument("--no-copy-assets", action="store_true", help="Only create vars.yml; do not copy other tenant files/symlinks.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing tenant directory.")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned changes without writing files.")
    return parser.parse_args()


def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def repo_root() -> Path:
    root = Path.cwd()
    missing = [name for name in REPO_MARKERS if not (root / name).exists()]
    if missing:
        die(f"run this script from the FlexPod repository root; missing {', '.join(missing)}")
    return root


def validate_tenant_name(name: str) -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", name):
        die("tenant names may contain lowercase letters, digits, '_' and '-', and must start with a letter or digit")
    return name


def resolve_source_dir_name(source: str) -> str:
    if source in {"tenant_template", "_tenant_template"}:
        return "_tenant_template"
    return validate_tenant_name(source)


def validate_prefix(prefix: str, mask: int) -> str:
    try:
        ipaddress.ip_network(f"{prefix}.0/{mask}", strict=False)
    except ValueError as exc:
        die(f"invalid network prefix {prefix}/{mask}: {exc}")
    return prefix


def recursive_replace(value: Any, old: str, new: str) -> Any:
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [recursive_replace(item, old, new) for item in value]
    if isinstance(value, dict):
        return {
            recursive_replace(key, old, new): recursive_replace(item, old, new)
            for key, item in value.items()
        }
    return value


def load_vars(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    if not isinstance(loaded, dict):
        die(f"{path} does not contain a YAML mapping")
    return loaded


def dump_vars(path: Path, data: dict[str, Any]) -> None:
    rendered = yaml.dump(
        data,
        Dumper=NoAliasDumper,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )
    path.write_text(rendered, encoding="utf-8")


def copy_tenant_assets(source_dir: Path, target_dir: Path, copy_assets: bool) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    if not copy_assets:
        return
    for item in source_dir.iterdir():
        if item.name == "vars.yml":
            continue
        target = target_dir / item.name
        if item.is_symlink():
            target.symlink_to(item.readlink())
        elif item.is_dir():
            shutil.copytree(item, target, symlinks=True)
        else:
            shutil.copy2(item, target)


def jinja_ref(name: str) -> str:
    return "{{ " + name + " }}"


def resolve_value(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    seen = {key}
    while isinstance(value, str):
        match = re.fullmatch(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}", value)
        if not match:
            return value
        next_key = match.group(1)
        if next_key in seen or next_key not in data:
            return value
        seen.add(next_key)
        value = data.get(next_key)
    return value


def virtual_indexes(registry_data: dict[str, Any]) -> dict[int, str]:
    indexes: dict[int, str] = {}
    for key, value in registry_data.items():
        match = VIRTUAL_INDEX_RE.match(str(key))
        if match:
            indexes[int(match.group("num"))] = str(value)
    return indexes


def selected_registry_targets(args: argparse.Namespace) -> list[str]:
    if args.no_virtual_registry or args.tenant_type != "virtual":
        return []
    return args.virtual_registry_target or []


def choose_virtual_index(registry_paths: list[Path], requested: int | None, tenant_name: str) -> int | None:
    if not registry_paths:
        return None
    used: dict[int, str] = {}
    for path in registry_paths:
        if not path.exists():
            die(f"virtual registry vars not found: {path}")
        used.update(virtual_indexes(load_vars(path)))
    if tenant_name in used.values():
        die(f"{tenant_name} already exists in the selected virtual registry vars")
    if requested is not None:
        if requested in used:
            die(f"v{requested} is already assigned to {used[requested]}")
        return requested
    normal_indexes = [index for index in used if index < 98]
    start = max(normal_indexes, default=9) + 1
    for index in range(start, 98):
        if index not in used:
            return index
    for index in range(10, 98):
        if index not in used:
            return index
    die("no free virtual tenant index below v98")
    return None


def ensure_csv_ref(data: dict[str, Any], key: str, ref: str) -> None:
    current = str(data.get(key, "")).strip()
    if not current:
        data[key] = ref
        return
    if ref in current:
        return
    data[key] = f"{current},{ref}"


def ensure_list_entry(data: dict[str, Any], key: str, match_key: str, match_value: str, entry: dict[str, Any]) -> None:
    items = data.setdefault(key, [])
    if not isinstance(items, list):
        die(f"{key} in registry vars must be a list")
    for item in items:
        if isinstance(item, dict) and item.get(match_key) == match_value:
            item.update(entry)
            return
    items.append(entry)


def virtual_payload(index: int, tenant_name: str, data: dict[str, Any]) -> dict[str, Any]:
    prefix = f"v{index}"
    return {
        f"{prefix}_name": tenant_name,
        f"{prefix}_access_vlan_name": jinja_ref(f"{prefix}_name") + "-Access",
        f"{prefix}_access_vlan_id": resolve_value(data, "t_access_vlan_id"),
        f"{prefix}_access_network_prefix": resolve_value(data, "t_access_network_prefix"),
        f"{prefix}_access_network_mask": resolve_value(data, "t_access_network_mask"),
        f"{prefix}_access_network_netmask": resolve_value(data, "t_access_network_netmask"),
        f"{prefix}_nfs_vlan_name": jinja_ref(f"{prefix}_name") + "-NFS",
        f"{prefix}_nfs_vlan_id": resolve_value(data, "t_nfs_vlan_id"),
        f"{prefix}_nfs_network_prefix": resolve_value(data, "t_nfs_network_prefix"),
        f"{prefix}_nfs_network_mask": resolve_value(data, "t_nfs_network_mask"),
        f"{prefix}_nfs_network_netmask": resolve_value(data, "t_nfs_network_netmask"),
    }


def update_virtual_registry(path: Path, index: int, tenant_name: str, data: dict[str, Any]) -> None:
    registry = load_vars(path)
    existing_name = registry.get(f"v{index}_name")
    if existing_name not in (None, tenant_name):
        die(f"{path} already assigns v{index} to {existing_name}")

    registry.update(virtual_payload(index, tenant_name, data))

    access_vlan_id = jinja_ref(f"v{index}_access_vlan_id")
    access_vlan_name = jinja_ref(f"v{index}_access_vlan_name")
    nfs_vlan_id = jinja_ref(f"v{index}_nfs_vlan_id")
    nfs_vlan_name = jinja_ref(f"v{index}_nfs_vlan_name")

    ensure_csv_ref(registry, "t_access_vlans_list", access_vlan_id)
    ensure_csv_ref(registry, "t_storage_vlans_list", nfs_vlan_id)

    ensure_list_entry(
        registry,
        "t_remaining_vlan_list",
        "id",
        access_vlan_id,
        {"name": access_vlan_name, "id": access_vlan_id, "native": "no", "state": "{{lan_state}}"},
    )
    ensure_list_entry(
        registry,
        "t_storage_vlan_list",
        "id",
        nfs_vlan_id,
        {"name": nfs_vlan_name, "id": nfs_vlan_id, "native": "no", "storage_protocol": "NFS", "state": "{{lan_state}}"},
    )
    ensure_list_entry(
        registry,
        "t_svi_list",
        "name",
        access_vlan_id,
        {
            "name": access_vlan_id,
            "vrf": jinja_ref(f"v{index}_name"),
            "address": jinja_ref(f"v{index}_access_network_prefix") + "." + jinja_ref("baseIP") + "/" + jinja_ref(f"v{index}_access_network_mask"),
            "hsrp": jinja_ref(f"v{index}_access_network_prefix") + ".1",
            "gw": jinja_ref(f"v{index}_access_network_prefix") + ".254",
            "metric": "10",
        },
    )
    ensure_list_entry(
        registry,
        "t_svi_list",
        "name",
        nfs_vlan_id,
        {
            "name": nfs_vlan_id,
            "vrf": jinja_ref(f"v{index}_name"),
            "address": jinja_ref(f"v{index}_nfs_network_prefix") + "." + jinja_ref("baseIP") + "/" + jinja_ref(f"v{index}_nfs_network_mask"),
            "hsrp": jinja_ref(f"v{index}_nfs_network_prefix") + ".1",
        },
    )

    dump_vars(path, registry)


def main() -> int:
    args = parse_args()
    root = repo_root()

    new_name = validate_tenant_name(args.name)
    source_name = args.source
    source_dir_name = resolve_source_dir_name(args.source)
    source_dir = root / "tenants" / source_dir_name
    target_dir = root / "tenants" / new_name
    source_vars = source_dir / "vars.yml"
    target_vars = target_dir / "vars.yml"

    if not source_vars.exists():
        die(f"source tenant vars not found: {source_vars}")
    if target_dir.exists() and not args.force:
        die(f"{target_dir} already exists; use --force to replace it")
    if target_dir.exists() and args.force and args.dry_run:
        print(f"Would replace existing {target_dir}")

    mask = args.mask
    netmask = args.netmask
    access_prefix = validate_prefix(args.access_prefix, mask)
    nfs_prefix = validate_prefix(args.nfs_prefix, mask)
    ib_prefix = validate_prefix(args.ib_prefix or args.access_prefix, mask)
    iscsi_a_prefix = validate_prefix(args.iscsi_a_prefix or args.nfs_prefix, mask)
    iscsi_b_prefix = validate_prefix(args.iscsi_b_prefix or args.nfs_prefix, mask)

    data = recursive_replace(copy.deepcopy(load_vars(source_vars)), source_dir_name, new_name)
    data.update(
        {
            "tenant_name": new_name,
            "tenant_type": args.tenant_type,
            "tid": str(args.tid),
            "lan_state": "present",
            "t_ib_vlan_id": args.ib_vlan or args.access_vlan,
            "t_ib_network_prefix": ib_prefix,
            "t_ib_network_mask": mask,
            "t_ib_network_netmask": netmask,
            "t_access_vlan_id": args.access_vlan,
            "t_access_network_prefix": access_prefix,
            "t_access_network_mask": mask,
            "t_access_network_netmask": netmask,
            "t_nfs_vlan_id": args.nfs_vlan,
            "t_nfs_network_prefix": nfs_prefix,
            "t_nfs_network_mask": mask,
            "t_nfs_network_netmask": netmask,
            "t_iscsiA_vlan_id": args.iscsi_a_vlan or args.nfs_vlan,
            "t_iscsiA_network_prefix": iscsi_a_prefix,
            "t_iscsiA_network_mask": mask,
            "t_iscsiA_network_netmask": netmask,
            "t_iscsiB_vlan_id": args.iscsi_b_vlan or args.nfs_vlan,
            "t_iscsiB_network_prefix": iscsi_b_prefix,
            "t_iscsiB_network_mask": mask,
            "t_iscsiB_network_netmask": netmask,
        }
    )

    optional_updates = {
        "api_key_id": args.api_key_id,
        "api_private_key": args.api_private_key,
        "org_name": args.org_name,
        "num_profiles": args.num_profiles,
    }
    data.update({key: value for key, value in optional_updates.items() if value is not None})

    registry_targets = selected_registry_targets(args)
    registry_paths = [root / "tenants" / target / "vars.yml" for target in registry_targets]
    selected_vindex = choose_virtual_index(registry_paths, args.virtual_index, new_name)

    print(f"Source tenant: {source_name}")
    print(f"New tenant:    {new_name}")
    print(f"Target dir:    {target_dir}")
    print(f"Access:        VLAN {data['t_access_vlan_id']} / {data['t_access_network_prefix']}/{mask}")
    print(f"NFS/storage:   VLAN {data['t_nfs_vlan_id']} / {data['t_nfs_network_prefix']}/{mask}")
    if selected_vindex is not None:
        print(f"Virtual index: v{selected_vindex}")
        for path in registry_paths:
            print(f"Registry vars: update {path}")

    if args.dry_run:
        print("\nDry-run only; no files were changed.")
        return 0

    if target_dir.exists() and args.force:
        shutil.rmtree(target_dir)

    copy_tenant_assets(source_dir, target_dir, copy_assets=not args.no_copy_assets)
    dump_vars(target_vars, data)

    if selected_vindex is not None:
        for path in registry_paths:
            update_virtual_registry(path, selected_vindex, new_name, data)

    print("\nCreated tenant files.")
    print("\nRecommended validation:")
    print(f"  ansible-playbook -i inventory TENANT.yml -e tenant={new_name} --syntax-check")
    print(f"  ansible-playbook -i inventory TENANT.yml -e tenant={new_name} -C")
    print(f"  ansible-playbook -i inventory TENANT.yml -e tenant={new_name} -e lan_state=absent -C")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
