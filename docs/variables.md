# Variables and Ownership

[Documentation index](README.md) | [Architecture](architecture.md) | [Tenant guide](tenants/README.md)

The framework separates shared defaults from tenant-local facts. This keeps the common policy naming and boot/storage defaults maintainable while preserving the rule that every tenant can be configured and unconfigured independently.

## File Ownership

| File or directory | Purpose | Configuration to expect |
| --- | --- | --- |
| `group_vars/all.yml` | Global fabric and service defaults. | DNS, NTP, base VLANs, shared feature flags, shared service values. |
| `group_vars/ucs.yml` | Global Cisco Intersight and UCS defaults. | Intersight endpoint, infrastructure org, OOB pool ranges, global UCS policy settings. |
| `group_vars/storagegrid.yml` | Shared StorageGRID integration. | StorageGRID VLANs, port-channel values, grid/client network values. |
| `group_vars/proxmox.yml` | Shared Proxmox integration. | Proxmox Nexus/uplink values. |
| `group_vars/tenant_defaults.yml` | Reusable tenant defaults. | Generated policy names, descriptions, boot defaults, common list defaults. |
| `host_vars/*.yml` | Per-device topology. | Nexus/MDS/ONTAP host-specific interface, peer, and platform settings. |
| `tenants/<tenant>/vars.yml` | Tenant source of truth. | Tenant ID, VLAN IDs, CIDRs, API references, storage identities, profile counts. |
| `tenants/dataspace/vars.yml` | Default virtual tenant registry owner. | `vNN_*` values consumed by virtual tenant logic. |

## What Must Stay Tenant-Local

- `tenant_name`, `tenant_type`, `tid`, and `lan_state`
- VLAN IDs, CIDRs, masks, and VRF names that identify a tenant
- API key references and private key paths
- Storage identities such as SVM, IQN, WWPN, LIF, export, LUN, volume, and pool starts
- Tenant-specific RKE2, Trident, Harvester, app, or manifest values

## What Belongs In Shared Defaults

- Generated names for policies, pools, vNICs, vHBAs, boot policies, and network groups
- Reusable descriptions
- Default masks/netmasks used by most tenants
- Common lists that are identical for all tenants

## Operator Guidance

When a value is repeated in many tenant files, ask two questions before moving it:

1. Is it truly identical for every tenant?
2. Is it not a credential, identity, VLAN, CIDR, or storage endpoint?

Only move it to shared defaults when both answers are yes.
