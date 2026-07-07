# Role: `ONTAP/ontap_network`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds ONTAP broadcast domains, VLAN ports, and network foundations for tenant storage.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

Main tasks detected:

- Create Management Broadcast Domain
- Create iSCSI broadcast domain ports with Jumbo frames
- Create NFS broadcast domain ports with Jumbo frames
- Create NVMe/TCP broadcast domain ports with Jumbo frames
- Create multimode/ LACP interface groups and add data ports
- Modify the MTU of the data ifgroup to 9000
- Create the management vlan interface
- Create the iSCSI vlans
- Create the NFS vlans
- Create the NVMe/TCP vlans
- Adding management vlan to the management broadcast domain
- Adding iSCSI-A, iSCSI-B vlans to the corresponding broadcast domains
- Adding NFS vlans to the corresponding broadcast domains
- Adding NVMe-TCP-A, NVMe-TCP-B vlans to the corresponding broadcast domains

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `netapp.ontap.na_ontap_broadcast_domain`
- `netapp.ontap.na_ontap_net_ifgrp`
- `netapp.ontap.na_ontap_rest_cli`
- `command`
- `netapp.ontap.na_ontap_net_vlan`
- `netapp.ontap.na_ontap_ports`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `item`
- `inventory_hostname`
- `username`
- `password`
- `ib_mgmt_vlan_list`
- `storage_vlan_list`
- `ifgrp_mode`
- `ifgrp_name`
- `ha_pairs`

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
