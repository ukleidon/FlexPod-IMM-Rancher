# Role: `rancher/harvester_rke_cluster`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Rancher roles](../../../docs/roles/rancher.md)

## Purpose

Creates or removes a Rancher-provisioned RKE2 cluster on Harvester HCI. The
default cluster name is `<tenant>-rke` and the default machine pool creates
three virtual machines in the tenant namespace.

## Called By

- `HARVESTER_RKE.yml`

## Functions Called

- `kubernetes.core.k8s_info` discovers the Harvester image and reads the
  tenant-adapted cloud-init ConfigMap.
- `ansible.builtin.template` writes generated manifests under
  `tenants/<tenant>/manifests/rancher`.
- `kubernetes.core.k8s` applies Rancher `HarvesterConfig` and
  `provisioning.cattle.io/v1 Cluster` resources.

## Configuration To Expect

The role uses kube context `harvester` to read Harvester state and context
`rancher` to create Rancher provisioning objects. Override these context names
from private variables when your kubeconfig uses different names. It selects
the newest Harvester image whose display name matches `sl-micro.x86_64-6.2*`
unless `harvester_rke_image_name` is set explicitly.

If the tenant-adapted cloud-init ConfigMap does not exist yet, the role falls
back to the Harvester `sle-micro-default` template and replaces `[TENANT]` with
the lower-case tenant name. The template already includes the domain suffix in
strings such as `[TENANT].example.com`.

## Operator Runbook

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 -C
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01
```

To remove only the selected tenant cluster:

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 -e lan_state=absent --tags harvester_rke -C
```

Review `harvester_rke_cloud_credential_secret_name` and
`harvester_rke_cloud_provider_config_secret` before using the role on another
Rancher installation. Also review `harvester_rke_rancher_creator_id`; Rancher
validates this annotation during cluster creation. The public defaults are
placeholders and must be supplied by a private inventory, Ansible Vault, or an
ignored local overlay. If a cluster already exists, the role preserves the live
creator annotation.
