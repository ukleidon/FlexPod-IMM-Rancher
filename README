########################################################################################################################

# -------------  The confiuration for multi-tenancy and secure-multi-tenancy is available now --------------------------
#
# The new setup of FlexPod with ansible is now based on the initial infrastructure setup without any workloads,
# and the workload setup on top of the infrastructure. This changed the way variables are defined and used.
#
# inventory:                   Inventory file for the HW components: UCS, Nexus, MDS, Ontap
# inventory_XXX:               Inventory file for an workload / tenant.                           ---- NEW ----
#                                 Define host, vcenter, RKE, OCP, ... systems.
#                                 ansible-playbook allows to use the -i option more than once.
# vars:                        This directory is removed in the new structure.                    ---- Removed ----
# vars/ontab:                  The content is not moved into host_vars and tenant_vars.           ---- Removed ----
# group_vars                   Directory used to define inventory-group specific variables.
# group_vars/all.yml:          This file: For variables required for the complete stack.
#           /ucs.yml:          Infrastructure part of the Intersight/UCS configuration.
#           /nexus.yml:        Infrastructure part of the Nexus configuration. i.e. VPC, port-channels, ...
#           /mds.yml:          Infrastructure part of the MDS configuration.
#           /ontap.yml:        Infrastrucrure part of the NetApp Ontap configuration.
#           /vmware.yml:       Global settings for VMware deployments used by all tenants.
# host_vars                    Directory for all host(name) specific variables.
# host_vars/n9kA.yml           Host specific varables for Nexus A
#          /n9kB.yml           Host specific varables for Nexus B
#          /mdsA.yml           Host specific varables for MDS A
#          /mdsB.yml           Host specific varables for MDS B
#          /c250-1.yml         Host specific varables for NetApp Storage 1                         ---- NEW ----
# tenants/                     Directory to collect all tenant relevant artifacts                  ---- NEW ----
# tenants/[tenant]             Directory to collect all artifacts for [tenant1]                    ---- NEW ----
#        /[tenant]/vars.yml:   File for all tenant specific variables                              ---- NEW ----
#                 /airgap:     All files required for airgapped installations.                     ---- NEW ----
#                 /manifests:  All K8s manifests used for this tenant                              ---- NEW ----
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# 
# To simplify the definiton of tenants and the structure with group_vars, host_vars and tenant specific
# variables, the role env_vars is introduces.
#
#
#      Define the variable files required for an role regardless if ansible will source it based on
#      the group or host definition. This takes care that the required group_vars are used even if
#      the actual entity is not part of the group.
#      Like: For UCS there is no host entry and a tenant host will not be listed in the ucs group.
#      With default behavior some variables are not used as ucs.yml is not sources.
#      The env_vars role will take care that ucs.yml is sourced before the tenant/vars.yaml is.   
#      With this we take care that all required information is avaliable to setup a tenant on top
#      of the FlexPod infrastructure. 

# roles/TENANT/env_vars/detauls/main.yml:
#  env_vars_all_file: "{{ playbook_dir }}/group_vars/all.yml"    # source the all.yml file
#  env_vars_ucs_file: "{{ playbook_dir }}/group_vars/ucs.yml"    # source the ucs.yml file
#  env_vars_env_name: "{{ tenant }}"                             # call -e tenant=[tenant name]
#  tenant_dir: "{{ tenants_dir }}/{{ tenant|lower }}"            # specify where the tenant info is located
#  env_vars_tenant_file: "{{ tenant_dir }}/vars.yml"             # source the tenant variables.

# roles/TENANT/env_vars/tasks/main.yml:
#  - name: Include cluster environment variables
#    tags: [always]
#    include_vars:
#      file: "{{ item }}"
#    loop:
#      - "{{ env_vars_all_file }}"
#      - "{{ env_vars_ucs_file }}"
#      - "{{ env_vars_tenant_file }}"
#
# TASK [TENANT/env_vars : Include cluster environment variables] ****************************************************************
# ok: [localhost] => (item=/home/admin/CVD/group_vars/all.yml)
# ok: [localhost] => (item=/home/admin/CVD/group_vars/ucs.yml)
# ok: [localhost] => (item=/home/admin/CVD/tenants/ac01/vars.yml)
#
#
#
#################################################################################################################################

