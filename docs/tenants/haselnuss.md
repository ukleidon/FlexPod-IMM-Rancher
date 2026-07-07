# Tenant: `haselnuss`

[Tenant index](README.md) | [Tenant directory](../../tenants/haselnuss/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/haselnuss/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `haselnuss` |
| Tenant ID | `24` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `405 / 172.16.135/24` |
| NFS VLAN/CIDR | `406 / 172.16.136/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=haselnuss` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=haselnuss --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=haselnuss -C
ansible-playbook -i inventory TENANT.yml -e tenant=haselnuss -e lan_state=absent -C
```
