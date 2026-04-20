#!/usr/bin/env python3
"""Hermes wrapper for the shared local Flow2API client."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


SHARED_CLIENT = Path("/home/linkaka/.codex/skills/flow2api-generate/scripts/flow2api_client.py")


def main() -> int:
    if not SHARED_CLIENT.exists():
        print(
            f"shared Flow2API client not found: {SHARED_CLIENT}",
            file=sys.stderr,
        )
        return 1
    os.environ.setdefault("FLOW2API_BASE_URL", "http://127.0.0.1:38000")
    runpy.run_path(str(SHARED_CLIENT), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
