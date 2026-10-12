"""Original new jack swing arrangement. Run with: uv run python <this-file>."""
from collections import defaultdict
import json
from pathlib import Path
import random

BASE = Path(__file__).resolve().parent
SEED = 108960
RNG = random.Random(SEED)
BARS = 96
TOTAL = BARS * 4
SECTIONS = [
    ("Intro", 0, 8), ("Verse 1", 8, 24), ("Pre-chorus", 24, 32),
    ("Chorus 1", 32, 48), ("Verse 2", 48, 64), ("Bridge", 64, 72),
    ("Final chorus", 72, 88), ("Outro", 88, 96),
]
CHORDS = {
    "F#m9": (42, [57, 61, 64, 68]),
    "Bm9": (35, [57, 61, 62, 66]),
    "E13": (40, [56, 61, 62, 66]),
    "Amaj9": (33, [56, 59, 61, 64]),
    "Dmaj9": (38, [54, 57, 61, 64]),
    "C#7sus": (37, [54, 59, 61, 68]),
    "C#7b9": (37, [53, 59, 62, 68]),
    "C#m7": (37, [56, 59, 61, 64]),
}
PROGRESSIONS = {
    "Intro": ["F#m9", "F#m9", "Bm9", "C#7b9", "F#m9", "Amaj9", "Dmaj9", "C#7b9"],
    "Verse": ["F#m9", "F#m9", "Bm9", "C#7b9", "F#m9", "Amaj9", "Dmaj9", "C#7b9"],
    "Pre-chorus": ["Dmaj9", "E13", "C#m7", "F#m9", "Bm9", "Dmaj9", "C#7sus", "C#7b9"],
    "Chorus": ["F#m9", "Bm9", "E13", "Amaj9", "Dmaj9", "Bm9", "C#7sus", "C#7b9"],
    "Bridge": ["Bm9", "Bm9", "E13", "Amaj9", "Dmaj9", "Bm9", "C#7sus", "C#7b9"],
    "Outro": ["F#m9", "Bm9", "E13", "Amaj9", "Dmaj9", "C#7b9", "F#m9", "F#m9"],
}
LAYERS = {}


def layer(id_, name, role, program=None, volume=100, pan=64):
    obj = {"id": id_, "name": name, "role": role,
           "kind": "drums" if program is None else "melodic",
           "volume": volume, "pan": pan, "notes": []}
    if program is not None:
        obj["program"] = program
    LAYERS[id_] = obj


layer("kick", "Kick - punchy drum machine", "Groove foundation", volume=112)
layer("snare", "Snare - gated backbeat", "Backbeat and ghost notes", volume=106)
layer("clap", "Hand clap", "Chorus backbeat reinforcement", volume=82, pan=68)
layer("hihat", "Hi-hat - closed and open", "Swung sixteenth pulse", volume=82, pan=77)
layer("shaker", "Shaker", "Swung percussion", volume=63, pan=43)
layer("tambourine", "Tambourine", "Chorus lift", volume=65, pan=89)
layer("toms", "Electronic toms", "Section transition fills", volume=88, pan=57)
layer("slap-bass", "Slap bass", "Syncopated bassline", 36, 106, 64)
layer("electric-piano", "Electric piano", "Extended chord harmony", 4, 88, 55)
layer("synth-stabs", "Poly synth stabs", "Rhythmic harmony", 90, 70, 77)
layer("muted-guitar", "Muted funk guitar", "Offbeat chord scratches", 28, 75, 35)
layer("synth-brass", "Synth brass", "Call-and-response accents", 62, 84, 74)
layer("lead-synth", "Saw synth lead", "Main instrumental hook", 81, 91, 64)
layer("string-pad", "Warm string pad", "Pre-chorus and bridge sustain", 50, 58, 60)
layer("bell-keys", "FM bell keys", "Phrase-end sparkle", 10, 61, 91)


