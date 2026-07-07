# Tenant: `ahorn`

[Tenant index](README.md) | [Tenant directory](../../tenants/ahorn/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/ahorn/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `ahorn` |
| Tenant ID | `32` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `445 / 172.16.175/24` |
| NFS VLAN/CIDR | `446 / 172.16.176/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=ahorn` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=ahorn --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=ahorn -C
ansible-playbook -i inventory TENANT.yml -e tenant=ahorn -e lan_state=absent -C
```
