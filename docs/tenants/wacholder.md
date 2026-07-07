# Tenant: `wacholder`

[Tenant index](README.md) | [Tenant directory](../../tenants/wacholder/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/wacholder/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `wacholder` |
| Tenant ID | `22` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `360 / 172.16.90/24` |
| NFS VLAN/CIDR | `361 / 172.16.91/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=wacholder` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=wacholder --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=wacholder -C
ansible-playbook -i inventory TENANT.yml -e tenant=wacholder -e lan_state=absent -C
```
