# Role: `INFRA/ontap_svm`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds or removes ONTAP SVMs and protocol services.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `INFRA.yml`

## Task Flow

Main tasks detected:

- INFRA - Create the aggregate list variable for tenant SVM
- See the aggregate list
- INFRA - Create SVM with specified protocols enabled
- INFRA - Enable NFS protcol with vstorage
- INFRA - Get the total number of data aggregates created across all nodes in the ONTAP Cluster
- See the aggr count
- INFRA - Create and enable iSCSI service
- INFRA - Create and enable FCP service
- INFRA - Create and enable NVMe service
- INFRA - Set password for vsadmin user
- INFRA - Unlock vsadmin user
- INFRA - Create login banner for the SVM
- INFRA - Remove insecure ciphers from the SVM

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

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `aggr_list`
- `ha_pairs`
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
