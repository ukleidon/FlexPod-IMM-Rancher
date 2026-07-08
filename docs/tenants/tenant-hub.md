# Tenant Example: `tenant-hub`

[Tenant examples](README.md) | [Workflows](../workflows.md) | [Variables](../variables.md) | [Validation](../validation.md)

This public page describes the tenant pattern without exposing internal tenant names, hostnames, VLAN IDs, or CIDRs.

## Tenant Facts

| Field | Public example |
| --- | --- |
| Tenant name | `tenant-hub` |
| Tenant type | `platform / registry` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `registry defined` |
| NFS VLAN/CIDR | `registry defined` |

## Configuration To Expect

Running `TENANT.yml -e tenant=<tenant-name>` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

Physical platform tenant that runs bare-metal Rancher and Harvester HCI, owns `vNN_*` entries, and publishes virtual tenant VLAN/CIDR mappings. UCS server profiles for this tenant boot from ONTAP iSCSI LUNs, and Harvester then hosts virtual tenant VMs.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant-hub --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant-hub -C
ansible-playbook -i inventory RKE2.yml -e tenant=tenant-hub -C
```
