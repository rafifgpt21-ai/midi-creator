"""Reproducible original progressive-house MIDI arrangement."""
import json
from pathlib import Path
import random

BASE = Path(__file__).resolve().parent
SEED = 126160
RNG = random.Random(SEED)
BARS, BPM, PPQN = 160, 126, 960
TOTAL = BARS * 4
SECTIONS = [
    ("Intro", 0, 16), ("Groove", 16, 32), ("Theme", 32, 48),
    ("Breakdown", 48, 64), ("Build 1", 64, 72), ("Drop 1", 72, 96),
    ("Interlude", 96, 112), ("Build 2", 112, 120),
    ("Final drop", 120, 144), ("Outro", 144, 160),
]
GAPS = [(287, 288), (479, 480)]
CHORDS = {
    "Fm9": {"root": 29, "voices": [56, 60, 63, 67], "arp": [65, 68, 72, 75, 79]},
    "Dbmaj9": {"root": 25, "voices": [53, 56, 60, 63], "arp": [65, 68, 72, 75, 73]},
    "Abmaj9": {"root": 32, "voices": [55, 58, 60, 63], "arp": [63, 67, 70, 72, 80]},
    "Ebadd9": {"root": 27, "voices": [55, 58, 63, 65], "arp": [63, 67, 70, 77, 75]},
}
LOOP = ["Fm9", "Dbmaj9", "Abmaj9", "Ebadd9"]
MELODY = [
    [72, 75, 77, 79], [80, 79, 77, 75],
    [77, 80, 84, 80], [77, 75, 73, 72],
    [75, 80, 84, 82], [80, 79, 75, 72],
    [79, 82, 77, 75], [79, 77, 75, 72],
]
LAYERS = {}


def make_layer(id_, name, role, program=None, volume=100, pan=64):
    layer = {"id": id_, "name": name, "kind": "drums" if program is None else "melodic",
             "role": role, "volume": volume, "pan": pan, "notes": []}
    if program is not None:
        layer["program"] = program
    LAYERS[id_] = layer


make_layer("kick", "Electronic kick", "Four-on-the-floor foundation", volume=112)
make_layer("clap", "Electronic clap", "Beats 2 and 4", volume=92)
make_layer("snare-roll", "Snare build and fills", "Accelerating build-up rolls", volume=82)
make_layer("closed-hat", "Closed hi-hat", "Sixteenth pulse", volume=70, pan=78)
make_layer("open-hat", "Open hi-hat", "Offbeat lift", volume=76, pan=71)
make_layer("ride", "Ride cymbal", "Final drop lift", volume=60, pan=83)
make_layer("shaker", "Shaker / maracas", "Subtle percussion syncopation", volume=57, pan=39)
make_layer("synth-bass", "Deep mono synth bass", "Offbeat low-end pulse", 38, 104, 64)
make_layer("poly-synth", "Wide saw poly synth", "Main chord hook", 81, 88, 58)
make_layer("pluck-arp", "Plucked synth arpeggio", "Repeating evolving motif", 80, 77, 74)
make_layer("warm-pad", "Warm atmospheric pad", "Sustained harmonic space", 89, 56, 53)
make_layer("lead-synth", "Melodic saw lead", "Original eight-bar melodic hook", 81, 85, 64)


def add(id_, pitch, start, duration, velocity):
    if start < 0 or start >= TOTAL:
        return
    stop = min(start + duration, TOTAL)
    for begin, end in GAPS:
        if begin <= start < end:
            return
        if start < begin < stop:
            stop = begin
    if stop - start <= .01:
        return
    LAYERS[id_]["notes"].append({
        "pitch": pitch, "start": round(start, 5), "duration": round(stop - start, 5),
        "velocity": max(1, min(127, round(velocity) + RNG.randint(-2, 2))),
    })


def hit(id_, pitch, bar, beat, duration=.09, velocity=90):
    add(id_, pitch, bar * 4 + beat, duration, velocity)


def chord(id_, pitches, bar, beat, duration, velocity):
    for i, pitch in enumerate(pitches):
        hit(id_, pitch, bar, beat, duration, velocity - i)


def context(bar):
    for name, start, stop in SECTIONS:
        if start <= bar < stop:
            return name, bar - start, stop
    raise ValueError(bar)


