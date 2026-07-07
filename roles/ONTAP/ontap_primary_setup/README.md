# Role: `ONTAP/ontap_primary_setup`

[Framework README](../../../README.md) | [Role index](../../../docs/roles/README.md) | [Variables](../../../docs/variables.md)

## Purpose

Runs the role task flow described below.

This README is written for operators who understand basic infrastructure concepts but do not live inside this automation every day. Run syntax and check-mode validation before using the role against live devices.

## Called By

- Not called directly by the current top-level playbooks. Treat as a helper or legacy role until referenced.

## Task Flow

Main tasks detected:

- Update the location of the ONTAP Cluster
- Ensure auto-revert is set for the cluster management interface
- Get the total number of port count across all nodes in the ONTAP Cluster
- See the total port count value
- Delete the default broadcast domains with node ports
- Set the Service processor network interface
- Zero all the spare disks
- Create the HA pairs count variable
- Ensure cluster HA status
- Disable flow control on data ports
- Enable CDP on the Storage Controller Nodes
- Enable LLDP on the Storage Controller Nodes
- Create the DNS server list
- Configure DNS
- Configure NTP
- Enable Takeover for Storage Failover
- Set Cluster's Timezone
- Add licenses using legacy keys
- Add licenses using NLF
- Configure SNMP contact

## Automation Functions Called

These are the primary Ansible modules or task functions detected in this role:

- `netapp.ontap.na_ontap_cluster`
- `netapp.ontap.na_ontap_interface`
- `ansible.builtin.set_fact`
- `ansible.builtin.debug`
- `netapp.ontap.na_ontap_broadcast_domain`
- `netapp.ontap.na_ontap_service_processor_network`
- `netapp.ontap.na_ontap_rest_cli`
- `command`
- `netapp.ontap.na_ontap_cluster_ha`
- `netapp.ontap.na_ontap_dns`
- `netapp.ontap.na_ontap_ntp`
- `netapp.ontap.na_ontap_license`
- `netapp.ontap.na_ontap_snmp_traphosts`
- `netapp.ontap.na_ontap_snmp`
- `netapp.ontap.na_ontap_user`
- `netapp.ontap.na_ontap_login_messages`
- `netapp.ontap.na_ontap_security_config`

## Inputs To Check

Most values come from `group_vars/*.yml`, `group_vars/tenant_defaults.yml`, `host_vars/*.yml`, or `tenants/<tenant>/vars.yml`. Pay particular attention to:

- `cluster_location`
- `cluster_name`
- `inventory_hostname`
- `username`
- `password`
- `cluster_mgmt_auto_revert`
- `cluster_mgmt_interface`
- `ha_pairs`
- `item`
- `total_port_count`
- `ha_pairs_count`
- `dns_server_list`
- `dns_servers`
- `dns_domain_name`
- `ntp_servers`
- `time_zone`
- `fcp_port_list`
- `autosupport_vars`
- `legacy_license_keys`
- `lookup`

## Configuration To Expect

Expect ONTAP SVM, network, protocol, volume, LIF, LUN, NVMe, export policy, and final service configuration depending on the role.

## Operator Runbook

1. Confirm the inventory group targeted by the parent playbook has the expected devices.
2. Confirm the tenant or infrastructure vars contain the VLAN IDs, CIDRs, credentials, and policy names for the environment.
3. Run syntax-check on the parent playbook.
4. Run check mode before live changes.
5. Review device or controller diffs and only then run without `-C`.

## Product References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
- [NetApp ONTAP Automation](https://docs.netapp.com/us-en/ontap-automation/)
- [NetApp ONTAP Ansible Collection](https://docs.ansible.com/projects/ansible/latest/collections/netapp/ontap/index.html)
