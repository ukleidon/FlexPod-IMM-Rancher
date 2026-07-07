# Tenant: `douglasie`

[Tenant index](README.md) | [Tenant directory](../../tenants/douglasie/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/douglasie/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `douglasie` |
| Tenant ID | `11` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `305 / 172.16.35/24` |
| NFS VLAN/CIDR | `306 / 172.16.36/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=douglasie` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=douglasie --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=douglasie -C
ansible-playbook -i inventory TENANT.yml -e tenant=douglasie -e lan_state=absent -C
```