HARMONY = []
for bar in range(BARS):
    name, local, section_end = context(bar)
    drop = name in ["Drop 1", "Final drop"]
    build = name.startswith("Build")
    breakdown = name in ["Breakdown", "Interlude"]
    final = bar == BARS - 1
    outro = name == "Outro"
    chord_name = "Fm9" if bar >= 158 else LOOP[(bar % 8) // 2]
    HARMONY.append(chord_name)
    data = CHORDS[chord_name]
    root, voices, arp = data["root"], data["voices"], data["arp"]
    energy = (1.04 if name == "Final drop" else 1.0 if drop else .92 if name == "Theme"
              else .78 if name == "Groove" else .58 if breakdown else .48)
    if build:
        energy = .63 + local * .045
    if outro:
        energy = .78 - local * .025

    # DJ-friendly four-on-the-floor; breakdowns and final bar create contrast.
    kick_active = not breakdown and not (build and local >= 6)
    if kick_active:
        for beat in ([0] if final else range(4)):
            hit("kick", 36, bar, beat, .13, 114 if drop else 106 if bar >= 16 else 98)
    if (drop or name in ["Groove", "Theme"] or build and local < 6 or outro and local < 8):
        for beat in [1, 3]:
            hit("clap", 39, bar, beat, .12, 99 if drop else 85)

    if bar >= 8 and not final:
        if breakdown:
            steps = [2, 10] if local >= 8 else []
        elif name == "Intro":
            steps = range(0, 16, 4)
        elif outro and local >= 8:
            steps = range(0, 16, 2)
        else:
            steps = range(16) if drop or name == "Theme" or build else range(0, 16, 2)
        for step in steps:
            # Suppress closed hats when the open hat articulates the offbeat.
            if step % 4 == 2 and (drop or name in ["Groove", "Theme"] or build or outro and local < 8):
                continue
            velocity = 65 if step % 4 == 0 else 48 if step % 2 == 0 else 34
            hit("closed-hat", 42, bar, step / 4, .06, velocity + energy * 7)
    if drop or name in ["Groove", "Theme"] or build or outro and local < 8:
        for beat in [.5, 1.5, 2.5, 3.5]:
            hit("open-hat", 46, bar, beat, .19, 72 + 8 * energy)
    if name == "Final drop" and local >= 8 or name == "Drop 1" and local >= 16:
        for beat in [.5, 1.5, 2.5, 3.5]:
            hit("ride", 51, bar, beat, .23, 61 if beat in [.5, 2.5] else 49)
    if drop or name == "Theme" or name == "Groove" and local >= 8:
        for beat in [.25, .75, 1.75, 2.25, 2.75, 3.75]:
            hit("shaker", 70, bar, beat, .06, 46 if beat % 1 == .75 else 33)

    if build:
        spacing = .5 if local < 4 else .25 if local < 6 else .125
        for step in range(round(4 / spacing)):
            beat = step * spacing
            velocity = 40 + local * 6 + beat * 5
            hit("snare-roll", 38, bar, beat, min(.06, spacing * .6), velocity)
    elif (drop or name == "Theme") and local % 8 == 7:
        for beat, vel in [(3, 62), (3.5, 73), (3.75, 87)]:
            hit("snare-roll", 38, bar, beat, .06, vel)

    # Bass stays off the kick with short mono notes, never two bass patches.
    bass_active = name in ["Groove", "Theme", "Drop 1", "Final drop"] or build and local < 6 or outro and local < 8
    if bass_active:
        pattern = [(.5, 0, .32), (1.5, 0, .31), (2.5, 0, .32), (3.5, 12 if drop and local % 4 == 3 else 0, .29)]
        for beat, offset, duration in pattern:
            hit("synth-bass", root + offset, bar, beat, duration, 99 if drop else 85)
        if drop and local % 4 == 1:
            hit("synth-bass", root + 12, bar, 3.875, .095, 63)
    elif name == "Interlude" and local >= 8:
        hit("synth-bass", root, bar, .5, .78, 68)
        hit("synth-bass", root, bar, 2.5, .78, 64)
    if final:
        hit("synth-bass", 29, bar, 0, 2.3, 65)

    # Chords form the primary hook; growth is in rhythm, velocity, and register.
    if drop or name == "Theme":
        comp = [(.5, .62), (1.5, .38), (2.5, .62), (3.5, .37)]
        if local % 8 in [3, 7]:
            comp = [(0, .50), (.75, .35), (1.5, .38), (2.5, .48), (3.25, .40)]
        chord_voices = voices + ([voices[-1] + 12] if name == "Final drop" and local >= 8 else [])
        for beat, duration in comp:
            chord("poly-synth", chord_voices, bar, beat, duration, 90 + 12 * energy)
    elif breakdown:
        if bar % 2 == 0:
            chord("poly-synth", voices, bar, 0, 7.6, 62 if local < 8 else 71)
    elif build:
        for beat in [0, 1.5, 2.5, 3.5]:
            chord("poly-synth", voices, bar, beat, .38, 63 + local * 5)
    elif name == "Groove" and local >= 8:
        for beat in [.5, 2.5]:
            chord("poly-synth", voices, bar, beat, .58, 74)
    elif name == "Intro" and local >= 8 and bar % 2 == 0:
        chord("poly-synth", voices, bar, 0, 6.7, 53 + local)
    elif outro and local < 8:
        for beat in [.5, 2.5]:
            chord("poly-synth", voices, bar, beat, .53, 78 - local * 2)
    elif bar == 158:
        chord("poly-synth", voices, bar, 0, 7.7, 54)

    if bar >= 4 and not final:
        pattern = [0, 2, 1, 3, 2, 4, 1, 3, 0, 2, 1, 4, 2, 3, 1, 2]
        if bar % 2:
            pattern = [2, 1, 0, 3, 2, 4, 1, 3, 2, 0, 1, 4, 3, 2, 1, 0]
        step_size = 4 if name == "Intro" and local < 8 else 2 if breakdown or outro and local >= 8 else 1
        if outro and local >= 12:
            step_size = 4
        for step in range(0, 16, step_size):
            pitch = arp[pattern[step]]
            if name == "Final drop" and local >= 16 and step in [6, 14]:
                pitch += 12
            velocity = 45 + energy * 32 + (9 if step % 4 == 0 else 0) + (local * .8 if build else 0)
            hit("pluck-arp", pitch, bar, step / 4, .17 if step_size == 1 else .30, velocity)

    if bar % 2 == 0:
        # A pad spans each two-bar chord, with a small release gap at changes.
        pad_pitches = [root + 24] + voices
        chord("warm-pad", pad_pitches, bar, 0, 7.8, 57 if breakdown else 46 if drop else 43)

    motif = MELODY[bar % 8]
    if drop and (name == "Final drop" or local >= 8):
        for i, (beat, duration) in enumerate([(0, .72), (1, .43), (1.75, .58), (2.75, .73)]):
            hit("lead-synth", motif[i], bar, beat, duration, 89 if i in [0, 2] else 80)
        # Every fourth bar ends earlier, leaving a breathing space.
        if local % 4 == 3:
            LAYERS["lead-synth"]["notes"][-1]["duration"] = .30
    elif breakdown and local >= 8:
        hit("lead-synth", motif[0], bar, .5, 1.2, 65)
        if local % 2:
            hit("lead-synth", motif[-1], bar, 2.5, .78, 61)
    elif name == "Theme" and local % 4 in [2, 3]:
        hit("lead-synth", motif[0], bar, .75, .50, 73)
        hit("lead-synth", motif[2], bar, 2.25, .80, 77)
    elif outro and local < 4:
        hit("lead-synth", motif[0], bar, .5, .75, 68 - local * 3)
        hit("lead-synth", motif[-1], bar, 2.5, .55, 62 - local * 3)
    elif final:
        hit("lead-synth", 77, bar, 0, 2.8, 59)


SCALE = {0, 1, 3, 5, 7, 8, 10}  # F natural minor pitch classes.
for id_, layer in LAYERS.items():
    layer["notes"].sort(key=lambda n: (n["start"], n["pitch"]))
    assert layer["notes"], id_
    ends = {}
    mono_end = -1
    for note in layer["notes"]:
        assert note["start"] >= ends.get(note["pitch"], -1) - 1e-6, (id_, "same-pitch overlap", note)
        ends[note["pitch"]] = note["start"] + note["duration"]
        assert note["start"] + note["duration"] <= TOTAL + 1e-6
        assert not any(begin <= note["start"] < end for begin, end in GAPS)
        if layer["kind"] == "melodic":
            assert note["pitch"] % 12 in SCALE, (id_, "outside scale", note)
        if id_ in ["synth-bass", "pluck-arp", "lead-synth"]:
            assert note["start"] >= mono_end - 1e-6, (id_, "not monophonic", note)
            mono_end = note["start"] + note["duration"]

spec = {
    "version": 1, "title": "Afterglow Circuit - Progressive House",
    "description": "Original melodic progressive-house instrumental inspired by the broad atmospheric electronic direction requested: patient development, repeating arpeggios, wide saw chords, deep mono bass, long breakdowns and two drops.",
    "prompt": "buatkan lagu baru seperti lagu deadmau5",
    "tempo_bpm": BPM, "time_signature": [4, 4], "bars": BARS,
    "ticks_per_beat": PPQN, "key_signature": "Fm",
    "sections": [{"name": name, "start": start * 4} for name, start, _ in SECTIONS],
    "assumptions": [
        "Memilih arah melodic/atmospheric progressive house dari referensi artis umum; tidak ada lagu tertentu atau bahan audio/MIDI yang diberikan.",
        "Komposisi baru orisinal dan instrumental; 126 BPM, F minor, 4/4, 160 bar, sekitar 5:04.76.",
        "12 layer lengkap: kick, clap, snare-roll, closed-hat, open-hat, ride, shaker/maracas, synth bass, saw chords, pluck arp, warm pad, saw lead.",
        "Groove lurus not 1/16 tanpa swing; variasi velocity kecil memakai seed 126160.",
        "Loop harmoni Fm9 - Dbmaj9 - Abmaj9 - Ebadd9, dua bar per chord; dua bar terakhir kembali ke Fm9.",
        "Drum mapping GM: kick 36, clap 39, snare 38, closed hat 42, open hat 46, ride 51, shaker/maracas 70.",
        "Program GM hanya penanda instrumen. Filter automation, sidechain, stereo widening, delay, reverb dan riser audio diatur di DAW; tidak terkandung dalam file MIDI.",
        "Satu file MIDI per instrumen, timeline global sama; tidak membuat MIDI gabungan.",
    ], "layers": list(LAYERS.values()),
}
BASE.joinpath("composition.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

review = ["# Penilaian musikal — Afterglow Circuit", "",
          "Audit berdasarkan event MIDI dan rancangan aransemen. Audio belum didengarkan.", "",
          "- Harmoni: Fm9–Dbmaj9–Abmaj9–Ebadd9, dua bar per chord, voicing bergerak dekat; semua instrumen bernada berada dalam F natural minor. Dua bar terakhir kembali ke tonic.",
          "- Register: bass MIDI 25–44; chord/pad menengah; arp dan lead di atas. Bass, arp dan lead diperiksa monofonik; chord/pad memang polifonik.",
          "- Groove: kick four-on-the-floor, clap beat 2/4, open hat offbeat, closed hat dengan aksen ringan, ride hadir di puncak drop. Bass offbeat menyisakan ruang bagi kick.",
          "- Tema: motif lead orisinal delapan bar mengikuti progression. Drop pertama membuka dengan chord/arp, lead masuk setelah delapan bar; final drop memberi hook langsung dan register arp lebih tinggi menjelang puncak.",
          "- Bentuk: intro 16 bar, groove 16, theme 16, breakdown 16, build 8, drop 24, interlude 16, build 8, final drop 24, outro 16.",
          "- Build: snare dipercepat dari not 1/8 ke 1/16 lalu 1/32; velocity naik. Kick/bass dihilangkan pada dua bar terakhir dan satu beat hening tepat sebelum kedua drop.",
          "- Frase/dinamika: lead mempunyai jeda di akhir kalimat empat bar; breakdown memberi nada panjang; outro mengurangi jumlah layer, velocity dan densitas arp; tonic penutup dibiarkan berbunyi.",
          "- Sound: arah saw chord, plucked arp, sub bass dan pad ditentukan melalui instrumen DAW. Sweeps filter dan efek pumping perlu automation/sidechain DAW; audit tidak mengklaim bunyi efek tersebut sudah dirender.", "",
          "## Layer dan register", "", "| Layer | Nada | Pitch MIDI min–max | Velocity min–max |", "| --- | ---: | --- | --- |"]
for id_, layer in LAYERS.items():
    notes = layer["notes"]
    review.append(f"| {layer['name']} | {len(notes)} | {min(n['pitch'] for n in notes)}–{max(n['pitch'] for n in notes)} | {min(n['velocity'] for n in notes)}–{max(n['velocity'] for n in notes)} |")
review += ["", "## Densitas per bagian", "", "| Bagian | Bar (1-based) | Nada drum | Nada instrumen bernada |", "| --- | --- | ---: | ---: |"]
for name, start, end in SECTIONS:
    counts = {kind: sum(sum(start * 4 <= n["start"] < end * 4 for n in l["notes"]) for l in LAYERS.values() if l["kind"] == kind) for kind in ["drums", "melodic"]}
    review.append(f"| {name} | {start + 1}–{end} | {counts['drums']} | {counts['melodic']} |")
review += ["", "Audit event lulus: scale, batas timeline, pitch overlap, monofoni bass/arp/lead, gap sebelum drop, dan keberadaan nada tiap layer."]
BASE.joinpath("musical-review.md").write_text("\n".join(review) + "\n", encoding="utf-8")
print(json.dumps({"title": spec["title"], "bars": BARS, "layers": len(LAYERS),
                  "notes": sum(len(l["notes"]) for l in LAYERS.values()), "seed": SEED}, indent=2))
