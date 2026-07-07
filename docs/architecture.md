# Architecture

[Documentation index](README.md) | [Variables](variables.md) | [Roles](roles/README.md) | [Product references](references.md)

The framework automates a FlexPod-style core infrastructure. FlexPod combines Cisco compute and networking with NetApp storage into a prevalidated architecture. The current framework maps that model into Ansible roles and tenant-specific YAML files.

## Logical Building Blocks

| Layer | Product area | Framework location | Configuration to expect |
| --- | --- | --- | --- |
| Ethernet fabric | Cisco Nexus NX-OS | `roles/INFRA/nexus_*`, `roles/TENANT/nexus_*` | Features, VLANs, trunks, port-channels, vPC, VRFs, SVIs, HSRP, peer-link VLANs. |
| SAN fabric | Cisco MDS or Nexus SAN roles | `roles/INFRA/mds_config`, `roles/INFRA/nexus_san_config` | VSANs, interfaces, device aliases, zones, zonesets. |
| Compute control plane | Cisco Intersight | `roles/*/ucs_*` | Pools, policies, templates, profiles, boot order, LAN/SAN connectivity. |
| Storage | NetApp ONTAP | `roles/*/ontap_*` | SVMs, VLAN ports, broadcast domains, LIFs, volumes, LUNs, igroups, NVMe. |
| Platform services | SUSE RKE2 and NetApp Trident | `roles/rancher/*`, `roles/TENANT/trident_install` | RKE2 cluster services, Kubernetes storage backend, Trident objects. |
| Tenant identity | YAML vars | `tenants/<tenant>/vars.yml` | VLAN IDs, CIDRs, tenant API key references, storage identities, profile counts. |

## Variable Load Order

Tenant playbooks load variables in this order:

1. `group_vars/all.yml`
2. `group_vars/ucs.yml`
3. `group_vars/storagegrid.yml`
4. `group_vars/proxmox.yml`
5. `group_vars/tenant_defaults.yml`
6. `tenants/{{ tenant }}/vars.yml`

Later files override earlier files. This is why tenant identity and tenant-specific networks belong in the tenant vars file.

## FlexPod Reference Alignment

The automation is not a generic data-center toolkit. It assumes a FlexPod-like design with redundant Cisco Nexus switching, UCS/Intersight compute policy control, and NetApp ONTAP shared storage. Use the [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html), [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/), and the CVD [FlexPod Datacenter using IaC with Cisco IMM M7, VMware vSphere 8, and NetApp ONTAP 9.12.1](https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/flexpod_imm_m7_iac.html) as architectural reference points when validating cabling, redundancy, protocol choices, and operational expectations.

## How FlexPod-IMM-Rancher Maps To The CVD Workflow

The CVD presents base infrastructure automation as a staged workflow across Nexus, ONTAP, UCS/Intersight, SAN, VMware, and final storage configuration. FlexPod-IMM-Rancher keeps those technology layers but exposes them through consolidated playbooks:

| CVD stage | FlexPod-IMM-Rancher entry point | What to expect |
| --- | --- | --- |
| Base Nexus, SAN, ONTAP, and Intersight setup | `INFRA.yml` | Shared FlexPod fabric, storage, and Intersight pool objects. |
| Workload or tenant network/storage/compute intent | `TENANT.yml -e tenant=<name>` | One tenant's VLANs, VRFs, storage, policies, profiles, and optional platform configuration. |
| Kubernetes or platform installation | `RKE2.yml -e tenant=<name>` or the RKE2 sections inside `TENANT.yml` | RKE2, Harvester, Trident, or tenant platform integration where inventory and playbook roles exist. |

Use the CVD for the product sequence and prerequisites, and use this repository's playbooks for the current tenant-aware implementation.
