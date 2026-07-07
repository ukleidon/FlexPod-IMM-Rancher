# Architecture Overview Diagram

[Documentation index](README.md) | [Architecture](architecture.md) | [Variables](variables.md) | [Playbooks](playbooks.md) | [Tenants](tenants/README.md)

This page gives a Technical Marketing style overview of the components managed by this Ansible framework. It is generated from the current repository variables and playbooks, so it is intended to explain what the automation is prepared to configure rather than to replace a cabling workbook or a low-level device configuration.

## Current Managed Estate

| Area | Current framework view |
| --- | --- |
| Multi-tenancy mode | `SMT: true` with default fallback VRF `admin` |
| Tenant directories | 37 total: 6 physical, 31 virtual |
| Virtual tenant registry entries | 50 entries across tenant vars with `v##_name` definitions |
| Core Ethernet fabric | Nexus pair `nx1` and `nx2`, vPC domain `101` |
| Storage system | One NetApp C250 storage system represented by C250-01 and C250-02 controller inventory entries |
| Compute automation | Cisco Intersight API creates UCS pools, policies, templates, and server profiles |
| Enabled shared protocols | iSCSI `true`, NFS `true`, FC `false`, NVMe/TCP `false`, FC-NVMe `false` |

## Physical Component View

```mermaid
flowchart TB
  operator["Ansible control host<br/>inventory, vars, playbooks"]
  intersight["Cisco Intersight API<br/>UCS pools, policies, templates, profiles"]

  subgraph ethernet["Cisco Nexus Ethernet fabric"]
    nx1["nx1<br/>Nexus A<br/>SVI base IP .2"]
    nx2["nx2<br/>Nexus B<br/>SVI base IP .3"]
    nx1 <-->|"vPC peer-link<br/>port-channel53"| nx2
  end

  upstream["External/uplink network<br/>port-channel52"]
  asa["ASA / firewall handoff<br/>transfer VLAN 3299<br/>tenant access trunk"]
  fi["Cisco UCS Fabric Interconnects<br/>FI-A port-channel49<br/>FI-B port-channel50"]
  ucs["UCS servers<br/>server profiles from templates"]
  subgraph c250["NetApp C250 storage system"]
    ontap1["ONTAP controller C250-01<br/>tenant SVMs and data services"]
    ontap2["ONTAP controller C250-02<br/>partner controller and data services"]
    ontap1 <-->|"HA / cluster interconnect<br/>single C250 storage system"| ontap2
  end
  sg["StorageGRID nodes<br/>client/grid VLANs"]
  proxmox["Proxmox uplinks"]
  k8s["RKE2 / Kubernetes<br/>NetApp Trident backend"]

  operator -->|"network_cli roles"| ethernet
  operator -->|"local ONTAP roles"| ontap1
  operator -->|"local ONTAP roles"| ontap2
  operator -->|"REST API roles"| intersight
  intersight --> fi
  fi -->|"server profile attachment"| ucs
  ethernet -->|"FI trunks: all tenant VLANs"| fi
  ethernet -->|"storage trunks: storage VLANs"| ontap1
  ethernet -->|"storage trunks: storage VLANs"| ontap2
  ethernet -->|"management/access handoff"| upstream
  ethernet -->|"ASA transfer/access VLANs"| asa
  ethernet -->|"StorageGRID VLANs"| sg
  ethernet -->|"Proxmox VLANs"| proxmox
  k8s -->|"CSI persistent volumes"| ontap1
  ucs -->|"OS/RKE2 workloads"| k8s
```

## Logical Tenant Isolation View

```mermaid
flowchart LR
  shared["Shared defaults<br/>group_vars/all.yml<br/>group_vars/tenant_defaults.yml"]
  tenantvars["Tenant vars<br/>tenants/&lt;tenant&gt;/vars.yml"]
  playbook["TENANT.yml<br/>-e tenant=&lt;name&gt;"]

  subgraph vrf["Per-tenant network boundary"]
    tenantvrf["VRF<br/>tenant name or vrf_name override"]
    mgmt["Management VLAN<br/>t_ib_vlan_id / CIDR"]
    access["Access VLAN<br/>t_access_vlan_id / CIDR"]
    nfs["NFS VLAN<br/>t_nfs_vlan_id / CIDR"]
    iscsi["iSCSI A/B VLANs<br/>t_iscsiA/B_vlan_id / CIDR"]
    svi["Nexus SVIs + HSRP<br/>t_svi_list"]
  end

  subgraph storage["Tenant storage boundary"]
    svm["ONTAP SVM<br/>svm_specs.svm_name"]
    lifs["Data and management LIFs<br/>NFS, iSCSI, optional FC/NVMe"]
    vols["Volumes, LUNs, igroups<br/>tenant-local names"]
  end

  subgraph compute["Tenant compute boundary"]
    org["Intersight organization<br/>tenant_name when SMT is true"]
    pools["UUID, MAC, WWPN, IQN, IP pools<br/>tid-based allocation"]
    policies["LAN/SAN/boot/vMedia/BIOS policies"]
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
  playbook --> org --> pools --> policies --> profiles
  profiles -->|"host consumes storage networks"| lifs
```

