"""Publish a Cubase starter bundle only after its MIDI and sound assets pass checks."""

from importlib.resources import files
import json
from pathlib import Path
import shutil
import tempfile

from pedalboard.io import AudioFile

from midi_creator.export import digest, generate_export, json_bytes, verify_export
from midi_creator.spec import compile_composition, load_json
from .config import StudioConfig, StudioError
from .drums import approved_sample, render_drums, sample_info
from .serum import run_serum


def recipes() -> dict:
    return json.loads(files(__package__).joinpath("recipes.json").read_text(encoding="utf-8"))["profiles"]


def infer_profile(layer) -> str:
    role = (layer.get("role", "") + " " + layer["id"]).lower()
    if "bass" in role:
        return "bass"
    if "brass" in role:
        return "brass"
    if "keys" in role or "bell" in role:
        return "keys"
    if any(x in role for x in ("pluck", "arp", "keys", "piano")):
        return "pluck"
    if any(x in role for x in ("pad", "harmony", "chord", "texture")):
        return "pad"
    return "lead"


def _relative_receipt(value, stage: Path):
    if isinstance(value, dict):
        return {key: _relative_receipt(item, stage) for key, item in value.items()}
    if isinstance(value, list):
        return [_relative_receipt(item, stage) for item in value]
    if isinstance(value, str):
        path = Path(value)
        if path.is_absolute() and path.is_relative_to(stage):
            return path.relative_to(stage).as_posix()
    return value


