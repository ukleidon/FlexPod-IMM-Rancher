# Tenant: `speierling`

[Tenant index](README.md) | [Tenant directory](../../tenants/speierling/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/speierling/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `speierling` |
| Tenant ID | `15` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `325 / 172.16.55/24` |
| NFS VLAN/CIDR | `326 / 172.16.56/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=speierling` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=speierling --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=speierling -C
ansible-playbook -i inventory TENANT.yml -e tenant=speierling -e lan_state=absent -C
```
