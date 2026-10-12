"""Small CLI used by humans and agents with the same composition contract."""

import argparse
import json
from pathlib import Path
import sys

from .export import generate_export, verify_export
from .midi import inspect_midi
from .spec import CompositionError, compile_composition, load_json, schema
from .timing import timing_report


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="midi-creator", description="Generate synchronized MIDI files from composition JSON.")
    commands = result.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Check schema, note ranges, timing, overlaps, and channel allocation")
    validate.add_argument("spec", type=Path)
    validate.add_argument("--combined", action="store_true", help="Also check channel constraints for an optional combined MIDI")
    generate = commands.add_parser("generate", help="Write per-layer MIDI, optional combined MIDI, manifest, and validation")
    generate.add_argument("spec", type=Path)
    generate.add_argument("--out", type=Path, help="New output directory (default: output next to the spec)")
    generate.add_argument("--combined", action="store_true", help="Also write an optional multitrack arrangement MIDI")
    verify = commands.add_parser("verify", help="Reopen an export and compare MIDI bytes and structure against its snapshot")
    verify.add_argument("folder", type=Path)
    inspect = commands.add_parser("inspect", help="Report MIDI tracks, timing, channels, notes, and structural errors")
    inspect.add_argument("midi", type=Path)
    commands.add_parser("schema", help="Print the authoritative composition JSON schema")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "schema":
            print(json.dumps(schema(), ensure_ascii=False, indent=2))
            return 0
        if args.command == "validate":
            composition = compile_composition(load_json(args.spec), combined=args.combined, strict_timing=True)
            result = {"ok": True, "layers": len(composition.layers), "end_tick": composition.end_tick,
                      "duration_seconds": composition.seconds,
                      "note_count": sum(len(layer.notes) for layer in composition.layers),
                      "timing": timing_report(composition)}
        elif args.command == "generate":
            result = generate_export(args.spec, args.out or args.spec.parent / "output", combined=args.combined)
            print(f"Created: {result['output']}")
            print(f"Layers: {len(result['manifest']['layers'])} | Validation: PASS")
            for entry in result["manifest"]["files"]:
                print(entry["path"])
            return 0
        elif args.command == "verify":
            result = verify_export(args.folder)
        else:
            result = inspect_midi(args.midi)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    except (CompositionError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
