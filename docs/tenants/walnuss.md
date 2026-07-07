# Tenant: `walnuss`

[Tenant index](README.md) | [Tenant directory](../../tenants/walnuss/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/walnuss/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `walnuss` |
| Tenant ID | `13` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `315 / 172.16.45/24` |
| NFS VLAN/CIDR | `316 / 172.16.46/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=walnuss` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=walnuss --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=walnuss -C
ansible-playbook -i inventory TENANT.yml -e tenant=walnuss -e lan_state=absent -C
```
