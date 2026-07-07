#!/usr/bin/env python3
"""Generate a browser-friendly FlexPod architecture overview from Ansible vars."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import sys
from typing import Any

import yaml


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text())
    except Exception as exc:  # pragma: no cover - operator feedback path
        return {"_error": str(exc)}
    return data or {}


def scalar(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ", ".join(scalar(item) for item in value)
    return str(value)


def md_escape(value: Any) -> str:
    text = scalar(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


VAR_PATTERN = re.compile(r"{{\s*([A-Za-z0-9_]+)(?:\s*\|\s*(lower|upper))?\s*}}")


def render_template(value: Any, context: dict[str, Any]) -> Any:
    if not isinstance(value, str):
        return value

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        transform = match.group(2)
        replacement = scalar(context.get(key, match.group(0)))
        if transform == "lower":
            replacement = replacement.lower()
        elif transform == "upper":
            replacement = replacement.upper()
        return replacement

    previous = value
    for _ in range(4):
        current = VAR_PATTERN.sub(replace, previous)
        if current == previous:
            return current
        previous = current
    return previous


def render_deep(value: Any, context: dict[str, Any]) -> Any:
    if isinstance(value, dict):
        return {key: render_deep(item, context) for key, item in value.items()}
    if isinstance(value, list):
        return [render_deep(item, context) for item in value]
    return render_template(value, context)


def cidr(prefix: Any, mask: Any) -> str:
    if prefix in (None, ""):
        return "-"
    if mask in (None, ""):
        return f"{prefix}.0"
    return f"{prefix}.0/{mask}"


def first_item(value: Any) -> dict[str, Any]:
    if isinstance(value, list) and value:
        return value[0] if isinstance(value[0], dict) else {}
    return {}


def role_names_from_playbook(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text()) or []
    roles: list[str] = []
    for play in data:
        for role in play.get("roles") or []:
            if isinstance(role, str):
                roles.append(role)
            elif isinstance(role, dict):
                roles.append(str(role.get("role", "-")))
    return roles


def tenant_records() -> list[dict[str, Any]]:
    base_context: dict[str, Any] = {}
    for relative in [
        "group_vars/all.yml",
        "group_vars/ucs.yml",
        "group_vars/tenant_defaults.yml",
    ]:
        base_context.update(load_yaml(ROOT / relative))

    records: list[dict[str, Any]] = []
    for path in sorted((ROOT / "tenants").glob("*/vars.yml")):
        if path.parent.name.startswith("_"):
            continue
        raw = load_yaml(path)
        context = dict(base_context)
        context.update(raw)
        data = render_deep(raw, context)
        svm = data.get("svm_specs") or {}

        virtual_tenants = []
        for key, value in data.items():
            match = re.fullmatch(r"v(\d+)_name", str(key))
            if not match:
                continue
            number = match.group(1)
            virtual_tenants.append(
                {
                    "number": int(number),
                    "name": value,
                    "access_vlan": data.get(f"v{number}_access_vlan_id"),
                    "access_cidr": cidr(
                        data.get(f"v{number}_access_network_prefix"),
                        data.get(f"v{number}_access_network_mask"),
                    ),
                    "nfs_vlan": data.get(f"v{number}_nfs_vlan_id"),
                    "nfs_cidr": cidr(
                        data.get(f"v{number}_nfs_network_prefix"),
                        data.get(f"v{number}_nfs_network_mask"),
                    ),
                }
            )
        virtual_tenants.sort(key=lambda item: item["number"])

        record = {
            "directory": path.parent.name,
            "tenant_name": data.get("tenant_name", path.parent.name),
            "tenant_type": data.get("tenant_type", "physical"),
            "tid": data.get("tid"),
            "vrf": data.get("vrf_name") or data.get("tenant_name", path.parent.name),
            "num_profiles": data.get("num_profiles"),
            "vlans": {
                "mgmt": data.get("t_ib_vlan_id"),
                "access": data.get("t_access_vlan_id"),
                "nfs": data.get("t_nfs_vlan_id"),
                "iscsi_a": data.get("t_iscsiA_vlan_id"),
                "iscsi_b": data.get("t_iscsiB_vlan_id"),
                "nvme_a": data.get("t_nvme_tcpA_vlan_id"),
                "nvme_b": data.get("t_nvme_tcpB_vlan_id"),
            },
            "cidrs": {
                "mgmt": cidr(data.get("t_ib_network_prefix"), data.get("t_ib_network_mask")),
                "access": cidr(data.get("t_access_network_prefix"), data.get("t_access_network_mask")),
                "nfs": cidr(data.get("t_nfs_network_prefix"), data.get("t_nfs_network_mask")),
                "iscsi_a": cidr(data.get("t_iscsiA_network_prefix"), data.get("t_iscsiA_network_mask")),
                "iscsi_b": cidr(data.get("t_iscsiB_network_prefix"), data.get("t_iscsiB_network_mask")),
            },
            "svm": {
                "name": svm.get("svm_name"),
                "protocols": svm.get("allowed_protocols"),
                "client_match": svm.get("client_match"),
                "mgmt_lif": (svm.get("svm_mgmt_lif") or {}).get("address")
                if isinstance(svm.get("svm_mgmt_lif"), dict)
                else None,
            },
            "virtual_tenants": virtual_tenants,
        }
        records.append(record)
    return records


def connection_rows(nx1: dict[str, Any], nx2: dict[str, Any], nexus: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    mapping = [
        ("uplink", "uplink_PC", "uplink_interface_list", "External/uplink handoff"),
        ("peerlink", "peerlink_PC", "peerlink_interface_list", "Nexus vPC peer-link"),
        ("FI A", "FI_A_PC", "FI_A_interface_list", "UCS Fabric Interconnect A"),
        ("FI B", "FI_B_PC", "FI_B_interface_list", "UCS Fabric Interconnect B"),
        ("Storage A", "storage_A_PC", "storage_A_interface_list", "ONTAP storage node path"),
        ("Storage B", "storage_B_PC", "storage_B_interface_list", "ONTAP storage node path"),
        ("Storage C", "storage_C_PC", "storage_C_interface_list", "ONTAP storage node path"),
        ("Storage D", "storage_D_PC", "storage_D_interface_list", "ONTAP storage node path"),
        ("ASA/firewall", "-", "asa_interface_list", "Transfer/access trunk handoff"),
        ("StorageGRID 01", "-", "sg01_interface_list", "StorageGRID data path"),
        ("StorageGRID 02", "-", "sg02_interface_list", "StorageGRID data path"),
        ("StorageGRID 03", "-", "sg03_interface_list", "StorageGRID data path"),
        ("Proxmox 01", "-", "proxmox01_interface_list", "Proxmox uplink"),
        ("Proxmox 02", "-", "proxmox02_interface_list", "Proxmox uplink"),
    ]
    rows = []
    for label, pc_key, int_key, purpose in mapping:
        pc = "-"
        if pc_key != "-":
            item = first_item(nexus.get(pc_key))
            pc = f"{item.get('interface', '-')}: {item.get('description', '-')}"
        nx1_ports = ", ".join(f"{x.get('interface')} ({x.get('description')})" for x in nx1.get(int_key, [])) or "-"
        nx2_ports = ", ".join(f"{x.get('interface')} ({x.get('description')})" for x in nx2.get(int_key, [])) or "-"
        rows.append((label, pc, nx1_ports, nx2_ports, purpose))
    return rows


def ontap_rows() -> list[tuple[str, str, str, str]]:
    rows = []
    base_context = load_yaml(ROOT / "group_vars/all.yml")
    for path in sorted((ROOT / "host_vars").glob("c250-*.yml")):
        raw = load_yaml(path)
        context = dict(base_context)
        context.update(raw)
        data = render_deep(raw, context)
        nodes = []
        aggregates = []
        for ha_pair in data.get("ha_pairs") or []:
            for node in ha_pair.get("node_specs") or []:
                nodes.append(f"{node.get('node_name')} ({node.get('node_mgmt_ip')})")
                for aggregate in node.get("data_aggregates") or []:
                    aggregates.append(aggregate.get("aggr_name"))
        svm = data.get("svm_specs") or {}
        protocols = ", ".join(svm.get("allowed_protocols") or []) or "-"
        rows.append(
            (
                data.get("cluster_name", path.stem),
                ", ".join(nodes),
                svm.get("svm_name", "-"),
                f"{protocols}; aggregates: {', '.join(aggregates) or '-'}",
            )
        )
    return rows


def san_rows() -> list[tuple[str, str, str, str]]:
    rows = []
    base_context: dict[str, Any] = {}
    for relative in ["group_vars/all.yml", "group_vars/ucs.yml", "group_vars/tenant_defaults.yml"]:
        base_context.update(load_yaml(ROOT / relative))
    for name in ["mdsA", "mdsB", "n9kSSA", "n9kSSB"]:
        path = ROOT / "host_vars" / f"{name}.yml"
        if not path.exists():
            continue
        raw = load_yaml(path)
        context = dict(base_context)
        context.update(raw)
        data = render_deep(raw, context)
        rows.append(
            (
                name,
                scalar(data.get("vsan_name")),
                scalar(data.get("vsan_id")),
                f"zoneset {scalar(data.get('zoneset_name'))}; port-channel {scalar(data.get('port_channel_id'))}",
            )
        )
    return rows


def tenant_table(records: list[dict[str, Any]]) -> str:
    lines = [
        "| Directory | Tenant / type | VRF | VLANs | CIDRs | ONTAP SVM | UCS profiles |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in records:
        vlans = item["vlans"]
        cidrs = item["cidrs"]
        vlan_text = (
            f"mgmt {vlans['mgmt']}<br>access {vlans['access']}<br>"
            f"NFS {vlans['nfs']}<br>iSCSI A/B {vlans['iscsi_a']}/{vlans['iscsi_b']}"
        )
        if vlans["nvme_a"] or vlans["nvme_b"]:
            vlan_text += f"<br>NVMe A/B {vlans['nvme_a']}/{vlans['nvme_b']}"
        cidr_text = (
            f"mgmt {cidrs['mgmt']}<br>access {cidrs['access']}<br>"
            f"NFS {cidrs['nfs']}<br>iSCSI A/B {cidrs['iscsi_a']} / {cidrs['iscsi_b']}"
        )
        svm = item["svm"]
        svm_text = f"{svm['name'] or '-'}<br>{md_escape(svm['protocols'])}<br>client {md_escape(svm['client_match'])}"
        lines.append(
            "| "
            + " | ".join(
                [
                    md_escape(item["directory"]),
                    f"{md_escape(item['tenant_name'])}<br>{md_escape(item['tenant_type'])}, tid {md_escape(item['tid'])}",
                    md_escape(item["vrf"]),
                    vlan_text,
                    cidr_text,
                    svm_text,
                    md_escape(item["num_profiles"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def virtual_table(records: list[dict[str, Any]]) -> str:
    virtuals = []
    for item in records:
        for vt in item["virtual_tenants"]:
            virtuals.append((item["directory"], item["tenant_name"], vt))
    if not virtuals:
        return "No virtual tenant registry entries were detected in tenant vars."
    lines = [
        "| Parent directory | Parent tenant | Virtual tenant | Access VLAN / CIDR | NFS VLAN / CIDR |",
        "| --- | --- | --- | --- | --- |",
    ]
    for parent_dir, parent_name, vt in virtuals:
        lines.append(
            f"| {md_escape(parent_dir)} | {md_escape(parent_name)} | "
            f"v{vt['number']} {md_escape(vt['name'])} | "
            f"{md_escape(vt['access_vlan'])} / {md_escape(vt['access_cidr'])} | "
            f"{md_escape(vt['nfs_vlan'])} / {md_escape(vt['nfs_cidr'])} |"
        )
    return "\n".join(lines)


def table(headers: list[str], rows: list[tuple[Any, ...]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md_escape(item) for item in row) + " |")
    return "\n".join(output)


def managed_roles() -> dict[str, list[str]]:
    return {
        "INFRA.yml": role_names_from_playbook(ROOT / "INFRA.yml"),
        "TENANT.yml": role_names_from_playbook(ROOT / "TENANT.yml"),
        "RKE2.yml": role_names_from_playbook(ROOT / "RKE2.yml"),
    }


def main() -> None:
    all_vars = load_yaml(ROOT / "group_vars/all.yml")
    nexus = load_yaml(ROOT / "group_vars/nexus.yml")
    nx1 = load_yaml(ROOT / "host_vars/nx1.yml")
    nx2 = load_yaml(ROOT / "host_vars/nx2.yml")
    records = tenant_records()
    physical_count = sum(1 for item in records if item["tenant_type"] == "physical")
    virtual_count = sum(1 for item in records if item["tenant_type"] == "virtual")
    virtual_registry_count = sum(len(item["virtual_tenants"]) for item in records)
    roles = managed_roles()

    content = f"""# Architecture Overview Diagram

