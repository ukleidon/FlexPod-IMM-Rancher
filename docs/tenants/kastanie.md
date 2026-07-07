# Tenant: `kastanie`

[Tenant index](README.md) | [Tenant directory](../../tenants/kastanie/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/kastanie/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `kastanie` |
| Tenant ID | `33` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `450 / 172.16.180/24` |
| NFS VLAN/CIDR | `451 / 172.16.181/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=kastanie` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=kastanie --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=kastanie -C
ansible-playbook -i inventory TENANT.yml -e tenant=kastanie -e lan_state=absent -C
```
