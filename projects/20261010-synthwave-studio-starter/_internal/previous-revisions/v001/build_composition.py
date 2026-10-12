"""A deterministic 16-bar sound-check arrangement for the Serum/Cubase starter."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
layers = []


def layer(identifier, name, role, program=None, volume=100, pan=64):
    item = {"id": identifier, "name": name, "role": role,
            "kind": "melodic" if program is not None else "drums", "volume": volume, "pan": pan, "notes": []}
    if program is not None:
        item["program"] = program
    layers.append(item)
    return item["notes"]


def note(notes, pitch, start, duration, velocity):
    notes.append({"pitch": pitch, "start": start, "duration": duration, "velocity": velocity})


pad = layer("pad", "Serum - Warm Neon Pad", "harmony", 89, 80, 64)
bass = layer("bass", "Serum - Night Drive Bass", "bass", 38, 100, 64)
arp = layer("arp", "Serum - Skyline Arp", "arpeggio", 81, 76, 76)
lead = layer("lead", "Serum - Midnight Lead", "melody", 80, 88, 64)
brass = layer("brass", "Serum - Retro Brass", "synth brass", 62, 78, 48)
keys = layer("keys", "Serum - Glass Keys", "keys accents", 10, 74, 66)
kick = layer("kick", "Drums - Kick", "percussion", volume=100)
snare = layer("snare", "Drums - Snare", "percussion", volume=90)
hat = layer("closed-hat", "Drums - Closed Hat", "percussion", volume=68, pan=72)
opened = layer("open-hat", "Drums - Open Hat", "percussion", volume=64, pan=80)

chords = [(45, [57, 60, 64, 71]), (41, [57, 60, 65, 69]),
          (48, [55, 60, 64, 67]), (43, [55, 59, 62, 69])]
for bar in range(16):
    root, chord = chords[(bar // 2) % 4]
    start = bar * 4
    if bar % 2 == 0:
        for pitch in chord:
            note(pad, pitch, start, 6.9 if bar < 14 else 4.7, 70 + (pitch % 5))
    if bar in (0, 2, 4, 6, 12, 14):
        for pitch in chord[:3]:
            note(keys, pitch + 12, start + 0.5, 1.2, 65 + pitch % 7)
    if 2 <= bar <= 14:
        for step in range(8):
            if bar == 14 and step >= 4:
                continue
            note(bass, root - 12 + (12 if step in (3, 7) else 0), start + step * 0.5, 0.38,
                 96 if step % 2 == 0 else 82)
    if 4 <= bar <= 14:
        for step in range(8):
            if bar == 14 and step >= 4:
                continue
            note(arp, chord[[0, 2, 1, 3, 2, 1, 3, 2][step]] + 12, start + step * 0.5,
                 0.24, 70 + (step % 3) * 6)
    if 8 <= bar <= 13:
        for offset in (0.0, 1.5):
            for pitch in chord[:3]:
                note(brass, pitch, start + offset, 0.7, 80 if offset == 0 else 68)
    if 2 <= bar <= 14:
        for beat in range(4 if bar < 14 else 2):
            note(kick, 36, start + beat, 0.15, 110 if beat in (0, 2) else 101)
        for beat in (1, 3) if bar < 14 else (1,):
            note(snare, 38, start + beat, 0.15, 99 if beat == 1 else 108)
        for step in range(8 if bar < 14 else 4):
            note(hat, 42, start + step * 0.5, 0.1, 74 if step % 2 == 0 else 52)
    if 6 <= bar <= 13 and bar % 2:
        note(opened, 46, start + 3.5, 0.2, 66)

motifs = [[(76, 0, 0.7), (79, 1, 0.5), (81, 2, 1.2)],
          [(79, 0, 0.6), (76, 1, 1.0), (72, 2.5, 0.7)],
          [(77, 0, 0.7), (76, 1.5, 0.4), (72, 2.5, 1.0)],
          [(74, 0.5, 0.7), (71, 2, 0.7), (69, 3, 0.7)]]
for bar in range(8, 15):
    for pitch, offset, duration in motifs[(bar - 8) % 4]:
        if bar == 14 and offset > 1:
            continue
        note(lead, pitch, bar * 4 + offset, duration, 85 if offset == 0 else 78)

source = {"version": 1, "title": "Neon Workshop - Serum Synthwave Starter", "tempo_bpm": 110,
          "time_signature": [4, 4], "key_signature": "Am", "bars": 16, "ticks_per_beat": 480,
          "description": "A reusable sound-check arrangement for six Serum 2 synthwave profiles and four sampled drums.",
          "assumptions": ["110 BPM and A minor are starting values, not a requested finished song.",
                          "Dry synth patches leave room for Cubase chorus, delay, and reverb.",
                          "The final bar provides release space; no combined MIDI was requested."],
          "sections": [{"name": "Atmosphere", "start": 0}, {"name": "Bass and drums", "start": 8},
                       {"name": "Arp", "start": 16}, {"name": "Lead and brass", "start": 32},
                       {"name": "Release", "start": 58}], "layers": layers}
(ROOT / "composition.json").write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
(ROOT / "bindings.json").write_text(json.dumps({"pad": "pad", "bass": "bass", "arp": "pluck", "lead": "lead",
                                               "brass": "brass", "keys": "keys"}, indent=2) + "\n", encoding="utf-8")
