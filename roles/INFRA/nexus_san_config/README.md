# Role: `INFRA/nexus_san_config`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds Fibre Channel SAN features, interfaces, VSANs, device-alias entries, zones, and zonesets.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `configure_mds_features.yml`
- `configure_mds_interfaces.yml`
- `configure_mds_vsans.yml`
- `configure_mds_da.yml`
- `configure_mds_zones.yml`
- `activate_mds_zoneset.yml`
- `save_mds_config.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `cisco.nxos.nxos_zone_zoneset`
- `cisco.nxos.nxos_devicealias`
- `cisco.nxos.nxos_feature`
- `cisco.nxos.nxos_interfaces`
- `cisco.nxos.nxos_udld_interface`
- `cisco.nxos.nxos_command`
- `cisco.nxos.nxos_l2_interfaces`
- `command`
- `cisco.nxos.nxos_config`
- `cisco.nxos.nxos_vsan`
- `include_tasks`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `vsan_id`
- `zoneset_name`
- `fcp_zone_name`
- `fc_nvme_zone_name`
- `item`
- `fcp_device_alias_list`
- `fc_nvme_device_alias_list`
- `enabled_mds_features`
- `ucs_interface_list`
- `port_channel_id`
- `port_channel_description`
- `port_channel_speed`
- `port_channel_duplex`
- `native_vlan_id`
- `storage_interface_list`
- `vsan_name`

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
- [Cisco MDS 9000 Configuration Guides](https://www.cisco.com/c/en/us/support/storage-networking/mds-9000-nx-os-san-os-software/products-installation-and-configuration-guides-list.html)
