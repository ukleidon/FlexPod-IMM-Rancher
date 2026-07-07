# Tenant Directory

[Public tenant examples](../../docs/tenants/README.md) | [Variables](../../docs/variables.md)

This directory contains tenant-local artifacts such as `vars.yml`, optional manifests, airgap content, and workload-specific files. The public README is intentionally anonymized and does not expose deployment-specific tenant names, VLAN IDs, CIDRs, hostnames, or SVM names.

For the public operating model, use the neutral examples in `docs/tenants/`. For a real deployment, keep live tenant facts in a private branch, private overlay, Ansible Vault, or internal documentation.

## Configuration To Expect

Running `TENANT.yml -e tenant=<tenant-name>` configures or validates only the selected tenant's network, storage, compute policy, and platform objects. Running with `-e lan_state=absent` should remove only that tenant's network-facing objects.

## Operator Checks

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -C
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -e lan_state=absent -C
```
