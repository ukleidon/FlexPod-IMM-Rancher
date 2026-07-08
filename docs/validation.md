# Validation

[Documentation index](README.md) | [Workflows](workflows.md) | [Operations](operations.md) | [Playbooks](playbooks.md)

Validation is the safety gate for this framework. Always start with syntax checks and check mode before making live changes.

## Execution Environment

Run this once on a new or rebuilt control host to install the collections used by the current roles:

```bash
ansible-galaxy collection install cisco.intersight cisco.nxos netapp.ontap community.vmware kubernetes.core
```

If a collection is already pinned by the control-host image, keep the locally approved version. The playbook validation below confirms whether the installed modules can be loaded.

Harvester and Rancher Kubernetes operations also need the Python Kubernetes client in the interpreter selected by `harvester_ansible_python_interpreter`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-python.txt
```

## Publication Check

Run this before staging or pushing to GitHub:

```bash
./scripts/publication_check.py
```

Expected result: no literal API keys, private key files, passwords, or token values are detected.

## Framework Health

```bash
ansible-playbook -i inventory INFRA.yml --syntax-check
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory RKE2.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 --syntax-check
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 --syntax-check
```

Expected result: playbooks parse cleanly. Tenant or platform playbooks can warn about empty host groups when the selected inventory has no matching hosts.

## Tenant Present Path

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -C
```

Expected result: Nexus, ONTAP, Intersight, OS install, RKE2, and Trident sections either validate or skip safely depending on inventory and check-mode guards.

## Tenant Absent Path

```bash
ansible-playbook -i inventory TENANT.yml -e tenant=tenant01 -e lan_state=absent -C
```

Expected result: the selected tenant removal path validates without requiring another tenant file.

## Harvester Tenant Path

```bash
ansible-playbook -i inventory HARVESTER.yml -e tenant=tenant01 -C
```

Expected result: the control node can use the Harvester kube context, load the selected tenant vars, read the `sle-micro-default` cloud-init ConfigMap, and validate namespace, NetworkAttachmentDefinition, DHCP IPPool, and tenant cloud-init intent.

## Rancher-Provisioned Virtual RKE2 Path

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 -C
```

Expected result: with private Rancher and Harvester values supplied, the role discovers or uses a Harvester image, resolves tenant cloud-init user data, and validates Rancher `HarvesterConfig` plus `provisioning.cattle.io/v1 Cluster` objects for `<tenant>-rke`.

Public defaults intentionally contain placeholders such as `REPLACE_ME_RANCHER_CREATOR_ID`. Syntax checks can run with placeholders; live check mode against Rancher needs private overrides.

## Optional Workload Add-On Path

```bash
ansible-playbook -i inventory HARVESTER_RKE.yml -e tenant=tenant01 \
  --tags workload_cluster -e harvester_workload_apply=true -C
```

Expected result: the role skips safely when the downstream kubeconfig context `<tenant>-rke` is absent. When present, it validates kube-vip, storage annotations, Trident PSA RBAC, optional Kasten, and extra tenant manifests.

## YAML and Documentation

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in list(Path('group_vars').rglob('*.yml')) + list(Path('tenants').rglob('*.yml')):
    yaml.safe_load(path.read_text())
print('YAML parse OK')
PY
```

Expected result: all variable files parse as YAML.

## Documentation and Mermaid Check

```bash
grep -RIn "```mermaid" docs
grep -RIn "REPLACE_ME\\|CHANGE_ME" docs roles group_vars tenants | head
```

Expected result: documentation contains renderable Mermaid blocks and public placeholders are visible where live values must be supplied privately.
