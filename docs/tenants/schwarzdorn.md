# Tenant: `schwarzdorn`

[Tenant index](README.md) | [Tenant directory](../../tenants/schwarzdorn/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/schwarzdorn/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `schwarzdorn` |
| Tenant ID | `31` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `440 / 172.16.170/24` |
| NFS VLAN/CIDR | `441 / 172.16.171/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=schwarzdorn` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=schwarzdorn --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=schwarzdorn -C
ansible-playbook -i inventory TENANT.yml -e tenant=schwarzdorn -e lan_state=absent -C
```
