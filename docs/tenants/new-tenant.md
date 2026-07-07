# New Tenant Guide

[Tenant examples](README.md) | [Variables](../variables.md) | [Validation](../validation.md)

Use this guide to create a new tenant from a template while keeping tenant-specific values isolated in `tenants/<tenant>/vars.yml`.

The public example values below use documentation networks. Replace them with deployment-specific VLANs, CIDRs, tenant names, and key references in a private branch or overlay.

## Example Input

| Field | Example value | Purpose |
| --- | --- | --- |
| Tenant name | `tenant41` | Directory name and default tenant identity. |
| Tenant ID | `41` | Used for generated pools such as MAC, WWPN, UUID, or IQN ranges. |
| Access VLAN/CIDR | `455 / 198.51.100.0/24` | Used for access and management-side traffic. |
| NFS VLAN/CIDR | `456 / 203.0.113.0/24` | Used for storage/NFS traffic. |

## Dry Run First

```bash
./scripts/create_tenant.py \
  --name tenant41 \
  --tid 41 \
  --access-vlan 455 \
  --access-prefix 198.51.100 \
  --nfs-vlan 456 \
  --nfs-prefix 203.0.113 \
  --source tenant_template \
  --dry-run
```

For virtual tenants, the script can update one or more registry vars files with `vNN_*` values. In public documentation, call this a registry or hub tenant. In a private deployment, select the real registry tenant name.

## Create The Tenant

```bash
./scripts/create_tenant.py \
  --name tenant41 \
  --tid 41 \
  --access-vlan 455 \
  --access-prefix 198.51.100 \
  --nfs-vlan 456 \
  --nfs-prefix 203.0.113 \
  --source tenant_template
```

## Validate

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant41 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant41 -C
```
