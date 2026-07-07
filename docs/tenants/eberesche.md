# Tenant: `eberesche`

[Tenant index](README.md) | [Tenant directory](../../tenants/eberesche/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/eberesche/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `eberesche` |
| Tenant ID | `12` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `310 / 172.16.40/24` |
| NFS VLAN/CIDR | `311 / 172.16.41/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=eberesche` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=eberesche --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=eberesche -C
ansible-playbook -i inventory TENANT.yml -e tenant=eberesche -e lan_state=absent -C
```
