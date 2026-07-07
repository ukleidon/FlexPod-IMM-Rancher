# Tenant: `robinie`

[Tenant index](README.md) | [Tenant directory](../../tenants/robinie/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/robinie/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `robinie` |
| Tenant ID | `10` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `300 / 172.16.30/24` |
| NFS VLAN/CIDR | `301 / 172.16.31/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=robinie` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=robinie --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=robinie -C
ansible-playbook -i inventory TENANT.yml -e tenant=robinie -e lan_state=absent -C
```
