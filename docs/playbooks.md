# Playbooks

[Documentation index](README.md) | [Operations](operations.md) | [Validation](validation.md)

This page describes the top-level playbooks an operator should run. Each table lists the plays and role functions called by the playbook.

## CVD-Aligned Run Model

The FlexPod CVD uses separate automation stages for network, storage, compute, SAN, VMware, and final storage configuration. FlexPod-IMM-Rancher packages the current implementation into focused operator entry points:

- `INFRA.yml` for the shared FlexPod foundation.
- `TENANT.yml -e tenant=<name>` for one tenant's independent lifecycle.
- `RKE2.yml -e tenant=<name>` when Kubernetes platform work should be run separately.
- `HARVESTER.yml -e tenant=<name>` for Harvester tenant support objects.
- `HARVESTER_RKE.yml -e tenant=<name>` for Rancher-provisioned virtual RKE2 clusters on Harvester.

Do not copy old `Setup_*` playbook names from legacy examples into FlexPod-IMM-Rancher. Use the tables below to see which role functions are called by the current playbooks.

## `INFRA.yml`

Builds or validates shared FlexPod infrastructure.

```bash
ansible-playbook -i inventory INFRA.yml -C
```

Expected configuration: Shared Nexus, ONTAP, Intersight, StorageGRID, Proxmox, and ASA integration objects.

### Functions Called

| Play                         | Hosts     | Roles called                                                                                                           |
| ---------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------- |
| Configure Nexus for FlexPod  | nexus     | `INFRA/env_vars`, `INFRA/nexus_config`, `INFRA/nexus_config_sg`, `INFRA/nexus_config_ip`, `INFRA/nexus_config_proxmox` |
| Configure ONTAP for FlexPod  | ontap     | `INFRA/env_vars`, `INFRA/ontap_network`, `INFRA/ontap_svm`, `INFRA/ontap_volumes`, `INFRA/ontap_lifs`                  |
| Create Tenant in Intersight  | localhost | `INFRA/env_vars`, `INFRA/ucs_create_pools`                                                                             |
| Create Tenant in Intersight  | nexus     | `INFRA/env_vars`, `INFRA/nexus_config_asa`                                                                             |

## `TENANT.yml`

Builds or removes one selected tenant.

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -C
```

Expected configuration: Tenant VLANs, VRFs, storage objects, Intersight policies/profiles, OS install prep, RKE2, and Trident depending on inventory.

### Functions Called

| Play                                                | Hosts                          | Roles called                                                                                                                                         |
| --------------------------------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| nexus                                               | nexus                          | `TENANT/env_vars`, `TENANT/nexus_config`, `TENANT/nexus_config_ip`, `TENANT/nexus_config_sg`, `TENANT/nexus_config_asa`                              |
| Configure ONTAP for FlexPod                         | ontap                          | `TENANT/env_vars`, `TENANT/ontap_network`, `TENANT/ontap_svm`, `TENANT/ontap_volumes`, `TENANT/ontap_lifs`, `TENANT/ontap_luns`, `TENANT/ontap_nvme` |
| Create Tenant in Intersight                         | localhost                      | `TENANT/env_vars`, `TENANT/ucs_create_pools`, `TENANT/ucs_create_server_policies`, `TENANT/ucs_create_sp_template`                                   |
| Create Server Profiles from Template                | localhost                      | `TENANT/env_vars`, `TENANT/ucs_create_server`                                                                                                        |
| Install SUSE Linux                                  | rke2_servers,rke2_agents,hosts | `TENANT/env_vars`, `TENANT/os_install_suse`                                                                                                          |
| Prepare installation of Rancher RKE2 control nodes  | rke2_servers,rke2_agents       | `rancher/env_vars`, `rancher/pre_rke_install`                                                                                                        |
| Install RKE2 Controll node server                   | rke2_servers                   | `rancher/env_vars`, `rancher/rke2_server`                                                                                                            |
| Install RKE2 dedicated agent nodes                  | rke2_agents                    | `rancher/rke2_agent`                                                                                                                                 |
| Deploy NetApp Trident and Configure Trident Backend | k8s                            | `TENANT/env_vars`, `TENANT/trident_install`                                                                                                          |

## `RKE2.yml`

Runs the RKE2 role flow for a selected tenant context.

```bash
ansible-playbook -i inventory RKE2.yml -e tenant=tenant01 -C
```

Expected configuration: RKE2 prerequisite, server, and agent configuration where matching hosts exist.

### Functions Called

| Play                | Hosts        | Roles called                                  |
| ------------------- | ------------ | --------------------------------------------- |
| Testing play        | rke2_servers | `rancher/env_vars`, `rancher/pre_rke_install` |
| Install RKE2 Server | rke2_servers | `rancher/env_vars`, `rancher/rke2_server`     |
| Agent play          | rke2_agents  | `rancher/rke2_agent`                          |

## `HARVESTER.yml`

Creates Harvester HCI support objects for one virtual tenant. Platform-wide
Harvester settings are available through the same playbook but are opt-in.

```bash
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 -C
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 -e harvester_manage_platform=true --tags harvester_platform -C
```

The Harvester playbooks use `harvester_ansible_python_interpreter`, defaulting
to `.venv/bin/python` under the repository root, because `kubernetes.core`
requires the Python Kubernetes client on the Ansible controller. Install the
Python dependency with `python -m pip install -r requirements-python.txt` inside
that virtualenv, or override the interpreter variable.

Expected configuration: tenant namespace, Harvester access/storage networks,
DHCP IPPools, and tenant-adapted `sle-micro-default` cloud-init.

### Functions Called

| Play | Hosts | Roles called |
| --- | --- | --- |
| Preflight tenant input and variable files | localhost | `common/tenant_preflight` |
| Configure Harvester platform baseline | localhost | `TENANT/env_vars`, `harvester/platform_config` |
| Configure Harvester tenant support objects | localhost | `TENANT/env_vars`, `TENANT/harvester_tenant_config` |

## `HARVESTER_RKE.yml`

Creates a virtual RKE2 cluster through Rancher, using Harvester HCI for the
virtual machines. The default cluster name is `<tenant>-rke` and the default
node count is three.

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 -C
```

Expected configuration: Harvester tenant objects plus Rancher
`HarvesterConfig` and `provisioning.cattle.io/v1 Cluster` manifests. Optional
post-cluster configuration can apply kube-vip, storage annotations, and Kasten
K10 once the downstream kubeconfig context exists.

### Functions Called

| Play | Hosts | Roles called |
| --- | --- | --- |
| Preflight tenant input and variable files | localhost | `common/tenant_preflight` |
| Prepare Harvester objects for the virtual tenant | localhost | `TENANT/env_vars`, `TENANT/harvester_tenant_config` |
| Create virtual RKE2 cluster through Rancher | localhost | `TENANT/env_vars`, `rancher/harvester_rke_cluster` |
| Configure the installed virtual RKE2 cluster | localhost | `TENANT/env_vars`, `rancher/harvester_workload_config` |
