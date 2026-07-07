# Tenant: `schwarzerle`

[Tenant index](README.md) | [Tenant directory](../../tenants/schwarzerle/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/schwarzerle/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `schwarzerle` |
| Tenant ID | `20` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `385 / 172.16.115/24` |
| NFS VLAN/CIDR | `386 / 172.16.116/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=schwarzerle` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=schwarzerle --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=schwarzerle -C
ansible-playbook -i inventory TENANT.yml -e tenant=schwarzerle -e lan_state=absent -C
```
