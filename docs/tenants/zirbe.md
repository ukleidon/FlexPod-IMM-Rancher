# Tenant: `zirbe`

[Tenant index](README.md) | [Tenant directory](../../tenants/zirbe/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/zirbe/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `zirbe` |
| Tenant ID | `29` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `430 / 172.16.160/24` |
| NFS VLAN/CIDR | `431 / 172.16.161/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=zirbe` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=zirbe --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=zirbe -C
ansible-playbook -i inventory TENANT.yml -e tenant=zirbe -e lan_state=absent -C
```
