# GitHub Publication Checklist

[Documentation index](README.md) | [Validation](validation.md) | [Variables](variables.md)

This repository is designed to be useful as a public automation example without exposing live deployment secrets. The checked-in files should contain topology examples, variable names, role logic, and operator guidance, but no real keys or passwords.

## What Must Not Be Committed

- Intersight API key IDs for live accounts
- private key files such as `*.pem`, `*.key`, or `Keys/*.txt`
- ONTAP, Nexus, MDS, ESXi, vCenter, Trident, or tenant passwords
- Ansible Vault password files
- local inventory overlays with customer-only addresses or credentials
- generated logs, retry files, or device backups

## Placeholder Model

Public files use placeholders such as `CHANGE_ME_INTERSIGHT_API_KEY_ID`, `CHANGE_ME_LOCAL_USER_PASSWORD`, or `CHANGE_ME_TRIDENT_PASSWORD`. Replace these only in a private working copy, ignored local file, Ansible Vault, environment-backed variable, or deployment overlay.

## Recommended Pre-Push Workflow

```bash
./scripts/publication_check.py
ansible-playbook -i inventory INFRA.yml --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 --syntax-check
git status --short
git diff --check
```

Expected result: the publication check passes, playbooks parse, and git shows only intentional documentation, template, script, or sanitized variable changes.

## GitHub Notes

- Keep `README.md` as the browser landing page.
- Keep `README` as the short structure note for operators who open the legacy text file.
- Use `requirements.yml` to document Ansible collection dependencies.
- Use `.gitignore` to keep local keys, vault files, logs, retry files, and generated device backups out of the repository.
