# Tenant: `edelkastanie`

[Tenant index](README.md) | [Tenant directory](../../tenants/edelkastanie/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/edelkastanie/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `edelkastanie` |
| Tenant ID | `20` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `350 / 172.16.80/24` |
| NFS VLAN/CIDR | `351 / 172.16.81/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=edelkastanie` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=edelkastanie --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=edelkastanie -C
ansible-playbook -i inventory TENANT.yml -e tenant=edelkastanie -e lan_state=absent -C
```
