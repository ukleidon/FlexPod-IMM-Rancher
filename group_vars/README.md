# Group Variables

[Framework README](../README.md) | [Variables](../docs/variables.md)

Group variable files provide shared defaults. Tenant-specific IDs, CIDRs, credentials, storage identities, and API key references should stay in the tenant vars file.

| File                  | Purpose                       | Operator notes                                                        |
| --------------------- | ----------------------------- | --------------------------------------------------------------------- |
| `all.yml`             | Global defaults               | Shared fabric, DNS/NTP, base VLANs, and common toggles.               |
| `mds.yml`             | MDS defaults                  | Shared SAN fabric values.                                             |
| `nexus.yml`           | Nexus defaults                | Shared NX-OS values if included by a playbook or role.                |
| `ontap.yml`           | ONTAP defaults                | Shared ONTAP cluster/protocol values.                                 |
| `proxmox.yml`         | Proxmox integration           | Shared Proxmox network values.                                        |
| `storagegrid.yml`     | StorageGRID integration       | Shared grid/client VLAN and port-channel values.                      |
| `tenant_defaults.yml` | Shared tenant defaults        | Generated names, descriptions, boot defaults, and reusable lists.     |
| `ucs.yml`             | Cisco Intersight/UCS defaults | API endpoint, infrastructure org, OOB pools, and UCS policy defaults. |
| `vmware.yml`          | VMware defaults               | Shared VMware/vCenter values.                                         |
