# Role: `rancher/harvester_workload_config`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Rancher roles](../../../docs/roles/rancher.md)

## Purpose

Converts the useful parts of the legacy `harvester/tenant.sh` and Kasten K10
helpers into an Ansible role for an already installed tenant RKE2 cluster. It
can apply the tenant kube-vip manifest, mark the snapshot class for Kasten,
make the Harvester CSI storage class non-default, apply the Trident PSA RBAC
manifest, and optionally install and configure Kasten K10.

## Called By

- `HARVESTER_RKE.yml` when `harvester_workload_apply=true` is supplied.

## Functions Called

- `kubernetes.core.k8s_info` checks existing storage and snapshot resources.
- `kubernetes.core.k8s_json_patch` updates annotations predictably.
- `kubernetes.core.helm_repository` and `kubernetes.core.helm` install Kasten
  when enabled.
- `kubernetes.core.k8s` applies generated tenant manifests.

## Configuration To Expect

The role targets kube context `<tenant>-rke` by default. It is intentionally
disabled in the top-level playbook until Rancher has created the downstream
cluster and the kubeconfig context is available.

## Operator Runbook

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 --tags workload_cluster -e harvester_workload_apply=true -C
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 --tags workload_cluster -e harvester_workload_apply=true
```

Kasten installation is opt-in:

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 --tags kasten \
  -e harvester_workload_apply=true -e harvester_workload_install_kasten=true
```

Provide StorageGRID credentials through tenant vars or extra vars before
enabling `harvester_workload_kasten_location_profile_enabled`.
