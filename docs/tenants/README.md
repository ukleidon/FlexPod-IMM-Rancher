# Tenant Index

[Documentation index](../README.md) | [New tenant guide](new-tenant.md) | [Variables](../variables.md)

Tenant files are the source of truth for tenant-local IDs, VLANs, CIDRs, storage identity, API key references, and platform overrides. Keep real secrets outside the public repository.

| Tenant                      | Type | Access             | NFS                | Tenant directory                               |
| --------------------------- | ---- | ------------------ | ------------------ | ---------------------------------------------- |
| [`ac01`](ac01.md)           | -    | 1112 / 10.111.2/24 | 1113 / 10.111.3/24 | [directory](../../tenants/ac01/README.md)      |
| [`harvester`](harvester.md) | -    | 1042 / 10.104.2/24 | 1047 / 10.104.7/24 | [directory](../../tenants/harvester/README.md) |
| [`test01`](test01.md)       | -    | 304 / 172.18.4/24  | 303 / 172.18.3/24  | [directory](../../tenants/test01/README.md)    |
