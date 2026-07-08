# Operations

[Documentation index](README.md) | [Workflows](workflows.md) | [Playbooks](playbooks.md) | [Validation](validation.md)

Use this page as a day-to-day runbook. The commands are ordered from lowest risk to live configuration.

## Execution Environment Checklist

1. Confirm the Ansible control host can reach the jumphost, infrastructure devices, Intersight API, and tenant hosts.
2. Confirm the required Ansible collections are installed:

```bash
ansible-galaxy collection install cisco.intersight cisco.nxos netapp.ontap community.vmware kubernetes.core
```

3. Create the repository-local Python environment used by the Harvester playbooks when Kubernetes modules are required:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-python.txt
```

4. Confirm Python dependencies required by the control host image are already present, especially for NetApp ONTAP, VMware, Kubernetes, and network transports.
5. Confirm the Intersight API key files referenced by `group_vars/ucs.yml` and the selected tenant vars file exist on the control host.
6. Confirm the kubeconfig contexts for Rancher and Harvester exist when running `HARVESTER.yml` or `HARVESTER_RKE.yml`. Public defaults use `harvester` and `rancher`; private deployments can override `harvester_context` and `rancher_context`.

## CVD-Aligned Rollout Order

Use the Cisco FlexPod IaC CVD as the product sequencing reference, then run the FlexPod-IMM-Rancher playbooks that map to that sequence:

| Stage | Command | Purpose |
| --- | --- | --- |
| Shared foundation syntax | `ansible-playbook -i inventory INFRA.yml --syntax-check` | Confirm base playbook parsing before touching devices. |
| Shared foundation check mode | `ansible-playbook -i inventory INFRA.yml -C` | Validate shared Nexus, ONTAP, Intersight, StorageGRID, Proxmox, and ASA intent. |
| Shared foundation live | `ansible-playbook -i inventory INFRA.yml` | Configure shared infrastructure after check-mode output is understood. |
| Tenant syntax | `ansible-playbook -i inventory TENANT.yml -e tenant=<name> --syntax-check` | Confirm the selected tenant variable stack loads. |
| Tenant check mode | `ansible-playbook -i inventory TENANT.yml -e tenant=<name> -C` | Validate only that tenant's network, storage, compute, and optional platform intent. |
| Tenant live | `ansible-playbook -i inventory TENANT.yml -e tenant=<name>` | Configure the selected tenant independently. |
| Optional RKE2 check mode | `ansible-playbook -i inventory RKE2.yml -e tenant=<name> -C` | Validate Kubernetes platform configuration when run outside `TENANT.yml`. |
| Harvester tenant syntax | `ansible-playbook -i inventory HARVESTER.yml -e tenant=<name> --syntax-check` | Confirm the virtual tenant can load Harvester support roles. |
| Harvester tenant check mode | `ansible-playbook -i inventory HARVESTER.yml -e tenant=<name> -C` | Validate tenant namespace, networks, DHCP pools, and cloud-init intent against Harvester. |
| Virtual RKE2 syntax | `ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=<name> --syntax-check` | Confirm Rancher and Harvester RKE2 provisioning roles parse. |
| Virtual RKE2 check mode | `ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=<name> -C` | Validate Rancher provisioning intent when private Rancher and Harvester values are supplied. |

## Before You Run

1. Confirm the SSH path to the Ansible host works.
2. Confirm `inventory` points at the intended devices and hosts.
3. Confirm the tenant vars file exists: `tenants/<tenant>/vars.yml`.
4. Confirm any API key references in tenant vars and `group_vars/ucs.yml` are current.
5. Confirm VLAN IDs and CIDRs do not collide with existing tenants.
6. For Harvester workflows, confirm the selected tenant is virtual or explicitly allowed through `harvester_tenant_force_non_virtual`.
7. For Rancher-provisioned RKE2, confirm the Rancher Harvester cloud credential, cloud-provider config secret, and creator ID are provided from private variables.

## Validate Shared Infrastructure

```bash
ansible-playbook -i inventory INFRA.yml --syntax-check
ansible-playbook -i inventory INFRA.yml -C
```

Expected result: no syntax errors. Check mode can report changed tasks on network devices when it detects desired configuration differences.

## Validate One Tenant

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -C
```

Expected result: tenant vars load after shared defaults, Nexus ASA trunk tasks have access VLAN lists, and no undefined variables appear.

## Validate Tenant Removal

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -e lan_state=absent -C
```

Expected result: only the selected tenant is removed from device intent. No other tenant vars should be edited or required.

## Create A New Tenant

```bash
./scripts/create_tenant.py \
  --name tenant41 \
  --tid 41 \
  --access-vlan 455 \
  --access-prefix 198.51.100 \
  --nfs-vlan 456 \
  --nfs-prefix 203.0.113 \
  --dry-run
```

Remove `--dry-run` only after the generated target path and virtual registry target look correct.

## Validate Harvester Tenant Support

Use this when a virtual tenant needs Harvester namespace, network, DHCP, and cloud-init support objects:

```bash
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 -C
```

Platform-wide Harvester settings are opt-in because they affect all tenants:

```bash
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 \
  -e harvester_manage_platform=true --tags harvester_platform -C
```

Expected result: check mode can contact Harvester, read the `sle-micro-default` cloud-init ConfigMap, and report intended namespace, NetworkAttachmentDefinition, DHCP IPPool, and ConfigMap changes.

## Create A Virtual RKE2 Cluster On Harvester

Run this after the tenant support objects are valid and after private Rancher/Harvester values are supplied:

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 -C
```

Run live only after the check-mode output and Rancher placeholder overrides are correct:

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01
```

The default cluster name is `tenant01-rke` and the default node count is three. The role discovers the newest Harvester image matching `sl-micro.x86_64-6.2*` unless `harvester_rke_image_name` is set.

## Configure The Downstream RKE2 Cluster

After Rancher has created the cluster and the downstream kubeconfig context exists, optional add-ons can be applied:

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 \
  --tags workload_cluster -e harvester_workload_apply=true -C
```

Expected result: the role skips safely if the downstream kube context is absent. When the context exists, it can apply kube-vip, Trident PSA RBAC, storage annotations, optional Kasten objects, and tenant extra manifests.

## Live Run

Run live only after syntax and check mode are understood:

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01
```

## Troubleshooting Pointers

- Undefined variable: check `roles/TENANT/env_vars/tasks/main.yml` load order and the selected tenant vars file.
- Wrong VLAN on Nexus: check `t_access_vlan_id`, `t_nfs_vlan_id`, `t_storage_vlan_list`, and `t_access_vlans_list`.
- Intersight policy mismatch: check `group_vars/ucs.yml`, tenant API key references, and generated names from `group_vars/tenant_defaults.yml`.
- ONTAP object mismatch: check SVM, LIF, WWPN, IQN, pool, and protocol values in the tenant vars file.
- Harvester check-mode failure: check kubeconfig context names, `kubernetes.core` dependencies, and whether the default cloud-init ConfigMap exists.
- Rancher RKE2 creation failure: check `harvester_rke_cloud_credential_secret_name`, `harvester_rke_cloud_provider_config_secret`, `harvester_rke_rancher_creator_id`, and the selected Harvester image.
