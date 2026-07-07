# Tenant: `silberweide`

[Tenant index](README.md) | [Tenant directory](../../tenants/silberweide/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/silberweide/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `silberweide` |
| Tenant ID | `22` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `395 / 172.16.125/24` |
| NFS VLAN/CIDR | `396 / 172.16.126/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=silberweide` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=silberweide --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=silberweide -C
ansible-playbook -i inventory TENANT.yml -e tenant=silberweide -e lan_state=absent -C
```
