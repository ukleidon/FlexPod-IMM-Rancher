# Tenant: `weissdorn`

[Tenant index](../README.md) | [Framework tenant guide](../../docs/tenants/weissdorn.md) | [Variables](../../docs/variables.md)

This directory is the source of truth for tenant-specific configuration. The playbook loads shared defaults first and then loads `tenants/weissdorn/vars.yml`, so values in this file override shared defaults for this tenant only.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `weissdorn` |
| Tenant ID | `26` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `415 / 172.16.145/24` |
| NFS VLAN/CIDR | `416 / 172.16.146/24` |

## What To Configure Here

- tenant identity and lifecycle
- VLAN IDs and network prefixes
- Intersight API key references for this tenant
- ONTAP SVM, LIF, IQN, WWPN, volume, and pool values
- tenant-specific RKE2, Harvester, Trident, or application overrides

## Expected Configuration

Running `TENANT.yml -e tenant=weissdorn` should configure or validate only this tenant's network, storage, compute policy, and platform objects. Running with `-e lan_state=absent` should remove only this tenant's network-facing objects.

## Validation

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=weissdorn --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=weissdorn -C
ansible-playbook -i inventory TENANT.yml -e tenant=weissdorn -e lan_state=absent -C
```
