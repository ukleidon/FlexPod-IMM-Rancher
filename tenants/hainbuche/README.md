# Tenant: `hainbuche`

[Tenant index](../README.md) | [Framework tenant guide](../../docs/tenants/hainbuche.md) | [Variables](../../docs/variables.md)

This directory is the source of truth for tenant-specific configuration. The playbook loads shared defaults first and then loads `tenants/hainbuche/vars.yml`, so values in this file override shared defaults for this tenant only.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `hainbuche` |
| Tenant ID | `16` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `330 / 172.16.60/24` |
| NFS VLAN/CIDR | `331 / 172.16.61/24` |

## What To Configure Here

- tenant identity and lifecycle
- VLAN IDs and network prefixes
- Intersight API key references for this tenant
- ONTAP SVM, LIF, IQN, WWPN, volume, and pool values
- tenant-specific RKE2, Harvester, Trident, or application overrides

## Expected Configuration

Running `TENANT.yml -e tenant=hainbuche` should configure or validate only this tenant's network, storage, compute policy, and platform objects. Running with `-e lan_state=absent` should remove only this tenant's network-facing objects.

## Validation

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=hainbuche --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=hainbuche -C
ansible-playbook -i inventory TENANT.yml -e tenant=hainbuche -e lan_state=absent -C
```
