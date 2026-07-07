# Tenant: `weissdorn`

[Tenant index](README.md) | [Tenant directory](../../tenants/weissdorn/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/weissdorn/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `weissdorn` |
| Tenant ID | `26` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `415 / 172.16.145/24` |
| NFS VLAN/CIDR | `416 / 172.16.146/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=weissdorn` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=weissdorn --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=weissdorn -C
ansible-playbook -i inventory TENANT.yml -e tenant=weissdorn -e lan_state=absent -C
```
