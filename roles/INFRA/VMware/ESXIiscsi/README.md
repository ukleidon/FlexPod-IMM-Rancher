# Role: `INFRA/VMware/ESXIiscsi`

[Framework README](../../../../README.md) | [Role index](../../../../docs/roles/README.md) | [Variables](../../../../docs/variables.md)

## Purpose

Configures VMware or ESXi integration around FlexPod storage and network assumptions.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `modify_esxi_iscsi_vswitch.yml`
- `create_esxi_iscsiB_PG.yml`
- `create_esxi_iscsi_vmk.yml`
- `add_esxi_iscsi_targets.yml`
- `rescan_esxi_iscsi_HBA.yml`
- `add_esxi_coredump.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `command`
- `community.vmware.vmware_portgroup`
- `community.vmware.vmware_vmkernel`
- `include_tasks`
- `community.vmware.vmware_vswitch`
- `community.vmware.vmware_host_scanhba`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `vcenter_hostname`
- `item`
- `iscsi_targets`
- `iscsi_b_portgroup`
- `iscsi_b_vswitch`
- `inventory_hostname`
- `ansible_user`
- `ansible_ssh_pass`
- `iscsi_mtu`
- `iscsi_a_vswitch`
- `iscsi_a_portgroup`
- `iscsi_a_ip`
- `iscsi_mask`
- `iscsi_b_ip`
- `iscsi_a_uplink`
- `iscsi_b_uplink`

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
