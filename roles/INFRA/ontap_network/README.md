# Role: `INFRA/ontap_network`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds ONTAP broadcast domains, VLAN ports, and network foundations for tenant storage.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `INFRA.yml`

## Task Flow

Main tasks detected:

- Create Management Broadcast Domain
- INFRA - Create iSCSI broadcast domain ports with Jumbo frames
- INFRA - Create NFS broadcast domain ports with Jumbo frames
- INFRA - Create NVMe/TCP broadcast domain ports with Jumbo frames
- INFRA - Create the management vlan interface
- INFRA - Create the iSCSI vlans
- INFRA - Create the NFS vlans
- INFRA - Create the NVMe/TCP vlans
- INFRA - Adding management vlan to the management broadcast domain
- INFRA - Adding iSCSI-A, iSCSI-B vlans to the corresponding broadcast domains
- INFRA - Adding NFS vlans to the corresponding broadcast domains
- INFRA - Adding NVMe-TCP-A, NVMe-TCP-B vlans to the corresponding broadcast domains

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `netapp.ontap.na_ontap_broadcast_domain`
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
- `ha_pairs`
- `ifgrp_name`

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