def swing(beat):
    """60:40 sixteenth pairs: 0,.30,.50,.80 within a beat."""
    grid = round(beat * 4)
    if abs(beat * 4 - grid) < 1e-8 and grid % 2:
        return beat + .05
    return beat


def add(id_, pitch, start, duration, velocity):
    if start >= TOTAL:
        return
    duration = min(duration, TOTAL - start)
    if duration < .01:
        return
    LAYERS[id_]["notes"].append({
        "pitch": pitch, "start": round(start, 5), "duration": round(duration, 5),
        "velocity": max(1, min(127, round(velocity) + RNG.randint(-3, 3))),
    })


def hit(id_, pitch, bar, beat, duration=.10, velocity=90):
    add(id_, pitch, bar * 4 + swing(beat), duration, velocity)


def chord(id_, pitches, bar, beat, duration, velocity, strum=0):
    for i, pitch in enumerate(pitches):
        add(id_, pitch, bar * 4 + swing(beat) + i * strum, duration, velocity - i)


def context(bar):
    for name, begin, end in SECTIONS:
        if begin <= bar < end:
            family = "Verse" if name.startswith("Verse") else "Chorus" if "chorus" in name.lower() and name != "Pre-chorus" else name
            local = bar - begin
            return name, family, local, end
    raise ValueError(bar)


