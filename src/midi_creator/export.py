"""Produce immutable, self-contained export folders and verify them later."""

import hashlib
import json
from pathlib import Path
import tempfile

from . import __version__
from .midi import check_rendered, render_files
from .spec import CompositionError, compile_composition, load_json
from .timing import timing_report


def json_bytes(value) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_export(folder: Path) -> dict:
    internal = folder / "_internal" if (folder / "_internal/manifest.json").is_file() else folder
    manifest = load_json(internal / "manifest.json")
    if not isinstance(manifest, dict) or manifest.get("version") not in (1, 2) or type(manifest.get("combined")) is not bool:
        raise CompositionError("Unsupported or malformed export manifest")
    legacy = manifest["version"] == 1
    if not legacy and manifest.get("midi_profile") != "cubase-single-track":
        raise CompositionError("Unsupported MIDI export profile")
    source = load_json(internal / "composition.json")
    composition = compile_composition(source, combined=manifest["combined"])
    expected = render_files(composition, combined=manifest["combined"], legacy=legacy)
    entries = manifest.get("files", [])
    if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
        raise CompositionError("Malformed manifest file inventory")
    inventory = {entry.get("path"): entry.get("sha256") for entry in entries if isinstance(entry.get("path"), str)}
    if len(inventory) != len(entries) or set(inventory) != set(expected):
        raise CompositionError("Manifest file inventory differs from the composition")
    errors = []
    if manifest.get("composition_sha256") != digest((internal / "composition.json").read_bytes()):
        errors.append("Composition snapshot checksum mismatch")
    actual_midis = {path.relative_to(folder).as_posix() for path in folder.rglob("*.mid")}
    if actual_midis != set(expected):
        errors.append("MIDI files on disk differ from the expected inventory")
    reports = {}
    for relative, expected_bytes in expected.items():
        path = folder / relative  # Inventory already matched trusted, generated paths.
        is_combined = relative == ("midi/arrangement.mid" if legacy else "MIDI/arrangement.mid")
        directory = "midi/layers" if legacy else "MIDI"
        layers = composition.layers if is_combined else tuple(
            layer for layer in composition.layers if relative == f"{directory}/{layer.id}.mid")
        if not path.is_file():
            errors.append(f"Missing MIDI file: {relative}")
            continue
        actual_bytes = path.read_bytes()
        if digest(actual_bytes) != inventory[relative]:
            errors.append(f"Checksum mismatch: {relative}")
        if actual_bytes != expected_bytes:
            errors.append(f"MIDI bytes differ from the composition: {relative}")
        reports[relative] = check_rendered(path, composition, layers, single_track=not is_combined, legacy=legacy)
        if not reports[relative]["ok"]:
            errors.append(f"MIDI validation failed: {relative}")
    # Older snapshots remain verifiable, but their off-grid positions are now
    # visible separately from structural validity. Explicit strict snapshots
    # are checked by compile_composition as well.
    return {"ok": not errors, "errors": errors, "files": reports,
            "timing": timing_report(composition)}


def generate_export(source_path: Path, output: Path, *, combined: bool = False) -> dict:
    composition = compile_composition(load_json(source_path), combined=combined, strict_timing=True)
    output = output.resolve()
    if output.exists():
        raise CompositionError(f"Output already exists: {output}. Choose a new revision/output folder.")
    output.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_files(composition, combined=combined)
    snapshot = json_bytes(composition.source)
    manifest = {
        "version": 2, "midi_profile": "cubase-single-track",
        "generator": {"name": "midi-creator", "version": __version__},
        "title": composition.source["title"], "combined": combined,
        "composition_sha256": digest(snapshot),
        "tempo_bpm": composition.source["tempo_bpm"],
        "time_signature": composition.source["time_signature"],
        "bars": composition.source["bars"], "ticks_per_beat": composition.ppqn,
        "end_tick": composition.end_tick, "duration_seconds": composition.seconds,
        "layers": [{
            "id": layer.id, "name": layer.name, "kind": layer.kind,
            "channel": layer.channel, "program": layer.program,
            "note_count": len(layer.notes), "file": f"MIDI/{layer.id}.mid",
        } for layer in composition.layers],
        "files": [{"path": relative, "sha256": digest(data)} for relative, data in rendered.items()],
    }
    # Publish only after every file can be reopened and validated successfully.
    with tempfile.TemporaryDirectory(prefix=".midi-creator-", dir=output.parent) as temporary:
        stage = Path(temporary) / "export"
        stage.mkdir()
        for relative, data in rendered.items():
            path = stage / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        internal = stage / "_internal"
        internal.mkdir()
        (internal / "composition.json").write_bytes(snapshot)
        (internal / "manifest.json").write_bytes(json_bytes(manifest))
        report = verify_export(stage)
        if not report["ok"]:
            raise CompositionError(f"Export verification failed: {report['errors']}")
        (internal / "validation.json").write_bytes(json_bytes(report))
        lines = [
            f"# {composition.source['title']}", "",
            f"{composition.source['bars']} bars | {composition.source['tempo_bpm']} BPM (quarter notes) | "
            f"{composition.source['time_signature'][0]}/{composition.source['time_signature'][1]}",
            f"Duration: {composition.seconds:.3f} seconds. All layers start at tick 0 and end at {composition.end_tick}.",
            "", "| Layer | Kind | Channel | Program (0-based) | Notes | File |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for layer in composition.layers:
            label = layer.name.replace("|", "\\|").replace("\n", " ").replace("\r", " ")
            lines.append(f"| {label} | {layer.kind} | {layer.channel} | {layer.program if layer.program is not None else '-'} | "
                         f"{len(layer.notes)} | [MIDI](MIDI/{layer.id}.mid) |")
        if combined:
            lines.extend(["", "Combined: [arrangement.mid](MIDI/arrangement.mid)."])
        lines.extend(["", "Validation: PASS. Recheck with `midi-creator verify <this-folder>`.", "",
                      "MIDI stores performance data; choose instruments in your DAW to hear it."])
        (internal / "summary.md").write_text("\n".join(lines).replace(
            "](MIDI/", "](../MIDI/") + "\n", encoding="utf-8")
        from .producer import project_readme
        readme = project_readme(composition)
        if combined:
            readme += "\n## File gabungan yang diminta\n\n[Arrangement multitrack](MIDI/arrangement.mid). " \
                      "File gabungan memakai conductor track, marker/key, dan Program Change GM; " \
                      "gunakan file per-layer untuk import ke track Serum yang presetnya sudah dipilih.\n"
        (stage / "README.md").write_text(readme, encoding="utf-8")
        if output.exists():
            raise CompositionError(f"Output was created during generation: {output}")
        stage.rename(output)
    return {"output": str(output), "manifest": manifest, "validation": report}
