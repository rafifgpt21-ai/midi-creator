"""SMF rendering and independent checks on the bytes written to disk."""

from io import BytesIO
from pathlib import Path

import mido

from .spec import Composition, Layer, ticks


def event_track(events: list[tuple[int, int, object]], end_tick: int) -> mido.MidiTrack:
    track = mido.MidiTrack()
    previous = 0
    for absolute, _, message in sorted(events, key=lambda item: (item[0], item[1])):
        track.append(message.copy(time=absolute - previous))
        previous = absolute
    track.append(mido.MetaMessage("end_of_track", time=end_tick - previous))
    return track


def conductor(composition: Composition) -> mido.MidiTrack:
    source = composition.source
    numerator, denominator = (int(value) for value in source["time_signature"])
    events = [
        (0, 0, mido.MetaMessage("track_name", name=source["title"])),
        (0, 1, mido.MetaMessage("set_tempo", tempo=composition.tempo)),
        (0, 2, mido.MetaMessage("time_signature", numerator=numerator, denominator=denominator)),
    ]
    if "key_signature" in source:
        events.append((0, 3, mido.MetaMessage("key_signature", key=source["key_signature"])))
    for section in source.get("sections", []):
        events.append((ticks(section["start"], composition.ppqn), 4,
                       mido.MetaMessage("marker", text=section["name"])))
    return event_track(events, composition.end_tick)


def layer_track(layer: Layer, end_tick: int, *, send_program: bool = True) -> mido.MidiTrack:
    channel = layer.channel - 1
    events = [(0, 0, mido.MetaMessage("track_name", name=layer.name))]
    if send_program and layer.program is not None:
        events.append((0, 1, mido.Message("program_change", channel=channel, program=layer.program)))
    events.extend([
        (0, 2, mido.Message("control_change", channel=channel, control=7, value=layer.volume)),
        (0, 3, mido.Message("control_change", channel=channel, control=10, value=layer.pan)),
    ])
    for note in layer.notes:
        # Release before retrigger when the same pitch ends and starts on one tick.
        events.append((note.end, 4, mido.Message("note_off", channel=channel, note=note.pitch, velocity=0)))
        events.append((note.start, 5, mido.Message("note_on", channel=channel, note=note.pitch, velocity=note.velocity)))
    return event_track(events, end_tick)


def render_midi(composition: Composition, layers: tuple[Layer, ...], *, single_track: bool = False,
                legacy: bool = False) -> bytes:
    midi = mido.MidiFile(type=0 if single_track and legacy else 1, ticks_per_beat=composition.ppqn, charset="utf-8")
    if single_track:
        if len(layers) != 1:
            raise ValueError("A per-layer MIDI must contain exactly one instrument")
        metadata = conductor(composition)
        if legacy:
            metadata[0] = mido.MetaMessage("text", text=composition.source["title"], time=0)
        else:
            # Text/key/section descriptions live in README. Keep import metadata
            # on the instrument track and avoid Cubase's format-0 dissolve path.
            metadata = event_track([(0, index, message.copy(time=0)) for index, message in enumerate(metadata)
                                    if message.type in ("set_tempo", "time_signature")], composition.end_tick)
        midi.tracks.append(mido.merge_tracks([metadata, layer_track(layers[0], composition.end_tick,
                                                                   send_program=legacy)]))
    else:
        midi.tracks.append(conductor(composition))
        midi.tracks.extend(layer_track(layer, composition.end_tick) for layer in layers)
    buffer = BytesIO()
    midi.save(file=buffer)
    return buffer.getvalue()


def render_files(composition: Composition, *, combined: bool, legacy: bool = False) -> dict[str, bytes]:
    directory = "midi/layers" if legacy else "MIDI"
    result = {f"{directory}/{layer.id}.mid": render_midi(composition, (layer,), single_track=True,
                                                       legacy=legacy) for layer in composition.layers}
    if combined:
        result["midi/arrangement.mid" if legacy else "MIDI/arrangement.mid"] = render_midi(composition, composition.layers)
    return result


