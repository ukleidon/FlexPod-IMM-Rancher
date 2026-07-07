# Tenant: `gpusystem`

[Tenant index](README.md) | [Tenant directory](../../tenants/gpusystem/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/gpusystem/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `gpu` |
| Tenant ID | `02` |
| Tenant type | `-` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `204 / 172.17.4/24` |
| NFS VLAN/CIDR | `203 / 172.17.3/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=gpusystem` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=gpusystem --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=gpusystem -C
ansible-playbook -i inventory TENANT.yml -e tenant=gpusystem -e lan_state=absent -C
```
