# Tenant: `rosskastanie`

[Tenant index](README.md) | [Tenant directory](../../tenants/rosskastanie/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/rosskastanie/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `rosskastanie` |
| Tenant ID | `21` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `355 / 172.16.85/24` |
| NFS VLAN/CIDR | `356 / 172.16.86/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=rosskastanie` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=rosskastanie --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=rosskastanie -C
ansible-playbook -i inventory TENANT.yml -e tenant=rosskastanie -e lan_state=absent -C
```
