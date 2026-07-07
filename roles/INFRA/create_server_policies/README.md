# Role: `INFRA/create_server_policies`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds Intersight server, BIOS, adapter, boot, LAN, SAN, QoS, and connectivity policies.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `gather_policy_info.yml`
- `gather_pool_info.yml`
- `create_bios_policies.yml`
- `create_imc_policy.yml`
- `create_kvm_policy.yml`
- `create_vmedia_policy.yml`
- `create_boot_order_policy.yml`
- `create_ipmi_policy.yml`
- `create_local_user_policy.yml`
- `create_ethernet_qos_policy.yml`
- `create_ethernet_network_control_policy.yml`
- `create_ethernet_adapter_policies.yml`
- `create_ethernet_network_group_policy.yml`
- `create_iscsi_adapter_policy.yml`
- `create_iscsi_target_policy.yml`
- `create_iscsi_boot_policy.yml`
- `create_iscsi_lan_connectivity_policy.yml`
- `create_fc_lan_connectivity_policy.yml`
- `create_fc_network_policy.yml`
- `create_fc_qos_policy.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `cisco.intersight.intersight_rest_api`
- `include_tasks`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `api_private_key`
- `api_key_id`
- `api_uri`
- `validate_certs`
- `state`
- `name_of_bios_policy`
- `description_of_bios_policy`
- `intersight_org`
- `prefix`
- `name_of_m5_bios_policy`
- `description_of_m5_bios_policy`
- `name_of_ethernet_adapter_vmware_policy`
- `description_of_ethernet_adapter_vmware_policy`
- `vmware_completion_queue_count`
- `vmware_completion_ring_size`
- `vmware_number_of_interrupts`
- `vmware_receive_queue_count`
- `vmware_receive_ring_size`
- `vmware_transmit_queue_count`
- `vmware_transmit_ring_size`

## Configuration To Expect

Expect Cisco Intersight pools, policies, LAN/SAN connectivity objects, boot policies, templates, and server profiles.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
- [Cisco Intersight API Docs](https://intersight.com/apidocs/)
- [Cisco Intersight Ansible Collection](https://docs.ansible.com/projects/ansible/latest/collections/cisco/intersight/index.html)
