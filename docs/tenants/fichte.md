# Tenant: `fichte`

[Tenant index](README.md) | [Tenant directory](../../tenants/fichte/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/fichte/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `fichte` |
| Tenant ID | `23` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `400 / 172.16.130/24` |
| NFS VLAN/CIDR | `401 / 172.16.131/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=fichte` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=fichte --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=fichte -C
ansible-playbook -i inventory TENANT.yml -e tenant=fichte -e lan_state=absent -C
```