## Playbook And Role Flow

```mermaid
flowchart TB
  infra["INFRA.yml<br/>shared FlexPod base"]
  tenant["TENANT.yml<br/>one tenant at a time"]
  rke["RKE2.yml<br/>platform configuration"]

  infra --> infnexus["INFRA/nexus_*<br/>features, VLANs, vPC, ASA, SG, Proxmox"]
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

| Connection | Port-channel | nx1 interfaces | nx2 interfaces | Purpose |
| --- | --- | --- | --- | --- |
| uplink | port-channel52: Fake-Uplink | Ethernet1/52 (Fake-Uplink) | Ethernet1/52 (Fake-Uplink) | External/uplink handoff |
| peerlink | port-channel53: vPC Peer Link | Ethernet1/53 (KL-IDTA-nx2:Eth1/53), Ethernet1/54 (KL-IDTA-nx2:Eth1/54) | Ethernet1/53 (KL-IDTA-nx1:Eth1/53), Ethernet1/54 (KL-IDTA-nx1:Eth1/54) | Nexus vPC peer-link |
| FI A | port-channel49: Uplink-FI-A | Ethernet1/49 (KL-IDTA-FI-A:Eth1/53) | Ethernet1/49 (KL-IDTA-FI-A:Eth1/54) | UCS Fabric Interconnect A |
| FI B | port-channel50: Uplink-FI-B | Ethernet1/50 (KL-IDTA-FI-B:Eth1/53) | Ethernet1/50 (KL-IDTA-FI-B:Eth1/54) | UCS Fabric Interconnect B |
| Storage A | port-channel25: C250-02n1-a0a | Ethernet1/25 (C250-02n1:e2a), Ethernet1/26 (C250-02n1:e2b) | Ethernet1/25 (C250-02n1:e2c), Ethernet1/26 (C250-02n1:e2d) | ONTAP storage node path |
| Storage B | port-channel27: C250-02n2-a0a | Ethernet1/27 (C250-02n2:e2a), Ethernet1/28 (C250-02n2:e2b) | Ethernet1/27 (C250-02n2:e2c), Ethernet1/28 (C250-02n2:e2d) | ONTAP storage node path |
| Storage C | port-channel29: C250-01n1-a0a | Ethernet1/29 (C250-01n1:e2a), Ethernet1/30 (C250-01n1:e2b) | Ethernet1/29 (C250-01n1:e2c), Ethernet1/30 (C250-01n1:e2d) | ONTAP storage node path |
| Storage D | port-channel31: C250-01n2-a0a | Ethernet1/31 (C250-01n2:e2a), Ethernet1/32 (C250-01n2:e2b) | Ethernet1/31 (C250-01n2:e2c), Ethernet1/32 (C250-01n2:e2d) | ONTAP storage node path |
| ASA/firewall | - | Ethernet1/17 (T-Admin-ASA-Eth1/6), Ethernet1/18 (T-Tenant-ASA-Eth1/7) | Ethernet1/17 (T-Admin-ASA-Eth1/6), Ethernet1/18 (T-Tenant-ASA-Eth1/7) | Transfer/access trunk handoff |
| StorageGRID 01 | - | Ethernet1/35 (sg5712-01-eth1) | Ethernet1/35 (sg5712-01-eth3) | StorageGRID data path |
| StorageGRID 02 | - | Ethernet1/36 (sg5712-02-eth1) | Ethernet1/36 (sg5712-02-eth3) | StorageGRID data path |
| StorageGRID 03 | - | Ethernet1/37 (sg5712-03-eth1) | Ethernet1/37 (sg5712-03-eth3) | StorageGRID data path |
| Proxmox 01 | - | Ethernet1/47 (Uplink Proxmox) | Ethernet1/47 (Uplink Proxmox) | Proxmox uplink |
| Proxmox 02 | - | Ethernet1/48 (Uplink Proxmox) | Ethernet1/48 (Uplink Proxmox) | Proxmox uplink |

## ONTAP Controller And SAN Objects

The physical view treats C250-01 and C250-02 as connected controllers in the same NetApp C250 storage system. The table below keeps the inventory entries visible because the playbooks target them through `host_vars/c250-*.yml`.

| Storage inventory entry | Node details from vars | Infrastructure SVM | Protocols and aggregates |
| --- | --- | --- | --- |
| C250-01 | c250-01n1 (172.16.4.21), c250-01n2 (172.16.4.23) | Infra-SVM | nfs, iscsi; aggregates: c250_01n1_aggr1, c250_01n2_aggr1 |
| C250-02 | c250-02n1 (172.16.4.26), c250-02n2 (172.16.4.28) | - | -; aggregates: c250_02n1_aggr1, c250_02n2_aggr1 |

| SAN device | VSAN name | VSAN ID | Zoning / port-channel intent |
| --- | --- | --- | --- |
| mdsA | FlexPod-Fabric-A | 101 | zoneset FlexPod-Fabric-A; port-channel 15 |
| mdsB | FlexPod-Fabric-B | 102 | zoneset FlexPod-Fabric-B; port-channel 15 |
| n9kSSA | FlexPod-Fabric-A | 101 | zoneset FlexPod-Fabric-A; port-channel 1103 |
| n9kSSB | FlexPod-Fabric-B | 102 | zoneset FlexPod-Fabric-B; port-channel 1103 |

## Tenant Catalog

Each row below comes from `tenants/<tenant>/vars.yml`. For secure multi-tenancy, the VRF normally follows the tenant name; a tenant can override that with `vrf_name` when it intentionally uses a shared or upstream VRF.

| Directory | Tenant / type | VRF | VLANs | CIDRs | ONTAP SVM | UCS profiles |
| --- | --- | --- | --- | --- | --- | --- |
| ahorn | ahorn<br>virtual, tid 32 | ahorn | mgmt 445<br>access 445<br>NFS 446<br>iSCSI A/B 446/446 | mgmt 172.16.175.0/24<br>access 172.16.175.0/24<br>NFS 172.16.176.0<br>iSCSI A/B 172.16.176.0/24 / 172.16.176.0/24 | ahorn_svm<br>nfs<br>client 172.16.176.0/24 | 3 |
| belchen | belchen<br>physical, tid 03 | belchen | mgmt 212<br>access 211<br>NFS 210<br>iSCSI A/B 208/209 | mgmt 172.17.12.0/24<br>access 172.17.11.0/24<br>NFS 172.17.10.0<br>iSCSI A/B 172.17.8.0/24 / 172.17.9.0/24 | belchen_svm<br>nfs, iscsi<br>client 172.17.10.0/24 | 3 |
| birke | birke<br>virtual, tid 27 | birke | mgmt 420<br>access 420<br>NFS 421<br>iSCSI A/B 421/421 | mgmt 172.16.150.0/24<br>access 172.16.150.0/24<br>NFS 172.16.151.0<br>iSCSI A/B 172.16.151.0/24 / 172.16.151.0/24 | birke_svm<br>nfs<br>client 172.16.151.0/24 | 3 |
| dataspace | DataSpace<br>physical, tid 01 | admin | mgmt 101<br>access 102<br>NFS 103<br>iSCSI A/B 104/105<br>NVMe A/B 198/199 | mgmt 172.16.4.0/22<br>access 172.16.8.0/23<br>NFS 172.16.10.0<br>iSCSI A/B 172.16.11.0/24 / 172.16.12.0/24 | Infra-SVM<br>nfs, iscsi<br>client 172.16.10.0/24 | 0 |
| douglasie | douglasie<br>virtual, tid 11 | douglasie | mgmt 305<br>access 305<br>NFS 306<br>iSCSI A/B 306/306 | mgmt 172.16.35.0/24<br>access 172.16.35.0/24<br>NFS 172.16.36.0<br>iSCSI A/B 172.16.36.0/24 / 172.16.36.0/24 | douglasie_svm<br>nfs<br>client 172.16.36.0/24 | 3 |
| eberesche | eberesche<br>virtual, tid 12 | eberesche | mgmt 310<br>access 310<br>NFS 311<br>iSCSI A/B 311/311 | mgmt 172.16.40.0/24<br>access 172.16.40.0/24<br>NFS 172.16.41.0<br>iSCSI A/B 172.16.41.0/24 / 172.16.41.0/24 | eberesche_svm<br>nfs<br>client 172.16.41.0/24 | 3 |
| edelkastanie | edelkastanie<br>virtual, tid 20 | edelkastanie | mgmt 350<br>access 350<br>NFS 351<br>iSCSI A/B 351/351 | mgmt 172.16.80.0/24<br>access 172.16.80.0/24<br>NFS 172.16.81.0<br>iSCSI A/B 172.16.81.0/24 / 172.16.81.0/24 | edelkastanie_svm<br>nfs<br>client 172.16.81.0/24 | 3 |
| edeltanne | edeltanne<br>virtual, tid 21 | edeltanne | mgmt 390<br>access 390<br>NFS 391<br>iSCSI A/B 391/391 | mgmt 172.16.120.0/24<br>access 172.16.120.0/24<br>NFS 172.16.121.0<br>iSCSI A/B 172.16.121.0/24 / 172.16.121.0/24 | edeltanne_svm<br>nfs<br>client 172.16.121.0/24 | 3 |
| eibe | eibe<br>virtual, tid 18 | eibe | mgmt 335<br>access 335<br>NFS 336<br>iSCSI A/B 336/336 | mgmt 172.16.65.0/24<br>access 172.16.65.0/24<br>NFS 172.16.66.0<br>iSCSI A/B 172.16.66.0/24 / 172.16.66.0/24 | eibe_svm<br>nfs<br>client 172.16.66.0/24 | 3 |
| elsbeere | elsbeere<br>virtual, tid 14 | elsbeere | mgmt 320<br>access 320<br>NFS 321<br>iSCSI A/B 321/321 | mgmt 172.16.50.0/24<br>access 172.16.50.0/24<br>NFS 172.16.51.0<br>iSCSI A/B 172.16.51.0/24 / 172.16.51.0/24 | elsbeere_svm<br>nfs<br>client 172.16.51.0/24 | 3 |
| feldahorn | feldahorn<br>virtual, tid 20 | feldahorn | mgmt 380<br>access 380<br>NFS 381<br>iSCSI A/B 381/381 | mgmt 172.16.110.0/24<br>access 172.16.110.0/24<br>NFS 172.16.111.0<br>iSCSI A/B 172.16.111.0/24 / 172.16.111.0/24 | feldahorn_svm<br>nfs<br>client 172.16.111.0/24 | 3 |
| fichte | fichte<br>virtual, tid 23 | fichte | mgmt 400<br>access 400<br>NFS 401<br>iSCSI A/B 401/401 | mgmt 172.16.130.0/24<br>access 172.16.130.0/24<br>NFS 172.16.131.0<br>iSCSI A/B 172.16.131.0/24 / 172.16.131.0/24 | fichte_svm<br>nfs<br>client 172.16.131.0/24 | 3 |
| gpusystem | gpu<br>physical, tid 02 | gpu | mgmt 200<br>access 204<br>NFS 203<br>iSCSI A/B 201/202<br>NVMe A/B 205/206 | mgmt 172.17.0.0/24<br>access 172.17.4.0/24<br>NFS 172.17.3.0<br>iSCSI A/B 172.17.1.0/24 / 172.17.2.0/24 | gpu_svm<br>nfs, iscsi<br>client 172.17.3.0/24 | 0 |
| hainbuche | hainbuche<br>virtual, tid 16 | hainbuche | mgmt 330<br>access 330<br>NFS 331<br>iSCSI A/B 331/331 | mgmt 172.16.60.0/24<br>access 172.16.60.0/24<br>NFS 172.16.61.0<br>iSCSI A/B 172.16.61.0/24 / 172.16.61.0/24 | hainbuche_svm<br>nfs<br>client 172.16.61.0/24 | 3 |
| harvester | DataSpace<br>physical, tid 01 | DataSpace | mgmt 101<br>access 102<br>NFS 103<br>iSCSI A/B 104/105<br>NVMe A/B 198/199 | mgmt 172.16.4.0/22<br>access 172.16.8.0/23<br>NFS 172.16.10.0<br>iSCSI A/B 172.16.11.0/24 / 172.16.12.0/24 | Infra-SVM<br>nfs, iscsi<br>client 172.16.10.0/24 | 0 |
| haselnuss | haselnuss<br>virtual, tid 24 | haselnuss | mgmt 405<br>access 405<br>NFS 406<br>iSCSI A/B 406/406 | mgmt 172.16.135.0/24<br>access 172.16.135.0/24<br>NFS 172.16.136.0<br>iSCSI A/B 172.16.136.0/24 / 172.16.136.0/24 | haselnuss_svm<br>nfs<br>client 172.16.136.0/24 | 3 |
| kastanie | kastanie<br>virtual, tid 33 | kastanie | mgmt 450<br>access 450<br>NFS 451<br>iSCSI A/B 451/451 | mgmt 172.16.180.0/24<br>access 172.16.180.0/24<br>NFS 172.16.181.0<br>iSCSI A/B 172.16.181.0/24 / 172.16.181.0/24 | kastanie_svm<br>nfs<br>client 172.16.181.0/24 | 3 |
| laerche | laerche<br>virtual, tid 30 | laerche | mgmt 435<br>access 435<br>NFS 436<br>iSCSI A/B 436/436 | mgmt 172.16.165.0/24<br>access 172.16.165.0/24<br>NFS 172.16.166.0<br>iSCSI A/B 172.16.166.0/24 / 172.16.166.0/24 | laerche_svm<br>nfs<br>client 172.16.166.0/24 | 3 |
| robinie | robinie<br>virtual, tid 10 | robinie | mgmt 300<br>access 300<br>NFS 301<br>iSCSI A/B 301/301 | mgmt 172.16.30.0/24<br>access 172.16.30.0/24<br>NFS 172.16.31.0<br>iSCSI A/B 172.16.31.0/24 / 172.16.31.0/24 | robinie_svm<br>nfs<br>client 172.16.31.0/24 | 3 |
| rosskastanie | rosskastanie<br>virtual, tid 21 | rosskastanie | mgmt 355<br>access 355<br>NFS 356<br>iSCSI A/B 356/356 | mgmt 172.16.85.0/24<br>access 172.16.85.0/24<br>NFS 172.16.86.0<br>iSCSI A/B 172.16.86.0/24 / 172.16.86.0/24 | rosskastanie_svm<br>nfs<br>client 172.16.86.0/24 | 3 |
| rotbuche | rotbuche<br>virtual, tid 23 | rotbuche | mgmt 365<br>access 365<br>NFS 366<br>iSCSI A/B 366/366 | mgmt 172.16.95.0/24<br>access 172.16.95.0/24<br>NFS 172.16.96.0<br>iSCSI A/B 172.16.96.0/24 / 172.16.96.0/24 | rotbuche_svm<br>nfs<br>client 172.16.96.0/24 | 3 |
| schwarzdorn | schwarzdorn<br>virtual, tid 31 | schwarzdorn | mgmt 440<br>access 440<br>NFS 441<br>iSCSI A/B 441/441 | mgmt 172.16.170.0/24<br>access 172.16.170.0/24<br>NFS 172.16.171.0<br>iSCSI A/B 172.16.171.0/24 / 172.16.171.0/24 | schwarzdorn_svm<br>nfs<br>client 172.16.171.0/24 | 3 |
| schwarzerle | schwarzerle<br>virtual, tid 20 | schwarzerle | mgmt 385<br>access 385<br>NFS 386<br>iSCSI A/B 386/386 | mgmt 172.16.115.0/24<br>access 172.16.115.0/24<br>NFS 172.16.116.0<br>iSCSI A/B 172.16.116.0/24 / 172.16.116.0/24 | schwarzerle_svm<br>nfs<br>client 172.16.116.0/24 | 3 |
| seebuck | seebuck<br>physical, tid 04 | seebuck | mgmt 216<br>access 220<br>NFS 217<br>iSCSI A/B 215/218 | mgmt 172.17.16.0/24<br>access 172.17.20.0/24<br>NFS 172.17.17.0<br>iSCSI A/B 172.16.23.0/24 / 172.17.18.0/24 | seebuck_svm<br>nfs, iscsi<br>client 172.17.17.0/24 | 3 |
| silberweide | silberweide<br>virtual, tid 22 | silberweide | mgmt 395<br>access 395<br>NFS 396<br>iSCSI A/B 396/396 | mgmt 172.16.125.0/24<br>access 172.16.125.0/24<br>NFS 172.16.126.0<br>iSCSI A/B 172.16.126.0/24 / 172.16.126.0/24 | silberweide_svm<br>nfs<br>client 172.16.126.0/24 | 3 |
| sommerlinde | sommerlinde<br>virtual, tid 24 | sommerlinde | mgmt 370<br>access 370<br>NFS 371<br>iSCSI A/B 371/371 | mgmt 172.16.100.0/24<br>access 172.16.100.0/24<br>NFS 172.16.101.0<br>iSCSI A/B 172.16.101.0/24 / 172.16.101.0/24 | sommerlinde_svm<br>nfs<br>client 172.16.101.0/24 | 3 |
| speierling | speierling<br>virtual, tid 15 | speierling | mgmt 325<br>access 325<br>NFS 326<br>iSCSI A/B 326/326 | mgmt 172.16.55.0/24<br>access 172.16.55.0/24<br>NFS 172.16.56.0<br>iSCSI A/B 172.16.56.0/24 / 172.16.56.0/24 | speierling_svm<br>nfs<br>client 172.16.56.0/24 | 3 |
| stechpalme | stechpalme<br>virtual, tid 25 | stechpalme | mgmt 410<br>access 410<br>NFS 411<br>iSCSI A/B 411/411 | mgmt 172.16.140.0/24<br>access 172.16.140.0/24<br>NFS 172.16.141.0<br>iSCSI A/B 172.16.141.0/24 / 172.16.141.0/24 | stechpalme_svm<br>nfs<br>client 172.16.141.0/24 | 3 |
| stieleiche | stieleiche<br>virtual, tid 28 | stieleiche | mgmt 425<br>access 425<br>NFS 426<br>iSCSI A/B 426/426 | mgmt 172.16.155.0/24<br>access 172.16.155.0/24<br>NFS 172.16.156.0<br>iSCSI A/B 172.16.156.0/24 / 172.16.156.0/24 | stieleiche_svm<br>nfs<br>client 172.16.156.0/24 | 3 |
| test01 | test01<br>physical, tid 03 | test01 | mgmt 300<br>access 3304<br>NFS 3303<br>iSCSI A/B 301/302<br>NVMe A/B 305/306 | mgmt 172.18.0.0/24<br>access 172.18.4.0/24<br>NFS 172.18.3.0<br>iSCSI A/B 172.18.1.0/24 / 172.18.2.0/24 | test01_svm<br>nfs, iscsi<br>client 172.18.3.0/24 | 3 |
| vogelkirsche | vogelkirsche<br>virtual, tid 25 | vogelkirsche | mgmt 375<br>access 375<br>NFS 376<br>iSCSI A/B 376/376 | mgmt 172.16.105.0/24<br>access 172.16.105.0/24<br>NFS 172.16.106.0<br>iSCSI A/B 172.16.106.0/24 / 172.16.106.0/24 | vogelkirsche_svm<br>nfs<br>client 172.16.106.0/24 | 3 |
| wacholder | wacholder<br>virtual, tid 22 | wacholder | mgmt 360<br>access 360<br>NFS 361<br>iSCSI A/B 361/361 | mgmt 172.16.90.0/24<br>access 172.16.90.0/24<br>NFS 172.16.91.0<br>iSCSI A/B 172.16.91.0/24 / 172.16.91.0/24 | wacholder_svm<br>nfs<br>client 172.16.91.0/24 | 3 |
| waldkiefer | waldkiefer<br>virtual, tid 19 | waldkiefer | mgmt 345<br>access 345<br>NFS 346<br>iSCSI A/B 346/346 | mgmt 172.16.75.0/24<br>access 172.16.75.0/24<br>NFS 172.16.76.0<br>iSCSI A/B 172.16.76.0/24 / 172.16.76.0/24 | waldkiefer_svm<br>nfs<br>client 172.16.76.0/24 | 3 |
| walnuss | walnuss<br>virtual, tid 13 | walnuss | mgmt 315<br>access 315<br>NFS 316<br>iSCSI A/B 316/316 | mgmt 172.16.45.0/24<br>access 172.16.45.0/24<br>NFS 172.16.46.0<br>iSCSI A/B 172.16.46.0/24 / 172.16.46.0/24 | walnuss_svm<br>nfs<br>client 172.16.46.0/24 | 3 |
| weissdorn | weissdorn<br>virtual, tid 26 | weissdorn | mgmt 415<br>access 415<br>NFS 416<br>iSCSI A/B 416/416 | mgmt 172.16.145.0/24<br>access 172.16.145.0/24<br>NFS 172.16.146.0<br>iSCSI A/B 172.16.146.0/24 / 172.16.146.0/24 | weissdorn_svm<br>nfs<br>client 172.16.146.0/24 | 3 |
| winterlinde | winterlinde<br>virtual, tid 17 | winterlinde | mgmt 340<br>access 340<br>NFS 341<br>iSCSI A/B 341/341 | mgmt 172.16.70.0/24<br>access 172.16.70.0/24<br>NFS 172.16.71.0<br>iSCSI A/B 172.16.71.0/24 / 172.16.71.0/24 | winterlinde_svm<br>nfs<br>client 172.16.71.0/24 | 3 |
| zirbe | zirbe<br>virtual, tid 29 | zirbe | mgmt 430<br>access 430<br>NFS 431<br>iSCSI A/B 431/431 | mgmt 172.16.160.0/24<br>access 172.16.160.0/24<br>NFS 172.16.161.0<br>iSCSI A/B 172.16.161.0/24 / 172.16.161.0/24 | zirbe_svm<br>nfs<br>client 172.16.161.0/24 | 3 |

## Virtual Tenant Registry

The registry below shows `v##_name` definitions found inside tenant vars. These are used by carrier tenants such as the DataSpace/Harvester definitions to publish virtual tenant access and NFS VLANs from a parent tenant context.

