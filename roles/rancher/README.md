# Role Family: `rancher`

[Framework README](../../README.md) | [Role index](../../docs/roles/README.md)

This directory groups related automation roles. Each role README explains the purpose, task functions called, and expected configuration.

| Role                                           | Called by                  | Expected configuration                                                       |
| ---------------------------------------------- | -------------------------- | ---------------------------------------------------------------------------- |
| [`env_vars`](env_vars/README.md)               | `TENANT.yml`, `TENANT.yml` | Loads the ordered YAML variable stack used by the playbook.                  |
| [`pre_rke_install`](pre_rke_install/README.md) | `TENANT.yml`               | Prepares hosts for RKE2 installation, including proxy and prerequisite work. |
| [`rke2_agent`](rke2_agent/README.md)           | `TENANT.yml`               | Installs and joins RKE2 worker/agent nodes.                                  |
| [`rke2_common`](rke2_common/README.md)         | -                          | Provides common RKE2 install, tarball, repository, image, and service tasks. |
| [`rke2_server`](rke2_server/README.md)         | `TENANT.yml`               | Installs and joins RKE2 control-plane nodes.                                 |
