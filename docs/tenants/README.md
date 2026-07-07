# Tenant Index

[Documentation index](../README.md) | [New tenant guide](new-tenant.md) | [Variables](../variables.md)

Tenant files are the source of truth for tenant-local IDs, VLANs, CIDRs, storage identity, API key references, and platform overrides. Keep real secrets outside the public repository.

| Tenant                            | Type    | Access                                                                 | NFS                 | Tenant directory                                  |
| --------------------------------- | ------- | ---------------------------------------------------------------------- | ------------------- | ------------------------------------------------- |
| [`ahorn`](ahorn.md)               | virtual | 445 / 172.16.175/24                                                    | 446 / 172.16.176/24 | [directory](../../tenants/ahorn/README.md)        |
| [`belchen`](belchen.md)           | -       | 211 / 172.17.11/24                                                     | 210 / 172.17.10/24  | [directory](../../tenants/belchen/README.md)      |
| [`birke`](birke.md)               | virtual | 420 / 172.16.150/24                                                    | 421 / 172.16.151/24 | [directory](../../tenants/birke/README.md)        |
| [`dataspace`](dataspace.md)       | -       | 102 / 172.16.8/23                                                      | 103 / 172.16.10/24  | [directory](../../tenants/dataspace/README.md)    |
| [`douglasie`](douglasie.md)       | virtual | 305 / 172.16.35/24                                                     | 306 / 172.16.36/24  | [directory](../../tenants/douglasie/README.md)    |
| [`eberesche`](eberesche.md)       | virtual | 310 / 172.16.40/24                                                     | 311 / 172.16.41/24  | [directory](../../tenants/eberesche/README.md)    |
| [`edelkastanie`](edelkastanie.md) | virtual | 350 / 172.16.80/24                                                     | 351 / 172.16.81/24  | [directory](../../tenants/edelkastanie/README.md) |
| [`edeltanne`](edeltanne.md)       | virtual | 390 / 172.16.120/24                                                    | 391 / 172.16.121/24 | [directory](../../tenants/edeltanne/README.md)    |
| [`eibe`](eibe.md)                 | virtual | 335 / 172.16.65/24                                                     | 336 / 172.16.66/24  | [directory](../../tenants/eibe/README.md)         |
| [`elsbeere`](elsbeere.md)         | virtual | 320 / 172.16.50/24                                                     | 321 / 172.16.51/24  | [directory](../../tenants/elsbeere/README.md)     |
| [`feldahorn`](feldahorn.md)       | virtual | 380 / 172.16.110/24                                                    | 381 / 172.16.111/24 | [directory](../../tenants/feldahorn/README.md)    |
| [`fichte`](fichte.md)             | virtual | 400 / 172.16.130/24                                                    | 401 / 172.16.131/24 | [directory](../../tenants/fichte/README.md)       |
| [`gpusystem`](gpusystem.md)       | -       | 204 / 172.17.4/24                                                      | 203 / 172.17.3/24   | [directory](../../tenants/gpusystem/README.md)    |
| [`hainbuche`](hainbuche.md)       | virtual | 330 / 172.16.60/24                                                     | 331 / 172.16.61/24  | [directory](../../tenants/hainbuche/README.md)    |
| [`harvester`](harvester.md)       | -       | 102 / 172.16.8/23                                                      | 103 / 172.16.10/24  | [directory](../../tenants/harvester/README.md)    |
| [`haselnuss`](haselnuss.md)       | virtual | 405 / 172.16.135/24                                                    | 406 / 172.16.136/24 | [directory](../../tenants/haselnuss/README.md)    |
| [`kastanie`](kastanie.md)         | virtual | 450 / 172.16.180/24                                                    | 451 / 172.16.181/24 | [directory](../../tenants/kastanie/README.md)     |
| [`laerche`](laerche.md)           | virtual | 435 / 172.16.165/24                                                    | 436 / 172.16.166/24 | [directory](../../tenants/laerche/README.md)      |
| [`robinie`](robinie.md)           | virtual | 300 / 172.16.30/24                                                     | 301 / 172.16.31/24  | [directory](../../tenants/robinie/README.md)      |
| [`rosskastanie`](rosskastanie.md) | virtual | 355 / 172.16.85/24                                                     | 356 / 172.16.86/24  | [directory](../../tenants/rosskastanie/README.md) |
| [`rotbuche`](rotbuche.md)         | virtual | 365 / 172.16.95/24                                                     | 366 / 172.16.96/24  | [directory](../../tenants/rotbuche/README.md)     |
| [`schwarzdorn`](schwarzdorn.md)   | virtual | 440 / 172.16.170/24                                                    | 441 / 172.16.171/24 | [directory](../../tenants/schwarzdorn/README.md)  |
| [`schwarzerle`](schwarzerle.md)   | virtual | 385 / 172.16.115/24                                                    | 386 / 172.16.116/24 | [directory](../../tenants/schwarzerle/README.md)  |
| [`seebuck`](seebuck.md)           | -       | 220 / 172.17.20/24                                                     | 217 / 172.17.17/24  | [directory](../../tenants/seebuck/README.md)      |
| [`silberweide`](silberweide.md)   | virtual | 395 / 172.16.125/24                                                    | 396 / 172.16.126/24 | [directory](../../tenants/silberweide/README.md)  |
| [`sommerlinde`](sommerlinde.md)   | virtual | 370 / 172.16.100/24                                                    | 371 / 172.16.101/24 | [directory](../../tenants/sommerlinde/README.md)  |
| [`speierling`](speierling.md)     | virtual | 325 / 172.16.55/24                                                     | 326 / 172.16.56/24  | [directory](../../tenants/speierling/README.md)   |
| [`stechpalme`](stechpalme.md)     | virtual | 410 / 172.16.140/24                                                    | 411 / 172.16.141/24 | [directory](../../tenants/stechpalme/README.md)   |
| [`stieleiche`](stieleiche.md)     | virtual | 425 / 172.16.155/24                                                    | 426 / 172.16.156/24 | [directory](../../tenants/stieleiche/README.md)   |
| [`test01`](test01.md)             | -       | 3304 / 172.18.4/24                                                     | 3303 / 172.18.3/24  | [directory](../../tenants/test01/README.md)       |
| [`vogelkirsche`](vogelkirsche.md) | virtual | {{ t_ib_vlan_id }} / {{ t_ib_network_prefix }}/{{ t_ib_network_mask }} | 376 / 172.16.106/24 | [directory](../../tenants/vogelkirsche/README.md) |
| [`wacholder`](wacholder.md)       | virtual | 360 / 172.16.90/24                                                     | 361 / 172.16.91/24  | [directory](../../tenants/wacholder/README.md)    |
| [`waldkiefer`](waldkiefer.md)     | virtual | 345 / 172.16.75/24                                                     | 346 / 172.16.76/24  | [directory](../../tenants/waldkiefer/README.md)   |
| [`walnuss`](walnuss.md)           | virtual | 315 / 172.16.45/24                                                     | 316 / 172.16.46/24  | [directory](../../tenants/walnuss/README.md)      |
| [`weissdorn`](weissdorn.md)       | virtual | 415 / 172.16.145/24                                                    | 416 / 172.16.146/24 | [directory](../../tenants/weissdorn/README.md)    |
| [`winterlinde`](winterlinde.md)   | virtual | {{ t_ib_vlan_id }} / {{ t_ib_network_prefix }}/{{ t_ib_network_mask }} | 341 / 172.16.71/24  | [directory](../../tenants/winterlinde/README.md)  |
| [`zirbe`](zirbe.md)               | virtual | 430 / 172.16.160/24                                                    | 431 / 172.16.161/24 | [directory](../../tenants/zirbe/README.md)        |
