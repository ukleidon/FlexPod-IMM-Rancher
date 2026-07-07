# Validation

[Documentation index](README.md) | [Operations](operations.md) | [Playbooks](playbooks.md)

Validation is the safety gate for this framework. Always start with syntax checks and check mode before making live changes.

## Execution Environment

Run this once on a new or rebuilt control host to install the collections used by the current roles:

```bash
ansible-galaxy collection install cisco.intersight cisco.nxos netapp.ontap community.vmware
```

If a collection is already pinned by the control-host image, keep the locally approved version. The playbook validation below confirms whether the installed modules can be loaded.

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
