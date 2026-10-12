"""The same studio operations serve the CLI and MCP clients."""

from importlib.resources import files
import json
from pathlib import Path
import re
import shutil
import tempfile

import mido

from midi_creator.export import digest, json_bytes
from .bridge import CubaseBridge
from .config import StudioConfig, StudioError, save_json
from .drums import approved_sample, catalog
from .serum import run_serum
from .session import recipes


class Studio:
    def __init__(self, config: StudioConfig):
        self.config = config
        self.cubase = CubaseBridge(config)

    def doctor(self, *, live: bool = False) -> dict:
        plugin = Path(self.config.data["serum_plugin"])
        metadata_path = plugin / "Contents/Resources/moduleinfo.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.is_file() else {}
        inputs, outputs = mido.get_input_names(), mido.get_output_names()
        ports = (self.config.data["midi_request_output"] in outputs and
                 self.config.data["midi_response_input"] in inputs)
        missing_samples = [path for path in self.config.data["drum_samples"].values() if not Path(path).is_file()]
        ready = plugin.exists() and not missing_samples
        return {"ok": ready, "ready_to_prepare": ready, "workspace": str(self.config.workspace),
                "serum": {"path": str(plugin), "installed": plugin.exists(), "version": metadata.get("Version")},
                "midi": {"inputs": inputs, "outputs": outputs, "configured_ports_available": ports},
                "drum_roots": self.config.data["drum_roots"], "drum_pitches": sorted(self.config.data["drum_samples"]),
                "missing_samples": missing_samples,
                "cubase": self.cubase.status() if live else {"connected": None, "tested": False},
                "capabilities": {"midi_generation": True, "serum_vstpreset_creation": "requires plugin worker check",
                                 "drum_sample_stems": True, "live_control": "requires Cubase handshake",
                                 "native_project_creation": False, "native_preset_loading": False}}

    def configure_drums(self, roots: list[str], samples: dict[str, str] | None = None) -> dict:
        if not roots or any(not Path(root).is_dir() for root in roots):
            raise StudioError("Provide existing drum sample folders")
        if samples is None:
            samples = self.config.data["drum_samples"]
        if not isinstance(samples, dict) or any(not isinstance(p, str) or not p.isdigit() or not 0 <= int(p) <= 127
                                              or not isinstance(s, str) for p, s in samples.items()):
            raise StudioError("Map MIDI pitches 0..127 to sample paths")
        candidate = StudioConfig(self.config.path, {**self.config.data, "drum_roots": [str(Path(x).resolve()) for x in roots],
                                                    "drum_samples": samples})
        for sample in samples.values():
            approved_sample(candidate, sample)
        save_json(candidate.path, candidate.data)
        self.config = candidate
        self.cubase = CubaseBridge(candidate)
        return {"ok": True, "roots": candidate.data["drum_roots"], "samples": samples}

    def sample_catalog(self, query: str = "", limit: int = 100) -> dict:
        return catalog(self.config, query=query, limit=limit)

    def preset_catalog(self, query: str = "", limit: int = 100) -> dict:
        if not 1 <= limit <= 1000:
            raise StudioError("Preset catalog limit must be 1..1000")
        root = Path(self.config.data["serum_presets"]).resolve()
        if not root.is_dir():
            raise StudioError(f"Serum preset folder does not exist: {root}")
        rows, total = [], 0
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() not in (".serumpreset", ".fxp", ".vstpreset") or not path.is_file():
                continue
            if not path.resolve().is_relative_to(root) or query.lower() not in path.name.lower():
                continue
            total += 1
            if len(rows) < limit:
                rows.append({"path": str(path), "format": path.suffix,
                             "offline_load_supported": path.suffix.lower() == ".vstpreset"})
        return {"ok": True, "presets": rows, "total_matches": total,
                "note": "Serum-native .SerumPreset/.fxp files are browsable; load through Serum UI, not this offline VST3 loader"}

    def create_preset(self, output: str, profile: str = "lead", parameters: dict | None = None,
                      base_preset: str | None = None) -> dict:
        profiles = recipes()
        if profile not in profiles:
            raise StudioError(f"Choose a profile: {', '.join(profiles)}")
        parameters = parameters or {}
        if not isinstance(parameters, dict):
            raise StudioError("Parameters must be an object")
        values = {**profiles[profile]["parameters"], **parameters}
        destination = self.config.artifact(output)
        if destination.exists():
            raise StudioError("Preset folder already exists; choose a new revision")
        base = self.config.artifact(base_preset, must_exist=True) if base_preset else None
        if base and base.suffix.lower() != ".vstpreset":
            raise StudioError("The base preset must be a workspace .vstpreset")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".studio-preset-", dir=destination.parent) as temporary:
            stage = Path(temporary) / "preset"
            stage.mkdir()
            item = {"output": str(stage / "preset.vstpreset"), "parameters": values}
            if base:
                item["base_preset"] = str(base)
            receipt = run_serum(self.config, "build", items=[item])
            receipt["presets"][0]["file"] = "preset.vstpreset"
            receipt.update(profile=profile, requested_parameters=values, base_preset=str(base) if base else None,
                           sha256=digest((stage / "preset.vstpreset").read_bytes()))
            (stage / "recipe.json").write_bytes(json_bytes(receipt))
            stage.rename(destination)
        return {"ok": True, "output": str(destination), "preset": str(destination / "preset.vstpreset"),
                "round_trip_verified": True}

    def install_remote(self) -> dict:
        root = Path(self.config.data["cubase_driver_scripts"])
        destination = root / "MIDI Creator/Studio Bridge/MIDI Creator_Studio Bridge.js"
        source = files(__package__).joinpath("cubase_remote.js").read_text(encoding="utf-8")
        for placeholder, key in (("__INPUT_MATCH__", "cubase_input_match"), ("__OUTPUT_MATCH__", "cubase_output_match")):
            escaped = json.dumps(self.config.data[key], ensure_ascii=True)[1:-1].replace("'", "\\'")
            source = source.replace(placeholder, escaped)
        info = Path(self.config.data["serum_plugin"]) / "Contents/Resources/moduleinfo.json"
        if not info.is_file():
            raise StudioError("Serum moduleinfo.json is required to discover the instrument class UID")
        metadata = json.loads(info.read_text(encoding="utf-8"))
        classes = [c for c in metadata.get("Classes", []) if c.get("Category") == "Audio Module Class"
                   and c.get("Name") == self.config.data["serum_plugin_name"]]
        if len(classes) != 1 or not re.fullmatch(r"[A-Fa-f0-9]{32}", classes[0].get("CID", "")):
            raise StudioError("Unable to uniquely discover the Serum instrument class UID")
        source = source.replace("__SERUM_UID__", classes[0]["CID"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and destination.read_text(encoding="utf-8") != source:
            backup = destination.with_suffix(".js.backup")
            if backup.exists():
                raise StudioError(f"Existing remote backup must be preserved: {backup}")
            shutil.copy2(destination, backup)
        destination.write_text(source, encoding="utf-8")
        return {"ok": True, "script": str(destination), "serum_uid": classes[0]["CID"],
                "live_connected": None, "connection_checked": False,
                "next_step": "In Cubase MIDI Remote, enable Scripting Tools, Reload Scripts, and activate Studio Bridge. "
                             "Use the configured LoopBe port for both input and output. Exclude it from All MIDI Inputs and "
                             "from musical track outputs. Run midi-studio doctor --live."}
