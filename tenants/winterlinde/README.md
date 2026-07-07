# Tenant: `winterlinde`

[Tenant index](../README.md) | [Framework tenant guide](../../docs/tenants/winterlinde.md) | [Variables](../../docs/variables.md)

This directory is the source of truth for tenant-specific configuration. The playbook loads shared defaults first and then loads `tenants/winterlinde/vars.yml`, so values in this file override shared defaults for this tenant only.

## Tenant Facts

| Field | Value |
| --- | --- |
| Tenant name | `winterlinde` |
| Tenant ID | `17` |
| Tenant type | `virtual` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `{{ t_ib_vlan_id }} / {{ t_ib_network_prefix }}/{{ t_ib_network_mask }}` |
| NFS VLAN/CIDR | `341 / 172.16.71/24` |

## What To Configure Here

- tenant identity and lifecycle
- VLAN IDs and network prefixes
- Intersight API key references for this tenant
- ONTAP SVM, LIF, IQN, WWPN, volume, and pool values
- tenant-specific RKE2, Harvester, Trident, or application overrides

## Expected Configuration

Running `TENANT.yml -e tenant=winterlinde` should configure or validate only this tenant's network, storage, compute policy, and platform objects. Running with `-e lan_state=absent` should remove only this tenant's network-facing objects.

## Validation

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=winterlinde --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=winterlinde -C
ansible-playbook -i inventory TENANT.yml -e tenant=winterlinde -e lan_state=absent -C
```
