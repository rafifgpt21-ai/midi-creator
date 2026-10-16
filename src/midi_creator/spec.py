"""Parse the composition contract and resolve all timing before writing files."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from importlib.resources import files
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator


class CompositionError(ValueError):
    """A composition or deliverable violates the project contract."""


@dataclass(frozen=True)
class Note:
    pitch: int
    start: int
    end: int
    velocity: int


@dataclass(frozen=True)
class ControlChange:
    start: int
    control: int
    value: int


@dataclass(frozen=True)
class Layer:
    id: str
    name: str
    kind: str
    channel: int  # Human-facing channels: 1..16.
    program: int | None
    volume: int
    pan: int
    notes: tuple[Note, ...]
    control_changes: tuple[ControlChange, ...] = ()


@dataclass(frozen=True)
class Composition:
    source: dict
    ppqn: int
    end_tick: int
    tempo: int
    layers: tuple[Layer, ...]

    @property
    def seconds(self) -> float:
        return self.end_tick / self.ppqn * self.tempo / 1_000_000


def schema() -> dict:
    return json.loads(files("midi_creator").joinpath("composition.schema.json").read_text(encoding="utf-8"))


def load_json(path: Path) -> dict:
    def reject_constant(value):
        raise CompositionError(f"Non-finite JSON number: {value}")

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise CompositionError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        return json.loads(path.read_text(encoding="utf-8-sig"), parse_constant=reject_constant,
                          object_pairs_hook=unique_keys)
    except (OSError, ValueError) as exc:
        raise CompositionError(f"Cannot read {path}: {exc}") from exc


def decimal(value) -> Decimal:
    result = Decimal(str(value))
    if not result.is_finite():
        raise CompositionError("All timing values must be finite")
    return result


def ticks(value, ppqn: int) -> int:
    return int((decimal(value) * ppqn).to_integral_value(rounding=ROUND_HALF_UP))


def pitch_number(value: str | int) -> int:
    if isinstance(value, (int, float)) and not isinstance(value, bool) and decimal(value) == int(value):
        number = int(value)
    else:
        match = re.fullmatch(r"([A-Ga-g])([#b]?)(-?\d+)", str(value))
        if not match:
            raise CompositionError(f"Invalid pitch: {value!r}")
        letter, accidental, octave = match.groups()
        number = (int(octave) + 1) * 12 + {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[letter.upper()]
        number += {"": 0, "#": 1, "b": -1}[accidental]
    if not 0 <= number <= 127:
        raise CompositionError(f"Pitch outside MIDI 0..127: {value!r}")
    return number


def check_overlaps(notes: list[Note] | tuple[Note, ...], label: str) -> None:
    last_end = {}
    for note in sorted(notes, key=lambda n: (n.start, n.end, n.pitch)):
        if note.start < last_end.get(note.pitch, -1):
            raise CompositionError(f"{label}: overlapping pitch {note.pitch} at tick {note.start}")
        last_end[note.pitch] = note.end


def compile_composition(source: dict, *, combined: bool = False, strict_timing: bool = False) -> Composition:
    errors = sorted(Draft202012Validator(schema()).iter_errors(source), key=lambda e: str(e.json_path))
    if errors:
        error = errors[0]
        raise CompositionError(f"{error.json_path}: {error.message}")
    ppqn = int(source.get("ticks_per_beat", 480))
    numerator, denominator = (int(value) for value in source["time_signature"])
    total = decimal(source["bars"]) * numerator * 4 / denominator
    end_tick = ticks(total, ppqn)
    if end_tick <= 0 or end_tick > 0x0FFFFFFF:
        raise CompositionError("Composition duration exceeds the supported MIDI tick range")
    for section in source.get("sections", []):
        if decimal(section["start"]) >= total:
            raise CompositionError(f"Section {section['name']!r} must start before the end")

    melodic = [layer for layer in source["layers"] if layer["kind"] == "melodic"]
    explicit = [int(layer["channel"]) for layer in melodic if "channel" in layer]
    if combined and len(explicit) != len(set(explicit)):
        raise CompositionError("Combined melodic layers need distinct channels")
    available = [channel for channel in range(1, 17) if channel != 10 and channel not in explicit]
    layer_ids = set()
    layers = []
    for raw in source["layers"]:
        identifier = raw["id"]
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", identifier):
            raise CompositionError(f"Invalid layer filename: {identifier!r}")
        if identifier in layer_ids:
            raise CompositionError(f"Duplicate layer id: {identifier}")
        # These basenames are reserved by Windows even when an extension is added.
        if identifier in {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}:
            raise CompositionError(f"Reserved filename for layer id: {identifier}")
        layer_ids.add(identifier)
        if raw["kind"] == "drums":
            channel = 10
        elif "channel" in raw:
            channel = int(raw["channel"])
        elif not combined:
            channel = 1
        elif available:
            channel = available.pop(0)
        else:
            raise CompositionError("A combined MIDI supports 15 melodic channels; generate without --combined for more layers")

        notes = []

        def add_note(event: dict, offset: Decimal = Decimal(0)) -> None:
            start = offset + decimal(event["start"])
            end = start + decimal(event["duration"])
            if end > total:
                raise CompositionError(f"{identifier}: note ends at beat {end}, beyond {total}")
            begin_tick, finish_tick = ticks(start, ppqn), ticks(end, ppqn)
            if finish_tick <= begin_tick:
                raise CompositionError(f"{identifier}: note duration rounds to zero ticks; increase ticks_per_beat")
            notes.append(Note(pitch_number(event["pitch"]), begin_tick, finish_tick, int(event.get("velocity", 90))))
            if len(notes) > 1_000_000:
                raise CompositionError(f"{identifier}: exceeds the one-million-note limit")

        for event in raw.get("notes", []):
            add_note(event)
        for clip in raw.get("clips", []):
            for iteration in range(int(clip.get("repeat", 1))):
                offset = decimal(clip["start"]) + iteration * decimal(clip.get("every", 0))
                for event in clip["notes"]:
                    add_note(event, offset)
        check_overlaps(notes, identifier)
        controls = []
        control_ticks = set()
        for event in raw.get("control_changes", []):
            if decimal(event["start"]) > total:
                raise CompositionError(f"{identifier}: control change beyond composition end")
            tick = ticks(event["start"], ppqn)
            control = int(event["control"])
            if (tick, control) in control_ticks:
                raise CompositionError(f"{identifier}: duplicate controller {control} at tick {tick}")
            control_ticks.add((tick, control))
            controls.append(ControlChange(tick, control, int(event["value"])))
        program = int(raw["program"]) if "program" in raw else None
        layers.append(Layer(identifier, raw["name"], raw["kind"], channel, program,
                            int(raw.get("volume", 100)), int(raw.get("pan", 64)),
                            tuple(sorted(notes, key=lambda n: (n.start, n.pitch, n.end, n.velocity))),
                            tuple(sorted(controls, key=lambda c: (c.start, c.control)))))

    drums = [layer for layer in layers if layer.kind == "drums"]
    if combined and len(drums) > 1:
        if len({layer.control_changes for layer in drums}) > 1:
            raise CompositionError("Combined drum layers share channel 10: use the same control automation or generate without --combined")
        if len({(layer.volume, layer.pan) for layer in drums}) > 1:
            raise CompositionError("Combined drum layers share channel 10: use the same volume/pan or generate without --combined")
        check_overlaps([note for layer in drums for note in layer.notes], "Combined drum layers")
    tempo = int((Decimal(60_000_000) / decimal(source["tempo_bpm"])).to_integral_value(rounding=ROUND_HALF_UP))
    composition = Composition(source, ppqn, end_tick, tempo, tuple(layers))
    mode = source.get('timing', {}).get('mode')
    if mode == 'strict' or strict_timing and mode != 'free':
        from .timing import require_grid
        require_grid(composition)
    return composition
