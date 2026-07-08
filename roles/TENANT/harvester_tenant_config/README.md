# Role: `TENANT/harvester_tenant_config`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Tenant roles](../../../docs/roles/tenant.md)

## Purpose

Creates or removes the Harvester HCI objects required for one virtual tenant.
The role replaces the legacy CSV and shell-script workflow from
the original lab artifact directory with tenant variables from
`tenants/<tenant>/vars.yml`.

## Called By

- `HARVESTER.yml`
- `HARVESTER_RKE.yml`

## Functions Called

- `ansible.builtin.assert` validates that the selected tenant is virtual and
  has the required VLAN/CIDR values.
- `kubernetes.core.k8s_info` reads the Harvester cloud-init template
  `sle-micro-default`.
- `ansible.builtin.template` writes generated manifests to
  `tenants/<tenant>/manifests/harvester`.
- `kubernetes.core.k8s` applies or removes Harvester namespace, network, DHCP,
  and cloud-init resources.

## Configuration To Expect

For tenant `tenant01`, the role creates these resources on kube context
`harvester`:

- Namespace `tenant01`.
- NetworkAttachmentDefinitions `tenant01-access` and `tenant01-storage`.
- DHCP IPPools for the access and storage networks.
- Tenant-adapted cloud-init ConfigMap `tenant01-sle-micro-default`.

The access network uses `t_access_vlan_id` and `t_access_network_prefix`.
The storage network uses `t_nfs_vlan_id` and `t_nfs_network_prefix`. Generated
files stay inside the tenant directory so tenants remain independently
configurable and removable.

The `sle-micro-default` cloud-init template contains the token `[TENANT]` in
entries such as `[TENANT].example.com`. The role replaces only the token with
the lower-case tenant name, for example `tenant01`, so the rendered value is
`tenant01.example.com`.

## Operator Runbook

```bash
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 -C
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01
```

To remove only the selected tenant's Harvester support objects:

```bash
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 -e lan_state=absent -C
```

## Product References

- [SUSE Harvester Documentation](https://docs.harvesterhci.io/)
- [Rancher Kubernetes Engine 2](https://docs.rke2.io/)
- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
