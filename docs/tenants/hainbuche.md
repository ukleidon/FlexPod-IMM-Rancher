# Tenant: `hainbuche`

[Tenant index](README.md) | [Tenant directory](../../tenants/hainbuche/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/hainbuche/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `hainbuche` |
| Tenant ID | `16` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `330 / 172.16.60/24` |
| NFS VLAN/CIDR | `331 / 172.16.61/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=hainbuche` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=hainbuche --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=hainbuche -C
ansible-playbook -i inventory TENANT.yml -e tenant=hainbuche -e lan_state=absent -C
```
