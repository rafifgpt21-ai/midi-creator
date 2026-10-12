"""Local setup, sound preparation, and connection diagnostics."""

import argparse
import json
from pathlib import Path
import sys

from midi_creator.spec import load_json
from .config import StudioError, defaults, load_config, save_json
from .serum import run_serum
from .service import Studio
from .session import prepare_session, verify_session


def parser():
    result = argparse.ArgumentParser(prog="midi-studio", description="Prepare Serum/Cubase sessions and run the local MCP server")
    result.add_argument("--config", type=Path)
    commands = result.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a local configuration and MCP client snippets")
    init.add_argument("--workspace", type=Path, default=Path.cwd())
    doctor = commands.add_parser("doctor", help="Inspect assets and MIDI ports; optionally request a Cubase handshake")
    doctor.add_argument("--live", action="store_true")
    commands.add_parser("install-remote", help="Install the MIDI Creator driver; existing differing scripts are backed up")
    samples = commands.add_parser("samples", help="Find drum one-shots in configured roots")
    samples.add_argument("--query", default="")
    samples.add_argument("--limit", type=int, default=100)
    drums = commands.add_parser("configure-drums", help="Set sample folders and an explicit pitch-to-sample map")
    drums.add_argument("--root", type=Path, action="append", required=True)
    drums.add_argument("--map", type=Path)
    inspect = commands.add_parser("serum-parameters", help="Inspect actual plugin parameter names and values")
    inspect.add_argument("--query", default="")
    inspect.add_argument("--limit", type=int, default=50)
    preset = commands.add_parser("preset", help="Create and reopen a real Serum VST3 preset")
    preset.add_argument("--profile", choices=["bass", "lead", "pluck", "pad", "brass", "keys"], default="lead")
    preset.add_argument("--parameters", type=Path)
    preset.add_argument("--base-preset")
    preset.add_argument("--out", required=True)
    prepare = commands.add_parser("prepare", help="Publish verified MIDI, Serum presets, drum samples, and aligned audio")
    prepare.add_argument("spec")
    prepare.add_argument("--out", required=True)
    prepare.add_argument("--bindings", type=Path)
    prepare.add_argument("--no-audio", action="store_true")
    verify = commands.add_parser("verify", help="Check the studio bundle inventory, MIDI, and stem alignment")
    verify.add_argument("folder")
    commands.add_parser("mcp", help="Run the MCP server over stdio (no TCP listener)")
    return result


def init_workspace(path: Path, workspace: Path):
    workspace = workspace.resolve()
    if path.exists():
        raise StudioError(f"Configuration already exists: {path}")
    save_json(path, defaults(workspace))
    client = {"mcpServers": {"midi-studio": {"command": sys.executable,
               "args": ["-m", "midi_creator.studio.mcp_server", "--config", str(path.resolve())],
               "env": {"MIDI_STUDIO_CONFIG": str(path.resolve())}}}}
    folder = workspace / "integrations"
    folder.mkdir(exist_ok=True)
    if not (folder / "mcp.local.json").exists():
        save_json(folder / "mcp.local.json", client)
    return {"ok": True, "config": str(path.resolve()), "mcp_client_config": str(folder / "mcp.local.json")}


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "init":
            result = init_workspace(args.config or args.workspace / "studio.local.json", args.workspace)
        elif args.command == "mcp":
            from .mcp_server import run
            run(args.config)
            return 0
        else:
            config = load_config(args.config)
            studio = Studio(config)
            if args.command == "doctor":
                result = studio.doctor(live=args.live)
            elif args.command == "install-remote":
                result = studio.install_remote()
            elif args.command == "samples":
                result = studio.sample_catalog(args.query, args.limit)
            elif args.command == "configure-drums":
                result = studio.configure_drums([str(root) for root in args.root], load_json(args.map) if args.map else None)
            elif args.command == "serum-parameters":
                result = run_serum(config, "inspect", query=args.query, limit=args.limit)
            elif args.command == "preset":
                result = studio.create_preset(args.out, args.profile, load_json(args.parameters) if args.parameters else None,
                                              args.base_preset)
            elif args.command == "prepare":
                result = prepare_session(config, args.spec, args.out,
                                         load_json(args.bindings) if args.bindings else None,
                                         render_audio=not args.no_audio)
            else:
                result = verify_session(config.artifact(args.folder, must_exist=True))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == "doctor" and args.live:
            return 0 if result["ok"] and result["cubase"].get("connected") else 1
        return 0 if result.get("ok") else 1
    except (StudioError, OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
