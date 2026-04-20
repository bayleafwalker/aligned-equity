from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    hla_root = Path("/projects/dev/homelab-analytics")
    if not hla_root.exists():
        print("homelab-analytics not found; skipping HLA manifest loader check")
        return 0
    hla_python = hla_root / ".venv/bin/python"
    if hla_python.exists():
        return _run_with_hla_python(repo_root, hla_root, hla_python)

    sys.path.insert(0, str(hla_root))
    try:
        from packages.shared.external_registry import load_extension_registry_manifest
    except Exception as exc:
        print(
            "homelab-analytics manifest loader unavailable in current environment; "
            f"skipping HLA loader check: {exc}"
        )
        return 0

    manifest = load_extension_registry_manifest(repo_root)
    print(
        "HLA manifest loader accepted "
        f"{manifest.display_name or 'aligned-equity'} with modules "
        f"{', '.join(manifest.extension_modules)}"
    )
    return 0


def _run_with_hla_python(repo_root: Path, hla_root: Path, hla_python: Path) -> int:
    script = """
from pathlib import Path
import sys

repo_root = Path(sys.argv[1])
hla_root = Path(sys.argv[2])
sys.path.insert(0, str(hla_root))
from packages.shared.external_registry import load_extension_registry_manifest

manifest = load_extension_registry_manifest(repo_root)
print(
    "HLA manifest loader accepted "
    f"{manifest.display_name or 'aligned-equity'} with modules "
    f"{', '.join(manifest.extension_modules)}"
)
""".strip()
    completed = subprocess.run(
        [str(hla_python), "-c", script, str(repo_root), str(hla_root)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.stdout.strip():
        print(completed.stdout.strip())
    if completed.returncode != 0:
        if completed.stderr.strip():
            print(completed.stderr.strip(), file=sys.stderr)
        return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
