# Role: `TENANT/nexus_config`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds Layer 2 Nexus features, VLANs, trunk allowed VLAN lists, port-channels, and peer-link updates.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `initiate_nxos_config_backup.yml`
- `configure_nxos_features.yml`
- `configure_nxos_vlans.yml`
- `configure_default_gw.yml`
- `set_nxos_interfaces.yml`
- `save_nxos_config.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `cisco.nxos.nxos_static_routes`
- `cisco.nxos.nxos_feature`
- `cisco.nxos.nxos_vlans`
- `cisco.nxos.nxos_config`
- `include_tasks`
- `cisco.nxos.nxos_l2_interfaces`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `ntp_distribution_gw`
- `item`
- `enabled_features`
- `t_ib_mgmt_vlan_list`
- `t_storage_vlan_list`
- `t_remaining_vlan_list`
- `backup_dir`
- `native_vlan_id`
- `t_all_vlans_list`
- `peerlink_PC`
- `t_mgmt_vlans_list`
- `uplink_PC`
- `t_storage_vlans_list`
- `storage_A_PC`
- `storage_C_PC`

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
