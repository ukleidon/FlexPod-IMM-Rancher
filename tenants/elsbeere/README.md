# Tenant: `elsbeere`

[Tenant index](../README.md) | [Framework tenant guide](../../docs/tenants/elsbeere.md) | [Variables](../../docs/variables.md)

This directory is the source of truth for tenant-specific configuration. The playbook loads shared defaults first and then loads `tenants/elsbeere/vars.yml`, so values in this file override shared defaults for this tenant only.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `elsbeere` |
| Tenant ID | `14` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `320 / 172.16.50/24` |
| NFS VLAN/CIDR | `321 / 172.16.51/24` |

## What To Configure Here

- tenant identity and lifecycle
- VLAN IDs and network prefixes
- Intersight API key references for this tenant
- ONTAP SVM, LIF, IQN, WWPN, volume, and pool values
- tenant-specific RKE2, Harvester, Trident, or application overrides

## Expected Configuration

Running `TENANT.yml -e tenant=elsbeere` should configure or validate only this tenant's network, storage, compute policy, and platform objects. Running with `-e lan_state=absent` should remove only this tenant's network-facing objects.

## Validation

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=elsbeere --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=elsbeere -C
ansible-playbook -i inventory TENANT.yml -e tenant=elsbeere -e lan_state=absent -C
```
