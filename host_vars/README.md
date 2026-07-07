# Host Variables

[Documentation index](../docs/README.md) | [Variables](../docs/variables.md)

`host_vars/` contains device-specific topology, interface, and platform values for inventory hosts. The public documentation intentionally uses neutral device labels instead of site hostnames.

| Public label | Configuration to expect |
| --- | --- |
| `nexus-a.yml` / `nexus-b.yml` | vPC peer settings, physical interface lists, port-channel members, base SVI addressing logic. |
| `storage-controller-a.yml` / `storage-controller-b.yml` | ONTAP node, aggregate, SVM, LIF, and platform-specific values. |
| `san-fabric-a.yml` / `san-fabric-b.yml` | VSAN, zoning, device alias, and SAN interface values when FC roles are used. |

Keep live management addresses, site names, and device hostnames in private deployment documentation.
