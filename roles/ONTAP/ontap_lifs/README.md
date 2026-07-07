# Role: `ONTAP/ontap_lifs`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds ONTAP NFS, iSCSI, FC, FC-NVMe, or NVMe/TCP data LIFs.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

Main tasks detected:

- Create LIF(s) for NFS access
- Get the iSCSI LIFs list with their corresponding home nodes
- Get the iSCSI storage VLANs list
- Create iSCSI LIFs on nodes
- Create FCP LIF(s) on Nodes
- Create NVMe FC LIF(s) on Nodes
- Get the NVMe/TCP LIFs list with their corresponding home nodes
- Get the NVMe/TCP storage VLANs list
- Create NVMe/TCP LIFs on nodes
- Create LIF for SVM Management
- Create a default route in infra SVM

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `netapp.ontap.na_ontap_interface`
- `ansible.builtin.set_fact`
- `netapp.ontap.na_ontap_net_routes`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `svm_specs`
- `item`
- `inventory_hostname`
- `username`
- `password`
- `ha_pairs`
- `storage_vlan_list`
- `ifgrp_name`
- `iscsi_lifs_list`
- `iscsi_vlans_list`
- `nvme_tcp_lifs_list`
- `nvme_tcp_vlans_list`
- `ib_mgmt_vlan_list`

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
