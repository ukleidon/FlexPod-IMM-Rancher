# Rancher/RKE2 Roles

[Role index](README.md) | [Workflows](../workflows.md) | [Playbooks](../playbooks.md) | [Product references](../references.md)

Use this page to understand what each role is expected to configure before opening the detailed role README.

| Role                                                                       | Called by                                          | Expected configuration                                                       |
| -------------------------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------- |
| [`rancher/env_vars`](../../roles/rancher/env_vars/README.md)               | `TENANT.yml`, `TENANT.yml`, `RKE2.yml`, `RKE2.yml` | Loads the ordered YAML variable stack used by the playbook.                  |
| [`rancher/harvester_rke_cluster`](../../roles/rancher/harvester_rke_cluster/README.md) | `HARVESTER_RKE.yml` | Creates or removes a Rancher-provisioned RKE2 cluster on Harvester HCI. |
| [`rancher/harvester_workload_config`](../../roles/rancher/harvester_workload_config/README.md) | `HARVESTER_RKE.yml` | Applies tenant kube-vip, storage annotations, and optional Kasten configuration to the downstream RKE2 cluster. |
| [`rancher/pre_rke_install`](../../roles/rancher/pre_rke_install/README.md) | `TENANT.yml`, `RKE2.yml`                           | Prepares hosts for RKE2 installation, including proxy and prerequisite work. |
| [`rancher/rke2_agent`](../../roles/rancher/rke2_agent/README.md)           | `TENANT.yml`, `RKE2.yml`                           | Installs and joins RKE2 worker/agent nodes.                                  |
| [`rancher/rke2_common`](../../roles/rancher/rke2_common/README.md)         | -                                                  | Provides common RKE2 install, tarball, repository, image, and service tasks. |
| [`rancher/rke2_server`](../../roles/rancher/rke2_server/README.md)         | `TENANT.yml`, `RKE2.yml`                           | Installs and joins RKE2 control-plane nodes.                                 |

## Rancher-Provisioned Harvester Clusters

The Harvester RKE roles are local-control-node roles that use kubeconfig
contexts rather than SSHing into tenant hosts. `rancher/harvester_rke_cluster`
creates Rancher provisioning objects for `<tenant>-rke`; `rancher/harvester_workload_config`
runs later, after the downstream kube context exists.

Public defaults use placeholders for Rancher cloud credentials and creator IDs.
Override those values from private inventory or Ansible Vault before a live run.
