# Tenant: `feldahorn`

[Tenant index](README.md) | [Tenant directory](../../tenants/feldahorn/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/feldahorn/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `feldahorn` |
| Tenant ID | `20` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `380 / 172.16.110/24` |
| NFS VLAN/CIDR | `381 / 172.16.111/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=feldahorn` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=feldahorn --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=feldahorn -C
ansible-playbook -i inventory TENANT.yml -e tenant=feldahorn -e lan_state=absent -C
```
