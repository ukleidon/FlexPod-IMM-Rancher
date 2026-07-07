#!/usr/bin/env python3
"""Generate public-safe documentation pages for FlexPod-IMM-Rancher.

The public repository intentionally keeps the framework mechanics visible while
using neutral sample device names, tenant names, and documentation networks in
rendered Markdown. Internal, site-specific values belong in private deployment docs.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate public-safe FlexPod documentation.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root. Default: current directory.")
    parser.add_argument(
        "--architecture-only",
        action="store_true",
        help="Only regenerate docs/architecture-overview.md.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text()) or {}
    except Exception:
        return {}


def role_names_from_playbook(path: Path) -> list[str]:
    plays = load_yaml(path)
    if not isinstance(plays, list):
        return []
    roles: list[str] = []
    for play in plays:
        if not isinstance(play, dict):
            continue
        for role in play.get("roles") or []:
            if isinstance(role, str):
                roles.append(role)
            elif isinstance(role, dict):
                roles.append(str(role.get("role", "-")))
    return roles


def md_escape(value: Any) -> str:
    text = "-" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[tuple[Any, ...]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md_escape(item) for item in row) + " |")
    return "\n".join(output)


def managed_roles(root: Path) -> dict[str, list[str]]:
    return {
        name: role_names_from_playbook(root / name)
        for name in ["INFRA.yml", "TENANT.yml", "RKE2.yml"]
        if (root / name).exists()
    }


def generate_architecture(root: Path) -> None:
    roles = managed_roles(root)
    connection_rows = [
        ("External network", "Nexus peer uplink port-channel", "Data center, campus, or firewall handoff"),
        ("Cisco UCS Fabric Interconnect A", "Nexus vPC member port-channel", "Carries management, access, and storage VLANs to UCS fabric A"),
        ("Cisco UCS Fabric Interconnect B", "Nexus vPC member port-channel", "Carries management, access, and storage VLANs to UCS fabric B"),
        ("NetApp storage controller A", "Nexus storage port-channel pair", "Carries tenant storage VLANs and storage LIF traffic"),
        ("NetApp storage controller B", "Nexus storage port-channel pair", "Carries tenant storage VLANs and storage LIF traffic"),
        ("Firewall or routed edge", "Tenant access and transfer VLAN trunks", "Provides north-south routing or security policy outside the tenant VRF"),
        ("Optional StorageGRID", "StorageGRID client and grid VLAN trunks", "Adds object-storage connectivity when the role set is used"),
        ("Optional virtualization hosts", "Hypervisor uplinks", "Carries workload and storage networks to non-UCS hosts when configured"),
    ]

    tenant_rows = [
        (
            "tenant01",
            "physical",
            "tenant01",
            "mgmt 301<br>access 302<br>NFS 303<br>iSCSI A/B 304/305",
            "mgmt 192.0.2.0/24<br>access 198.51.100.0/24<br>NFS 203.0.113.0/24",
            "tenant01_svm<br>NFS and optional iSCSI",
            "3",
        ),
        (
            "tenant02",
            "virtual",
            "tenant02",
            "access 312<br>NFS 313",
            "access 198.51.100.0/24<br>NFS 203.0.113.0/24",
            "tenant02_svm<br>NFS",
            "3",
        ),
        (
            "tenant-hub",
            "carrier / registry",
            "shared or upstream VRF",
            "registry publishes vNN access/NFS VLANs",
            "documentation networks only",
            "shared SVM or delegated tenant SVMs",
            "deployment-specific",
        ),
    ]

    virtual_rows = [
        ("tenant-hub", "v10 tenant01", "access VLAN 302 / 198.51.100.0/24", "NFS VLAN 303 / 203.0.113.0/24"),
        ("tenant-hub", "v11 tenant02", "access VLAN 312 / 198.51.100.0/24", "NFS VLAN 313 / 203.0.113.0/24"),
        ("tenant-hub", "v12 tenant03", "access VLAN 322 / 198.51.100.0/24", "NFS VLAN 323 / 203.0.113.0/24"),
    ]

    role_rows = [
        (playbook, "<br>".join(role_list) or "-")
        for playbook, role_list in roles.items()
    ]

    content = f"""# Architecture Overview Diagram

