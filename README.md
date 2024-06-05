[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/ucs-compute-solutions/FlexPod-IMM-VMware)

 FlexPod Converged Infrastructure setup using Ansible for FlexPod Datacenter with Cisco UCS M7 IMM, VMware vSphere 8.0, and NetApp ONTAP 9.12.1

Note that the scripts in this repository have now been successfully tested with NetApp ONTAP 9.13.1, NetApp ONTAP 9.14.1, and VMware vSphere 8.0 Update 2.

This repository for FlexPod contains Ansible playbooks to configure Cisco Nexus, Cisco UCS Intersight, Cisco MDS, NetApp ONTAP, VMware ESXi, and VMware vCenter. This repository can be used for setting up Cisco devices, NetApp ONTAP Storage, and VMware ESXi and vCenter as covered in the following Cisco Validated Design (CVD): https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/flexpod_imm_m7_iac.html.

The CVD lays out the complete process for configuring the FlexPod using Ansible. Since these playbooks are intended to save time in setting up a working FlexPod, a complete FlexPod as shown below is needed to execute the playbooks. Various simulators could be used to partially test individual playbooks.

![block-diagram](https://github.com/ucs-compute-solutions/FlexPod-IMM-VMware/blob/main/ReadmePics/Main-Topology.jpg)  

 Set up the execution environment

To execute various ansible playbooks, a linux based system will need to be setup as described in the CVD with the packages listed at the following pages:

- Cisco UCS Intersight: https://galaxy.ansible.com/ui/repo/published/cisco/intersight/
- Cisco NxOS: https://galaxy.ansible.com/ui/repo/published/cisco/nxos/
- NetApp ONTAP: https://galaxy.ansible.com/ui/repo/published/netapp/ontap/
- VMware: https://galaxy.ansible.com/ui/repo/published/community/vmware/

 How to execute these playbooks?

![block-diagram](https://github.com/ucs-compute-solutions/FlexPod-IMM-VMware/blob/main/ReadmePics/Ansible-Order.jpg)

Because a number of manual tasks need to be executed between running the Ansible playbooks, the CVD document should be used as a guide for running the playbooks. Commentary is included in the variable files to guide filling in those values.

In this version of the FlexPod setup, FC boot with FC-NVMe and NFS is configured by default in the variable files, but iSCSI boot and NVMe-TCP with NFS can also be used.
The steps for setting up a FlexPod with FC boot with FC-NVMe and NFS storage protocols are:

1.  Create a directory and clone the repository from Github with "git clone https://github.com/ucs-compute-solutions/FlexPod-IMM-VMware.git".
2.  Fill in the variable files according to the CVD.
3.  Follow the manual steps in the CVD to set up the Nexus switches on the network and ssh into each switch.
4.  Execute the Nexus playbook with "ansible-playbook ./Setup_Nexus.yml -i inventory" to setup the Nexus switches.
5.  Follow the manual steps in the CVD to add timezone information to the Nexus switches.
6.  Follow the manual steps in the CVD to get the NetApp storage cluster on the network.
7.  Execute the NetApp storage playbook with "ansible-playbook -i inventory Setup_ONTAP.yml -t ontap_config_part_1".
8.  Query the Infra-SVM iSCSI IQN and add to the "all.yml" file.
9.  Follow the manual steps in the CVD to create an Intersight Account, and get the Cisco UCS Fabric Interconnects (FIs) on the network in Intersight Managed Mode.
10.  Claim the FIs into Intersight and setup and deploy the Domain Profile.
11.  Execute the IMM playbooks with "ansible-playbook ./Setup_IMM_Pools.yml", "ansible-playbook ./Setup_IMM_Server_Policies.yml", and 
     "ansible-playbook ./Setup_IMM_Server_Profile_Templates.yml" to setup the Cisco UCS Server Profile Templates, Policies, and Pools.
12.  Follow the manual steps in the CVD to create UCS IMM server profiles for three or more VMware ESXi management hosts.
13.  Query the ESXi host IQNs or WWPNs from the server profiles and add to the "all.yml" file.
14.  If configuring Fibre Channel, follow the manual steps in the CVD to set up the MDS switches on the network and ssh into each switch.
15.  If configuring Fibre Channel, execute the MDS playbook with "ansible-playbook ./Setup_MDS.yml -i inventory".
16.  If configuring Fibre Channel, follow the manual steps in the CVD to add timezone information to the MDS switches. 
17.  Execute the NetApp storage playbook with "ansible-playbook -i inventory Setup_ONTAP.yml -t ontap_config_part_2" to create and map the ESXi boot LUNs.
18.  Follow the manual steps in the CVD to install VMware ESXi and assign IPs on the three (or more) host servers using Cisco Intersight OS Install.
19.  Execute the ESXi playbook with "ansible-playbook ./Setup_ESXi.yml -i inventory" to setup the ESXi hosts.
20.  Bring a vCenter into the environment by either installing vCenter on the first ESXi host according to the CVD, copying it in, or establishing L3 routing to it.
21.  Setup the vCenter and add the three or more ESXi hosts to it by executing "ansible-playbook ./Setup_vCenter.yml -i inventory".
22.  Follow the manual steps in the CVD to complete setting up vCenter and the ESXi hosts.
23.  Execute the NetApp storage playbook with "ansible-playbook -i inventory Setup_ONTAP.yml -t ontap_config_part_3" to setup NVMe-TCP and finalize ONTAP Storage.
24.  Execute the manual steps in the CVD to complete the NVMe-TCP setup.
25.  Follow the steps in the CVD to install the ONTAP Tools VM via Ansible.
26.  Follow the steps in the CVD to install the SnapCenter VMware Plug-In via Ansible.
27.  Follow the steps in the CVD to install Active IQ Unified Manager via Ansible.
28.  Follow the manual steps in the CVD to finish setting up ONTAP tools, the SnapCenter Plug-in, and AIQUM.
29.  Follow the manual steps in the CVD to setup Cisco Intersight Assist and Cisco Nexus Dashboard Fabric Controller (NDFC) SAN.

The Ansible playbooks and CVD are structured in a way that a Fibre Channel Boot, Fibre Channel Boot with FC-NVMe, iSCSI Boot or iSCSI Boot with NVMe-TCP FlexPod or combination configurations can be setup by adjusting the variables. Also, the playbooks can be used to setup the following topology utilizing Cisco Nexus switches that support SAN Switching (93180YC-FX, 93360YC-FX2, or 9336C-FX2-E) for both LAN and SAN switching and 100G FCoE Uplinks from the FIs to the switches.

![block-diagram](https://github.com/ucs-compute-solutions/FlexPod-IMM-VMware/blob/main/ReadmePics/NexusSAN-Topology.jpg)



The confiuration for multi-tenancy and secure-multi-tenancy is available now 

 The new setup of FlexPod with ansible is now based on the initial infrastructure setup without any workloads,
 and the workload setup on top of the infrastructure. This changed the way variables are defined and used.

 inventory:                   Inventory file for the HW components: UCS, Nexus, MDS, Ontap
 inventory_XXX:               Inventory file for an workload / tenant.                           ---- NEW ----
                                 Define host, vcenter, RKE, OCP, ... systems.
                                 ansible-playbook allows to use the -i option more than once.
 vars:                        This directory is removed in the new structure.                    ---- Removed ----
 vars/ontab:                  The content is not moved into host_vars and tenant_vars.           ---- Removed ----
 group_vars                   Directory used to define inventory-group specific variables.
 group_vars/all.yml:          This file: For variables required for the complete stack.
           /ucs.yml:          Infrastructure part of the Intersight/UCS configuration.
           /nexus.yml:        Infrastructure part of the Nexus configuration. i.e. VPC, port-channels, ...
           /mds.yml:          Infrastructure part of the MDS configuration.
           /ontap.yml:        Infrastrucrure part of the NetApp Ontap configuration.
           /vmware.yml:       Global settings for VMware deployments used by all tenants.
 host_vars                    Directory for all host(name) specific variables.
 host_vars/n9kA.yml           Host specific varables for Nexus A
          /n9kB.yml           Host specific varables for Nexus B
          /mdsA.yml           Host specific varables for MDS A
          /mdsB.yml           Host specific varables for MDS B
          /c250-1.yml         Host specific varables for NetApp Storage 1                         ---- NEW ----
 tenants/                     Directory to collect all tenant relevant artifacts                  ---- NEW ----
 tenants/[tenant]             Directory to collect all artifacts for [tenant1]                    ---- NEW ----
        /[tenant]/vars.yml:   File for all tenant specific variables                              ---- NEW ----
                 /airgap:     All files required for airgapped installations.                     ---- NEW ----
                 /manifests:  All K8s manifests used for this tenant                              ---- NEW ----
 
 To simplify the definiton of tenants and the structure with group_vars, host_vars and tenant specific
 variables, the role env_vars is introduces.


Define the variable files required for an role regardless if ansible will source it based on
the group or host definition. This takes care that the required group_vars are used even if
the actual entity is not part of the group.
Like: For UCS there is no host entry and a tenant host will not be listed in the ucs group.
With default behavior some variables are not used as ucs.yml is not sources.
The env_vars role will take care that ucs.yml is sourced before the tenant/vars.yaml is.   
With this we take care that all required information is avaliable to setup a tenant on top
of the FlexPod infrastructure. 

 roles/TENANT/env_vars/detauls/main.yml:
  env_vars_all_file: "{{ playbook_dir }}/group_vars/all.yml"    # source the all.yml file
  env_vars_ucs_file: "{{ playbook_dir }}/group_vars/ucs.yml"    # source the ucs.yml file
  env_vars_env_name: "{{ tenant }}"                             # call -e tenant=[tenant name]
  tenant_dir: "{{ tenants_dir }}/{{ tenant|lower }}"            # specify where the tenant info is located
  env_vars_tenant_file: "{{ tenant_dir }}/vars.yml"             # source the tenant variables.

 roles/TENANT/env_vars/tasks/main.yml:
  - name: Include cluster environment variables
    tags: [always]
    include_vars:
      file: "{{ item }}"
    loop:
      - "{{ env_vars_all_file }}"
      - "{{ env_vars_ucs_file }}"
      - "{{ env_vars_tenant_file }}"

 TASK [TENANT/env_vars : Include cluster environment variables] 
 ok: [localhost] => (item=/home/admin/CVD/group_vars/all.yml)
 ok: [localhost] => (item=/home/admin/CVD/group_vars/ucs.yml)
 ok: [localhost] => (item=/home/admin/CVD/tenants/ac01/vars.yml)

