# Operations

[Documentation index](README.md) | [Playbooks](playbooks.md) | [Validation](validation.md)

Use this page as a day-to-day runbook. The commands are ordered from lowest risk to live configuration.

## Execution Environment Checklist

1. Confirm the Ansible control host can reach the jumphost, infrastructure devices, Intersight API, and tenant hosts.
2. Confirm the required collections are installed:

```bash
ansible-galaxy collection install cisco.intersight cisco.nxos netapp.ontap community.vmware
```

3. Confirm Python dependencies required by the control host image are already present, especially for NetApp ONTAP, VMware, and network transports.
4. Confirm the Intersight API key files referenced by `group_vars/ucs.yml` and the selected tenant vars file exist on the control host.

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

## Before You Run

1. Confirm the SSH path to the Ansible host works.
2. Confirm `inventory` points at the intended devices and hosts.
3. Confirm the tenant vars file exists: `tenants/<tenant>/vars.yml`.
4. Confirm any API key references in tenant vars and `group_vars/ucs.yml` are current.
5. Confirm VLAN IDs and CIDRs do not collide with existing tenants.

## Validate Shared Infrastructure

```bash
ansible-playbook -i inventory INFRA.yml --syntax-check
ansible-playbook -i inventory INFRA.yml -C
```

Expected result: no syntax errors. Check mode can report changed tasks on network devices when it detects desired configuration differences.

## Validate One Tenant

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=eibe --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=eibe -C
```

Expected result: tenant vars load after shared defaults, Nexus ASA trunk tasks have access VLAN lists, and no undefined variables appear.

## Validate Tenant Removal

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=eibe -e lan_state=absent -C
```

Expected result: only the selected tenant is removed from device intent. No other tenant vars should be edited or required.

## Create A New Tenant

```bash
./scripts/create_tenant.py \
  --name tenant41 \
  --tid 41 \
  --access-vlan 455 \
  --access-prefix 172.16.185 \
  --nfs-vlan 456 \
  --nfs-prefix 172.16.186 \
  --dry-run
```

Remove `--dry-run` only after the generated target path and virtual registry target look correct.

## Live Run

Run live only after syntax and check mode are understood:

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=eibe
```

## Troubleshooting Pointers

- Undefined variable: check `roles/TENANT/env_vars/tasks/main.yml` load order and the selected tenant vars file.
- Wrong VLAN on Nexus: check `t_access_vlan_id`, `t_nfs_vlan_id`, `t_storage_vlan_list`, and `t_access_vlans_list`.
- Intersight policy mismatch: check `group_vars/ucs.yml`, tenant API key references, and generated names from `group_vars/tenant_defaults.yml`.
- ONTAP object mismatch: check SVM, LIF, WWPN, IQN, pool, and protocol values in the tenant vars file.