[Documentation index](README.md) | [Architecture](architecture.md) | [Variables](variables.md) | [Playbooks](playbooks.md) | [Tenants](tenants/README.md)

This page gives a Technical Marketing style overview of the components managed by this Ansible framework. Because this is the public FlexPod-IMM-Rancher repository, device names, tenant names, VLAN IDs, and IP networks in this page are anonymized examples. Private deployment documentation can keep the full site-specific values.

## Current Public View

| Area | Public documentation view |
| --- | --- |
| Multi-tenancy mode | Secure multi-tenancy with one logical VRF boundary per tenant |
| Tenant examples | Public docs show neutral sample tenants while private deployment docs keep the real tenant catalog |
| Core Ethernet fabric | Redundant Cisco Nexus pair with vPC, peer-link, VLAN trunks, SVIs, and HSRP |
| Storage system | One NetApp C-Series storage system represented as two connected ONTAP controllers |
| Compute automation | Cisco Intersight API creates UCS pools, policies, templates, and server profiles |
| Enabled shared protocols | NFS and iSCSI are the primary public examples; FC, NVMe/TCP, and FC-NVMe are role-supported patterns |

## Physical Component View

```mermaid
flowchart TB
  operator["Ansible control host<br/>inventory, vars, playbooks"]
  intersight["Cisco Intersight API<br/>UCS pools, policies, templates, profiles"]

  subgraph ethernet["Cisco Nexus Ethernet fabric"]
    nxa["Nexus A<br/>SVI/HSRP peer"]
    nxb["Nexus B<br/>SVI/HSRP peer"]
    nxa <-->|"vPC peer-link"| nxb
  end

  upstream["External or routed network<br/>uplink handoff"]
  firewall["Firewall / edge handoff<br/>transfer and access VLAN trunks"]
  fi["Cisco UCS Fabric Interconnect pair<br/>FI-A and FI-B"]
  ucs["UCS servers<br/>server profiles from templates"]
  subgraph storage["NetApp C-Series storage system"]
    storagea["ONTAP controller A<br/>tenant SVMs and data services"]
    storageb["ONTAP controller B<br/>partner controller and data services"]
    storagea <-->|"HA / cluster interconnect<br/>single storage system"| storageb
  end
  objectstore["Optional StorageGRID<br/>client/grid VLANs"]
  hypervisor["Optional virtualization hosts<br/>workload and storage uplinks"]
  k8s["RKE2 / Kubernetes<br/>NetApp Trident backend"]

  operator -->|"network_cli roles"| ethernet
  operator -->|"local ONTAP roles"| storage
  operator -->|"REST API roles"| intersight
  intersight --> fi
  fi -->|"server profile attachment"| ucs
  ethernet -->|"FI trunks: tenant VLAN sets"| fi
  ethernet -->|"storage trunks: storage VLAN sets"| storage
  ethernet -->|"north-south handoff"| upstream
  ethernet -->|"edge transfer/access VLANs"| firewall
  ethernet -->|"optional object-storage VLANs"| objectstore
  ethernet -->|"optional hypervisor VLANs"| hypervisor
  ucs -->|"OS/RKE2 workloads"| k8s
  k8s -->|"CSI persistent volumes"| storage
```

## Logical Tenant Isolation View

