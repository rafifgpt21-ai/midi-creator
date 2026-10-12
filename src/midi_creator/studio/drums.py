"""Read-only sample discovery and sample-accurate, aligned drum stems."""

import math
from pathlib import Path
import re

import numpy as np
from pedalboard.io import AudioFile

from midi_creator.spec import Composition, Layer
from .config import StudioConfig, StudioError

AUDIO_EXTENSIONS = {".wav", ".aif", ".aiff", ".flac"}
GM_ROLES = {36: "kick", 38: "snare", 39: "clap", 42: "closed-hat", 46: "open-hat", 49: "crash"}


def classify(path: Path) -> str | None:
    name = re.sub(r"[^a-z0-9]+", " ", str(path).lower())
    if "loop" in name.split() or "loops" in name.split():
        return None
    if "open" in name.split() and re.search(r"\b(hats?|hi ?hats?|hh)\b", name):
        return "open-hat"
    for role, pattern in (("kick", r"\bkicks?\b"), ("snare", r"\bsnares?\b"),
                          ("clap", r"\bclaps?\b"), ("closed-hat", r"\b(hats?|hi ?hats?|hh)\b"),
                          ("crash", r"\bcrash(es)?\b")):
        if re.search(pattern, name):
            return role
    return None


def catalog(config: StudioConfig, *, query: str = "", limit: int = 100) -> dict:
    if not 1 <= limit <= 1000:
        raise StudioError("Sample catalog limit must be 1..1000")
    roots = [Path(root).resolve() for root in config.data["drum_roots"]]
    missing = [str(root) for root in roots if not root.is_dir()]
    if missing:
        raise StudioError(f"Missing sample folders: {missing}")
    rows, total, counts, seen = [], 0, {}, set()
    for root in roots:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in AUDIO_EXTENSIONS:
                continue
            resolved = path.resolve()
            if not resolved.is_relative_to(root) or resolved in seen:
                continue
            seen.add(resolved)
            role = classify(path)
            if not role:
                continue
            counts[role] = counts.get(role, 0) + 1
            if query.lower() not in str(path).lower():
                continue
            total += 1
            if len(rows) < limit:
                rows.append({"path": str(path), "role": role, "bytes": path.stat().st_size})
    return {"ok": True, "total_matches": total, "role_counts": counts, "samples": rows,
            "classification": "filename heuristic; inspect duration and audition before choosing"}


def sample_info(path: Path) -> dict:
    with AudioFile(str(path)) as stream:
        return {"path": str(path), "sample_rate": stream.samplerate, "channels": stream.num_channels,
                "frames": stream.frames, "seconds": stream.frames / stream.samplerate}


def approved_sample(config: StudioConfig, value: str) -> Path:
    path = Path(value).resolve()
    if not any(path.is_relative_to(Path(root).resolve()) for root in config.data["drum_roots"]):
        raise StudioError(f"Sample must be inside a configured drum root: {path}")
    if not path.is_file() or path.suffix.lower() not in AUDIO_EXTENSIONS:
        raise StudioError(f"Unsupported or missing drum sample: {path}")
    info = sample_info(path)
    if not 0 < info["seconds"] <= 10 or not 1 <= info["channels"] <= 2:
        raise StudioError(f"Expected a mono/stereo one-shot of at most 10 seconds: {path}")
    return path


def read_sample(path: Path, sample_rate: int) -> np.ndarray:
    with AudioFile(str(path)) as stream:
        original_rate = stream.samplerate
        audio = stream.read(stream.frames)
    if not np.isfinite(audio).all():
        raise StudioError(f"Non-finite sample audio: {path}")
    if audio.shape[0] == 1:
        audio = np.repeat(audio, 2, axis=0)
    if audio.shape[0] != 2 or audio.shape[1] < 1:
        raise StudioError(f"Expected mono or stereo audio: {path}")
    if original_rate != sample_rate:
        length = max(1, round(audio.shape[1] * sample_rate / original_rate))
        positions = np.arange(length) * original_rate / sample_rate
        audio = np.array([np.interp(positions, np.arange(audio.shape[1]), channel) for channel in audio],
                         dtype=np.float32)
    return audio


def render_drums(composition: Composition, layer: Layer, samples: dict[int, Path],
                 output: Path, sample_rate: int = 48000) -> dict:
    needed = {note.pitch for note in layer.notes}
    if needed - set(samples):
        raise StudioError(f"Missing drum mapping for {layer.id}: pitches {sorted(needed - set(samples))}")
    frames = round(composition.seconds * sample_rate)
    audio = np.zeros((2, frames), dtype=np.float32)
    loaded = {pitch: read_sample(samples[pitch], sample_rate) for pitch in needed}
    pan = layer.pan / 127
    # Unity at center; reduce one side as the layer moves towards the other side.
    balance = np.array([min(1.0, math.sqrt(2 * (1 - pan))), min(1.0, math.sqrt(2 * pan))])[:, None]
    for note in layer.notes:
        start = round(note.start / composition.ppqn * composition.tempo / 1_000_000 * sample_rate)
        sample = loaded[note.pitch]
        count = min(sample.shape[1], frames - start)
        audio[:, start:start + count] += sample[:, :count] * (note.velocity / 127) * (layer.volume / 127) * balance
    # Smooth the global cutoff when a one-shot extends beyond the composition.
    fade = min(frames, round(sample_rate * 0.005))
    audio[:, -fade:] *= np.linspace(1, 0, fade)
    peak = float(np.max(np.abs(audio)))
    if peak <= 1e-7:
        raise StudioError(f"Silent drum layer: {layer.id}")
    gain = min(1.0, 0.95 / peak)
    with AudioFile(str(output), "w", sample_rate, 2, bit_depth=24) as stream:
        stream.write(audio * gain)
    return {"file": str(output), "frames": frames, "sample_rate": sample_rate,
            "source_peak": peak, "applied_gain": gain, "auditioned": False}
