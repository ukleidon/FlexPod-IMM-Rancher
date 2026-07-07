#!/usr/bin/env python3
"""Fail if publication-sensitive credentials are present as literal values.

Run from the repository root before staging or pushing to GitHub:

    ./scripts/publication_check.py

The check allows placeholders, empty strings, and Jinja variable references.
Real secrets belong in ignored local files, Ansible Vault, environment-backed
vars, or a private deployment overlay that is not committed.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path.cwd()
TEXT_SUFFIXES = {
    ".cfg",
    ".conf",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".txt",
    ".yaml",
    ".yml",
}
SENSITIVE_KEYS = {
    "api_key_id",
    "api_private_key",
    "authentication_password",
    "password",
    "password_for_local_user",
    "privacy_password",
    "secret",
    "t_password_for_local_user",
    "token",
    "vcenter_password",
    "vsadmin_password",
}
IGNORED_KEYWORDS = {
    "always_update_password",
    "enable_password_expiry",
    "enforce_strong_password",
    "ispasswordset",
    "password_history",
}
SECRET_PATH_RE = re.compile(
    r"(?i)(^|/)(keys?|secrets?|credentials?)(/|$)|\.(pem|p12|pfx|key)$|secretkey\.txt$"
)
PRIVATE_KEY_RE = re.compile(r"BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY")
LINE_RE = re.compile(r"^(\s*)([A-Za-z0-9_\"'-]+)(\s*:\s*)(.*?)(\s*(#.*)?)$")


def is_text_candidate(path: Path) -> bool:
    if ".git" in path.parts:
        return False
    if any(part in {"__pycache__", ".pytest_cache"} for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES or path.suffix == "" or path.name in {"inventory", "README", "ansible.cfg"}


def normalize_key(raw: str) -> str:
    return raw.strip().strip("'\"").lower()


def is_sensitive_key(key: str) -> bool:
    key = normalize_key(key)
    if key in IGNORED_KEYWORDS:
        return False
    return key in SENSITIVE_KEYS or key.endswith("_password") or key.endswith("_secret") or key.endswith("_token")


def is_safe_value(raw: str) -> bool:
    value = raw.strip().rstrip(",").strip().strip("'\"")
    if not value or value in {"null", "None", "~"}:
        return True
    upper = value.upper()
    if any(token in upper for token in ("CHANGE_ME", "REPLACE_ME", "EXAMPLE_", "YOUR_")):
        return True
    if "{{" in value and "}}" in value:
        return True
    if value.lower() in {"false", "true"}:
        return True
    return False


def main() -> int:
    problems: list[str] = []

    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        rel = path.relative_to(ROOT)
        rel_text = str(rel)
        if ".git" in path.parts:
            continue
        if SECRET_PATH_RE.search(rel_text) and not rel_text.endswith(".example"):
            problems.append(f"{rel}: sensitive file path should not be committed")
            continue
        if not is_text_candidate(path):
            continue
        text = path.read_text(errors="ignore")
        if PRIVATE_KEY_RE.search(text):
            problems.append(f"{rel}: private key block detected")
        if path.suffix.lower() == ".py":
            continue
        for nr, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = LINE_RE.match(line)
            if not match:
                continue
            key = normalize_key(match.group(2))
            value = match.group(4)
            if is_sensitive_key(key) and not is_safe_value(value):
                problems.append(f"{rel}:{nr}: literal value for sensitive key `{key}`")

    if problems:
        print("Publication check failed:")
        for problem in problems[:200]:
            print(f"- {problem}")
        if len(problems) > 200:
            print(f"- ... {len(problems) - 200} additional issue(s)")
        return 1

    print("Publication check passed: no literal keys/passwords detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