def inspect_midi(path: Path) -> dict:
    errors = []
    try:
        midi = mido.MidiFile(path, charset="utf-8", clip=False)
    except (OSError, ValueError, EOFError, KeyError) as exc:
        return {"ok": False, "errors": [f"Cannot parse MIDI: {exc}"]}
    if midi.type not in (0, 1):
        errors.append("Expected synchronous MIDI format 0 or 1")
    if midi.ticks_per_beat <= 0:
        errors.append("SMPTE timing is not supported; expected positive PPQN")
    tracks = []
    tempos = []
    signatures = []
    sysex_count = 0
    for index, track in enumerate(midi.tracks):
        absolute = 0
        active = {}
        notes = []
        channels = set()
        programs = []
        end_markers = 0
        peak_polyphony = 0
        for message in track:
            if not isinstance(message.time, int) or message.time < 0:
                errors.append(f"Track {index}: invalid delta time")
            absolute += message.time
            if message.type == "end_of_track":
                end_markers += 1
            elif message.type == "set_tempo":
                tempos.append({"tick": absolute, "microseconds_per_quarter": message.tempo})
            elif message.type == "time_signature":
                signatures.append({"tick": absolute, "numerator": message.numerator, "denominator": message.denominator})
            elif message.type == "program_change":
                programs.append({"channel": message.channel + 1, "program": message.program})
            elif message.type == "sysex":
                sysex_count += 1
            if not message.is_meta and hasattr(message, "channel"):
                channels.add(message.channel + 1)
            if message.type in ("note_on", "note_off"):
                key = message.channel, message.note
                if message.type == "note_on" and message.velocity > 0:
                    if key in active:
                        errors.append(f"Track {index}: overlapping pitch {message.note} at tick {absolute}")
                    active[key] = absolute
                    notes.append(message.note)
                    peak_polyphony = max(peak_polyphony, len(active))
                elif key not in active:
                    errors.append(f"Track {index}: unmatched note-off for pitch {message.note} at tick {absolute}")
                else:
                    if absolute <= active[key]:
                        errors.append(f"Track {index}: non-positive note duration for pitch {message.note}")
                    del active[key]
        if active:
            errors.append(f"Track {index}: {len(active)} notes still active at end")
        if end_markers != 1 or not track or track[-1].type != "end_of_track":
            errors.append(f"Track {index}: expected exactly one final end_of_track")
        tracks.append({
            "index": index, "name": track.name, "end_tick": absolute,
            "note_count": len(notes), "channels": sorted(channels), "programs": programs,
            "pitch_min": min(notes) if notes else None,
            "pitch_max": max(notes) if notes else None,
            "peak_polyphony": peak_polyphony,
        })
    if not tracks:
        errors.append("MIDI has no tracks")
    if any(item["microseconds_per_quarter"] <= 0 for item in tempos):
        errors.append("Invalid explicit tempo")
    return {
        "ok": not errors, "errors": errors, "format": midi.type,
        "ticks_per_beat": midi.ticks_per_beat, "tracks": tracks,
        "note_count": sum(track["note_count"] for track in tracks),
        "end_tick": max((track["end_tick"] for track in tracks), default=0),
        "tempos": tempos, "time_signatures": signatures,
        "sysex_count": sysex_count,
        "warnings": [] if tempos else ["No explicit tempo; standard MIDI default is 500000 microseconds per quarter"],
    }


def check_rendered(path: Path, composition: Composition, layers: tuple[Layer, ...], *, single_track: bool = False,
                   legacy: bool = False) -> dict:
    report = inspect_midi(path)
    errors = report["errors"]
    if "tracks" not in report:
        return report
    expected_format = 0 if single_track and legacy else 1
    expected_tracks = 1 if single_track else len(layers) + 1
    if report["format"] != expected_format or len(report["tracks"]) != expected_tracks:
        errors.append("Unexpected MIDI format or track count")
    if report["ticks_per_beat"] != composition.ppqn:
        errors.append("PPQN differs from the composition")
    if any(track["end_tick"] != composition.end_tick for track in report["tracks"]):
        errors.append("Track length differs from the shared composition timeline")
    if report["note_count"] != sum(len(layer.notes) for layer in layers):
        errors.append("Note count differs from the composition")
    if report["tempos"] != [{"tick": 0, "microseconds_per_quarter": composition.tempo}]:
        errors.append("Tempo differs from the composition")
    numerator, denominator = composition.source["time_signature"]
    if report["time_signatures"] != [{"tick": 0, "numerator": numerator, "denominator": denominator}]:
        errors.append("Time signature differs from the composition")
    instrument_tracks = report["tracks"] if single_track else report["tracks"][1:]
    for track, layer in zip(instrument_tracks, layers):
        if track["name"] != layer.name:
            errors.append(f"{layer.id}: unexpected track name")
        if track["channels"] != [layer.channel] or track["note_count"] != len(layer.notes):
            errors.append(f"{layer.id}: unexpected channel or note count")
        expected_programs = [] if layer.program is None or single_track and not legacy else [{"channel": layer.channel, "program": layer.program}]
        if track["programs"] != expected_programs:
            errors.append(f"{layer.id}: unexpected program")
    if report["sysex_count"]:
        errors.append("Unexpected SysEx in generated MIDI")
    report["ok"] = not errors
    return report
