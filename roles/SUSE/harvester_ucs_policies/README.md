# Role: `SUSE/harvester_ucs_policies`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Runs the role task flow described below.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `AA04.yml`

## Task Flow

Main tasks detected:

- Stop because the public AA04 Harvester UCS policy role is a placeholder
- Placeholder acknowledged

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `ansible.builtin.fail`
- `ansible.builtin.debug`

## Inputs To Check

- No Jinja variables were detected in the task files.

## Configuration To Expect

Expect Cisco Intersight pools, policies, LAN/SAN connectivity objects, boot policies, templates, and server profiles.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
- [Cisco Intersight API Docs](https://intersight.com/apidocs/)
- [Cisco Intersight Ansible Collection](https://docs.ansible.com/projects/ansible/latest/collections/cisco/intersight/index.html)
