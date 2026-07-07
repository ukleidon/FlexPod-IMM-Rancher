# Role: `rancher/env_vars`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Loads the ordered YAML variable stack used by the playbook.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`
- `TENANT.yml`
- `RKE2.yml`
- `RKE2.yml`

## Task Flow

Main tasks detected:

- Include cluster environment variables

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `include_vars`
- `file`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `item`
- `env_vars_common_file`
- `env_vars_all_file`
- `env_vars_ucs_file`
- `env_vars_tenant_defaults_file`
- `env_vars_tenant_file`

## Configuration To Expect

Expect RKE2 server/agent installation, cluster join configuration, proxy handling, and service state changes.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
- [SUSE RKE2 Documentation](https://docs.rke2.io/)
