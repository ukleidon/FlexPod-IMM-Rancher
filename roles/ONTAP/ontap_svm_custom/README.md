# Role: `ONTAP/ontap_svm_custom`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds or removes ONTAP SVMs and protocol services.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `create_svm.yml`
- `delete_svm.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `ansible.builtin.set_fact`
- `ansible.builtin.debug`
- `netapp.ontap.na_ontap_svm`
- `netapp.ontap.na_ontap_nfs`
- `netapp.ontap.na_ontap_iscsi`
- `netapp.ontap.na_ontap_fcp`
- `netapp.ontap.na_ontap_nvme`
- `netapp.ontap.na_ontap_user`
- `netapp.ontap.na_ontap_login_messages`
- `netapp.ontap.na_ontap_rest_cli`
- `command`
- `netapp.ontap.na_ontap_interface`
- `netapp.ontap.na_ontap_net_routes`
- `netapp.ontap.na_ontap_rest_info`
- `netapp.ontap.na_ontap_lun_map`
- `netapp.ontap.na_ontap_lun`
- `netapp.ontap.na_ontap_igroup`
- `netapp.ontap.na_ontap_volume`
- `include_tasks`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `aggr_list`
- `ha_pairs`
- `item`
- `inventory_hostname`
- `username`
- `password`
- `svm_specs`
- `lookup`
- `total_aggr_count`
- `job_schedule`
- `storage_vlan_list`
- `ifgrp_name`
- `iscsi_lifs_list`
- `iscsi_vlans_list`
- `nvme_tcp_lifs_list`
- `nvme_tcp_vlans_list`
- `ib_mgmt_vlan_list`
- `svm_nvme_info`
- `svm_lunmaps_info`
- `svm_lun_info`

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