[Documentation index](README.md) | [Architecture](architecture.md) | [Variables](variables.md) | [Playbooks](playbooks.md) | [Tenants](tenants/README.md)

This page gives a Technical Marketing style overview of the components managed by this Ansible framework. It is generated from the current repository variables and playbooks, so it is intended to explain what the automation is prepared to configure rather than to replace a cabling workbook or a low-level device configuration.

## Current Managed Estate

| Area | Current framework view |
| --- | --- |
| Multi-tenancy mode | `SMT: {md_escape(all_vars.get('SMT'))}` with default fallback VRF `{md_escape(all_vars.get('default_vrf'))}` |
| Tenant directories | {len(records)} total: {physical_count} physical, {virtual_count} virtual |
| Virtual tenant registry entries | {virtual_registry_count} entries across tenant vars with `v##_name` definitions |
| Core Ethernet fabric | Nexus pair `nx1` and `nx2`, vPC domain `{md_escape(nexus.get('vpc_domain_id'))}` |
| Storage system | One NetApp C250 storage system represented by C250-01 and C250-02 controller inventory entries |
| Compute automation | Cisco Intersight API creates UCS pools, policies, templates, and server profiles |
| Enabled shared protocols | iSCSI `{md_escape(all_vars.get('configure_iscsi'))}`, NFS `{md_escape(all_vars.get('configure_nfs'))}`, FC `{md_escape(all_vars.get('configure_fc'))}`, NVMe/TCP `{md_escape(all_vars.get('configure_nvme_tcp'))}`, FC-NVMe `{md_escape(all_vars.get('configure_fc_nvme'))}` |

