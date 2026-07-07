#!/usr/bin/env python3
"""Regenerate the public-safe architecture overview page."""

from __future__ import annotations

from generate_public_docs import generate_architecture
from pathlib import Path
import sys


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    generate_architecture(root.resolve())


if __name__ == "__main__":
    main()
