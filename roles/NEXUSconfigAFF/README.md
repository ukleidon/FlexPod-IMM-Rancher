# Role: `NEXUSconfigAFF`

[Framework README](../../README.md) | [Role index](../../docs/roles/README.md) | [Variables](../../docs/variables.md)

## Purpose

Runs the role task flow described below.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `initiate_nxos_config_backup.yml`
- `configure_nxos_vlans.yml`
- `set_nxos_interfaces.yml`
- `configure_nxos_vpc.yml`
- `update_peer_link.yml`
- `save_nxos_config.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `cisco.nxos.nxos_vlans`
- `cisco.nxos.nxos_vpc_interface`
- `cisco.nxos.nxos_config`
- `include_tasks`
- `cisco.nxos.nxos_lag_interfaces`
- `cisco.nxos.nxos_interfaces`
- `cisco.nxos.nxos_l2_interfaces`
- `cisco.nxos.nxos_command`
- `set_fact`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `item`
- `storage_vlan_list`
- `aff_port_channels`
- `backup_dir`
- `storage_C_PC`
- `storage_C_interface_list`
- `storage_D_PC`
- `storage_D_interface_list`
- `native_vlan_id`
- `storage_vlans_list`
- `current_config`
- `parsed_config`
- `update_vlans`
- `peerlink_PC`

## Configuration To Expect

Expect NX-OS features, VLAN objects, trunk allowed VLAN lists, port-channel settings, vPC settings, and saved running configuration tasks.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
- [Cisco Nexus 9000 Configuration Guides](https://www.cisco.com/c/en/us/support/switches/nexus-9000-series-switches/products-installation-and-configuration-guides-list.html)
- [Cisco NX-OS Ansible Collection](https://docs.ansible.com/projects/ansible/latest/collections/cisco/nxos/index.html)
