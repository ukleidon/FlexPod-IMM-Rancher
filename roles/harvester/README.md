# Harvester Roles

[Framework README](../../README.md) | [Role index](../../docs/roles/README.md) | [Playbooks](../../docs/playbooks.md)

The Harvester roles manage the HCI layer that hosts virtual tenants. Use them
after the FlexPod foundation exists and before creating Rancher-provisioned
virtual RKE2 clusters.

## Roles

- [`platform_config`](platform_config/README.md) configures cluster-wide
  Harvester settings such as NTP, proxy, add-ons, and the `data-9000` storage
  network.

Platform configuration is intentionally opt-in because it affects the whole
Harvester cluster, not just one tenant.
