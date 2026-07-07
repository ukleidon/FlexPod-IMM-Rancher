# Tenant: `zirbe`

[Tenant index](../README.md) | [Framework tenant guide](../../docs/tenants/zirbe.md) | [Variables](../../docs/variables.md)

This directory is the source of truth for tenant-specific configuration. The playbook loads shared defaults first and then loads `tenants/zirbe/vars.yml`, so values in this file override shared defaults for this tenant only.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `zirbe` |
| Tenant ID | `29` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `430 / 172.16.160/24` |
| NFS VLAN/CIDR | `431 / 172.16.161/24` |

## What To Configure Here

- tenant identity and lifecycle
- VLAN IDs and network prefixes
- Intersight API key references for this tenant
- ONTAP SVM, LIF, IQN, WWPN, volume, and pool values
- tenant-specific RKE2, Harvester, Trident, or application overrides

## Expected Configuration

Running `TENANT.yml -e tenant=zirbe` should configure or validate only this tenant's network, storage, compute policy, and platform objects. Running with `-e lan_state=absent` should remove only this tenant's network-facing objects.

## Validation

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=zirbe --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=zirbe -C
ansible-playbook -i inventory TENANT.yml -e tenant=zirbe -e lan_state=absent -C
```
