# Role: `common/tenant_preflight`

[Common roles](../README.md) | [Role inventory](../../README.md)

## Purpose

This role validates tenant input before a tenant or RKE2 playbook reaches Nexus, ONTAP, Intersight, Kubernetes, or host operating-system tasks.

It is intentionally lightweight. It checks the operator supplied `-e tenant=<name>`, confirms that `tenants/<tenant>/vars.yml` exists, parses the file, and verifies the tenant identity fields needed by the rest of the framework.

## Functions Called

| Function | Module |
| --- | --- |
| Validate `tenant` extra var | `ansible.builtin.assert` |
| Build expected tenant paths | `ansible.builtin.set_fact` |
| Check for the tenant vars file | `ansible.builtin.stat` |
| Stop on missing tenant vars | `ansible.builtin.fail` |
| Parse tenant vars | `ansible.builtin.include_vars` |

## Configuration To Expect

The selected tenant directory must contain a valid `vars.yml` file with:

| Variable | Requirement |
| --- | --- |
| `tenant_name` | Required tenant display/configuration name. |
| `tenant_type` | Optional; defaults to `physical`. When set, use `physical` or `virtual`. |

## Operator Use

Run preflight by itself when checking a tenant name or a copied tenant directory:

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=<tenant-name> -C --tags preflight
```

The role is also tagged `always`, so it runs before tenant and RKE2 phase tags.
