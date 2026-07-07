# Role: `INFRA/create_pools`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds Intersight pools such as IP, MAC, UUID, IQN, iSCSI, and Fibre Channel WWN pools.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `create_ip_pools.yml`
- `create_mac_pools.yml`
- `create_uuid_pool.yml`
- `create_iqn_pools.yml`
- `create_iscsi_pools.yml`
- `create_fc_ww_pools.yml`
- `create_oob_ip_pool.yml`
- `create_ib_ip_pool.yml`

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
- `ip_pool_start_for_management_access`
- `size_of_ip_pool_for_management_access`
- `name_of_ip_pool_for_management_access`
- `description_of_ip_pool_for_mgmt_access`
- `netmask_mgmt`
- `gateway_mgmt`
- `primary_dns_mgmt`
- `secondary_dns_mgmt`
- `ip_block`
- `intersight_org`
- `prefix`
- `org_name`
- `name_of_wwnn_pool`
- `description_of_wwnn_pool`
- `wwnn_pool_start`

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
