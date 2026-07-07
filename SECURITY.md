# Security and Publication Notes

This repository is prepared for public publication. Keep live credentials and deployment-specific identity material out of git.

## Do Not Commit

- Intersight API key IDs or private key files
- ONTAP, Nexus, MDS, ESXi, vCenter, Trident, or tenant passwords
- Ansible Vault password files
- customer-only local inventory overlays

## Before You Push

Run:

```bash
./scripts/publication_check.py
git diff --check
git status --short
```

Store real deployment secrets in ignored local files, Ansible Vault, environment-backed variables, or a private overlay repository.
