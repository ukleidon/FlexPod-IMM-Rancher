# Tenant: `harvester`

[Tenant index](README.md) | [Tenant directory](../../tenants/harvester/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/harvester/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `RTP4-SUSE` |
| Tenant ID | `10` |
| Tenant type | `-` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `1042 / 10.104.2/24` |
| NFS VLAN/CIDR | `1047 / 10.104.7/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=harvester` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=harvester --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=harvester -C
ansible-playbook -i inventory TENANT.yml -e tenant=harvester -e lan_state=absent -C
```