| Parent directory | Parent tenant | Virtual tenant | Access VLAN / CIDR | NFS VLAN / CIDR |
| --- | --- | --- | --- | --- |
| dataspace | DataSpace | v10 robinie | 300 / 172.16.30.0/24 | 301 / 172.16.31.0/24 |
| dataspace | DataSpace | v11 douglasie | 305 / 172.16.35.0/24 | 306 / 172.16.36.0/24 |
| dataspace | DataSpace | v12 eberesche | 310 / 172.16.40.0/24 | 311 / 172.16.41.0/24 |
| dataspace | DataSpace | v13 walnuss | 315 / 172.16.45.0/24 | 316 / 172.16.46.0/24 |
| dataspace | DataSpace | v14 elsbeere | 320 / 172.16.50.0/24 | 321 / 172.16.51.0/24 |
| dataspace | DataSpace | v15 speierling | 325 / 172.16.55.0/24 | 326 / 172.16.56.0/24 |
| dataspace | DataSpace | v16 hainbuche | 330 / 172.16.60.0/24 | 331 / 172.16.61.0/24 |
| dataspace | DataSpace | v17 eibe | 335 / 172.16.65.0/24 | 336 / 172.16.66.0/24 |
| dataspace | DataSpace | v18 winterlinde | 340 / 172.16.70.0/24 | 341 / 172.16.71.0/24 |
| dataspace | DataSpace | v19 waldkiefer | 345 / 172.16.75.0/24 | 346 / 172.16.76.0/24 |
| dataspace | DataSpace | v20 edelkastanie | 350 / 172.16.80.0/24 | 351 / 172.16.81.0/24 |
| dataspace | DataSpace | v21 rosskastanie | 355 / 172.16.85.0/24 | 356 / 172.16.86.0/24 |
| dataspace | DataSpace | v22 wacholder | 360 / 172.16.90.0/24 | 361 / 172.16.91.0/24 |
| dataspace | DataSpace | v23 rotbuche | 365 / 172.16.95.0/24 | 366 / 172.16.96.0/24 |
| dataspace | DataSpace | v24 sommerlinde | 370 / 172.16.100.0/24 | 371 / 172.16.101.0/24 |
| dataspace | DataSpace | v25 vogelkirsche | 375 / 172.16.105.0/24 | 376 / 172.16.106.0/24 |
| dataspace | DataSpace | v26 feldahorn | 380 / 172.16.110.0/24 | 381 / 172.16.111.0/24 |
| dataspace | DataSpace | v27 schwarzerle | 385 / 172.16.115.0/24 | 386 / 172.16.116.0/24 |
| dataspace | DataSpace | v28 edeltanne | 390 / 172.16.120.0/24 | 391 / 172.16.121.0/24 |
| dataspace | DataSpace | v29 silberweide | 395 / 172.16.125.0/24 | 396 / 172.16.126.0/24 |
| dataspace | DataSpace | v30 fichte | 400 / 172.16.130.0/24 | 401 / 172.16.131.0/24 |
| dataspace | DataSpace | v31 haselnuss | 405 / 172.16.135.0/24 | 406 / 172.16.136.0/24 |
| dataspace | DataSpace | v32 stechpalme | 410 / 172.16.140.0/24 | 411 / 172.16.141.0/24 |
| dataspace | DataSpace | v33 weissdorn | 415 / 172.16.145.0/24 | 416 / 172.16.146.0/24 |
| dataspace | DataSpace | v34 birke | 420 / 172.16.150.0/24 | 421 / 172.16.151.0/24 |
| dataspace | DataSpace | v35 stieleiche | 425 / 172.16.155.0/24 | 426 / 172.16.156.0/24 |
| dataspace | DataSpace | v36 zirbe | 430 / 172.16.160.0/24 | 431 / 172.16.161.0/24 |
| dataspace | DataSpace | v37 laerche | 435 / 172.16.165.0/24 | 436 / 172.16.166.0/24 |
| dataspace | DataSpace | v38 schwarzdorn | 440 / 172.16.170.0/24 | 441 / 172.16.171.0/24 |
| dataspace | DataSpace | v39 ahorn | 445 / 172.16.175.0/24 | 446 / 172.16.176.0/24 |
| dataspace | DataSpace | v40 kastanie | 450 / 172.16.180.0/24 | 451 / 172.16.181.0/24 |
| dataspace | DataSpace | v98 gpu | 204 / 172.17.4.0/24 | 203 / 172.17.3.0/24 |
| dataspace | DataSpace | v99 tanne | 3998 / 172.16.254.0/24 | 3999 / 172.16.255.0/24 |
| harvester | DataSpace | v10 robinie | 300 / 172.16.30.0/24 | 301 / 172.16.31.0/24 |
| harvester | DataSpace | v11 douglasie | 305 / 172.16.35.0/24 | 306 / 172.16.36.0/24 |
| harvester | DataSpace | v12 eberesche | 310 / 172.16.40.0/24 | 311 / 172.16.41.0/24 |
| harvester | DataSpace | v13 walnuss | 315 / 172.16.45.0/24 | 316 / 172.16.46.0/24 |
| harvester | DataSpace | v14 elsbeere | 320 / 172.16.50.0/24 | 321 / 172.16.51.0/24 |
| harvester | DataSpace | v15 speierling | 325 / 172.16.55.0/24 | 326 / 172.16.56.0/24 |
| harvester | DataSpace | v16 hainbuche | 330 / 172.16.60.0/24 | 331 / 172.16.61.0/24 |
| harvester | DataSpace | v17 eibe | 335 / 172.16.65.0/24 | 336 / 172.16.66.0/24 |
| harvester | DataSpace | v18 winterlinde | 340 / 172.16.70.0/24 | 341 / 172.16.71.0/24 |
| harvester | DataSpace | v19 waldkiefer | 345 / 172.16.75.0/24 | 346 / 172.16.76.0/24 |
| harvester | DataSpace | v20 edelkastanie | 350 / 172.16.80.0/24 | 351 / 172.16.81.0/24 |
| harvester | DataSpace | v21 rosskastanie | 355 / 172.16.85.0/24 | 356 / 172.16.86.0/24 |
| harvester | DataSpace | v22 wacholder | 360 / 172.16.90.0/24 | 361 / 172.16.91.0/24 |
| harvester | DataSpace | v23 rotbuche | 365 / 172.16.95.0/24 | 366 / 172.16.96.0/24 |
| harvester | DataSpace | v24 sommerlinde | 370 / 172.16.100.0/24 | 371 / 172.16.101.0/24 |
| harvester | DataSpace | v25 vogelkirsche | 375 / 172.16.105.0/24 | 376 / 172.16.106.0/24 |
| harvester | DataSpace | v99 tanne | 3998 / 172.16.254.0/24 | 3999 / 172.16.255.0/24 |

