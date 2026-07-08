# FlexPod-IMM-Rancher Documentation

This documentation is optimized for browser preview. It explains the automation in the order an operator usually needs it: architecture, workflows, variables, playbooks, roles, tenants, operations, validation, and product references.

## Start Here

1. [Architecture](architecture.md)
2. [Architecture overview diagrams](architecture-overview.md)
3. [Workflows](workflows.md)
4. [Variables](variables.md)
5. [Playbooks](playbooks.md)
6. [Roles](roles/README.md)
7. [Tenants](tenants/README.md)
8. [Operations](operations.md)
9. [Validation](validation.md)
10. [GitHub publication checklist](github-publication.md)
11. [Product references](references.md)

## Reading Model

- Use the workflow page to understand deployment order, tenant lifecycle, Harvester support objects, Rancher RKE2 cluster creation, and public publication safety.
- Use the playbook pages to understand exactly which roles each entry point calls.
- Use the role pages when a task fails or you need to know what a section configures.
- Use the tenant pages to review tenant-specific facts without exposing credential values.
- Use the operations and validation pages to prepare the Ansible control node and follow the CVD-aligned rollout order.
- Use the GitHub publication checklist before staging or pushing sanitized examples.
- Use the product references when you need the official Cisco, NetApp, SUSE, or Ansible behavior behind a task.
