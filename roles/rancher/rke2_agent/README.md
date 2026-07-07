# Role: `rancher/rke2_agent`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Installs and joins RKE2 worker/agent nodes.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`
- `RKE2.yml`

## Task Flow

Main tasks detected:

- RKE2 agent and server tasks
- Does config file already have server token?  # noqa command-instead-of-shell
- Add token to config.yaml
- Does config file already have server url?  # noqa command-instead-of-shell
- Add server url to config file
- Start rke2-agent

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `ansible.builtin.include_role`
- `ansible.builtin.command`
- `ansible.builtin.lineinfile`
- `ansible.builtin.systemd`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `hostvars`
- `kubernetes_api_server_host`

## Configuration To Expect

Expect RKE2 server/agent installation, cluster join configuration, proxy handling, and service state changes.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
- [SUSE RKE2 Documentation](https://docs.rke2.io/)
