# Tenant: `belchen`

[Tenant index](README.md) | [Tenant directory](../../tenants/belchen/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/belchen/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `belchen` |
| Tenant ID | `03` |
| Tenant type | `-` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `211 / 172.17.11/24` |
| NFS VLAN/CIDR | `210 / 172.17.10/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=belchen` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=belchen --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=belchen -C
ansible-playbook -i inventory TENANT.yml -e tenant=belchen -e lan_state=absent -C
```
