# Tenant: `edeltanne`

[Tenant index](README.md) | [Tenant directory](../../tenants/edeltanne/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/edeltanne/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `edeltanne` |
| Tenant ID | `21` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `390 / 172.16.120/24` |
| NFS VLAN/CIDR | `391 / 172.16.121/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=edeltanne` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=edeltanne --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=edeltanne -C
ansible-playbook -i inventory TENANT.yml -e tenant=edeltanne -e lan_state=absent -C
```