## Physical Component View

```mermaid
flowchart TB
  operator["Ansible control host<br/>inventory, vars, playbooks"]
  intersight["Cisco Intersight API<br/>UCS pools, policies, templates, profiles"]

  subgraph ethernet["Cisco Nexus Ethernet fabric"]
    nx1["nx1<br/>Nexus A<br/>SVI base IP .2"]
    nx2["nx2<br/>Nexus B<br/>SVI base IP .3"]
    nx1 <-->|"vPC peer-link<br/>port-channel53"| nx2
  end

  upstream["External/uplink network<br/>port-channel52"]
  asa["ASA / firewall handoff<br/>transfer VLAN 3299<br/>tenant access trunk"]
  fi["Cisco UCS Fabric Interconnects<br/>FI-A port-channel49<br/>FI-B port-channel50"]
  ucs["UCS servers<br/>server profiles from templates"]
  subgraph c250["NetApp C250 storage system"]
    ontap1["ONTAP controller C250-01<br/>tenant SVMs and data services"]
    ontap2["ONTAP controller C250-02<br/>partner controller and data services"]
    ontap1 <-->|"HA / cluster interconnect<br/>single C250 storage system"| ontap2
  end
  sg["StorageGRID nodes<br/>client/grid VLANs"]
  proxmox["Proxmox uplinks"]
  k8s["RKE2 / Kubernetes<br/>NetApp Trident backend"]

  operator -->|"network_cli roles"| ethernet
  operator -->|"local ONTAP roles"| ontap1
  operator -->|"local ONTAP roles"| ontap2
  operator -->|"REST API roles"| intersight
  intersight --> fi
  fi -->|"server profile attachment"| ucs
  ethernet -->|"FI trunks: all tenant VLANs"| fi
  ethernet -->|"storage trunks: storage VLANs"| ontap1
  ethernet -->|"storage trunks: storage VLANs"| ontap2
  ethernet -->|"management/access handoff"| upstream
  ethernet -->|"ASA transfer/access VLANs"| asa
  ethernet -->|"StorageGRID VLANs"| sg
  ethernet -->|"Proxmox VLANs"| proxmox
  k8s -->|"CSI persistent volumes"| ontap1
  ucs -->|"OS/RKE2 workloads"| k8s
```

