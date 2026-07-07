# Architecture Overview Diagram

[Documentation index](README.md) | [Architecture](architecture.md) | [Variables](variables.md) | [Playbooks](playbooks.md) | [Tenants](tenants/README.md)

This page gives a Technical Marketing style overview of the components managed by this Ansible framework. Because this is the public FlexPod-IMM-Rancher repository, device names, tenant names, VLAN IDs, and IP networks in this page are anonymized examples. Private deployment documentation can keep the full site-specific values.

## Current Public View

| Area | Public documentation view |
| --- | --- |
| Multi-tenancy mode | Secure multi-tenancy with one logical VRF boundary per tenant |
| Tenant examples | Public docs show neutral sample tenants while private deployment docs keep the real tenant catalog |
| Core Ethernet fabric | Redundant Cisco Nexus pair with vPC, peer-link, VLAN trunks, SVIs, and HSRP |
| Storage system | One NetApp C-Series storage system represented as two connected ONTAP controllers |
| Compute automation | Cisco Intersight API creates UCS pools, policies, templates, and server profiles |
| Enabled shared protocols | NFS and iSCSI are the primary public examples; FC, NVMe/TCP, and FC-NVMe are role-supported patterns |

## Physical Component View

```mermaid
flowchart TB
  operator["Ansible control host<br/>inventory, vars, playbooks"]
  intersight["Cisco Intersight API<br/>UCS pools, policies, templates, profiles"]

  subgraph ethernet["Cisco Nexus Ethernet fabric"]
    nxa["Nexus A<br/>SVI/HSRP peer"]
    nxb["Nexus B<br/>SVI/HSRP peer"]
    nxa <-->|"vPC peer-link"| nxb
  end

  upstream["External or routed network<br/>uplink handoff"]
  firewall["Firewall / edge handoff<br/>transfer and access VLAN trunks"]
  fi["Cisco UCS Fabric Interconnect pair<br/>FI-A and FI-B"]
  ucs["UCS servers<br/>server profiles from templates"]
  subgraph storage["NetApp C-Series storage system"]
    storagea["ONTAP controller A<br/>tenant SVMs and data services"]
    storageb["ONTAP controller B<br/>partner controller and data services"]
    storagea <-->|"HA / cluster interconnect<br/>single storage system"| storageb
  end
  objectstore["Optional StorageGRID<br/>client/grid VLANs"]
  hypervisor["Optional virtualization hosts<br/>workload and storage uplinks"]
  k8s["RKE2 / Kubernetes<br/>NetApp Trident backend"]

  operator -->|"network_cli roles"| ethernet
  operator -->|"local ONTAP roles"| storage
  operator -->|"REST API roles"| intersight
  intersight --> fi
  fi -->|"server profile attachment"| ucs
  ethernet -->|"FI trunks: tenant VLAN sets"| fi
  ethernet -->|"storage trunks: storage VLAN sets"| storage
  ethernet -->|"north-south handoff"| upstream
  ethernet -->|"edge transfer/access VLANs"| firewall
  ethernet -->|"optional object-storage VLANs"| objectstore
  ethernet -->|"optional hypervisor VLANs"| hypervisor
  ucs -->|"iSCSI boot LUNs<br/>via tenant iSCSI A/B VLANs"| storage
  ucs -->|"OS/RKE2 workloads"| k8s
  k8s -->|"CSI persistent volumes"| storage
```

## Logical Tenant Isolation View

