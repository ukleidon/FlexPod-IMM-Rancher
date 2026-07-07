# FlexPod IMM Rancher Public KL-IDTA Framework

This repository automates a FlexPod-based lab and tenant environment. It uses Ansible to configure the shared Cisco Nexus, Cisco MDS, Cisco Intersight, NetApp ONTAP, and optional RKE2/Rancher layers that make up the infrastructure.

The core design follows the FlexPod operating model: Cisco UCS/Intersight for compute, Cisco Nexus/MDS for Ethernet and SAN connectivity, and NetApp ONTAP for shared storage. For architecture background, start with the [Cisco FlexPod Design Guides](https://www.cisco.com/c/en/us/solutions/design-zone/data-center-design-guides/flexpod-design-guides.html) and [NetApp FlexPod Solutions](https://docs.netapp.com/us-en/flexpod/).

## Who This Is For

This documentation is written for infrastructure operators with some networking, server, and storage experience. You should be comfortable with VLANs, IP subnets, VRFs, server profiles, and storage SVM/LIF concepts, but you do not need to know every Ansible role by heart.

## Validated Design Context

FlexPod-IMM-Rancher follows the same operating model as the Cisco Validated Design [FlexPod Datacenter using IaC with Cisco IMM M7, VMware vSphere 8, and NetApp ONTAP 9.12.1](https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/flexpod_imm_m7_iac.html). That CVD is the reference for the base FlexPod sequencing, product roles, redundancy model, and Ansible-based deployment flow.

The difference is that FlexPod-IMM-Rancher adds a lean multi-tenant structure on top of the shared infrastructure. A complete FlexPod stack is required for end-to-end validation. Individual roles can still be syntax-checked or check-mode tested against a partial lab when the inventory and device reachability match the role being tested.

## Execution Environment

Run the framework from an Ansible control host with network reachability to the Nexus, MDS, ONTAP, Intersight API, and any tenant hosts that will receive OS or RKE2 configuration. Use the control host's existing Python or virtual environment when one is already prepared.

Install the collections used by the current roles before running playbooks:

```bash
ansible-galaxy collection install cisco.intersight cisco.nxos netapp.ontap community.vmware
```

Keep the Intersight API key references in `group_vars/ucs.yml` and `tenants/<tenant>/vars.yml` current before running live or check-mode tasks.

## GitHub Publication Safety

This repository is prepared for GitHub publication with placeholder credentials. Do not commit live Intersight API keys, private key files, ONTAP passwords, Trident backend passwords, local user passwords, or tenant-specific secret material.

Before staging changes, run:

```bash
./scripts/publication_check.py
```

Keep real deployment secrets in ignored local files, Ansible Vault, environment-backed vars, or a private overlay that is not committed.

## Main Entry Points

| File                                                           | Use it for                                                     | Expected result                                                                                                               |
| -------------------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [`INFRA.yml`](INFRA.yml)                                       | Build or validate shared FlexPod infrastructure.               | Shared Nexus, ONTAP, Intersight, StorageGRID, Proxmox, and ASA integration objects.                                           |
| [`TENANT.yml`](TENANT.yml)                                     | Build or remove one selected tenant.                           | Tenant VLANs, VRFs, storage objects, Intersight policies/profiles, OS install prep, RKE2, and Trident depending on inventory. |
| [`RKE2.yml`](RKE2.yml)                                         | Run the RKE2 role flow for a selected tenant context.          | RKE2 prerequisite, server, and agent configuration where matching hosts exist.                                                |
| [`TEST.yml`](TEST.yml)                                         | Run a repository-specific automation workflow.                 | Configuration described by the plays and roles in the playbook.                                                               |
| [`scripts/create_tenant.py`](scripts/create_tenant.py)         | Create a new tenant directory from a known-good tenant.        | New `tenants/<name>/vars.yml` and optional virtual registry vars updates.                                                     |
| [`scripts/publication_check.py`](scripts/publication_check.py) | Check for accidental literal keys/passwords before publishing. | The repo is safe to stage from a credential hygiene perspective.                                                              |

## Recommended Operator Path

1. Read [Architecture](docs/architecture.md) to understand how the framework maps to FlexPod.
2. Read [Variables](docs/variables.md) before changing tenant or infrastructure data.
3. Create or review the tenant with [New Tenant Guide](docs/tenants/new-tenant.md).
4. Run syntax checks from [Validation](docs/validation.md).
5. Run check mode with `-C`.
6. Run live only after the expected device/controller changes are understood.

## Quick Validation

```bash
ansible-playbook -i inventory INFRA.yml --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=eibe --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=eibe -C
```

## Documentation

- [Documentation index](docs/README.md)
- [Architecture overview diagrams](docs/architecture-overview.md)
- [Playbooks](docs/playbooks.md)
- [Variables](docs/variables.md)
- [Roles](docs/roles/README.md)
- [Tenants](docs/tenants/README.md)
- [Operations](docs/operations.md)
- [Validation](docs/validation.md)
- [GitHub publication checklist](docs/github-publication.md)
- [Product references](docs/references.md)

## Safety Rules

- A tenant must be configurable and unconfigurable independent of every other tenant.
- Tenant-specific VLANs, CIDRs, credentials, storage identities, and API key references stay in `tenants/<tenant>/vars.yml`.
- Shared generated defaults stay in `group_vars/tenant_defaults.yml`.
- Run `--syntax-check` and `-C` before live changes.
- Do not run legacy or archived playbooks unless they have been deliberately brought forward and validated.
