# Role: `INFRA/VMware/VMWAREvcenter`

[Framework README](../../../../README.md) | [Role index](../../../../docs/roles/README.md) | [Variables](../../../../docs/variables.md)

## Purpose

Configures VMware or ESXi integration around FlexPod storage and network assumptions.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `create_dc.yml`
- `create_cluster.yml`
- `create_vds.yml`
- `create_vds_pg.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `community.vmware.vmware_cluster`
- `community.vmware.vmware_cluster_drs`
- `community.vmware.vmware_cluster_ha`
- `community.vmware.vmware_datacenter`
- `community.vmware.vmware_dvswitch`
- `community.vmware.vmware_dvs_portgroup`
- `include_tasks`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `vcenter_hostname`
- `vcenter_username`
- `vcenter_password`
- `vcenter_dc`
- `vcenter_cluster`
- `dvs_name`
- `dv_version`
- `dv_mtu`
- `dv_uplink`
- `dv_protocol`
- `dv_operation`
- `iscsi_nvme_tcp_dvs_name`
- `item`
- `vds0_vlan_list`
- `iscsi_nvme_tcp_vds_vlan_list`

## Configuration To Expect

Expect the configuration described by the called task files. Review the task flow and variables before running live.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
- [Community VMware Ansible Collection](https://docs.ansible.com/projects/ansible/latest/collections/community/vmware/index.html)
