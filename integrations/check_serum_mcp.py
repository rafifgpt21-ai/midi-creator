"""Check the upstream Serum MCP connection and optionally generate a new native preset.

Run from the workspace with the upstream environment:
integrations/serum-mcp/.venv/Scripts/python.exe integrations/check_serum_mcp.py --out <new-folder>
"""

import argparse
import asyncio
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def contains(actual, expected):
    """Compare requested values, allowing serialized float precision and extra defaults."""
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and contains(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) >= len(expected) and all(
            contains(actual[index], value) for index, value in enumerate(expected))
    if type(expected) in (int, float) and type(actual) in (int, float):
        return math.isclose(actual, expected, rel_tol=1e-5, abs_tol=1e-5)
    return actual == expected


async def check(args):
    workspace = Path(__file__).resolve().parents[1]
    repo = workspace / "integrations" / "serum-mcp"
    config = json.loads((workspace / "studio.local.json").read_text(encoding="utf-8"))
    root = Path(config["serum_presets"]).parent
    presets = root / "Presets" / "User"
    if not presets.is_dir():
        raise ValueError(f"Missing Serum User folder: {presets}")
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    env = {"SERUM_PRESETS_PATH": str(presets), "SERUM_TABLES_PATH": str(root / "Tables"),
           "SERUM_SAMPLES_PATH": str(root / "Samples")}
    if config.get("drum_roots"):
        env["SAMPLE_BANK_PATH"] = config["drum_roots"][0]
    params = StdioServerParameters(command=str(repo / ".venv" / "Scripts" / "python.exe"),
                                  args=["-m", "serum_mcp.server"], cwd=str(repo), env=env)
    receipt = {"ok": False, "checked_at": datetime.now(timezone.utc).isoformat(),
               "repository": "https://github.com/Celian-mrc/serum-mcp",
               "commit": subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                                  text=True).strip(),
               "plugin_loaded": False, "audio_rendered": False, "auditioned": False}
    try:
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=60)) as client:
                initialized = await client.initialize()
                available = await client.list_tools()
                receipt["server"] = initialized.serverInfo.model_dump()
                receipt["tools"] = sorted(tool.name for tool in available.tools)
                save(output / "tool-schemas.json", [tool.model_dump() for tool in available.tools])

                async def call(name, arguments):
                    result = await client.call_tool(name, arguments)
                    if result.isError:
                        raise RuntimeError(f"{name}: {result.content}")
                    return "\n".join(block.text for block in result.content if block.type == "text")

                schema = json.loads(await call("list_parameters", {}))
                save(output / "parameters.json", schema)
                references = json.loads(await call("find_reference_presets", {"query": args.query, "limit": 3}))
                save(output / "references.json", references)
                if args.reference:
                    description = await call("describe_preset", {"preset_path": str(args.reference.resolve())})
                    (output / "reference-description.txt").write_text(description, encoding="utf-8")
                if args.spec:
                    from serum_mcp.generation.spec import PresetSpec
                    from serum_mcp.preset.introspect import extract_spec
                    from serum_mcp.preset.packer import unpack_file
                    from serum_mcp.tools._naming import sanitize_subfolder, slugify_preset_name

                    raw = json.loads(args.spec.read_text(encoding="utf-8"))
                    spec = PresetSpec.model_validate(raw)
                    bank = args.subfolder or f"MIDI Creator/{output.name}"
                    target = presets / sanitize_subfolder(bank) / (slugify_preset_name(spec.name) + ".SerumPreset")
                    if target.exists():
                        raise FileExistsError(f"Preserve existing preset: {target}")
                    result = await call("generate_preset", {"spec": raw, "subfolder": bank})
                    generated = Path(result.splitlines()[0]).resolve()
                    if generated != target.resolve():
                        raise ValueError("MCP returned an unexpected preset path")
                    description = await call("describe_preset", {"preset_path": str(generated)})
                    preset = unpack_file(generated)
                    recovered = extract_spec(preset.data)
                    actual = recovered.model_dump(by_alias=True)
                    comparisons = {}
                    for field in ("oscillators", "filters", "envelopes", "lfos", "macros", "fx_chain", "global"):
                        if field in raw:
                            comparisons[field] = contains(actual[field], raw[field])
                    comparisons["mod_routes"] = all(any(contains(route, wanted)
                        for route in actual["mod_routes"]) for wanted in raw.get("mod_routes", []))
                    comparisons["name"] = preset.metadata.get("presetName") == spec.name
                    if not all(comparisons.values()):
                        save(output / "decoded-spec.json", actual)
                        save(output / "comparison.json", comparisons)
                        raise ValueError(f"Preset readback mismatch: {comparisons}")
                    copied = output / generated.name
                    shutil.copy2(generated, copied)
                    shutil.copy2(args.spec, output / "preset-spec.json")
                    (output / "description.txt").write_text(description, encoding="utf-8")
                    save(output / "decoded-spec.json", actual)
                    receipt["preset"] = {"file": str(copied), "installed": str(generated),
                        "sha256": hashlib.sha256(copied.read_bytes()).hexdigest(),
                        "structural_readback": comparisons, "dependency_note": result.splitlines()[1:]}
                receipt["ok"] = True
    except Exception as exc:
        def messages(error):
            if isinstance(error, BaseExceptionGroup):
                return "; ".join(messages(child) for child in error.exceptions)
            return str(error)
        receipt["error"] = messages(exc)
        raise
    finally:
        save(output / "receipt.json", receipt)
        print(json.dumps(receipt, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--subfolder")
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--query", default="warm pad")
    asyncio.run(check(parser.parse_args()))


if __name__ == "__main__":
    main()
