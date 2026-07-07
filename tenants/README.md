# Tenants

[Framework README](../README.md) | [Tenant docs](../docs/tenants/README.md) | [New tenant guide](../docs/tenants/new-tenant.md)

Each first-level tenant directory contains a `vars.yml` file and optional assets such as manifests, airgap links, or tenant helper files. The tenant vars file is the source of truth for that tenant.

| Tenant         | Type    | State   | Access                                                                 | NFS                 | README                           |
| -------------- | ------- | ------- | ---------------------------------------------------------------------- | ------------------- | -------------------------------- |
| `ahorn`        | virtual | present | 445 / 172.16.175/24                                                    | 446 / 172.16.176/24 | [README](ahorn/README.md)        |
| `belchen`      | -       | present | 211 / 172.17.11/24                                                     | 210 / 172.17.10/24  | [README](belchen/README.md)      |
| `birke`        | virtual | present | 420 / 172.16.150/24                                                    | 421 / 172.16.151/24 | [README](birke/README.md)        |
| `dataspace`    | -       | present | 102 / 172.16.8/23                                                      | 103 / 172.16.10/24  | [README](dataspace/README.md)    |
| `douglasie`    | virtual | present | 305 / 172.16.35/24                                                     | 306 / 172.16.36/24  | [README](douglasie/README.md)    |
| `eberesche`    | virtual | present | 310 / 172.16.40/24                                                     | 311 / 172.16.41/24  | [README](eberesche/README.md)    |
| `edelkastanie` | virtual | present | 350 / 172.16.80/24                                                     | 351 / 172.16.81/24  | [README](edelkastanie/README.md) |
| `edeltanne`    | virtual | present | 390 / 172.16.120/24                                                    | 391 / 172.16.121/24 | [README](edeltanne/README.md)    |
| `eibe`         | virtual | present | 335 / 172.16.65/24                                                     | 336 / 172.16.66/24  | [README](eibe/README.md)         |
| `elsbeere`     | virtual | present | 320 / 172.16.50/24                                                     | 321 / 172.16.51/24  | [README](elsbeere/README.md)     |
| `feldahorn`    | virtual | present | 380 / 172.16.110/24                                                    | 381 / 172.16.111/24 | [README](feldahorn/README.md)    |
| `fichte`       | virtual | present | 400 / 172.16.130/24                                                    | 401 / 172.16.131/24 | [README](fichte/README.md)       |
| `gpusystem`    | -       | present | 204 / 172.17.4/24                                                      | 203 / 172.17.3/24   | [README](gpusystem/README.md)    |
| `hainbuche`    | virtual | present | 330 / 172.16.60/24                                                     | 331 / 172.16.61/24  | [README](hainbuche/README.md)    |
| `harvester`    | -       | present | 102 / 172.16.8/23                                                      | 103 / 172.16.10/24  | [README](harvester/README.md)    |
| `haselnuss`    | virtual | present | 405 / 172.16.135/24                                                    | 406 / 172.16.136/24 | [README](haselnuss/README.md)    |
| `kastanie`     | virtual | present | 450 / 172.16.180/24                                                    | 451 / 172.16.181/24 | [README](kastanie/README.md)     |
| `laerche`      | virtual | present | 435 / 172.16.165/24                                                    | 436 / 172.16.166/24 | [README](laerche/README.md)      |
| `robinie`      | virtual | present | 300 / 172.16.30/24                                                     | 301 / 172.16.31/24  | [README](robinie/README.md)      |
| `rosskastanie` | virtual | present | 355 / 172.16.85/24                                                     | 356 / 172.16.86/24  | [README](rosskastanie/README.md) |
| `rotbuche`     | virtual | present | 365 / 172.16.95/24                                                     | 366 / 172.16.96/24  | [README](rotbuche/README.md)     |
| `schwarzdorn`  | virtual | present | 440 / 172.16.170/24                                                    | 441 / 172.16.171/24 | [README](schwarzdorn/README.md)  |
| `schwarzerle`  | virtual | present | 385 / 172.16.115/24                                                    | 386 / 172.16.116/24 | [README](schwarzerle/README.md)  |
| `seebuck`      | -       | present | 220 / 172.17.20/24                                                     | 217 / 172.17.17/24  | [README](seebuck/README.md)      |
| `silberweide`  | virtual | present | 395 / 172.16.125/24                                                    | 396 / 172.16.126/24 | [README](silberweide/README.md)  |
| `sommerlinde`  | virtual | present | 370 / 172.16.100/24                                                    | 371 / 172.16.101/24 | [README](sommerlinde/README.md)  |
| `speierling`   | virtual | present | 325 / 172.16.55/24                                                     | 326 / 172.16.56/24  | [README](speierling/README.md)   |
| `stechpalme`   | virtual | present | 410 / 172.16.140/24                                                    | 411 / 172.16.141/24 | [README](stechpalme/README.md)   |
| `stieleiche`   | virtual | present | 425 / 172.16.155/24                                                    | 426 / 172.16.156/24 | [README](stieleiche/README.md)   |
| `test01`       | -       | present | 3304 / 172.18.4/24                                                     | 3303 / 172.18.3/24  | [README](test01/README.md)       |
| `vogelkirsche` | virtual | present | {{ t_ib_vlan_id }} / {{ t_ib_network_prefix }}/{{ t_ib_network_mask }} | 376 / 172.16.106/24 | [README](vogelkirsche/README.md) |
| `wacholder`    | virtual | present | 360 / 172.16.90/24                                                     | 361 / 172.16.91/24  | [README](wacholder/README.md)    |
| `waldkiefer`   | virtual | present | 345 / 172.16.75/24                                                     | 346 / 172.16.76/24  | [README](waldkiefer/README.md)   |
| `walnuss`      | virtual | present | 315 / 172.16.45/24                                                     | 316 / 172.16.46/24  | [README](walnuss/README.md)      |
| `weissdorn`    | virtual | present | 415 / 172.16.145/24                                                    | 416 / 172.16.146/24 | [README](weissdorn/README.md)    |
| `winterlinde`  | virtual | present | {{ t_ib_vlan_id }} / {{ t_ib_network_prefix }}/{{ t_ib_network_mask }} | 341 / 172.16.71/24  | [README](winterlinde/README.md)  |
| `zirbe`        | virtual | present | 430 / 172.16.160/24                                                    | 431 / 172.16.161/24 | [README](zirbe/README.md)        |
