# Role: `TENANT/ontap_nvme`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds NVMe namespaces, subsystems, and host NQN mappings.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`

## Task Flow

Main tasks detected:

- Create NVMe namespace
- Create the host NQNs list for FC-NVMe config
- Create the host NQNs list for NVMe/TCP config
- Create the final host NQNs list to be added to the NVMe subsystem
- See the host NQNs list
- Create NVMe subsystem and add the host NQNs to the subsystem
- Get the list of Namespace paths to be associated with the subsystem
- Map the namespaces to the NVMe subsystem

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `netapp.ontap.na_ontap_nvme_namespace`
- `ansible.builtin.set_fact`
- `ansible.builtin.debug`
- `netapp.ontap.na_ontap_nvme_subsystem`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `svm_specs`
- `item`
- `inventory_hostname`
- `username`
- `password`
- `fc_nvme_nqn`
- `fc_esxi_hosts`
- `nvme_tcp_nqn`
- `iscsi_esxi_hosts`
- `nvme_nqns`
- `ns_paths_list`

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
