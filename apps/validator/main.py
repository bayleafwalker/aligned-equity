from __future__ import annotations

import sys
from pathlib import Path

from aligned_equity.validation import validate_repository


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    errors = validate_repository(repo_root)
    if errors:
        for error in errors:
            print(f"validation error: {error}", file=sys.stderr)
        return 1
    print("repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
