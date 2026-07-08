# Role: `harvester/platform_config`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Harvester roles](../../../docs/roles/harvester.md)

## Purpose

Configures cluster-wide Harvester HCI services that support virtual tenants:
proxy settings, NTP servers, the Harvester VM DHCP add-on, common Harvester
add-ons, the `data-9000` ClusterNetwork, the storage `VlanConfig`, and the
global Harvester storage-network setting.

## Called By

- `HARVESTER.yml` when `harvester_manage_platform=true` is supplied.

## Functions Called

- `kubernetes.core.k8s` to manage Harvester `Setting`, `Addon`,
  `ClusterNetwork`, and `VlanConfig` resources.
- `ansible.builtin.assert` for input validation.

## Configuration To Expect

The role patches Harvester platform objects on the kube context named by
`harvester_context`, normally `harvester`. Because these settings are shared by
all tenants, the role is opt-in and should be run deliberately.

## Operator Runbook

```bash
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 -e harvester_manage_platform=true --tags harvester_platform -C
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 -e harvester_manage_platform=true --tags harvester_platform
```

Review the proxy, NTP, NIC, VLAN, and storage-network values before applying
the role to a production Harvester cluster.