HARMONY = []
for bar in range(BARS):
    name, family, local, end = context(bar)
    chord_name = PROGRESSIONS[family][local % 8]
    root, voices = CHORDS[chord_name]
    HARMONY.append(chord_name)
    chorus = family == "Chorus"
    bridge = family == "Bridge"
    last_bar = bar == 95
    last_outro = family == "Outro" and local >= 4
    strength = .90 if family == "Intro" else .84 if bridge else 1.08 if chorus else 1.0
    if last_outro:
        strength *= 1 - .08 * (local - 4)

    # Rhythm arrangement: half-time bridge opening, drop at transition bars.
    kicks = ([0, 2.5] if bridge and local < 4 else
             [0, .75, 2, 2.75, 3.5] if chorus else
             [0, .75, 2, 2.5] if local % 2 == 0 else [0, 1.75, 2.5, 3.5])
    if family == "Intro" and local < 2:
        kicks = [0, 2.5] if local else [0]
    if local == 7 and family == "Pre-chorus":
        kicks = [0, 1.75, 2]
    if last_bar:
        kicks = [0]
    for beat in kicks:
        hit("kick", 36, bar, beat, velocity=(112 if beat == 0 else 102) * strength)

    snares = [2] if bridge and local < 4 else [1, 3]
    if family == "Intro" and local == 0 or last_bar:
        snares = []
    for beat in snares:
        hit("snare", 38, bar, beat, velocity=110 * strength)
        if chorus or family == "Pre-chorus" or family == "Verse" and local >= 8:
            hit("clap", 39, bar, beat + .01, velocity=88 * strength)
    if not last_bar and (family == "Verse" or chorus) and local % 2:
        hit("snare", 38, bar, 2.75, velocity=40)
        if local % 4 == 3:
            hit("snare", 38, bar, 3.75, velocity=49)

    if not last_bar:
        hat_grid = range(0, 16, 2) if bridge and local < 4 or family == "Intro" and local < 2 else range(16)
        opens = {14} if chorus or local % 2 == 1 else set()
        for step in hat_grid:
            if family == "Pre-chorus" and local == 7 and step >= 14:
                continue
            pitch = 46 if step in opens else 42
            vel = 77 if step % 4 == 0 else 65 if step % 2 == 0 else 43
            hit("hihat", pitch, bar, step / 4, .17 if pitch == 46 else .08, vel * strength)
        if chorus or family == "Verse" and name == "Verse 2" or family == "Pre-chorus":
            for step in range(16):
                hit("shaker", 82, bar, step / 4, .06, (55 if step % 2 else 41) * strength)
        if chorus:
            for beat in [.5, 1, 2.5, 3]:
                hit("tambourine", 54, bar, beat, .09, 64 if beat in [1, 3] else 46)
        if bar == end - 1 and family != "Outro" or chorus and local % 8 == 7:
            # A fill occupies the end of the phrase without an extra kick roll.
            for beat, pitch, vel in [(3.25, 50, 84), (3.5, 47, 90), (3.75, 45, 100)]:
                hit("toms", pitch, bar, beat, .14, vel)

    # Bass locks to the kick but retains sixteenth pickups and register pops.
    if bar >= 4:
        bass_pattern = ([(0, 0, .42), (1.5, 7, .20), (2.5, 12, .34)] if bridge and local < 4 else
                        [(0, 0, .35), (.75, 12, .16), (1.5, 0, .19), (2, 7, .19),
                         (2.75, 0, .25), (3.5, 12, .18)] if chorus else
                        [(0, 0, .35), (.75, 0, .18), (1.75, 12, .15),
                         (2.5, 7, .25), (3.5, 0, .18)])
        if last_bar:
            bass_pattern = [(0, 0, 1.7)]
        for beat, offset, duration in bass_pattern:
            # The fifth of C# is G#; every dominant's third stays in the keys/lead.
            hit("slap-bass", root + offset, bar, beat, duration,
                (108 if beat == 0 else 93 if offset == 12 else 84) * strength)
        if not last_bar and local % 2 == 1:
            next_root = CHORDS[PROGRESSIONS[family][(local + 1) % 8]][0]
            if bar == end - 1 and bar + 1 < BARS:
                _, next_family, next_local, _ = context(bar + 1)
                next_root = CHORDS[PROGRESSIONS[next_family][next_local % 8]][0]
            hit("slap-bass", next_root - 1, bar, 3.75, .12, 69 * strength)

    # Rhodes comping: short offbeats contrasted with held section-opening chords.
    if last_bar:
        chord("electric-piano", [42] + voices, bar, 0, 3.65, 78)
    elif bridge or family == "Intro" and local < 4:
        chord("electric-piano", voices, bar, 0, 2.65, 76)
        if not bridge:
            chord("electric-piano", voices, bar, 3, .58, 67)
    else:
        keys_hits = [(0, .58, 87), (1.5, .38, 72), (2.75, .68, 83)] if chorus else [(0, .72, 79), (1.75, .30, 66), (2.5, .66, 75)]
        for beat, duration, vel in keys_hits:
            chord("electric-piano", voices, bar, beat, duration, vel * strength)

    # Muted guitar plays narrow chord fragments, with tiny downstroke offsets.
    if bar >= 4 and not last_bar and not (bridge and local < 4):
        guitar_voices = voices[1:]
        guitar_hits = [.5, 1.25, 2.5, 3.25] if chorus else [.5, 2.25, 3.25]
        for beat in guitar_hits:
            chord("muted-guitar", guitar_voices, bar, beat, .095,
                  78 if beat in [.5, 2.5] else 63, strum=.004)

    if (chorus or family == "Pre-chorus" or name == "Verse 2" and local >= 8) and not last_bar:
        for beat in ([.75, 2.25] if chorus else [2.25]):
            chord("synth-stabs", [p + 12 for p in voices[1:]], bar, beat, .16, 82 if chorus else 67)

    if family in ["Pre-chorus", "Bridge"] or chorus and local >= 8 or last_outro:
        chord("string-pad", voices, bar, 0, 3.72, 56 if bridge else 48)

    # Brass occupies the late-bar answer, leaving room for the lead hook.
    if chorus and local % 2 == 1 or family == "Pre-chorus" and local >= 4 or family == "Intro" and local >= 6:
        for beat, dur, vel in [(3.25, .16, 83), (3.75, .13, 96)]:
            chord("synth-brass", [p + 12 for p in voices[:3]], bar, beat, dur, vel)
    elif family == "Verse" and local % 4 == 3:
        chord("synth-brass", [p + 12 for p in voices[:3]], bar, 3.25, .28, 70)

    hook = {
        "F#m9": [73, 76, 78, 76, 73], "Bm9": [74, 73, 71, 69, 66],
        "E13": [71, 73, 74, 73, 71], "Amaj9": [73, 76, 80, 76, 73],
        "Dmaj9": [78, 76, 73, 69, 73], "C#7sus": [73, 78, 80, 78, 73],
        "C#7b9": [77, 80, 83, 80, 77], "C#m7": [73, 76, 80, 76, 71],
    }[chord_name]
    if chorus:
        for i, (beat, dur) in enumerate([(0, .46), (.75, .18), (1.25, .40), (2, .43), (2.75, .30)]):
            # Two four-bar sentences; the second gains a small pickup variation.
            pitch = hook[i]
            hit("lead-synth", pitch, bar, beat, dur, 101 if i == 2 else 91)
        if name == "Final chorus" and local in [4, 12]:
            hit("lead-synth", 78, bar, 3.5, .17, 88)
    elif family == "Verse" and local % 4 in [1, 3]:
        for beat, pitch, dur in [(1.25, hook[0], .22), (2, hook[1], .37), (2.75, hook[-1], .28)]:
            hit("lead-synth", pitch, bar, beat, dur, 72 if name == "Verse 1" else 80)
    elif bridge and local >= 4:
        hit("lead-synth", hook[0], bar, .5, .9, 74)
        hit("lead-synth", hook[1], bar, 2.5, .7, 80)
    elif family == "Intro" and local in [2, 6]:
        hit("lead-synth", hook[0], bar, 1.25, .27, 69)
        hit("lead-synth", hook[1], bar, 2, .42, 74)
    elif family == "Outro" and local < 4:
        for beat, pitch in [(0, hook[0]), (1.25, hook[2]), (2.75, hook[-1])]:
            hit("lead-synth", pitch, bar, beat, .38, 84 - local * 5)
    elif last_bar:
        hit("lead-synth", 78, bar, 0, 1.8, 72)

    if (family == "Intro" and local % 2 == 0 or family in ["Verse", "Pre-chorus", "Bridge"] and local % 4 == 2):
        for beat, pitch in [(2.75, voices[-1] + 24), (3.25, voices[1] + 24)]:
            hit("bell-keys", pitch, bar, beat, .38, 63)
    if last_bar:
        hit("bell-keys", 80, bar, 1, 2.4, 50)