```mermaid
flowchart LR
  shared["Shared defaults<br/>group_vars/all.yml<br/>group_vars/tenant_defaults.yml"]
  tenantvars["Tenant vars<br/>tenants/&lt;tenant&gt;/vars.yml"]
  playbook["TENANT.yml<br/>-e tenant=&lt;name&gt;"]

  subgraph vrf["Per-tenant network boundary"]
    tenantvrf["Tenant VRF<br/>tenant name or vrf_name override"]
    mgmt["Management VLAN<br/>tenant management CIDR"]
    access["Access VLAN<br/>workload access CIDR"]
    nfs["NFS VLAN<br/>storage CIDR"]
    iscsi["iSCSI A/B VLANs<br/>boot or block storage CIDRs"]
    svi["Nexus SVIs + HSRP<br/>tenant routing boundary"]
  end

  subgraph storageTenant["Tenant storage boundary"]
    svm["ONTAP SVM<br/>tenant SVM name"]
    lifs["Data and management LIFs<br/>NFS, iSCSI, optional FC/NVMe"]
    vols["Volumes, LUNs, igroups<br/>tenant-local names"]
  end

  subgraph compute["Tenant compute boundary"]
    org["Intersight organization<br/>tenant-scoped when SMT is enabled"]
    pools["UUID, MAC, WWPN, IQN, IP pools<br/>tenant allocation block"]
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

  infra --> infnexus["INFRA/nexus_*<br/>features, VLANs, vPC, edge, object storage, hypervisor uplinks"]
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

{table(["Connection", "Public label", "Purpose"], connection_rows)}

## Storage And SAN Objects

The physical view treats both ONTAP controllers as connected controllers in the same NetApp storage system. Public docs do not expose site-specific controller hostnames, management IPs, or aggregate names.

{table(["Object", "Public label", "Configuration to expect"], [
    ("ONTAP controller A", "Storage controller A", "Node management, data aggregates, broadcast domains, VLAN ports, LIFs"),
    ("ONTAP controller B", "Storage controller B", "Partner node management, data aggregates, broadcast domains, VLAN ports, LIFs"),
    ("Tenant SVM", "tenant##_svm", "Root volume, management LIF, data LIFs, protocol services, export or block access"),
    ("SAN fabric A", "SAN-A", "VSAN, device aliases, zones, and zoneset for fabric A"),
    ("SAN fabric B", "SAN-B", "VSAN, device aliases, zones, and zoneset for fabric B"),
])}

## Public Tenant Examples

The table below is illustrative. Real tenant names, VLAN IDs, CIDRs, and SVM names are intentionally kept out of the public documentation.

{table(["Tenant", "Type", "VRF", "Example VLANs", "Example CIDRs", "Storage", "Profiles"], tenant_rows)}

## Virtual Tenant Registry Example

Carrier or hub tenants can publish `vNN_*` registry entries for virtual tenants. The public view shows the pattern without exposing the internal registry names.

{table(["Registry owner", "Virtual tenant", "Access network", "NFS network"], virtual_rows)}

## Managed Role Inventory

| Playbook | Roles called |
| --- | --- |
"""

    for playbook, roles_text in role_rows:
        content += f"| `{md_escape(playbook)}` | {md_escape(roles_text)} |\n"

    content += """
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

    output = root / "docs" / "architecture-overview.md"
    output.write_text(content)
    print(f"Wrote {output}")


def write_tenant_docs(root: Path) -> None:
    tenant_dir = root / "docs" / "tenants"
    tenant_dir.mkdir(parents=True, exist_ok=True)

    for path in tenant_dir.glob("*.md"):
        if path.name not in {"README.md", "new-tenant.md"}:
            path.unlink()

    (tenant_dir / "README.md").write_text("""# Public Tenant Examples

[Documentation index](../README.md) | [New tenant guide](new-tenant.md) | [Variables](../variables.md)

Tenant files are the source of truth for tenant-local IDs, VLANs, CIDRs, storage identity, API key references, and platform overrides. The public documentation uses neutral sample tenants and documentation networks. Internal tenant names and live addressing belong in private deployment documentation or overlays.

| Public example | Pattern | What it demonstrates |
| --- | --- | --- |
| [tenant01](tenant01.md) | Physical tenant | Dedicated VRF, access/NFS/iSCSI VLANs, tenant SVM, and UCS server profiles. |
| [tenant02](tenant02.md) | Virtual tenant | Compact access and NFS network pair for a tenant running on a shared platform. |
| [tenant-hub](tenant-hub.md) | Registry or carrier tenant | `vNN_*` virtual tenant registry ownership and shared platform integration. |

Use these examples to understand the expected structure. Use the `tenant_template` source alias as the neutral starting point for new public examples, and use private tenant directories only in deployment-specific branches or overlays.
""")

    samples = {
        "tenant01.md": (
            "tenant01",
            "physical",
            "301 / 192.0.2.0/24",
            "303 / 203.0.113.0/24",
            "Dedicated VRF, tenant SVM, NFS/iSCSI storage, Intersight policies, templates, and server profiles.",
        ),
        "tenant02.md": (
            "tenant02",
            "virtual",
            "312 / 198.51.100.0/24",
            "313 / 203.0.113.0/24",
            "Virtual tenant network and storage intent consumed by a shared platform or hub tenant.",
        ),
        "tenant-hub.md": (
            "tenant-hub",
            "carrier / registry",
            "registry defined",
            "registry defined",
            "Parent tenant that owns `vNN_*` entries and publishes virtual tenant VLAN/CIDR mappings.",
        ),
    }

    for filename, (name, tenant_type, access, nfs, expectation) in samples.items():
        (tenant_dir / filename).write_text(f"""# Tenant Example: `{name}`

[Tenant examples](README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This public page describes the tenant pattern without exposing internal tenant names, hostnames, VLAN IDs, or CIDRs.

## Tenant Facts

| Field | Public example |
| --- | --- |
| Tenant name | `{name}` |
| Tenant type | `{tenant_type}` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `{access}` |
| NFS VLAN/CIDR | `{nfs}` |

## Configuration To Expect

Running `TENANT.yml -e tenant=<tenant-name>` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

{expectation}

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -C
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -e lan_state=absent -C
```
""")

    (tenant_dir / "new-tenant.md").write_text("""# New Tenant Guide