## Logical Tenant Isolation View

```mermaid
flowchart LR
  shared["Shared defaults<br/>group_vars/all.yml<br/>group_vars/tenant_defaults.yml"]
  tenantvars["Tenant vars<br/>tenants/&lt;tenant&gt;/vars.yml"]
  playbook["TENANT.yml<br/>-e tenant=&lt;name&gt;"]

  subgraph vrf["Per-tenant network boundary"]
    tenantvrf["VRF<br/>tenant name or vrf_name override"]
    mgmt["Management VLAN<br/>t_ib_vlan_id / CIDR"]
    access["Access VLAN<br/>t_access_vlan_id / CIDR"]
    nfs["NFS VLAN<br/>t_nfs_vlan_id / CIDR"]
    iscsi["iSCSI A/B VLANs<br/>t_iscsiA/B_vlan_id / CIDR"]
    svi["Nexus SVIs + HSRP<br/>t_svi_list"]
  end

  subgraph storage["Tenant storage boundary"]
    svm["ONTAP SVM<br/>svm_specs.svm_name"]
    lifs["Data and management LIFs<br/>NFS, iSCSI, optional FC/NVMe"]
    vols["Volumes, LUNs, igroups<br/>tenant-local names"]
  end

  subgraph compute["Tenant compute boundary"]
    org["Intersight organization<br/>tenant_name when SMT is true"]
    pools["UUID, MAC, WWPN, IQN, IP pools<br/>tid-based allocation"]
    policies["LAN/SAN/boot/vMedia/BIOS policies"]
    profiles["Server profile template<br/>server profiles"]
  end

  shared --> tenantvars --> playbook
  playbook --> tenantvrf
  tenantvrf --> mgmt
  tenantvrf --> access
  tenantvrf --> nfs
  tenantvrf --> iscsi
  mgmt --> svi
  access --> svi
  nfs --> svi
  iscsi --> svi
  playbook --> svm --> lifs --> vols
  playbook --> org --> pools --> policies --> profiles
  profiles -->|"host consumes storage networks"| lifs
```

