# Playbooks

[Documentation index](README.md) | [Operations](operations.md) | [Validation](validation.md)

This page describes the top-level playbooks an operator should run. Each table lists the plays and role functions called by the playbook.

## CVD-Aligned Run Model

The FlexPod CVD uses separate automation stages for network, storage, compute, SAN, VMware, and final storage configuration. FlexPod-IMM-Rancher packages the current implementation into three operator entry points:

- `INFRA.yml` for the shared FlexPod foundation.
- `TENANT.yml -e tenant=<name>` for one tenant's independent lifecycle.
- Repository-specific platform playbooks, such as `HARV.yml`, when platform work should be run separately.

Do not copy old `Setup_*` playbook names from legacy examples into FlexPod-IMM-Rancher. Use the tables below to see which role functions are called by the current playbooks.

## `INFRA.yml`

Build or validate shared FlexPod infrastructure.

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

Build or remove one selected tenant.

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=ac01 -C
```

Expected configuration: Tenant VLANs, VRFs, storage objects, Intersight policies/profiles, OS install prep, RKE2, and Trident depending on inventory.

### Functions Called

| Play                                                | Hosts                    | Roles called                                                                                                                    |
| --------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| nexus                                               | nexus                    | `TENANT/env_vars`, `TENANT/nexus_config`, `TENANT/nexus_config_ip`                                                              |
| Configure ONTAP for FlexPod                         | ontap                    | `TENANT/env_vars`, `TENANT/ontap_network`, `TENANT/ontap_svm`, `TENANT/ontap_volumes`, `TENANT/ontap_lifs`, `TENANT/ontap_luns` |
| Create Tenant in Intersight                         | localhost                | `TENANT/env_vars`, `TENANT/ucs_create_pools`, `TENANT/ucs_create_server_policies`, `TENANT/ucs_create_sp_template`              |
| nexus                                               | nexus                    | `TENANT/nexus_config_proxmox`                                                                                                   |
| Prepare installation of Rancher RKE2 control nodes  | rke2_servers,rke2_agents | `rancher/env_vars`, `rancher/pre_rke_install`                                                                                   |
| Install RKE2 Controll node server                   | rke2_servers             | `rancher/env_vars`, `rancher/rke2_server`                                                                                       |
| Install RKE2 dedicated agent nodes                  | rke2_agents              | `rancher/rke2_agent`                                                                                                            |
| Deploy NetApp Trident and Configure Trident Backend | k8s                      | `TENANT/env_vars`, `TENANT/trident_install`                                                                                     |

## `HARV.yml`

Run the Harvester-focused tenant workflow.

```bash
ansible-playbook -i inventory HARV.yml -e tenant=harvester -C
```

Expected configuration: Harvester tenant storage, Intersight, and platform configuration where matching inventory exists.

### Functions Called

| Play                         | Hosts     | Roles called                                                                                                                    |
| ---------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Configure ONTAP for FlexPod  | ontap     | `TENANT/env_vars`, `TENANT/ontap_network`, `TENANT/ontap_svm`, `TENANT/ontap_volumes`, `TENANT/ontap_lifs`, `TENANT/ontap_luns` |
| Create Tenant in Intersight  | localhost | `TENANT/env_vars`, `TENANT/ucs_create_pools`, `TENANT/ucs_create_server_policies`, `TENANT/ucs_create_sp_template`              |

## `AA04.yml`

Run the AA04-specific Intersight tenant workflow.

```bash
ansible-playbook -i inventory AA04.yml -C
```

Expected configuration: AA04-specific Intersight tenant objects.

### Functions Called

| Play                         | Hosts     | Roles called                                     |
| ---------------------------- | --------- | ------------------------------------------------ |
| Create Tenant in Intersight  | localhost | `TENANT/env_vars`, `SUSE/harvester_ucs_policies` |

## `delete_ONTAP_SVM_Custom.yml`

Remove a custom ONTAP SVM workflow.

```bash
ansible-playbook -i inventory delete_ONTAP_SVM_Custom.yml -C
```

Expected configuration: Selected ONTAP custom SVM objects are removed according to vars.

### Functions Called

| Play                        | Hosts | Roles called                                 |
| --------------------------- | ----- | -------------------------------------------- |
| Configure ONTAP for FlexPod | ontap | `TENANT/env_vars`, `TENANT/ontap_svm_custom` |