[Tenant examples](README.md) | [Variables](../variables.md) | [Validation](../validation.md)

Use this guide to create a new tenant from a template while keeping tenant-specific values isolated in `tenants/<tenant>/vars.yml`.

The public example values below use documentation networks. Replace them with deployment-specific VLANs, CIDRs, tenant names, and key references in a private branch or overlay.

## Example Input

| Field | Example value | Purpose |
| --- | --- | --- |
| Tenant name | `tenant41` | Directory name and default tenant identity. |
| Tenant ID | `41` | Used for generated pools such as MAC, WWPN, UUID, or IQN ranges. |
| Access VLAN/CIDR | `455 / 198.51.100.0/24` | Used for access and management-side traffic. |
| NFS VLAN/CIDR | `456 / 203.0.113.0/24` | Used for storage/NFS traffic. |

## Dry Run First

```bash
./scripts/create_tenant.py \\
  --name tenant41 \\
  --tid 41 \\
  --access-vlan 455 \\
  --access-prefix 198.51.100 \\
  --nfs-vlan 456 \\
  --nfs-prefix 203.0.113 \\
  --source tenant_template \\
  --dry-run
```

For virtual tenants, the script can update one or more registry vars files with `vNN_*` values. In public documentation, call this a registry or hub tenant. In a private deployment, select the real registry tenant name.

## Create The Tenant

```bash
./scripts/create_tenant.py \\
  --name tenant41 \\
  --tid 41 \\
  --access-vlan 455 \\
  --access-prefix 198.51.100 \\
  --nfs-vlan 456 \\
  --nfs-prefix 203.0.113 \\
  --source tenant_template
```

## Validate

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant41 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant41 -C
```
""")

    print(f"Wrote public tenant docs in {tenant_dir}")


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    if not (root / "TENANT.yml").exists():
        raise SystemExit(f"{root} does not look like the FlexPod-IMM-Rancher repository root")
    generate_architecture(root)
    if not args.architecture_only:
        write_tenant_docs(root)


if __name__ == "__main__":
    main()
