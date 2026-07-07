# Role: `rancher/pre_rke_install`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Prepares hosts for RKE2 installation, including proxy and prerequisite work.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- `TENANT.yml`

## Task Flow

Main tasks detected:

- Add Interfaces to defined zone
- Restart Firewalld
- Disable FIREWALLD
- Disable SWAP since kubernetes can't work with swap enabled (1/2)
- Remove swap from fstab (2/2)
- Add a line to a file if the file does not exist, without passing regexp
- Determine the current repository filenames for airgapped installation in {{ tarball_install }}/airgap/
- Create images directory if it does not exist
- Copy repository files for Air-Gapped installation into place
- Create manifest directory if it does not exist
- Check for local manifests
- Copy local manifests into /var/lib/rancher/rke2/server/manifests/
- Check for rke2-server Proxy configuration
- Copy RKE2-Proxy config to /etc/default

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `ansible.posix.firewalld`
- `ansible.builtin.service`
- `ansible.builtin.systemd`
- `shell`
- `ansible.builtin.lineinfile`
- `ansible.builtin.find`
- `ansible.builtin.file`
- `copy`
- `ansible.builtin.stat`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `item`
- `firewall_interfaces`
- `proxys`
- `tarball_install`
- `tenant_dir`

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
