# Tenant: `rotbuche`

[Tenant index](README.md) | [Tenant directory](../../tenants/rotbuche/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/rotbuche/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `rotbuche` |
| Tenant ID | `23` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `365 / 172.16.95/24` |
| NFS VLAN/CIDR | `366 / 172.16.96/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=rotbuche` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=rotbuche --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=rotbuche -C
ansible-playbook -i inventory TENANT.yml -e tenant=rotbuche -e lan_state=absent -C
```
