from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from aligned_equity.research_case import build_research_case_packet, render_research_case_markdown


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and render a bounded, source-linked research case."
    )
    parser.add_argument("case_file", type=Path, help="JSON case bundle")
    parser.add_argument("--output", type=Path, help="write Markdown here instead of stdout")
    args = parser.parse_args(argv)

    try:
        bundle = json.loads(args.case_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read case bundle: {exc}", file=sys.stderr)
        return 2
    packet, errors = build_research_case_packet(bundle)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    markdown = render_research_case_markdown(packet)
    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
