# Role: `rancher/rke2_common`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Provides common RKE2 install, tarball, repository, image, and service tasks.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

The role calls these task files from `tasks/main.yml` or nested includes:

- `previous_install.yml`
- `images_tarball_install.yml`
- `calculate_rke2_version.yml`
- `tarball_install.yml`
- `rpm_install.yml`
- `network_manager_fix.yaml`
- `config.yml`
- `iptables_rules.yml`
- `add-audit-policy-config.yml`
- `add-registry-config.yml`

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `ansible.builtin.file`
- `ansible.builtin.copy`
- `group`
- `ansible.builtin.set_fact`
- `ansible.builtin.shell`
- `ansible.builtin.debug`
- `ansible.builtin.group`
- `ansible.builtin.user`
- `shell`
- `ansible.builtin.service`
- `ansible.builtin.reboot`
- `ansible.builtin.stat`
- `ansible.builtin.slurp`
- `ansible.utils.update_fact`
- `ansible.builtin.lineinfile`
- `ansible.builtin.iptables`
- `ansible.builtin.apt`
- `ansible.builtin.service_facts`
- `ansible.builtin.package_facts`
- `ansible.builtin.include_tasks`
- `ansible.builtin.systemd`
- `ansible.builtin.include_role`
- `ansible.builtin.blockinfile`
- `ansible.builtin.yum_repository`
- `ansible.builtin.yum`
- `ansible.builtin.tempfile`
- `ansible.builtin.get_url`
- `ansible.builtin.package`
- `ansible.builtin.unarchive`
- `ansible.builtin.command`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `audit_policy_config_file_path`
- `manifest_config_file_path`
- `registry_config_file_path`
- `rke2_channel`
- `rke2_version_url`
- `rke2_full_version`
- `rke2_version_dot_tmp`
- `rke2_version_majmin_tmp`
- `rke2_version_rpm_tmp`
- `rke2_version_dot`
- `rke2_version_majmin`
- `rke2_version_rpm`
- `full_orig_rke2_config`
- `rke2_config`
- `node_labels`
- `rke2_config_node_labels`
- `all_node_labels`
- `updated_rke2_config`
- `node_taints`
- `rke2_config_node_taints`

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
