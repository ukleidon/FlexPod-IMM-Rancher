# Tenant Directories

[Documentation index](../docs/README.md) | [Public tenant examples](../docs/tenants/README.md) | [Variables](../docs/variables.md)

Tenant directories are the source of truth for tenant-local IDs, VLANs, CIDRs, storage identity, API key references, manifests, and platform overrides. In the public repository, this overview is anonymized and does not list deployment-specific tenant names or networks.

Use the public examples in `docs/tenants/` to understand the model:

| Public example | Pattern | What it demonstrates |
| --- | --- | --- |
| `tenant01` | Physical tenant | Dedicated VRF, access/NFS/iSCSI VLANs, tenant SVM, and UCS server profiles. |
| `tenant02` | Virtual tenant | Compact access and NFS network pair for a tenant running on a shared platform. |
| `tenant-hub` | Registry or carrier tenant | `vNN_*` virtual tenant registry ownership and shared platform integration. |

Real tenant names, VLAN IDs, CIDRs, and SVM names should stay in private deployment documentation or overlays.
