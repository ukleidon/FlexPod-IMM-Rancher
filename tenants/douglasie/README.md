# Tenant: `douglasie`

[Tenant index](../README.md) | [Framework tenant guide](../../docs/tenants/douglasie.md) | [Variables](../../docs/variables.md)

This directory is the source of truth for tenant-specific configuration. The playbook loads shared defaults first and then loads `tenants/douglasie/vars.yml`, so values in this file override shared defaults for this tenant only.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `douglasie` |
| Tenant ID | `11` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `305 / 172.16.35/24` |
| NFS VLAN/CIDR | `306 / 172.16.36/24` |

## What To Configure Here

- tenant identity and lifecycle
- VLAN IDs and network prefixes
- Intersight API key references for this tenant
- ONTAP SVM, LIF, IQN, WWPN, volume, and pool values
- tenant-specific RKE2, Harvester, Trident, or application overrides

## Expected Configuration

Running `TENANT.yml -e tenant=douglasie` should configure or validate only this tenant's network, storage, compute policy, and platform objects. Running with `-e lan_state=absent` should remove only this tenant's network-facing objects.

## Validation

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=douglasie --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=douglasie -C
ansible-playbook -i inventory TENANT.yml -e tenant=douglasie -e lan_state=absent -C
```
