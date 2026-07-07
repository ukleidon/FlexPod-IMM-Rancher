# Tenant: `sommerlinde`

[Tenant index](README.md) | [Tenant directory](../../tenants/sommerlinde/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/sommerlinde/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `sommerlinde` |
| Tenant ID | `24` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `370 / 172.16.100/24` |
| NFS VLAN/CIDR | `371 / 172.16.101/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=sommerlinde` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=sommerlinde --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=sommerlinde -C
ansible-playbook -i inventory TENANT.yml -e tenant=sommerlinde -e lan_state=absent -C
```
