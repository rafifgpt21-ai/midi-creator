"""Check skill discovery, local links, source indexing, and semantic examples."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SKILLS = (
    "serum-sound-design", "serum-reference-match", "serum-synthesis",
    "serum-modulation", "serum-effects", "serum-preset-build", "serum-preset-qa",
)


def check_links(path: Path) -> list[str]:
    failures = []
    content = path.read_text(encoding="utf-8")
    for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
        target = raw.strip().strip("<>").split("#", 1)[0]
        if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.exists():
            failures.append(f"Broken link: {path}: {raw}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    root = args.root.resolve()
    errors = []
    markdown = []
    for name in SKILLS:
        folder = root / "skills" / name
        skill = folder / "SKILL.md"
        if not skill.is_file():
            errors.append(f"Missing skill: {name}")
            continue
        content = skill.read_text(encoding="utf-8")
        if not content.startswith("---\n"):
            errors.append(f"Missing frontmatter: {name}")
        else:
            frontmatter = content.split("---", 2)[1]
            if f"name: {name}\n" not in frontmatter:
                errors.append(f"Name mismatch: {name}")
            if not re.search(r"^description: .+", frontmatter, re.M):
                errors.append(f"Missing description: {name}")
        metadata = folder / "agents" / "openai.yaml"
        if not metadata.is_file():
            errors.append(f"Missing UI metadata: {name}")
        elif "$" + name not in metadata.read_text(encoding="utf-8"):
            errors.append(f"Default prompt omits invocation: {name}")
        markdown.extend(folder.rglob("*.md"))
    markdown.append(root / "docs" / "serum-sound-design" / "README.md")
    for path in markdown:
        if path.exists():
            errors.extend(check_links(path))
    index = root / "skills" / "serum-sound-design" / "references" / "index.md"
    if index.exists():
        text = index.read_text(encoding="utf-8")
        for reference in index.parent.glob("*.md"):
            if reference.name != "index.md" and reference.name not in text:
                errors.append(f"Unindexed reference: {reference.name}")
    internal = root / "docs" / "serum-sound-design" / "_internal"
    sources = json.loads((internal / "source-receipt.json").read_text(encoding="utf-8"))
    for source in sources:
        preserved = Path(source["preserved_path"])
        if not preserved.is_absolute():
            preserved = root / preserved
        if not preserved.is_file():
            errors.append(f"Missing preserved source: {preserved}")
        elif hashlib.sha256(preserved.read_bytes()).hexdigest() != source["sha256"]:
            errors.append(f"Source checksum mismatch: {preserved}")

    # Validate actual documented JSON with the pinned implementation. No preset
    # generation, plugin load, or changes to the user's sound library occur here.
    semantic = {"status": "untested", "examples": 0}
    upstream_src = root / "integrations" / "serum-mcp" / "src"
    sys.path.insert(0, str(upstream_src))
    try:
        from serum_mcp.generation.spec import PresetSpec
        from pydantic import BaseModel

        def reject_unknown(model: type[BaseModel], value: dict, location: str = "spec") -> None:
            accepted = {field.alias or name for name, field in model.model_fields.items()}
            unknown = set(value) - accepted
            if unknown:
                raise ValueError(f"{location}: unknown fields {sorted(unknown)}")
            # Explicitly validate nested objects too; default Pydantic extra-ignore
            # would otherwise accept a misspelled synthesis requirement silently.
            defs = {
                "oscillators": "OscillatorSpec", "filters": "FilterSpec",
                "envelopes": "EnvelopeSpec", "lfos": "LfoSpec", "macros": "MacroSpec",
                "fx_chain": "FxUnitSpec", "mod_routes": "ModRouteSpec",
            }
            if model is PresetSpec:
                import serum_mcp.generation.spec as spec_module
                for field, cls_name in defs.items():
                    for i, entry in enumerate(value.get(field, [])):
                        reject_unknown(getattr(spec_module, cls_name), entry, f"{field}[{i}]")
                for field, cls_name in [("global", "GlobalSpec"), ("arp", "ArpSpec"), ("voice_unison", "VoiceUnisonSpec")]:
                    if isinstance(value.get(field), dict):
                        reject_unknown(getattr(spec_module, cls_name), value[field], field)

        templates = root / "skills" / "serum-sound-design" / "references" / "templates.md"
        examples = re.findall(r"```json\n(.*?)\n```", templates.read_text(encoding="utf-8"), re.S)
        for block in examples:
            data = json.loads(block)
            if "name" in data:
                reject_unknown(PresetSpec, data)
                PresetSpec.model_validate(data)
                semantic["examples"] += 1
        # Observable schema invariants that protect the guide's common pitfalls.
        import serum_mcp.generation.spec as spec_module
        grain = spec_module.OscillatorSpec(granular_source="C:/test.wav", granular_grain_length=150)
        assert grain.granular_grain_length == 150
        lfo = spec_module.LfoSpec(rate=5, beat_sync=False, mode="Free")
        assert lfo.beat_sync is False and "beat_sync" in lfo.model_fields_set
        triangle = spec_module.LfoSpec(curve=[{"x": 0, "y": 0}, {"x": .5, "y": 1}, {"x": 1, "y": 0}])
        assert triangle.curve[1].y == 1
        # Exercise the real native-state mapper in memory, with no source assets
        # or output files. This distinguishes semantic defaults from stored state.
        from serum_mcp.preset.packer import unpack_file
        from serum_mcp.preset.mapping import apply_spec
        from serum_mcp.preset.safety import scan_wire_types
        fixture = root / "integrations" / "serum-mcp" / "fixtures" / "init_preset.SerumPreset"
        five_hz = apply_spec(unpack_file(fixture).data, PresetSpec(name="Mapper test", description="In-memory validation only", lfos=[lfo]))
        assert not scan_wire_types(five_hz)
        def find_plain(value, key):
            found = []
            if isinstance(value, dict):
                params = value.get("plainParams", {})
                if key in params:
                    found.append(params[key])
                for child in value.values():
                    found.extend(find_plain(child, key))
            elif isinstance(value, list):
                for child in value:
                    found.extend(find_plain(child, key))
            return found
        assert 5.0 in find_plain(five_hz, "kParamRate")
        assert 0.0 in find_plain(five_hz, "kParamBeatSync")
        zero_rate = apply_spec(unpack_file(fixture).data, PresetSpec(name="Zero test", description="In-memory validation only", lfos=[{"rate": 0.0, "beat_sync": False, "mode": "Free"}]))
        assert not find_plain(zero_rate, "kParamRate"), "Zero rate must follow inspected omission behavior"
        try:
            reject_unknown(PresetSpec, {"name": "Invalid", "oscillators": [{"grain_lenght": 150}]})
        except ValueError:
            pass
        else:
            errors.append("Unknown-field guard failed")
        semantic["status"] = "pass"
        semantic["invariants"] = ["grain milliseconds", "explicit false sync retained", "natural LFO y", "unknown nested keys rejected", "in-memory mapper writes free 5 Hz/sync false", "zero LFO rate omitted", "mapped plainParams wire types safe"]
    except ImportError as exc:
        errors.append(f"Run with upstream Python environment for semantic validation: {exc}")
    except Exception as exc:
        errors.append(f"Semantic validation failed: {type(exc).__name__}: {exc}")

    report = {
        "ok": not errors, "skill_count": len(SKILLS),
        "reference_count": len(list(index.parent.glob("*.md"))),
        "markdown_count": len(markdown), "semantic_validation": semantic,
        "errors": errors,
        "scope": "Skill metadata, links, source hashes and semantic specs; no plugin load or listening",
    }
    (internal / "pack-validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
