# Role: `INFRA/nexus_config`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds Layer 2 Nexus features, VLANs, trunk allowed VLAN lists, port-channels, and peer-link updates.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `INFRA.yml`

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `initiate_nxos_config_backup.yml`
- `configure_nxos_features.yml`
- `configure_nxos_global_settings.yml`
- `configure_domain_lookup.yml`
- `configure_nxos_vlans.yml`
- `configure_nxos_ntp.yml`
- `configure_default_gw.yml`
- `set_nxos_interfaces.yml`
- `configure_nxos_vpc.yml`
- `save_nxos_config.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `cisco.nxos.nxos_static_routes`
- `set_fact`
- `cisco.nxos.nxos_command`
- `cisco.nxos.nxos_feature`
- `cisco.nxos.nxos_config`
- `cisco.nxos.nxos_ntp_global`
- `cisco.nxos.nxos_l3_interfaces`
- `cisco.nxos.nxos_interfaces`
- `cisco.nxos.nxos_vlans`
- `cisco.nxos.nxos_vpc`
- `cisco.nxos.nxos_vpc_interface`
- `include_tasks`
- `cisco.nxos.nxos_udld_interface`
- `cisco.nxos.nxos_lag_interfaces`
- `cisco.nxos.nxos_l2_interfaces`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `ntp_distribution_gw`
- `dns_servers`
- `dns_domain_name`
- `dns_server_string`
- `item`
- `enabled_features`
- `global_settings`
- `global_NTP_servers`
- `vpc_destination`
- `ntp_distribution_vlan`
- `IB_MGMT_ntp_dist_IP`
- `ib_mgmt_vlan_list`
- `storage_vlan_list`
- `remaining_vlan_list`
- `vpc_domain_id`
- `vpc_role_priority`
- `vpc_source`
- `peerlink_PC`
- `uplink_PC`
- `backup_dir`

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
