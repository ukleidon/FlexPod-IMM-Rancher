# Role: `TENANT/ucs_create_sp_template`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Builds Intersight server profile templates and derives tenant server profiles.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`
- `HARV.yml`

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `gather_policy_info.yml`
- `create_fc_server_profile_template.yml`
- `derive_fc_profiles.yml`
- `create_iscsi_server_profile_template.yml`
- `derive_iscsi_profiles.yml`
- `create_local_server_profile_template.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `cisco.intersight.intersight_rest_api`
- `include_tasks`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `api_private_key`
- `api_key_id`
- `api_uri`
- `validates_certs`
- `state`
- `name_of_fc_SPT`
- `description_of_fc_SPT`
- `bios_policy_details`
- `fc_boot_order_policy_details`
- `imc_access_policy_details`
- `ipmi_policy_details`
- `local_user_policy_details`
- `fc_lan_connectivity_policy_details`
- `san_connectivity_policy_details`
- `kvm_policy_details`
- `vmedia_policy_details`
- `intersight_org`
- `prefix`
- `uuid_pool_details`
- `name_of_iscsi_SPT`

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
