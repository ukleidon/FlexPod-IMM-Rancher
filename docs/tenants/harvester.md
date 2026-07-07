# Tenant: `harvester`

[Tenant index](README.md) | [Tenant directory](../../tenants/harvester/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/harvester/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `DataSpace` |
| Tenant ID | `01` |
| Tenant type | `-` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `102 / 172.16.8/23` |
| NFS VLAN/CIDR | `103 / 172.16.10/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=harvester` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=harvester --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=harvester -C
ansible-playbook -i inventory TENANT.yml -e tenant=harvester -e lan_state=absent -C
```
