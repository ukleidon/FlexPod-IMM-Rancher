# Role: `TENANT/harvester_tenant_config`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Runs the role task flow described below.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TEST.yml`

## Task Flow

Main tasks detected:

- current_working_directory
- Create a directory if it does not exist
- Create Tenant namespace
- Generate tenant access network config
- Generate tenant storage network config
- Apply tenant access network on the Harvester cluster
- Apply tenant storage network on the Harvester cluster

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `ansible.builtin.debug`
- `ansible.builtin.file`
- `kubernetes.core.k8s`
- `template`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `current_working_directory`
- `tenant_name`
- `harvester_context`

## Configuration To Expect

Expect the configuration described by the called task files. Review the task flow and variables before running live.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
