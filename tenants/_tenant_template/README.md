# Tenant Template

[New tenant guide](../../docs/tenants/new-tenant.md) | [Variables](../../docs/variables.md) | [Tenants](../../docs/tenants/README.md)

This directory contains a sanitized, full-shape `vars.yml` template. Prefer `scripts/create_tenant.py` for day-to-day tenant creation because it clones working tenant assets and updates the registry-owning tenant vars for virtual tenants.

Use this template when you need to build a tenant manually or compare the intended variable sections:

1. Copy the directory to `tenants/<tenant>`.
2. Set identity, lifecycle, API key references, VLAN IDs, and CIDRs.
3. Replace storage IQNs, WWPNs, LIFs, pool starts, and app-specific overrides.
4. If it is a virtual tenant, update the `vNN_*` data in the registry-owning tenant vars file.
5. Validate with the commands in the new tenant guide.