```mermaid
flowchart LR
  shared["Shared defaults<br/>group_vars/all.yml<br/>group_vars/tenant_defaults.yml"]
  tenantvars["Tenant vars<br/>tenants/&lt;tenant&gt;/vars.yml"]
  playbook["TENANT.yml<br/>-e tenant=&lt;name&gt;"]

  subgraph vrf["Per-tenant network boundary"]
    tenantvrf["Tenant VRF<br/>tenant name or vrf_name override"]
    mgmt["Management VLAN<br/>tenant management CIDR"]
    access["Access VLAN<br/>workload access CIDR"]
    nfs["NFS VLAN<br/>storage CIDR"]
    iscsi["iSCSI A/B VLANs<br/>boot or block storage CIDRs"]
    svi["Nexus SVIs + HSRP<br/>tenant routing boundary"]
  end

  subgraph storageTenant["Tenant storage boundary"]
    svm["ONTAP SVM<br/>tenant SVM name"]
    lifs["Data and management LIFs<br/>NFS, iSCSI, optional FC/NVMe"]
    bootluns["Boot LUNs<br/>mapped to host initiators"]
    vols["Volumes, LUNs, igroups<br/>tenant-local names"]
  end

  subgraph compute["Tenant compute boundary"]
    org["Intersight organization<br/>tenant-scoped when SMT is enabled"]
    pools["UUID, MAC, WWPN, IQN, IP pools<br/>tenant allocation block"]
    policies["LAN/SAN/boot/vMedia/BIOS policies"]
    bootpolicy["iSCSI boot policy<br/>primary and secondary targets"]
    profiles["Server profile template<br/>server profiles"]
  end

  shared --> tenantvars --> playbook
  playbook --> tenantvrf
  tenantvrf --> mgmt
  tenantvrf --> access
  tenantvrf --> nfs
  tenantvrf --> iscsi
  mgmt --> svi
  access --> svi
  nfs --> svi
  iscsi --> svi
  playbook --> svm --> lifs --> vols
  lifs --> bootluns
  playbook --> org --> pools --> policies --> bootpolicy --> profiles
  profiles -->|"boot from ONTAP LUNs"| bootluns
  profiles -->|"host consumes storage networks"| lifs
```

## Playbook And Role Flow

```mermaid
flowchart TB
  infra["INFRA.yml<br/>shared FlexPod base"]
  tenant["TENANT.yml<br/>one tenant at a time"]
  rke["RKE2.yml<br/>platform configuration"]

  infra --> infnexus["INFRA/nexus_*<br/>features, VLANs, vPC, edge, object storage, hypervisor uplinks"]
  infra --> infontap["INFRA/ontap_*<br/>network, SVM, volumes, LIFs"]
  infra --> infucs["INFRA/ucs_create_pools<br/>shared Intersight pools"]

  tenant --> tnexus["TENANT/nexus_*<br/>tenant VLANs, VRF, SVIs, trunks"]
  tenant --> tontap["TENANT/ontap_*<br/>tenant SVM, LIFs, volumes, LUNs, NVMe"]
  tenant --> tucs["TENANT/ucs_*<br/>tenant pools, policies, templates, profiles"]
  tenant --> os["TENANT/os_install_suse<br/>OS installation workflow"]
  tenant --> trident["TENANT/trident_install<br/>Kubernetes storage backend"]

  rke --> pre["rancher/pre_rke_install"]
  rke --> server["rancher/rke2_server"]
  rke --> agent["rancher/rke2_agent"]
```

## Network Connections Managed By The Framework

| Connection | Public label | Purpose |
| --- | --- | --- |
| External network | Nexus peer uplink port-channel | Data center, campus, or firewall handoff |
| Cisco UCS Fabric Interconnect A | Nexus vPC member port-channel | Carries management, access, and storage VLANs to UCS fabric A, including iSCSI boot networks |
| Cisco UCS Fabric Interconnect B | Nexus vPC member port-channel | Carries management, access, and storage VLANs to UCS fabric B, including iSCSI boot networks |
| NetApp storage controller A | Nexus storage port-channel pair | Carries tenant storage VLANs and storage LIF traffic |
| NetApp storage controller B | Nexus storage port-channel pair | Carries tenant storage VLANs and storage LIF traffic |
| Firewall or routed edge | Tenant access and transfer VLAN trunks | Provides north-south routing or security policy outside the tenant VRF |
| Optional StorageGRID | StorageGRID client and grid VLAN trunks | Adds object-storage connectivity when the role set is used |
| Optional virtualization hosts | Hypervisor uplinks | Carries workload and storage networks to non-UCS hosts when configured |

## Storage And SAN Objects

The physical view treats both ONTAP controllers as connected controllers in the same NetApp storage system. Public docs do not expose site-specific controller hostnames, management IPs, or aggregate names.

| Object | Public label | Configuration to expect |
| --- | --- | --- |
| ONTAP controller A | Storage controller A | Node management, data aggregates, broadcast domains, VLAN ports, LIFs |
| ONTAP controller B | Storage controller B | Partner node management, data aggregates, broadcast domains, VLAN ports, LIFs |
| Tenant SVM | tenant##_svm | Root volume, management LIF, data LIFs, protocol services, export or block access |
| iSCSI boot LUNs | Tenant boot volume and host LUN mappings | UCS server profiles boot from ONTAP LUNs through tenant iSCSI A/B target LIFs |
| SAN fabric A | SAN-A | VSAN, device aliases, zones, and zoneset for fabric A |
| SAN fabric B | SAN-B | VSAN, device aliases, zones, and zoneset for fabric B |

