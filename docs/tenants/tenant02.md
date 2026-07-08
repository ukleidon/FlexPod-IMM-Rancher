# Tenant Example: `tenant02`

[Tenant examples](README.md) | [Workflows](../workflows.md) | [Variables](../variables.md) | [Validation](../validation.md)

This public page describes the tenant pattern without exposing internal tenant names, hostnames, VLAN IDs, or CIDRs.

## Tenant Facts

| Field | Public example |
| --- | --- |
| Tenant name | `tenant02` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `312 / 198.51.100.0/24` |
| NFS VLAN/CIDR | `313 / 203.0.113.0/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=<tenant-name>` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

Virtual tenant network and storage intent consumed by a shared platform or hub tenant. `HARVESTER.yml` creates the tenant namespace, access/storage networks, DHCP pools, and tenant cloud-init ConfigMap. `HARVESTER_RKE.yml` can then ask Rancher to create the default three-node `tenant02-rke` cluster on Harvester.

## Operator Checks

```bash
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant02 --syntax-check
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant02 -C
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant02 --syntax-check
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant02 -C
```