## Playbook And Role Flow

```mermaid
flowchart TB
  infra["INFRA.yml<br/>shared FlexPod base"]
  tenant["TENANT.yml<br/>one tenant at a time"]
  rke["RKE2.yml<br/>platform configuration"]

  infra --> infnexus["INFRA/nexus_*<br/>features, VLANs, vPC, ASA, SG, Proxmox"]
  infra --> infontap["INFRA/ontap_*<br/>network, SVM, volumes, LIFs"]
  infra --> infucs["INFRA/ucs_create_pools<br/>shared Intersight pools"]

  tenant --> tnexus["TENANT/nexus_*<br/>tenant VLANs, VRF, SVIs, trunks"]
  tenant --> tontap["TENANT/ontap_*<br/>tenant SVM, LIFs, volumes, LUNs, NVMe"]
  tenant --> tucs["TENANT/ucs_*<br/>tenant pools, policies, templates, profiles"]
  tenant --> os["TENANT/os_install_suse<br/>OS installation workflow"]
  tenant --> trident["TENANT/trident_install<br/>Kubernetes storage backend"]

  rke --> pre["rancher/pre_rke_install"]
  rke --> server["rancher/rke2_server"]
  rke --> agent["rancher/rke2_agent"]
```

## Network Connections Managed By The Framework

{table(["Connection", "Port-channel", "nx1 interfaces", "nx2 interfaces", "Purpose"], connection_rows(nx1, nx2, nexus))}

## ONTAP Controller And SAN Objects

The physical view treats C250-01 and C250-02 as connected controllers in the same NetApp C250 storage system. The table below keeps the inventory entries visible because the playbooks target them through `host_vars/c250-*.yml`.

{table(["Storage inventory entry", "Node details from vars", "Infrastructure SVM", "Protocols and aggregates"], ontap_rows())}

{table(["SAN device", "VSAN name", "VSAN ID", "Zoning / port-channel intent"], san_rows())}

## Tenant Catalog

Each row below comes from `tenants/<tenant>/vars.yml`. For secure multi-tenancy, the VRF normally follows the tenant name; a tenant can override that with `vrf_name` when it intentionally uses a shared or upstream VRF.

{tenant_table(records)}

## Virtual Tenant Registry

The registry below shows `v##_name` definitions found inside tenant vars. These are used by carrier tenants such as the DataSpace/Harvester definitions to publish virtual tenant access and NFS VLANs from a parent tenant context.

{virtual_table(records)}

## Managed Role Inventory

| Playbook | Roles called |
| --- | --- |
| `INFRA.yml` | {md_escape('<br>'.join(roles['INFRA.yml']))} |
| `TENANT.yml` | {md_escape('<br>'.join(roles['TENANT.yml']))} |
| `RKE2.yml` | {md_escape('<br>'.join(roles['RKE2.yml']))} |

## How To Explain This To An Audience

The easiest story is to present the framework in three layers:

1. The FlexPod base layer provides redundant Nexus switching, ONTAP storage, and Intersight-controlled UCS compute.
2. The tenant layer adds one isolated VRF, a small set of tenant VLANs and CIDRs, a tenant SVM, and tenant-scoped Intersight objects.
3. The platform layer consumes that tenant boundary for RKE2, Harvester, Trident, or other workloads.

That framing makes the separation model visible: shared hardware and shared automation patterns below, tenant-local network/storage/compute identities above.

## Related Design References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
"""

    output = ROOT / "docs" / "architecture-overview.md"
    output.write_text(content)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