# Check performance intent before writing the source spec. A layer may play
# chords, but bass and lead are strictly monophonic; no pitch can overlap itself.
for id_, obj in LAYERS.items():
    obj["notes"].sort(key=lambda n: (n["start"], n["pitch"]))
    pitch_ends = {}
    end = -1
    for note in obj["notes"]:
        assert note["start"] >= pitch_ends.get(note["pitch"], -1) - 1e-6, (id_, note)
        pitch_ends[note["pitch"]] = note["start"] + note["duration"]
        if id_ in ["slap-bass", "lead-synth"]:
            assert note["start"] >= end - 1e-6, ("monophony", id_, note)
            end = note["start"] + note["duration"]

spec = {
    "version": 1, "title": "Neon Step - New Jack Swing",
    "description": "Original instrumental song: swung drum-machine groove, slap bass, Rhodes ninth chords, muted funk guitar, synth brass responses and a recurring saw-synth hook.",
    "prompt": "buatkan lagu untuk genre new jack swing (semua instrumenya)",
    "tempo_bpm": 108, "time_signature": [4, 4], "bars": BARS,
    "ticks_per_beat": 960, "key_signature": "F#m",
    "sections": [{"name": name, "start": start * 4} for name, start, _ in SECTIONS],
    "assumptions": [
        "Komposisi instrumental orisinal; synth lead menjalankan fungsi melodi utama karena vokal/lirik tidak diminta.",
        "108 BPM, F# minor, 4/4, 96 bar; durasi 213.333 detik.",
        "Swing pasangan not 1/16 sebesar 60:40; variasi velocity memakai seed 108960 tanpa jitter onset tambahan.",
        "15 layer: tujuh bagian drum/percussion dan delapan instrumen melodi/harmoni; satu file MIDI per layer.",
        "Drum map General MIDI: kick 36, snare 38, clap 39, hi-hat 42/46, shaker 82, tambourine 54, toms 50/47/45.",
        "Preset GM adalah petunjuk sound; gunakan drum machine dengan gated snare, slap bass, Rhodes dan synth era 1990-an di DAW.",
        "Tidak ada file MIDI gabungan; semua layer tetap mulai pada tick 0 dan berakhir di panjang global.",
    ],
    "layers": list(LAYERS.values()),
}
BASE.joinpath("composition.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

review = [
    "# Penilaian musikal — Neon Step", "",
    "Penilaian ini menggunakan event MIDI dan rancangan aransemen; audio belum didengarkan.", "",
    "- Harmoni: F#m9/Bm9 dengan E13–Amaj9–Dmaj9; C#7sus menuju C#7b9 memberi tarikan kembali ke F#m9. E# pada dominant dipertahankan di keys dan hook.",
    "- Groove: not 1/16 60:40 (288/192 tick pada PPQN 960); snare di beat 2/4, ghost note pelan, kick sinkopasi, clap dan tambourine menambah chorus.",
    "- Bass mengikuti serangan kick penting, menyisakan ruang antar nada, dengan octave pop dan approach kromatik sebelum chord berikutnya.",
    "- Register: bass rendah, piano/gitar menengah, stabs/brass di atasnya, hook dan bell di register tinggi. Bass dan lead diperiksa monofonik.",
    "- Frase: hook berulang delapan bar dengan jeda akhir bar untuk jawaban brass; verse lebih jarang, bridge empat bar awal half-time.",
    "- Perkembangan: intro masuk bertahap, pre-chorus menambah layer, chorus penuh, verse kedua lebih kaya, bridge turun, final chorus kembali penuh, outro menipis dan berhenti pada tonic.",
    "- Dinamika: ghost note dan offbeat lebih ringan daripada downbeat/backbeat, pad rendah, serta pengurangan velocity di akhir outro.",
    "- Batas audit: kualitas timbre/mix dan bunyi gated snare bergantung pada instrumen DAW; tidak dinilai lewat audio.", "",
    "## Inventaris dan register", "",
    "| Layer | Nada | Pitch min–max | Velocity min–max |",
    "| --- | ---: | --- | --- |",
]
for id_, obj in LAYERS.items():
    notes = obj["notes"]
    review.append(f"| {obj['name']} | {len(notes)} | {min(n['pitch'] for n in notes)}–{max(n['pitch'] for n in notes)} | {min(n['velocity'] for n in notes)}–{max(n['velocity'] for n in notes)} |")
review += ["", "## Bentuk dan progresi (satu chord per bar)", "",
           "| Bagian | Bar (1-based) | Progresi |", "| --- | --- | --- |"]
for name, start, stop in SECTIONS:
    _, family, _, _ = context(start)
    review.append(f"| {name} | {start + 1}–{stop} | {' – '.join(PROGRESSIONS[family])}{' (diulang 2x)' if stop-start == 16 else ''} |")
review += ["", "Audit event: overlap pitch sama tidak ada; bass/lead monofonik; setiap layer mempunyai nada; seed tetap."]
BASE.joinpath("musical-review.md").write_text("\n".join(review) + "\n", encoding="utf-8")
print(json.dumps({"title": spec["title"], "bars": BARS, "layers": len(LAYERS),
                  "notes": sum(len(l["notes"]) for l in LAYERS.values()), "seed": SEED}, indent=2))
