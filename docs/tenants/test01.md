# Tenant: `test01`

[Tenant index](README.md) | [Tenant directory](../../tenants/test01/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/test01/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `test01` |
| Tenant ID | `03` |
| Tenant type | `-` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `304 / 172.18.4/24` |
| NFS VLAN/CIDR | `303 / 172.18.3/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=test01` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=test01 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=test01 -C
ansible-playbook -i inventory TENANT.yml -e tenant=test01 -e lan_state=absent -C
```
