# Tenant: `stieleiche`

[Tenant index](README.md) | [Tenant directory](../../tenants/stieleiche/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/stieleiche/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `stieleiche` |
| Tenant ID | `28` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `425 / 172.16.155/24` |
| NFS VLAN/CIDR | `426 / 172.16.156/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=stieleiche` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=stieleiche --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=stieleiche -C
ansible-playbook -i inventory TENANT.yml -e tenant=stieleiche -e lan_state=absent -C
```
