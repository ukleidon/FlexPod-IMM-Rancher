# Role: `INFRA/VMware/ESXIhosts`

[Framework README](../../../../README.md) | [Role index](../../../../docs/roles/README.md) | [Variables](../../../../docs/variables.md)

## Purpose

Configures VMware or ESXi integration around FlexPod storage and network assumptions.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `add_esxi_ntp.yml`
- `modify_esxi_vswitch0.yml`
- `create_esxi_ib_mgmt_PG.yml`
- `create_esxi_oob_mgmt_PG.yml`
- `create_esxi_nfs_PG.yml`
- `add_esxi_nfs_vmk.yml`
- `add_esxi_nfs_datastores.yml`
- `set_esxi_powermgmt_policy.yml`
- `upgrade_ESXi_drivers.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `community.vmware.vmware_host_datastore`
- `community.vmware.vmware_vmkernel`
- `set_fact`
- `community.vmware.vmware_host_ntp`
- `community.vmware.vmware_host_service_manager`
- `community.vmware.vmware_portgroup`
- `include_tasks`
- `community.vmware.vmware_vswitch`
- `community.vmware.vmware_host_powermgmt_policy`
- `command`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `inventory_hostname`
- `ansible_user`
- `ansible_ssh_pass`
- `item`
- `nfs_datastore_type`
- `nfs_ds_lif_map`
- `swap_ds_lif_map`
- `vcls_ds_lif_map`
- `nfs_portgroup`
- `nfs_ip`
- `nfs_mask`
- `ib_mgmt_ntp_servers`
- `ntp_server_string`
- `vcenter_hostname`
- `vcenter_username`
- `vcenter_password`
- `dvs_name`
- `vmotion_portgroup`
- `vmotion_ip`
- `vmotion_mask`

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
