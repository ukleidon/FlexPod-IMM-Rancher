# Tenant: `eibe`

[Tenant index](README.md) | [Tenant directory](../../tenants/eibe/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/eibe/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `eibe` |
| Tenant ID | `18` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `335 / 172.16.65/24` |
| NFS VLAN/CIDR | `336 / 172.16.66/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=eibe` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=eibe --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=eibe -C
ansible-playbook -i inventory TENANT.yml -e tenant=eibe -e lan_state=absent -C
```
