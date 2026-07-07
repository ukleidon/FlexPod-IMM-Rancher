# Tenant Example: `tenant02`

[Tenant examples](README.md) | [Variables](../variables.md) | [Validation](../validation.md)

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

Virtual tenant network and storage intent consumed by a shared platform or hub tenant.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -C
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -e lan_state=absent -C
```
