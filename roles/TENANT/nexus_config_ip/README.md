# Role: `TENANT/nexus_config_ip`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds or removes VRFs, SVIs, HSRP addresses, and default gateway routing on Nexus switches.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `initiate_nxos_config_backup.yml`
- `create_vrf.yml`
- `set_nxos_interfaces.yml`
- `save_nxos_config.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `cisco.nxos.nxos_vrf`
- `cisco.nxos.nxos_config`
- `include_tasks`
- `cisco.nxos.nxos_l3_interfaces`
- `cisco.nxos.nxos_interfaces`
- `cisco.nxos.nxos_vrf_interface`
- `cisco.nxos.nxos_hsrp`
- `group`
- `cisco.nxos.nxos_static_routes`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `tenant_name`
- `item`
- `t_svi_list`
- `backup_dir`
- `tid`

## Configuration To Expect

Expect VRFs, VLAN SVIs, HSRP virtual IPs, interface enablement, and default routes for tenant or infrastructure networks.

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
