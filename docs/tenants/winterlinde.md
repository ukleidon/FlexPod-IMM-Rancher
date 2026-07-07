# Tenant: `winterlinde`

[Tenant index](README.md) | [Tenant directory](../../tenants/winterlinde/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/winterlinde/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `winterlinde` |
| Tenant ID | `17` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `{{ t_ib_vlan_id }} / {{ t_ib_network_prefix }}/{{ t_ib_network_mask }}` |
| NFS VLAN/CIDR | `341 / 172.16.71/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=winterlinde` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=winterlinde --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=winterlinde -C
ansible-playbook -i inventory TENANT.yml -e tenant=winterlinde -e lan_state=absent -C
```
