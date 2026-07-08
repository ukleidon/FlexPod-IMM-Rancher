# Common Roles

[Role inventory](../README.md)

Common roles provide framework-level helpers that are shared by tenant and platform playbooks. They do not configure infrastructure directly; they validate input, normalize execution data, or prepare facts for the product-specific roles.

| Role | Purpose |
| --- | --- |
| [tenant_preflight](tenant_preflight/README.md) | Validates the selected tenant before any infrastructure phase starts. |
