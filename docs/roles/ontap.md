# Shared ONTAP Roles

[Role index](README.md) | [Playbooks](../playbooks.md) | [Product references](../references.md)

Use this page to understand what each role is expected to configure before opening the detailed role README.

| Role                                                                             | Called by | Expected configuration                                                                  |
| -------------------------------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------- |
| [`ONTAP/esxi_datastores`](../../roles/ONTAP/esxi_datastores/README.md)           | -         | Runs the role task flow described below.                                                |
| [`ONTAP/ontap_finalize_setup`](../../roles/ONTAP/ontap_finalize_setup/README.md) | -         | Applies final SVM services such as DNS, auditing, and final storage service settings.   |
| [`ONTAP/ontap_lifs`](../../roles/ONTAP/ontap_lifs/README.md)                     | -         | Builds ONTAP NFS, iSCSI, FC, FC-NVMe, or NVMe/TCP data LIFs.                            |
| [`ONTAP/ontap_luns`](../../roles/ONTAP/ontap_luns/README.md)                     | -         | Builds boot and data LUNs, igroups, and host-to-LUN mapping.                            |
| [`ONTAP/ontap_network`](../../roles/ONTAP/ontap_network/README.md)               | -         | Builds ONTAP broadcast domains, VLAN ports, and network foundations for tenant storage. |
| [`ONTAP/ontap_nvme`](../../roles/ONTAP/ontap_nvme/README.md)                     | -         | Builds NVMe namespaces, subsystems, and host NQN mappings.                              |
| [`ONTAP/ontap_primary_setup`](../../roles/ONTAP/ontap_primary_setup/README.md)   | -         | Runs the role task flow described below.                                                |
| [`ONTAP/ontap_svm`](../../roles/ONTAP/ontap_svm/README.md)                       | -         | Builds or removes ONTAP SVMs and protocol services.                                     |
| [`ONTAP/ontap_svm_custom`](../../roles/ONTAP/ontap_svm_custom/README.md)         | -         | Builds or removes ONTAP SVMs and protocol services.                                     |
| [`ONTAP/ontap_volumes`](../../roles/ONTAP/ontap_volumes/README.md)               | -         | Builds NFS/export-backed FlexVols and tenant data volumes.                              |
