# Tenant Example: `tenant01`

[Tenant examples](README.md) | [Variables](../variables.md) | [Validation](../validation.md)

This public page describes the tenant pattern without exposing internal tenant names, hostnames, VLAN IDs, or CIDRs.

## Tenant Facts

| Field | Public example |
| --- | --- |
| Tenant name | `tenant01` |
| Tenant type | `physical` |
| Lifecycle state | `present` |
| Access VLAN/CIDR | `301 / 192.0.2.0/24` |
| NFS VLAN/CIDR | `303 / 203.0.113.0/24` |

## Configuration To Expect

Running `TENANT.yml -e tenant=<tenant-name>` configures or validates this tenant's Nexus network objects, ONTAP storage objects, Intersight policy/profile objects, and optional RKE2/Trident assets according to inventory and tags.

Dedicated VRF, tenant SVM, NFS/iSCSI storage, Intersight policies, templates, and server profiles.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -C
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -e lan_state=absent -C
```
