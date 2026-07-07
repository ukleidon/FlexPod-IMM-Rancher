# Role: `INFRA/nexus_config_asa`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds or removes ASA-facing access and trunk VLAN configuration on Nexus switches.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `INFRA.yml`

## Task Flow

Main tasks detected:

- Configure Nexus for FlexPod
- Configure ONTAP for FlexPod
- Create Tenant in Intersight
- Modify the mtu speed and duplex for ASA ports
- {{ item.interface }}
- Enabling Infrastructure vlans on ASA Trunk Interfaces
- {{ asa_interface_list[0].interface }}
- {{ asa_interface_list[1].interface }}
- Set - switchport mode trunk

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `cisco.nxos.nxos_interfaces`
- `cisco.nxos.nxos_l2_interfaces`
- `cisco.nxos.nxos_config`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `item`
- `asa_interface_list`
- `transfer_vlan_id`
- `native_vlan_id`
- `vlans_list`

## Configuration To Expect

Expect ASA-facing access/trunk interfaces with the selected access VLANs allowed or removed.

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
