# Role: `TENANT/ontap_luns`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds boot and data LUNs, igroups, and host-to-LUN mapping.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`

## Task Flow

Main tasks detected:

- {{ t_ib_vlan_name }}
- {{ t_nfs_vlan_name }}
- {{ t_iscsiA_vlan_name }}
- {{ t_iscsiB_vlan_name }}
- {{ t_access_vlan_name }}
- {{ t_iscsiA_vlan_id }}
- {{ t_iscsiB_vlan_id }}
- {{ t_nfs_vlan_id }}
- {{ t_access_vlan_id }}
- TENANT - Create the boot LUNs for Servers for iSCSI config
- TENANT - Create the data LUNs for Servers for iSCSI config
- TENANT - Create the igroups for iSCSI
- TENANT - Create the boot LUNs for Servers for FC config
- TENANT - Get the FCP igroup names with their corresponding WWPNs
- TENANT - Create the igroups for FCP
- TENANT - Mapping LUN to iSCSI igroup
- TENANT - Mapping data LUN to iSCSI igroup
- TENANT - Mapping LUN to FCP igroup

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `netapp.ontap.na_ontap_lun`
- `netapp.ontap.na_ontap_igroup`
- `ansible.builtin.set_fact`
- `netapp.ontap.na_ontap_lun_map`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `tid`
- `tenant_name`
- `t_ib_vlan_name`
- `t_ib_vlan_id`
- `lan_state`
- `t_nfs_vlan_name`
- `t_nfs_vlan_id`
- `t_iscsiA_vlan_name`
- `t_iscsiA_vlan_id`
- `t_iscsiB_vlan_name`
- `t_iscsiB_vlan_id`
- `t_access_vlan_name`
- `t_access_vlan_id`
- `network_prefix`
- `baseIP`
- `network_mask`
- `t_ib_network_prefix`
- `t_ib_network_mask`
- `t_iscsiA_network_prefix`
- `t_iscsiA_network_mask`

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