## Public Tenant Examples

The table below is illustrative. Real tenant names, VLAN IDs, CIDRs, and SVM names are intentionally kept out of the public documentation.

| Tenant | Type | VRF | Example VLANs | Example CIDRs | Storage | Profiles |
| --- | --- | --- | --- | --- | --- | --- |
| tenant01 | physical | tenant01 | mgmt 301<br>access 302<br>NFS 303<br>iSCSI A/B 304/305 | mgmt 192.0.2.0/24<br>access 198.51.100.0/24<br>NFS 203.0.113.0/24 | tenant01_svm<br>NFS plus iSCSI boot LUNs | 3 |
| tenant02 | virtual | tenant02 | access 312<br>NFS 313 | access 198.51.100.0/24<br>NFS 203.0.113.0/24 | tenant02_svm<br>NFS | 3 |
| tenant-hub | carrier / registry | shared or upstream VRF | registry publishes vNN access/NFS VLANs | documentation networks only | shared SVM or delegated tenant SVMs | deployment-specific |

## Virtual Tenant Registry Example

Carrier or hub tenants can publish `vNN_*` registry entries for virtual tenants. The public view shows the pattern without exposing the internal registry names.

| Registry owner | Virtual tenant | Access network | NFS network |
| --- | --- | --- | --- |
| tenant-hub | v10 tenant01 | access VLAN 302 / 198.51.100.0/24 | NFS VLAN 303 / 203.0.113.0/24 |
| tenant-hub | v11 tenant02 | access VLAN 312 / 198.51.100.0/24 | NFS VLAN 313 / 203.0.113.0/24 |
| tenant-hub | v12 tenant03 | access VLAN 322 / 198.51.100.0/24 | NFS VLAN 323 / 203.0.113.0/24 |

## Managed Role Inventory

| Playbook | Roles called |
| --- | --- |
| `INFRA.yml` | INFRA/env_vars<br>INFRA/nexus_config<br>INFRA/nexus_config_sg<br>INFRA/nexus_config_ip<br>INFRA/nexus_config_proxmox<br>INFRA/env_vars<br>INFRA/ontap_network<br>INFRA/ontap_svm<br>INFRA/ontap_volumes<br>INFRA/ontap_lifs<br>INFRA/env_vars<br>INFRA/ucs_create_pools<br>INFRA/env_vars<br>INFRA/nexus_config_asa |
| `TENANT.yml` | TENANT/env_vars<br>TENANT/nexus_config<br>TENANT/nexus_config_ip<br>TENANT/nexus_config_sg<br>TENANT/nexus_config_asa<br>TENANT/env_vars<br>TENANT/ontap_network<br>TENANT/ontap_svm<br>TENANT/ontap_volumes<br>TENANT/ontap_lifs<br>TENANT/ontap_luns<br>TENANT/ontap_nvme<br>TENANT/env_vars<br>TENANT/ucs_create_pools<br>TENANT/ucs_create_server_policies<br>TENANT/ucs_create_sp_template<br>TENANT/env_vars<br>TENANT/ucs_create_server<br>TENANT/env_vars<br>TENANT/os_install_suse<br>rancher/env_vars<br>rancher/pre_rke_install<br>rancher/env_vars<br>rancher/rke2_server<br>rancher/rke2_agent<br>TENANT/env_vars<br>TENANT/trident_install |
| `RKE2.yml` | rancher/env_vars<br>rancher/pre_rke_install<br>rancher/env_vars<br>rancher/rke2_server<br>rancher/rke2_agent |

## How To Explain This To An Audience

The easiest story is to present the framework in three layers:

1. The FlexPod base layer provides redundant Nexus switching, ONTAP storage, and Intersight-controlled UCS compute.
2. The tenant layer adds one isolated VRF, a small set of tenant VLANs and CIDRs, a tenant SVM, tenant iSCSI boot LUNs, and tenant-scoped Intersight objects.
3. UCS server profiles boot from ONTAP-backed iSCSI LUNs through the tenant iSCSI A/B networks.
4. The platform layer consumes that tenant boundary for RKE2, Harvester, Trident, or other workloads.

That framing makes the separation model visible: shared hardware and shared automation patterns below, tenant-local network, boot-storage, data-storage, and compute identities above.

## Related Design References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
