# Architecture

[Documentation index](README.md) | [Overview diagrams](architecture-overview.md) | [Workflows](workflows.md) | [Variables](variables.md) | [Roles](roles/README.md) | [Product references](references.md)

The framework automates a FlexPod-style core infrastructure. FlexPod combines Cisco compute and networking with NetApp storage into a prevalidated architecture. The current framework maps that model into Ansible roles and tenant-specific YAML files. For a visual audience-facing view of the configured devices, tenant VRFs, SVMs, and server profile flow, open [Architecture overview diagrams](architecture-overview.md).

## Logical Building Blocks

| Layer | Product area | Framework location | Configuration to expect |
| --- | --- | --- | --- |
| Ethernet fabric | Cisco Nexus NX-OS | `roles/INFRA/nexus_*`, `roles/TENANT/nexus_*` | Features, VLANs, trunks, port-channels, vPC, VRFs, SVIs, HSRP, peer-link VLANs. |
| SAN fabric | Cisco MDS or Nexus SAN roles | `roles/INFRA/mds_config`, `roles/INFRA/nexus_san_config` | VSANs, interfaces, device aliases, zones, zonesets. |
| Compute control plane | Cisco Intersight | `roles/*/ucs_*` | Pools, policies, templates, profiles, boot order, LAN/SAN connectivity. |
| Storage | NetApp ONTAP | `roles/*/ontap_*` | SVMs, VLAN ports, broadcast domains, LIFs, volumes, LUNs, igroups, NVMe. |
| Physical platform services | SUSE RKE2, Rancher, and NetApp Trident | `roles/rancher/*`, `roles/TENANT/trident_install` | Bare-metal RKE2/Rancher services, Kubernetes storage backend, Trident objects. |
| Harvester HCI | SUSE Harvester and Rancher integration | `roles/harvester/*`, `roles/TENANT/harvester_tenant_config`, `roles/rancher/harvester_*` | Harvester platform settings, tenant namespaces, Harvester networks, DHCP pools, cloud-init templates, Rancher-provisioned virtual RKE2 clusters. |
| Tenant identity | YAML vars | `tenants/<tenant>/vars.yml` | VLAN IDs, CIDRs, tenant API key references, storage identities, profile counts. |

## Variable Load Order

Tenant playbooks load variables in this order:

1. `group_vars/all.yml`
2. `group_vars/ucs.yml`
3. `group_vars/storagegrid.yml`
4. `group_vars/mgmt-cluster.yml`
5. `group_vars/tenant_defaults.yml`
6. `tenants/{{ tenant }}/vars.yml`

Later files override earlier files. This is why tenant identity and tenant-specific networks belong in the tenant vars file.

## Tenant Execution Model

The public model separates tenants by placement as well as by network and storage identity:

| Tenant pattern | Where it runs | Automation entry points | Typical configuration |
| --- | --- | --- | --- |
| Physical platform tenant | Bare-metal UCS profiles | `TENANT.yml`, `RKE2.yml` | Rancher management plane, Harvester HCI hosts, ONTAP iSCSI boot LUNs, Trident storage backend. |
| Virtual tenant | VMs on Harvester HCI | `HARVESTER.yml`, `HARVESTER_RKE.yml` | Harvester namespace, access/storage networks, DHCP pools, tenant cloud-init ConfigMap, Rancher-created `<tenant>-rke` cluster. |
| Physical workload tenant | Bare-metal UCS profiles | `TENANT.yml` | Tenant VRF, VLANs, ONTAP SVM, iSCSI boot, Intersight policies, server profiles. |

Every tenant must remain independently configurable and removable. Do not make one tenant depend on another tenant directory for lifecycle operations. If a platform or hub tenant publishes virtual tenant registry values, treat that registry as an input source and keep the actual virtual tenant source of truth in the selected tenant vars file.

## FlexPod Reference Alignment

The automation is not a generic data-center toolkit. It assumes a FlexPod-like design with redundant Cisco Nexus switching, UCS/Intersight compute policy control, and NetApp ONTAP shared storage. Use the [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html), [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/), and the CVD [FlexPod Datacenter using IaC with Cisco IMM M7, VMware vSphere 8, and NetApp ONTAP 9.12.1](https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/flexpod_imm_m7_iac.html) as architectural reference points when validating cabling, redundancy, protocol choices, and operational expectations.

## How FlexPod-IMM-Rancher Maps To The CVD Workflow

The CVD presents base infrastructure automation as a staged workflow across Nexus, ONTAP, UCS/Intersight, SAN, VMware, and final storage configuration. FlexPod-IMM-Rancher keeps those technology layers but exposes them through consolidated playbooks:

| CVD stage | FlexPod-IMM-Rancher entry point | What to expect |
| --- | --- | --- |
| Base Nexus, SAN, ONTAP, and Intersight setup | `INFRA.yml` | Shared FlexPod fabric, storage, and Intersight pool objects. |
| Workload or tenant network/storage/compute intent | `TENANT.yml -e tenant=<name>` | One tenant's VLANs, VRFs, storage, policies, profiles, and optional platform configuration. |
| Physical Kubernetes platform installation | `RKE2.yml -e tenant=<name>` or the RKE2 sections inside `TENANT.yml` | Bare-metal RKE2 and Rancher components where matching inventory hosts exist. |
| Harvester tenant support | `HARVESTER.yml -e tenant=<name>` | Harvester tenant namespace, access/storage NetworkAttachmentDefinitions, DHCP IPPools, and tenant cloud-init template. |
| Virtual RKE2 on Harvester | `HARVESTER_RKE.yml -e tenant=<name>` | Rancher HarvesterConfig and Cluster resources for a default three-node `<tenant>-rke` RKE2 cluster. |

Use the CVD for the product sequence and prerequisites, and use this repository's playbooks for the current tenant-aware implementation.

## Harvester And Rancher Integration

The Harvester workflow assumes the Ansible control node has kubeconfig contexts for the Harvester cluster and the Rancher management plane. Public defaults use `harvester` and `rancher`; private deployments should override those names if their kubeconfig uses different context names.

`HARVESTER.yml` reads the `sle-micro-default` cloud-init ConfigMap from Harvester, replaces the `[TENANT]` token with the lower-case tenant name, and writes tenant-local manifests under `tenants/<tenant>/manifests/harvester` on live runs. `HARVESTER_RKE.yml` then creates Rancher provisioning resources that use the tenant networks and cloud-init data.

Rancher cloud credential names, cloud-provider config secret references, and creator IDs are intentionally placeholders in the public repository. Store live values in private variable files, Ansible Vault, environment-backed overlays, or a private deployment repository.
