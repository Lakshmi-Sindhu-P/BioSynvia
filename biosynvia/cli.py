"""Local command-line entry point; no network access or external services."""

import argparse
import json
from pathlib import Path
import sys

from .audit import audit
from .source import inventory_archive
import zipfile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BioSynvia offline data audit")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("audit", help="Validate two canonical CSV tables")
    check.add_argument("--sensors", type=Path, required=True)
    check.add_argument("--measurements", type=Path, required=True)
    check.add_argument("--output", type=Path, required=True, help="New JSON file; existing files are protected")
    inventory = commands.add_parser("inventory", help="Verify publisher checksum and list source ZIP members")
    inventory.add_argument("--archive", type=Path, required=True)
    inventory.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        inputs = [args.archive] if args.command == "inventory" else [args.sensors, args.measurements]
        if args.output.resolve() in [path.resolve() for path in inputs]:
            raise ValueError("Output must differ from input paths.")
        if args.output.exists():
            raise ValueError("Output already exists; choose a new filename.")
        report = (inventory_archive(args.archive) if args.command == "inventory"
                  else audit(args.sensors, args.measurements))
        serialized = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(serialized)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"Command could not run: {exc}", file=sys.stderr)
        return 1
    if args.command == "inventory":
        print(f"Publisher checksum verified. Inventoried {len(report['files'])} files.")
        print(f"Report: {args.output}; {len(report['warnings'])} structure warnings.")
        return 2 if report["warnings"] else 0
    status = "PASSED" if report["valid"] else "FAILED"
    print(f"Data checks {status}: {len(report['errors'])} errors, {len(report['warnings'])} warnings.")
    print(f"Report: {args.output}")
    print("This checks the provisional data contract, not scientific validity.")
    return 0 if report["valid"] else 2
