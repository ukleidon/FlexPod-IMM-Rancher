# Rancher/RKE2 Roles

[Role index](README.md) | [Playbooks](../playbooks.md) | [Product references](../references.md)

Use this page to understand what each role is expected to configure before opening the detailed role README.

| Role                                                                       | Called by                  | Expected configuration                                                       |
| -------------------------------------------------------------------------- | -------------------------- | ---------------------------------------------------------------------------- |
| [`rancher/env_vars`](../../roles/rancher/env_vars/README.md)               | `TENANT.yml`, `TENANT.yml` | Loads the ordered YAML variable stack used by the playbook.                  |
| [`rancher/pre_rke_install`](../../roles/rancher/pre_rke_install/README.md) | `TENANT.yml`               | Prepares hosts for RKE2 installation, including proxy and prerequisite work. |
| [`rancher/rke2_agent`](../../roles/rancher/rke2_agent/README.md)           | `TENANT.yml`               | Installs and joins RKE2 worker/agent nodes.                                  |
| [`rancher/rke2_common`](../../roles/rancher/rke2_common/README.md)         | -                          | Provides common RKE2 install, tarball, repository, image, and service tasks. |
| [`rancher/rke2_server`](../../roles/rancher/rke2_server/README.md)         | `TENANT.yml`               | Installs and joins RKE2 control-plane nodes.                                 |
