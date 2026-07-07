# Scripts

[Framework README](../README.md) | [New tenant guide](../docs/tenants/new-tenant.md)

Scripts support repeatable framework operations. They should be run from the repository root unless a script says otherwise.

## `create_tenant.py`

Purpose: create a new tenant directory from a known-good source tenant and update virtual tenant registry vars when needed.

Functions called:

- loads the source `tenants/<source>/vars.yml`
- replaces the source tenant name with the new tenant name
- updates tenant-local identity, VLAN, CIDR, and optional API/org fields
- copies non-vars tenant assets unless `--no-copy-assets` is used
- for virtual tenants, updates selected registry-owning tenant vars such as `tenants/dataspace/vars.yml`

Expected configuration:

- new `tenants/<name>/vars.yml`
- optional copied airgap/manifests/helper files
- optional `vNN_*` entries in the selected registry vars file

Always start with:

```bash
./scripts/create_tenant.py --name tenant41 --tid 41 --access-vlan 455 --access-prefix 172.16.185 --nfs-vlan 456 --nfs-prefix 172.16.186 --dry-run
```

## `publication_check.py`

Purpose: fail fast if literal keys or passwords are present before content is committed or pushed to GitHub.

Functions called:

- scans repository text files
- ignores placeholders, empty values, and Jinja variable references
- rejects committed key files and private key blocks
- reports file and line numbers for cleanup

Expected configuration:

- all secrets are placeholders, environment-backed values, Ansible Vault values, or ignored local files
- `Keys/`, private key files, and local credential overlays are not tracked by git

Run before staging:

```bash
./scripts/publication_check.py
```
