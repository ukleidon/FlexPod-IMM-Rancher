# Tenant: `waldkiefer`

[Tenant index](README.md) | [Tenant directory](../../tenants/waldkiefer/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/waldkiefer/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `waldkiefer` |
| Tenant ID | `19` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `345 / 172.16.75/24` |
| NFS VLAN/CIDR | `346 / 172.16.76/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=waldkiefer` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=waldkiefer --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=waldkiefer -C
ansible-playbook -i inventory TENANT.yml -e tenant=waldkiefer -e lan_state=absent -C
```
