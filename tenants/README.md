# Tenants

[Framework README](../README.md) | [Tenant docs](../docs/tenants/README.md) | [New tenant guide](../docs/tenants/new-tenant.md)

Each first-level tenant directory contains a `vars.yml` file and optional assets such as manifests, airgap links, or tenant helper files. The tenant vars file is the source of truth for that tenant.

| Tenant      | Type | State   | Access             | NFS                | README                        |
| ----------- | ---- | ------- | ------------------ | ------------------ | ----------------------------- |
| `ac01`      | -    | present | 1112 / 10.111.2/24 | 1113 / 10.111.3/24 | [README](ac01/README.md)      |
| `harvester` | -    | present | 1042 / 10.104.2/24 | 1047 / 10.104.7/24 | [README](harvester/README.md) |
| `test01`    | -    | present | 304 / 172.18.4/24  | 303 / 172.18.3/24  | [README](test01/README.md)    |
