"""Local device settings; artifact writes stay inside the configured workspace."""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import tempfile

from midi_creator.spec import load_json


class StudioError(ValueError):
    pass


def documents_folder() -> Path:
    # Windows redirects Documents to OneDrive on many studio machines.
    if os.name == "nt":
        import ctypes
        buffer = ctypes.create_unicode_buffer(32768)
        if ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buffer) == 0:
            return Path(buffer.value)
    return Path.home() / "Documents"


def defaults(workspace: Path) -> dict:
    documents = documents_folder()
    return {
        "version": 1, "workspace": str(workspace.resolve()),
        "serum_plugin": "C:/Program Files/Common Files/VST3/Serum2.vst3",
        "serum_plugin_name": "Serum 2",
        "serum_presets": str(documents / "Xfer/Serum 2 Presets/Presets"),
        "cubase_driver_scripts": str(documents / "Steinberg/Cubase/MIDI Remote/Driver Scripts/Local"),
        "midi_request_output": "LoopBe Internal MIDI 1",
        "midi_response_input": "LoopBe Internal MIDI 0",
        "cubase_input_match": "LoopBe Internal MIDI",
        "cubase_output_match": "LoopBe Internal MIDI",
        "drum_roots": [], "drum_samples": {},
        "template_project": None,
    }


def save_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Atomic configuration updates; no half-written file if an agent is interrupted.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     delete=False, suffix=".tmp") as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


@dataclass(frozen=True)
class StudioConfig:
    path: Path
    data: dict

    @property
    def workspace(self) -> Path:
        return Path(self.data["workspace"]).resolve()

    def artifact(self, value: str | Path, *, must_exist: bool = False) -> Path:
        result = Path(value)
        if not result.is_absolute():
            result = self.workspace / result
        result = result.resolve()
        if not result.is_relative_to(self.workspace):
            raise StudioError(f"Artifact must be inside workspace: {result}")
        if must_exist and not result.exists():
            raise StudioError(f"Missing artifact: {result}")
        return result


def load_config(path: Path | None = None) -> StudioConfig:
    path = (path or Path(os.environ.get("MIDI_STUDIO_CONFIG", "studio.local.json"))).resolve()
    if not path.is_file():
        raise StudioError(f"Missing configuration {path}; run midi-studio init first")
    data = load_json(path)
    allowed = set(defaults(path.parent))
    if not isinstance(data, dict) or data.get("version") != 1 or set(data) != allowed:
        raise StudioError("Unsupported studio configuration; compare with studio.example.json")
    for key in ("workspace", "serum_plugin", "serum_plugin_name", "serum_presets",
                "cubase_driver_scripts", "midi_request_output", "midi_response_input",
                "cubase_input_match", "cubase_output_match"):
        if not isinstance(data[key], str) or not data[key].strip():
            raise StudioError(f"{key} must be a nonempty string")
    if not isinstance(data["drum_roots"], list) or any(not isinstance(x, str) for x in data["drum_roots"]):
        raise StudioError("drum_roots must be a list of folder paths")
    if not isinstance(data["drum_samples"], dict):
        raise StudioError("drum_samples must map MIDI pitches to sample paths")
    for key, value in data["drum_samples"].items():
        if not key.isdigit() or not 0 <= int(key) <= 127 or not isinstance(value, str):
            raise StudioError("drum_samples must map MIDI pitches 0..127 to sample paths")
    if data["template_project"] is not None and not isinstance(data["template_project"], str):
        raise StudioError("template_project must be null or a .cpr path")
    return StudioConfig(path, data)


def plugin_binary(path: Path) -> Path:
    if path.is_dir() and path.suffix.lower() == ".vst3":
        candidates = list((path / "Contents/x86_64-win").glob("*.vst3"))
        if len(candidates) == 1:
            return candidates[0]
    return path
