"""Offline Serum host. Stdout is never part of the MCP protocol."""

import json
import math
from pathlib import Path
import sys
import traceback

import mido
import numpy as np
from pedalboard import load_plugin
from pedalboard.io import AudioFile


def describe(plugin, names):
    result = {}
    for name in names:
        parameter = plugin.parameters[name]
        result[name] = {"value": str(getattr(plugin, name)), "raw": float(parameter.raw_value),
                        "label": str(parameter.label),
                        "range": repr(parameter.range), "type": str(parameter.type)}
    return result


def apply(plugin, values):
    for name, value in values.items():
        if name not in plugin.parameters:
            raise ValueError(f"Unknown Serum parameter: {name}")
        if isinstance(value, dict):
            if set(value) != {"raw"} or type(value["raw"]) not in (int, float) or not 0 <= value["raw"] <= 1:
                raise ValueError(f"{name}: normalized raw value must be in 0..1")
            plugin.parameters[name].raw_value = value["raw"]
        else:
            setattr(plugin, name, value)


def render(plugin, midi_path: Path, wav_path: Path, sample_rate: int):
    midi = mido.MidiFile(midi_path)
    clock, events, volume, pan = 0.0, [], 100, 64
    # MidiFile iteration converts delta ticks using the file's own tempo.
    for message in midi:
        clock += message.time
        if message.type in ("note_on", "note_off", "pitchwheel", "aftertouch", "polytouch"):
            events.append((message.bytes(), clock))
        elif message.type == "control_change" and message.control in (7, 10):
            if message.control == 7:
                volume = message.value
            else:
                pan = message.value
        # GM programs and CC7/10 must not replace the deliberately designed Serum sound.
    audio = plugin(events, duration=clock, sample_rate=sample_rate, num_channels=2, buffer_size=512)
    # Hosts quantize duration to frames differently. Preserve the rounded MIDI
    # timeline, including leading silence, rather than trimming to the last note.
    frames, host_frames = round(clock * sample_rate), audio.shape[1]
    if abs(host_frames - frames) > 512:
        raise ValueError("Serum host duration differs by more than one processing block")
    audio = audio[:, :frames]
    if audio.shape[1] < frames:
        audio = np.pad(audio, ((0, 0), (0, frames - audio.shape[1])))
    balance = np.array([min(1.0, math.sqrt(2 * (1 - pan / 127))),
                        min(1.0, math.sqrt(2 * pan / 127))])[:, None]
    audio *= balance * (volume / 127)
    fade = min(frames, round(sample_rate * 0.005))
    audio[:, -fade:] *= np.linspace(1, 0, fade)
    if not np.isfinite(audio).all():
        raise ValueError("Serum rendered non-finite audio")
    peak = float(np.max(np.abs(audio)))
    if peak <= 1e-7:
        raise ValueError("Serum rendered silence; check authorization and preset")
    # Keep the original measured peak in the receipt; avoid clipping the delivered audio.
    gain = min(1.0, 0.95 / peak)
    with AudioFile(str(wav_path), "w", sample_rate, 2, bit_depth=24) as stream:
        stream.write(audio * gain)
    return {"file": str(wav_path), "frames": audio.shape[1], "sample_rate": sample_rate,
            "source_peak": peak, "applied_gain": gain, "host_frames": host_frames,
            "volume_cc": volume, "pan_cc": pan, "auditioned": False}


def main():
    request = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    response = Path(sys.argv[2])
    try:
        plugin = load_plugin(request["plugin"], plugin_name=request["plugin_name"])
        if not plugin.is_instrument:
            raise ValueError("Configured Serum entry is not an instrument")
        result = {"ok": True, "plugin": plugin.name, "version": plugin.version}
        operation = request["operation"]
        if operation == "inspect":
            query = request.get("query", "").lower()
            names = request.get("names") or [name for name in plugin.parameters if query in name]
            result["parameters"] = describe(plugin, names[:request.get("limit", 100)])
            result["total_matches"] = len(names)
        elif operation == "build":
            initial = plugin.preset_data
            result["presets"] = []
            for item in request["items"]:
                plugin.preset_data = initial
                if item.get("base_preset"):
                    plugin.load_preset(item["base_preset"])
                apply(plugin, item["parameters"])
                output = Path(item["output"])
                output.write_bytes(plugin.preset_data)
                # Reopen the emitted VST3 state and check the controls we changed.
                expected = {name: plugin.parameters[name].raw_value for name in item["parameters"]}
                plugin.preset_data = initial
                plugin.load_preset(str(output))
                for name, raw in expected.items():
                    if abs(plugin.parameters[name].raw_value - raw) > 1e-5:
                        raise ValueError(f"Preset round-trip failed for {name}")
                entry = {"file": str(output), "round_trip_verified": True,
                         "parameters": describe(plugin, item["parameters"])}
                if item.get("midi"):
                    entry["render"] = render(plugin, Path(item["midi"]), Path(item["preview"]),
                                             request.get("sample_rate", 48000))
                result["presets"].append(entry)
        elif operation == "render":
            plugin.load_preset(request["preset"])
            result["render"] = render(plugin, Path(request["midi"]), Path(request["output"]),
                                       request.get("sample_rate", 48000))
        else:
            raise ValueError(f"Unknown Serum worker operation: {operation}")
    except Exception as exc:
        result = {"ok": False, "error": str(exc)}
        traceback.print_exc(file=sys.stderr)
    response.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
