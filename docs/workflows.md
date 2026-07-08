# Workflows

[Documentation index](README.md) | [Architecture](architecture.md) | [Playbooks](playbooks.md) | [Operations](operations.md) | [Validation](validation.md)

This page shows how the public FlexPod-IMM-Rancher automation is expected to be used. It is written for operators who know infrastructure basics but do not need to understand every role before running the first safe validation.

All tenant names, domains, VLAN IDs, and addresses shown here are examples. Put real values only in a private inventory, Ansible Vault, ignored overlay, or deployment-specific branch.

## End-To-End Deployment Flow

```mermaid
flowchart TB
  prepare["Prepare control node<br/>collections, Python deps, kubeconfig"]
  publish["Run publication check<br/>before public commits"]
  infraSyntax["INFRA.yml syntax check"]
  infraCheck["INFRA.yml check mode"]
  infraLive["INFRA.yml live run"]
  tenantSyntax["TENANT.yml syntax check<br/>one tenant"]
  tenantCheck["TENANT.yml check mode"]
  tenantLive["TENANT.yml live run"]
  harvesterTenant["HARVESTER.yml<br/>tenant support objects"]
  harvesterRke["HARVESTER_RKE.yml<br/>Rancher-provisioned RKE2"]
  workload["Optional workload add-ons<br/>kube-vip, storage annotations, Kasten"]
  validate["Post-run validation<br/>device, API, and Kubernetes checks"]

  prepare --> publish --> infraSyntax --> infraCheck --> infraLive
  infraLive --> tenantSyntax --> tenantCheck --> tenantLive
  tenantLive --> harvesterTenant --> harvesterRke --> workload --> validate
```

Use the first half of this workflow for physical tenants. Use the full workflow when a tenant also needs Harvester HCI support and a virtual RKE2 cluster.

## Tenant Lifecycle

```mermaid
stateDiagram-v2
  [*] --> VarsReady: tenants/<tenant>/vars.yml exists
  VarsReady --> Syntax: ansible-playbook --syntax-check
  Syntax --> CheckMode: ansible-playbook -C
  CheckMode --> Present: live run with lan_state=present
  Present --> DriftReview: future check mode run
  DriftReview --> Present: intended drift accepted
  Present --> AbsentCheck: lan_state=absent -C
  AbsentCheck --> Absent: live absent run
  Absent --> [*]
```

Every tenant should be configurable and removable without editing another tenant directory. Shared defaults belong in `group_vars`, while tenant identity, VLANs, CIDRs, and storage identity stay in `tenants/<tenant>/vars.yml`.

## Harvester Tenant Workflow

```mermaid
flowchart LR
  vars["Tenant vars<br/>tenant_type=virtual<br/>access + NFS VLAN/CIDR"]
  env["TENANT/env_vars<br/>loads shared + tenant vars"]
  source["Harvester ConfigMap<br/>default/sle-micro-default"]
  render["Render tenant manifests<br/>tenants/<tenant>/manifests/harvester"]
  namespace["Namespace<br/><tenant>"]
  networks["NetworkAttachmentDefinitions<br/><tenant>-access + <tenant>-storage"]
  dhcp["DHCP IPPools<br/>access + storage"]
  cloudinit["Tenant cloud-init ConfigMap<br/><tenant>-sle-micro-default"]

  vars --> env --> source --> render
  render --> namespace
  render --> networks
  render --> dhcp
  render --> cloudinit
```

`HARVESTER.yml` creates the tenant namespace, Harvester networks, DHCP pools, and tenant-adapted cloud-init template. Platform-wide Harvester settings such as proxy, NTP, add-ons, ClusterNetwork, VlanConfig, and storage-network are opt-in through `harvester_manage_platform=true`.

## Rancher RKE2-On-Harvester Workflow

```mermaid
flowchart TB
  tenantObjects["HARVESTER.yml objects<br/>namespace, networks, DHCP, cloud-init"]
  image["Discover Harvester VM image<br/>sl-micro.x86_64-6.2*"]
  userData["Resolve cloud-init userData<br/>tenant ConfigMap or default template"]
  machineConfig["Rancher HarvesterConfig<br/>VM CPU, memory, disk, networks"]
  cluster["Rancher Cluster<br/><tenant>-rke, three nodes by default"]
  vms["Harvester VMs<br/>RKE2 control-plane + worker roles"]
  downstream["Downstream kube context<br/><tenant>-rke"]
  addons["Optional workload add-ons<br/>kube-vip, Trident PSA RBAC, Kasten"]

  tenantObjects --> image --> userData --> machineConfig --> cluster --> vms --> downstream --> addons
```

`HARVESTER_RKE.yml` assumes Rancher already has a Harvester cloud credential and cloud-provider configuration. The public repository contains placeholder values such as `REPLACE_ME_RANCHER_CREATOR_ID`; real Rancher references must come from a private variable source.

## Physical And Virtual Tenant Decision Flow

```mermaid
flowchart TD
  start["New workload or tenant request"]
  physical{"Needs bare-metal UCS server profiles?"}
  platform{"Is it the platform tenant<br/>for Rancher or Harvester?"}
  virtual{"Runs as VMs on Harvester?"}
  tenantVars["Create or update<br/>tenants/<tenant>/vars.yml"]
  tenantPlay["Run TENANT.yml<br/>network, storage, compute"]
  harvesterPlay["Run HARVESTER.yml<br/>tenant HCI support"]
  rkePlay["Run HARVESTER_RKE.yml<br/>virtual RKE2 cluster"]
  done["Validate and document<br/>tenant-specific private values"]

  start --> physical
  physical -->|yes| tenantVars --> tenantPlay --> done
  physical -->|no| platform
  platform -->|yes| tenantVars --> tenantPlay --> done
  platform -->|no| virtual
  virtual -->|yes| tenantVars --> harvesterPlay --> rkePlay --> done
  virtual -->|no| tenantVars --> tenantPlay --> done
```

Physical tenants use direct Nexus, ONTAP, Intersight, iSCSI boot, and optional RKE2/Trident flows. Virtual tenants use tenant YAML as the source of truth for Harvester networks and Rancher-provisioned RKE2 clusters.

## Public Repository Safety Flow

```mermaid
flowchart LR
  edit["Edit docs, roles, vars examples"]
  scan["Run publication_check.py"]
  grep["Run targeted lab-string scan"]
  syntax["Run syntax checks"]
  diff["Review git diff"]
  commit["Commit sanitized content"]
  push["Push to public GitHub"]

  edit --> scan --> grep --> syntax --> diff --> commit --> push
```

The publication flow is part of the documentation, not an optional extra. Public examples should keep topology shape, variable names, and operator guidance while removing live credentials, private hostnames, private domains, and customer-only addressing.