def prepare_session(config: StudioConfig, spec_path: str, output: str,
                    bindings: dict[str, str] | None = None, *, render_audio: bool = True,
                    sample_rate: int = 48000) -> dict:
    source_path = config.artifact(spec_path, must_exist=True)
    composition = compile_composition(load_json(source_path), strict_timing=True)
    destination = config.artifact(output)
    if destination.exists():
        raise StudioError(f"Output already exists; use a new revision: {destination}")
    if type(sample_rate) is not int or sample_rate not in (44100, 48000, 96000):
        raise StudioError("Supported session sample rates: 44100, 48000, 96000")
    bindings = bindings or {}
    ids = {layer.id for layer in composition.layers if layer.kind == "melodic"}
    if not isinstance(bindings, dict) or set(bindings) - ids or any(not isinstance(x, str) for x in bindings.values()):
        raise StudioError("Bindings must map melodic layer IDs to a profile or workspace .vstpreset")
    profiles = recipes()
    plan = []
    for source_layer, layer in zip(composition.source["layers"], composition.layers):
        if layer.kind == "melodic":
            chosen = bindings.get(layer.id, infer_profile(source_layer))
            if chosen in profiles:
                plan.append((layer, chosen, profiles[chosen]["parameters"], None))
            else:
                preset = config.artifact(chosen, must_exist=True)
                if preset.suffix.lower() != ".vstpreset":
                    raise StudioError("Custom Serum bindings must reference .vstpreset files")
                plan.append((layer, "custom", {}, preset))
    needed = {note.pitch for layer in composition.layers if layer.kind == "drums" for note in layer.notes}
    mapping = config.data["drum_samples"]
    if needed - {int(pitch) for pitch in mapping}:
        raise StudioError(f"Configure drum samples for MIDI pitches: {sorted(needed - {int(p) for p in mapping})}")
    samples = {pitch: approved_sample(config, mapping[str(pitch)]) for pitch in needed}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".studio-session-", dir=destination.parent) as temporary:
        stage = Path(temporary) / "session"
        generate_export(source_path, stage)
        (stage / "Presets").mkdir()
        (stage / "Audio").mkdir()
        (stage / "Drums").mkdir()
        tracks, items = [], []
        for layer, profile, parameters, base in plan:
            midi = stage / "MIDI" / f"{layer.id}.mid"
            preset = stage / "Presets" / f"{layer.id}.vstpreset"
            preview = stage / "Audio" / f"{layer.id}.wav"
            item = {"output": str(preset), "parameters": parameters}
            if base:
                item["base_preset"] = str(base)
            if render_audio:
                item.update(midi=str(midi), preview=str(preview))
            items.append(item)
            tracks.append({"id": layer.id, "name": layer.name, "instrument": config.data["serum_plugin_name"],
                           "profile": profile, "preset": f"Presets/{layer.id}.vstpreset",
                           "parameters": parameters, "midi": f"MIDI/{layer.id}.mid",
                           "audio": f"Audio/{layer.id}.wav" if render_audio else None,
                           "volume_cc": layer.volume, "pan_cc": layer.pan})
        serum_result = run_serum(config, "build", items=items, sample_rate=sample_rate) if items else None
        copied = {}
        kit = []
        for pitch, sample in sorted(samples.items()):
            target = stage / "Drums" / f"{pitch}-{sample.name}"
            shutil.copy2(sample, target)
            copied[pitch] = target
            kit.append({"pitch": pitch, "file": target.relative_to(stage).as_posix(),
                        "source": str(sample), "sha256": digest(target.read_bytes()), **sample_info(sample)})
        (stage / "_internal/drum-kit.json").write_bytes(json_bytes({"version": 1, "samples": kit}))
        (stage / "Drums/kit.sfz").write_text("\n".join(
            f"<region> sample={copied[pitch].name} key={pitch} loop_mode=one_shot" for pitch in sorted(copied)) + "\n",
            encoding="utf-8")
        drum_results = []
        for layer in composition.layers:
            if layer.kind != "drums":
                continue
            if render_audio:
                drum_results.append(render_drums(composition, layer, copied, stage / "Audio" / f"{layer.id}.wav", sample_rate))
            tracks.append({"id": layer.id, "name": layer.name, "instrument": "Drum samples / Groove Agent SE",
                           "midi": f"MIDI/{layer.id}.mid",
                           "audio": f"Audio/{layer.id}.wav" if render_audio else None,
                           "pitches": sorted({note.pitch for note in layer.notes})})
        by_id = {track["id"]: track for track in tracks}
        tracks = [by_id[layer.id] for layer in composition.layers]
        metadata = {"version": 2, "title": composition.source["title"],
                    "tempo_bpm": composition.source["tempo_bpm"],
                    "time_signature": composition.source["time_signature"], "bars": composition.source["bars"],
                    "sample_rate": sample_rate, "audio_frames": round(composition.seconds * sample_rate),
                    "tracks": tracks, "render_audio": render_audio,
                    "serum_receipt": _relative_receipt(serum_result, stage),
                    "drum_receipts": _relative_receipt(drum_results, stage),
                    "cubase_project_created": False, "audio_auditioned": False,
                    "template_project": config.data["template_project"]}
        (stage / "_internal/session.json").write_bytes(json_bytes(metadata))
        lines = [f"# {metadata['title']}: Cubase starter", "",
                 f"{metadata['tempo_bpm']} BPM | {metadata['time_signature'][0]}/{metadata['time_signature'][1]} | {metadata['bars']} bars", "",
                 "1. Create a separate Cubase project. Set its sample rate, tempo, and meter to the values above.",
                 "2. In MediaBay, browse this bundle's Presets folder and create an instrument track from each Serum VST preset.",
                 "3. Import each matching MIDI onto that instrument track at bar 1. Keep the leading silence.",
                 "4. For drums, load the copied samples into Groove Agent SE pads using the pitch numbers listed below; import audio stems at bar 1 only if included.",
                 "5. Save the result as a new .cpr and optionally use File > Save as Template for future sessions.", "",
                 "| Track | Instrument | Preset | MIDI | Audio |", "| --- | --- | --- | --- | --- |"]
        for track in tracks:
            label = track["name"].replace("|", "\\|").replace("\n", " ").replace("\r", " ")
            preset = f"[preset]({track['preset']})" if track.get("preset") else "kit/sample drum"
            audio = f"[stem]({track['audio']})" if track["audio"] else "-"
            lines.append(f"| {label} | {track['instrument']} | {preset} | [MIDI]({track['midi']}) | {audio} |")
        lines.extend(["", "## Drum", "", "This bundle uses the explicitly configured kit. MIDI pitch mapping:", "",
                      "| Pitch | Sample |", "| --- | --- |"])
        for entry in kit:
            lines.append(f"| {entry['pitch']} | [{Path(entry['file']).name}]({entry['file']}) |")
        lines.extend(["", "Choose kick/snare/hat length and character to fit the arrangement and leave room for the bass.",
                      "## Instruments outside Serum", "",
                      "Melodic tracks use Serum 2. Drums use the copied one-shots: load them in Groove Agent SE "
                      "and assign the pitches above, or use Drums/kit.sfz in an SFZ-compatible sampler.", "",
                      "Serum state reload and MIDI structure are verified. " +
                      ("Audio was rendered, not listened to." if render_audio else "No audio was rendered or listened to."),
                      "Separate drum MIDI layers have independent CC7/10 settings: use separate sampler tracks, or filter those controllers and mix per pad in a shared kit.",
                      "The .vstpreset files are Cubase/VST3 presets, not Serum's proprietary .SerumPreset format.",
                      "Per-layer MIDI has no Program Change; select the intended Serum preset before importing.",
                      "Rendered stems stop at the composition end; leave silence in the specification when a long release is wanted.",
                      "Using MIDI and its rendered audio together doubles that part: choose one playback source per track."])
        (stage / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        inventory = [{"path": path.relative_to(stage).as_posix(), "sha256": digest(path.read_bytes())}
                     for path in sorted(stage.rglob("*")) if path.is_file()]
        (stage / "_internal/studio-manifest.json").write_bytes(json_bytes({"version": 2, "files": inventory}))
        result = verify_session(stage)
        if not result["ok"]:
            raise StudioError(f"Session verification failed: {result['errors']}")
        (stage / "_internal/verification.json").write_bytes(json_bytes(result))
        if destination.exists():
            raise StudioError("Destination was created while preparing the session")
        stage.rename(destination)
    return {"ok": True, "output": str(destination), "tracks": len(tracks), "verification": result,
            "cubase_project_created": False}


def verify_session(folder: Path) -> dict:
    internal = folder / "_internal" if (folder / "_internal/session.json").is_file() else folder
    session, manifest = load_json(internal / "session.json"), load_json(internal / "studio-manifest.json")
    if session.get("version") not in (1, 2) or manifest.get("version") != session.get("version"):
        raise StudioError("Unsupported studio bundle")
    errors = []
    actual = {path.relative_to(folder).as_posix() for path in folder.rglob("*") if path.is_file()}
    entries = manifest.get("files", [])
    inventory = {entry["path"]: entry["sha256"] for entry in entries}
    exclusions = {path.relative_to(folder).as_posix() for path in
                  (internal / "studio-manifest.json", internal / "verification.json")}
    if len(inventory) != len(entries) or actual - exclusions != set(inventory):
        errors.append("Session file inventory differs")
    for relative, checksum in inventory.items():
        path = (folder / relative).resolve()
        if not path.is_relative_to(folder.resolve()) or not path.is_file():
            errors.append(f"Missing or unsafe session artifact: {relative}")
        elif digest(path.read_bytes()) != checksum:
            errors.append(f"Session checksum mismatch: {relative}")
    midi = verify_export(folder / "performance" if session["version"] == 1 else folder)
    errors.extend(midi["errors"])
    for track in session["tracks"]:
        if not track.get("audio"):
            continue
        path = (folder / track["audio"]).resolve()
        if not path.is_relative_to(folder.resolve()) or not path.is_file():
            errors.append(f"Missing or unsafe audio stem: {track['id']}")
            continue
        with AudioFile(str(path)) as stream:
            if stream.frames != session["audio_frames"] or stream.samplerate != session["sample_rate"] or stream.num_channels != 2:
                errors.append(f"Audio stem alignment mismatch: {track['id']}")
    return {"ok": not errors, "errors": errors, "midi_ok": midi["ok"],
            "tracks": len(session["tracks"]), "cubase_project_verified": False, "audio_auditioned": False}
