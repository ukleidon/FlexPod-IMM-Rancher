# Tenant: `stechpalme`

[Tenant index](README.md) | [Tenant directory](../../tenants/stechpalme/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/stechpalme/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `stechpalme` |
| Tenant ID | `25` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `410 / 172.16.140/24` |
| NFS VLAN/CIDR | `411 / 172.16.141/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=stechpalme` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=stechpalme --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=stechpalme -C
ansible-playbook -i inventory TENANT.yml -e tenant=stechpalme -e lan_state=absent -C
```
