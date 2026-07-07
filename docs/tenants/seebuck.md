# Tenant: `seebuck`

[Tenant index](README.md) | [Tenant directory](../../tenants/seebuck/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/seebuck/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `seebuck` |
| Tenant ID | `04` |
| Tenant type | `-` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `220 / 172.17.20/24` |
| NFS VLAN/CIDR | `217 / 172.17.17/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=seebuck` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=seebuck --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=seebuck -C
ansible-playbook -i inventory TENANT.yml -e tenant=seebuck -e lan_state=absent -C
```
