# Role: `ONTAP/ontap_volumes`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds NFS/export-backed FlexVols and tenant data volumes.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

Main tasks detected:

- Create the export policy rules
- Create FlexVols for datastores
- Create swap volumes
- Disable the volume efficiency on swap volumes
- Create NVMe datastores
- Create a FlexVol for the boot LUNs of servers
- Create vCLS datastores
- Create FlexVol for SVM audit log config
- Update load-sharing mirrors

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `netapp.ontap.na_ontap_export_policy_rule`
- `netapp.ontap.na_ontap_volume`
- `netapp.ontap.na_ontap_volume_efficiency`
- `netapp.ontap.na_ontap_rest_cli`
- `command`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `item`
- `inventory_hostname`
- `username`
- `password`
- `svm_specs`

## Configuration To Expect

Expect ONTAP SVM, network, protocol, volume, LIF, LUN, NVMe, export policy, and final service configuration depending on the role.

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
