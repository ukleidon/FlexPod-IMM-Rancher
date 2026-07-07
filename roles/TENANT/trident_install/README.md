# Role: `TENANT/trident_install`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Deploys NetApp Trident and configures the Kubernetes storage backend.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`

## Task Flow

Main tasks detected:

- current_working_directory
- Print version
- Create a directory if it does not exist
- Generate trident backend config
- Download Trident {{ trident.version }}
- unarchive trident installer
- move files to subfolder
- Apply Trident CRDs
- Apply Trident Namespace
- Apply Trident Bundle
- Pause for 1 minutes to build app cache
- Apply Trident CR
- Apply Trident Backend
- Clean Up folder

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `ansible.builtin.debug`
- `debug`
- `ansible.builtin.file`
- `template`
- `ansible.builtin.get_url`
- `ansible.builtin.unarchive`
- `command`
- `kubernetes.core.k8s`
- `ansible.builtin.pause`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `current_working_directory`
- `item`
- `tenant_name`
- `trident`

## Configuration To Expect

Expect Kubernetes Trident installation and backend configuration that maps the tenant SVM/storage settings into Kubernetes storage classes.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
- [NetApp ONTAP Automation](https://docs.netapp.com/us-en/ontap-automation/)
- [NetApp ONTAP Ansible Collection](https://docs.ansible.com/projects/ansible/latest/collections/netapp/ontap/index.html)
