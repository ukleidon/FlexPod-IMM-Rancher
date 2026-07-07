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
- for virtual tenants, updates selected registry-owning tenant vars such as `tenants/tenant-hub/vars.yml`

Expected configuration:

- new `tenants/<name>/vars.yml`
- optional copied airgap/manifests/helper files
- optional `vNN_*` entries in the selected registry vars file

Always start with:

```bash
./scripts/create_tenant.py --name tenant41 --tid 41 --access-vlan 455 --access-prefix 198.51.100 --nfs-vlan 456 --nfs-prefix 203.0.113 --dry-run
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

## Architecture Documentation Generator

`generate_architecture_overview.py` reads the current inventory, `group_vars`, `host_vars`, tenant vars, and playbooks, then renders `docs/architecture-overview.md`. Run it after changing tenant VLANs, VRFs, SVM settings, Nexus interface maps, or playbook role flow.

```bash
./scripts/generate_architecture_overview.py .
```

## Public Documentation Generator

`generate_public_docs.py` renders public-safe documentation with neutral hostnames, tenant names, VLANs, and documentation networks. Run it before publication when docs or framework structure changes.

```bash
./scripts/generate_public_docs.py .
```
