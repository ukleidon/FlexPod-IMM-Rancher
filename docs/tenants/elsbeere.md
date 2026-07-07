# Tenant: `elsbeere`

[Tenant index](README.md) | [Tenant directory](../../tenants/elsbeere/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/elsbeere/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `elsbeere` |
| Tenant ID | `14` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `320 / 172.16.50/24` |
| NFS VLAN/CIDR | `321 / 172.16.51/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=elsbeere` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=elsbeere --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=elsbeere -C
ansible-playbook -i inventory TENANT.yml -e tenant=elsbeere -e lan_state=absent -C
```
