# Public Tenant Examples

[Documentation index](../README.md) | [New tenant guide](new-tenant.md) | [Variables](../variables.md)

Tenant files are the source of truth for tenant-local IDs, VLANs, CIDRs, storage identity, API key references, and platform overrides. The public documentation uses neutral sample tenants and documentation networks. Internal tenant names and live addressing belong in private deployment documentation or overlays.

| Public example | Pattern | What it demonstrates |
| --- | --- | --- |
| [tenant01](tenant01.md) | Physical tenant | Dedicated VRF, access/NFS/iSCSI VLANs, tenant SVM, and UCS server profiles. |
| [tenant02](tenant02.md) | Virtual tenant | Compact access and NFS network pair for a tenant running on a shared platform. |
| [tenant-hub](tenant-hub.md) | Registry or carrier tenant | `vNN_*` virtual tenant registry ownership and shared platform integration. |

Use these examples to understand the expected structure. Use the `tenant_template` source alias as the neutral starting point for new public examples, and use private tenant directories only in deployment-specific branches or overlays.
