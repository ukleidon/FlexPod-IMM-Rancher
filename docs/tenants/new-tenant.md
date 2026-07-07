# New Tenant Guide

[Tenants](README.md) | [Variables](../variables.md) | [Validation](../validation.md) | [Template](../../tenants/_tenant_template/README.md)

Use `scripts/create_tenant.py` for the normal path. It clones a known-good tenant directory, updates tenant-local identity and network facts, preserves non-vars tenant assets, and, for virtual tenants, updates the registry-owning tenant vars file directly.

## 1. Choose Tenant Facts

Collect these values before creating the tenant:

| Fact | Example | Notes |
| --- | --- | --- |
| Tenant name | `tenant41` | Lowercase letters, digits, `_`, and `-`. |
| Tenant ID | `41` | Must be unique across tenant vars. |
| Access VLAN/CIDR | `455 / 172.16.185/24` | Used for access and management-side traffic. |
| NFS VLAN/CIDR | `456 / 172.16.186/24` | Used for storage/NFS traffic. |
| API key material | `api_key_id`, `api_private_key` | Keep only placeholders in public files. Real values belong in a private overlay or vault. |
| Storage facts | IQNs, LIFs, pool starts | Review after the clone because these are environment-specific. |

## 2. Dry Run

```bash
./scripts/create_tenant.py \
  --name tenant41 \
  --tid 41 \
  --access-vlan 455 \
  --access-prefix 172.16.185 \
  --nfs-vlan 456 \
  --nfs-prefix 172.16.186 \
  --source ac01 \
  --dry-run
```

For virtual tenants, the script reads the selected registry vars file and picks the next free `vNN` index. The default registry target for this repository is `tenants/harvester/vars.yml`.

## 3. Create

Remove `--dry-run` only after the plan shows the expected source tenant, target directory, VLAN IDs, CIDRs, and registry target.

Useful options:

| Option | Purpose |
| --- | --- |
| `--source ac01` | Clone another source tenant. Default is `ac01`. |
| `--virtual-registry-target harvester` | Update the virtual tenant registry owner. Repeat as needed. |
| `--no-virtual-registry` | Create only the tenant directory and do not update registry vars. |
| `--no-copy-assets` | Create only `vars.yml`. |
| `--api-key-id`, `--api-private-key` | Set placeholder references; do not commit live values. |

## 4. Review

Open `tenants/tenant41/vars.yml` and confirm tenant identity, lifecycle, API placeholders, VLANs, CIDRs, ONTAP values, RKE2 values, and any app-specific overrides.

## 5. Validate

```bash
./scripts/publication_check.py
ansible-playbook -i inventory TENANT.yml -e tenant=tenant41 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant41 -C
ansible-playbook -i inventory TENANT.yml -e tenant=tenant41 -e lan_state=absent -C
```

The final command matters: every tenant must be independently unconfigurable without relying on another tenant directory.
