# Tenant: `birke`

[Tenant index](README.md) | [Tenant directory](../../tenants/birke/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/birke/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `birke` |
| Tenant ID | `27` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `420 / 172.16.150/24` |
| NFS VLAN/CIDR | `421 / 172.16.151/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=birke` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=birke --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=birke -C
ansible-playbook -i inventory TENANT.yml -e tenant=birke -e lan_state=absent -C
```
