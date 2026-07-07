# Tenant: `laerche`

[Tenant index](README.md) | [Tenant directory](../../tenants/laerche/README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This page summarizes the checked-in tenant source of truth without exposing credential values. The live playbook loads shared defaults first and then overlays `tenants/laerche/vars.yml`.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `laerche` |
| Tenant ID | `30` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `435 / 172.16.165/24` |
| NFS VLAN/CIDR | `436 / 172.16.166/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=laerche` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=laerche --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=laerche -C
ansible-playbook -i inventory TENANT.yml -e tenant=laerche -e lan_state=absent -C
```