## Managed Role Inventory

| Playbook | Roles called |
| --- | --- |
| `INFRA.yml` | INFRA/env_vars<br>INFRA/nexus_config<br>INFRA/nexus_config_sg<br>INFRA/nexus_config_ip<br>INFRA/nexus_config_proxmox<br>INFRA/env_vars<br>INFRA/ontap_network<br>INFRA/ontap_svm<br>INFRA/ontap_volumes<br>INFRA/ontap_lifs<br>INFRA/env_vars<br>INFRA/ucs_create_pools<br>INFRA/env_vars<br>INFRA/nexus_config_asa |
| `TENANT.yml` | TENANT/env_vars<br>TENANT/nexus_config<br>TENANT/nexus_config_ip<br>TENANT/nexus_config_sg<br>TENANT/nexus_config_asa<br>TENANT/env_vars<br>TENANT/ontap_network<br>TENANT/ontap_svm<br>TENANT/ontap_volumes<br>TENANT/ontap_lifs<br>TENANT/ontap_luns<br>TENANT/ontap_nvme<br>TENANT/env_vars<br>TENANT/ucs_create_pools<br>TENANT/ucs_create_server_policies<br>TENANT/ucs_create_sp_template<br>TENANT/env_vars<br>TENANT/ucs_create_server<br>TENANT/env_vars<br>TENANT/os_install_suse<br>rancher/env_vars<br>rancher/pre_rke_install<br>rancher/env_vars<br>rancher/rke2_server<br>rancher/rke2_agent<br>TENANT/env_vars<br>TENANT/trident_install |
| `RKE2.yml` | rancher/env_vars<br>rancher/pre_rke_install<br>rancher/env_vars<br>rancher/rke2_server<br>rancher/rke2_agent |

## How To Explain This To An Audience

The easiest story is to present the framework in three layers:

1. The FlexPod base layer provides redundant Nexus switching, ONTAP storage, and Intersight-controlled UCS compute.
2. The tenant layer adds one isolated VRF, a small set of tenant VLANs and CIDRs, a tenant SVM, and tenant-scoped Intersight objects.
3. The platform layer consumes that tenant boundary for RKE2, Harvester, Trident, or other workloads.

That framing makes the separation model visible: shared hardware and shared automation patterns below, tenant-local network/storage/compute identities above.

## Related Design References

- [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html)
- [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/)
