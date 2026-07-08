# Public Tenant Examples

[Documentation index](../README.md) | [Workflows](../workflows.md) | [New tenant guide](new-tenant.md) | [Variables](../variables.md)

Tenant files are the source of truth for tenant-local IDs, VLANs, CIDRs, storage identity, API key references, and platform overrides. The public documentation uses neutral sample tenants and documentation networks. Internal tenant names and live addressing belong in private deployment documentation or overlays.

| Public example | Pattern | What it demonstrates |
| --- | --- | --- |
| [tenant01](tenant01.md) | Physical tenant | Dedicated VRF, access/NFS/iSCSI VLANs, tenant SVM, and UCS server profiles. |
| [tenant02](tenant02.md) | Virtual tenant | Compact access and NFS network pair for a tenant running on a shared platform. |
| [tenant-hub](tenant-hub.md) | Platform or registry tenant | Bare-metal Rancher and Harvester HCI plus `vNN_*` virtual tenant registry ownership. |

Use these examples to understand the expected structure. Use the `tenant_template` source alias as the neutral starting point for new public examples, and use private tenant directories only in deployment-specific branches or overlays.

## Placement Model

| Tenant type | Main playbooks | What to validate |
| --- | --- | --- |
| Physical | `TENANT.yml`, optional `RKE2.yml` | Nexus VRF/VLANs, ONTAP SVM/LIFs/LUNs, Intersight pools/policies/profiles, iSCSI boot, optional bare-metal RKE2. |
| Virtual | `HARVESTER.yml`, `HARVESTER_RKE.yml` | Harvester namespace, access/storage networks, DHCP pools, tenant cloud-init, Rancher-created `<tenant>-rke` cluster. |
| Platform or registry | `TENANT.yml`, optional `RKE2.yml` | Bare-metal Rancher, Harvester HCI hosts, virtual tenant registry values, shared storage integrations. |

The tenant vars file remains the source of truth. `vtenants.lst` is not used in the public workflow.
