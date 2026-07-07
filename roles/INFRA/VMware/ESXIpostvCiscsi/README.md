# Role: `INFRA/VMware/ESXIpostvCiscsi`

[Framework README](../../../../README.md) | [Role index](../../../../docs/roles/README.md) | [Variables](../../../../docs/variables.md)

## Purpose

Configures VMware or ESXi integration around FlexPod storage and network assumptions.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `migrate_to_iscsi_nvme_vds.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `include_tasks`
- `community.vmware.vmware_vmkernel`
- `community.vmware.vmware_vswitch`
- `community.vmware.vmware_dvs_host`
- `command`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `iscsi_a_vswitch`
- `vcenter_hostname`
- `vcenter_username`
- `vcenter_password`
- `inventory_hostname`
- `iscsi_a_portgroup`
- `iscsi_nvme_tcp_dvs_name`
- `iscsi_a_uplink`
- `iscsi_nvme_tcp_vds_vlan_list`
- `iscsi_mtu`
- `iscsi_a_ip`
- `iscsi_mask`
- `iscsi_b_vswitch`
- `iscsi_b_portgroup`
- `iscsi_b_uplink`
- `iscsi_b_ip`
- `nvme_tcp_mtu`
- `nvme_a_ip`
- `nvme_mask`
- `nvme_b_ip`

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
