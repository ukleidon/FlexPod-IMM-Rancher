# Tenant: `edeltanne`

[Tenant index](../README.md) | [Framework tenant guide](../../docs/tenants/edeltanne.md) | [Variables](../../docs/variables.md)

This directory is the source of truth for tenant-specific configuration. The playbook loads shared defaults first and then loads `tenants/edeltanne/vars.yml`, so values in this file override shared defaults for this tenant only.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `edeltanne` |
| Tenant ID | `21` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `390 / 172.16.120/24` |
| NFS VLAN/CIDR | `391 / 172.16.121/24` |

## What To Configure Here

- tenant identity and lifecycle
- VLAN IDs and network prefixes
- Intersight API key references for this tenant
- ONTAP SVM, LIF, IQN, WWPN, volume, and pool values
- tenant-specific RKE2, Harvester, Trident, or application overrides

## Expected Configuration

Running `TENANT.yml -e tenant=edeltanne` should configure or validate only this tenant's network, storage, compute policy, and platform objects. Running with `-e lan_state=absent` should remove only this tenant's network-facing objects.

## Validation

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=edeltanne --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=edeltanne -C
ansible-playbook -i inventory TENANT.yml -e tenant=edeltanne -e lan_state=absent -C
```
