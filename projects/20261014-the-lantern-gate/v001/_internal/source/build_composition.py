"""The Lantern Gate: deterministic BBCSO Discover orchestration, seed 20261014.

Rebuild: uv run python <this-file>. Writes composition.json beside this script.
All note onsets are straight on a common 1/16 grid; CC curves run at 1/32.
"""
from pathlib import Path
import json
import math
import random

HERE = Path(__file__).resolve().parent
RNG = random.Random(20261014)
BARS, BPM, PPQN = 96, 108, 960
TOTAL = BARS * 3
MODE = {0, 2, 4, 5, 7, 9, 11}  # D Dorian: D E F G A B C.
LAYERS, BINDINGS = {}, {}


def layer(identifier, name, patch, articulation, role, program, volume, pan,
          register, family, kind="melodic"):
    raw = dict(id=identifier, name=name, kind=kind, role=role, volume=volume,
               pan=pan, notes=[])
    if kind == "melodic":
        raw["program"] = program
    LAYERS[identifier] = raw
    BINDINGS[identifier] = dict(plugin="BBC Symphony Orchestra", edition="Discover",
        patch=patch, articulation=articulation, register=register, family=family,
        channel=10 if kind == "drums" else 1)


# One instance / fixed articulation per layer, including repeated instruments.
layer("s01-violins1-long", "01 Violins 1 - Long", "Strings: Violins 1", "Long",
      "tema utama; nada panjang pada klimaks", 40, 100, 52, [67, 98], "strings")
layer("s02-violins1-tremolo", "02 Violins 1 - Tremolo", "Strings: Violins 1", "Tremolo",
      "ketegangan menjelang gerbang", 44, 83, 52, [67, 98], "strings")
layer("s03-violins2-long", "03 Violins 2 - Long", "Strings: Violins 2", "Long",
      "garis harmoni dan jawaban", 40, 90, 58, [55, 96], "strings")
layer("s04-violins2-spiccato", "04 Violins 2 - Spiccato", "Strings: Violins 2", "Spiccato",
      "ostinato eighth-note 3+3", 45, 85, 58, [55, 96], "strings")
layer("s05-violins2-pizzicato", "05 Violins 2 - Pizzicato", "Strings: Violins 2", "Pizzicato",
      "langkah ringan di pembukaan", 45, 86, 58, [55, 96], "strings")
layer("s06-violas-long", "06 Violas - Long", "Strings: Violas", "Long",
      "suara tengah yang bergerak halus", 41, 93, 65, [48, 84], "strings")
layer("s07-violas-spiccato", "07 Violas - Spiccato", "Strings: Violas", "Spiccato",
      "jawaban ritmis pada ostinato", 45, 84, 65, [48, 84], "strings")
layer("s08-cellos-long", "08 Cellos - Long", "Strings: Cellos", "Long",
      "akar harmoni; countermelody tenor", 42, 98, 73, [36, 72], "strings")
layer("s09-cellos-spiccato", "09 Cellos - Spiccato", "Strings: Cellos", "Spiccato",
      "dorongan low strings", 45, 87, 73, [36, 72], "strings")
layer("s10-cellos-pizzicato", "10 Cellos - Pizzicato", "Strings: Cellos", "Pizzicato",
      "bass ringan pada bagian fantasy", 45, 91, 73, [36, 72], "strings")
layer("s11-basses-long", "11 Double Basses - Long", "Strings: Basses", "Long",
      "fondasi low bass tanpa voicing rapat", 43, 94, 78, [26, 54], "strings")
layer("w01-flutes-long", "12 Flutes a3 - Long", "Woodwinds: Flutes a3", "Long",
      "tema fantasy dan puncak frase", 73, 96, 61, [60, 96], "winds")
layer("w02-flutes-staccatissimo", "13 Flutes a3 - Staccatissimo", "Woodwinds: Flutes a3", "Staccatissimo",
      "kilau pendek; run transisi", 73, 82, 61, [60, 96], "winds")
layer("w03-oboes-long", "14 Oboes a3 - Long", "Woodwinds: Oboes a3", "Long",
      "jawaban hangat pada tema", 68, 84, 65, [58, 84], "winds")
layer("w04-clarinets-long", "15 Clarinets a3 - Long", "Woodwinds: Clarinets a3", "Long",
      "tema intim pada jeda tengah", 71, 91, 59, [50, 86], "winds")
layer("w05-bassoons-long", "16 Bassoons a3 - Long", "Woodwinds: Bassoons a3", "Long",
      "gerak tenor dan pengikat bass", 70, 86, 69, [34, 74], "winds")
layer("w06-piccolo-long", "17 Piccolo - Long", "Woodwinds: Piccolo", "Long",
      "kilau puncak; baru hadir saat akhir", 72, 70, 63, [74, 96], "winds")
layer("b01-horns-long", "18 Horns a4 - Long", "Brass: Horns a4", "Long",
      "tema heroik dalam register tengah", 60, 96, 57, [40, 77], "brass")
layer("b02-horns-staccatissimo", "19 Horns a4 - Staccatissimo", "Brass: Horns a4", "Staccatissimo",
      "aksen fanfare sebelum klimaks", 60, 88, 57, [40, 77], "brass")
layer("b03-trumpets-long", "20 Trumpets a3 - Long", "Brass: Trumpets a3", "Long",
      "mahkota tema saat akhir", 56, 89, 65, [52, 84], "brass")
layer("b04-trumpets-staccatissimo", "21 Trumpets a3 - Staccatissimo", "Brass: Trumpets a3", "Staccatissimo",
      "fanfare pendek di sela tema", 56, 83, 65, [52, 84], "brass")
layer("b05-tenor-trombones-long", "22 Tenor Trombones a3 - Long", "Brass: Tenor Trombones a3", "Long",
      "isi harmoni brass", 57, 88, 72, [43, 74], "brass")
layer("b06-bass-trombones-long", "23 Bass Trombones a2 - Long", "Brass: Bass Trombones a2", "Long",
      "fifth/root rendah saat tutti", 57, 85, 75, [34, 67], "brass")
layer("b07-tuba-long", "24 Tuba - Long", "Brass: Tuba", "Long",
      "fondasi brass pada frase penting", 58, 90, 70, [28, 60], "brass")
layer("k01-harp", "25 Harp - Plucks", "Percussion: Harp", "Plucks / default",
      "arpeggio Dorian sebagai cahaya fantasy", 46, 94, 54, [36, 96], "keys")
layer("k02-celeste", "26 Celeste - Hits", "Percussion: Celeste", "Hits / default",
      "gema motif kecil dan bintang di awal", 8, 82, 64, [60, 96], "keys")
layer("k03-glockenspiel", "27 Glockenspiel - Hits", "Percussion: Glockenspiel", "Hits / default",
      "titik cahaya pada nada puncak", 9, 71, 65, [72, 96], "keys")
layer("k04-tubular-bells", "28 Tubular Bells - Hits", "Percussion: Tubular Bells", "Hits / default",
      "tanda gerbang dan resolusi", 14, 76, 67, [60, 77], "keys")
layer("p01-timpani-hits", "29 Timpani - Hits", "Percussion: Timpani", "Hits",
      "pulsa bertonal D/A; roll dimainkan ulang dengan Hits", 47, 90, 66, [38, 57], "percussion")
for ident, name, art, pitch, volume, pan, role in [
    ("p02-bass-drum", "30 Bass Drum - Hits", "Hits", 36, 91, 64, "aksen structural; bukan kick pop"),
    ("p03-snare", "31 Snare Drum - Hits", "Hits", 40, 77, 66, "aksen march 6/8 dan roll dari repeated Hits"),
    ("p04-suspended-cymbal", "32 Suspended Cymbal - Hits", "Hits", 41, 70, 67, "aksen transisi lembut"),
    ("p05-suspended-cymbal-roll", "33 Suspended Cymbal - Roll", "Roll trigger", 43, 76, 67, "swell ke bagian epic"),
    ("p06-piatti", "34 Piatti - Hits", "Hits", 59, 75, 69, "crash orkestral pada klimaks"),
    ("p07-triangle", "35 Triangle - Hits", "Hits", 52, 68, 66, "kilau jarang pada pembukaan")
]:
    layer(ident, name, "Percussion: Untuned Percussion", art, role, None,
          volume, pan, [pitch, pitch], "percussion", kind="drums")
    BINDINGS[ident]["trigger_pitch"] = pitch


def add(ident, pitch, beat, duration, velocity):
    assert duration > 0 and 0 <= beat < TOTAL and beat + duration <= TOTAL + 1e-8
    if LAYERS[ident]["kind"] != "drums":
        assert pitch % 12 in MODE, (ident, pitch)
    lo, hi = BINDINGS[ident]["register"]
    assert lo <= pitch <= hi, (ident, pitch, lo, hi)
    LAYERS[ident]["notes"].append(dict(pitch=pitch, start=round(beat, 5),
        duration=round(duration, 5), velocity=max(1, min(122, int(velocity + RNG.choice([-3, -2, 0, 0, 1, 2, 3]))))))


def note(ident, pitch, bar, offset=0, duration=2.92, velocity=72):
    add(ident, pitch, (bar - 1) * 3 + offset, duration, velocity)


# Root, third, fifth and colour pitch classes. Inversions are deliberate.
CHORDS = {
    "Dm": (38, [2, 5, 9]), "Dmadd9": (38, [2, 5, 9, 4]),
    "Dm6": (38, [2, 5, 9, 11]), "Dm/F": (41, [2, 5, 9]),
    "G": (43, [7, 11, 2]), "G/D": (38, [7, 11, 2]),
    "C": (36, [0, 4, 7]), "C/D": (38, [0, 4, 7]),
    "F": (41, [5, 9, 0]), "F/A": (45, [5, 9, 0]),
    "Am7": (45, [9, 0, 4, 7]), "Am": (45, [9, 0, 4]),
    "Em7": (40, [4, 7, 11, 2]), "G/B": (35, [7, 11, 2]),
}
HARMONY = {}


def chord_span(start, names, repeats=1):
    for i, name in enumerate(names * repeats):
        HARMONY[start + i] = name


chord_span(1, ["Dmadd9"] * 4 + ["G/D"] * 2 + ["Dm"] * 2 + ["C/D"] * 2 + ["Dm6"] * 2)
base = ["Dmadd9", "F", "G", "Dm", "Dm/F", "Am7", "G", "Dm6"]
chord_span(13, base + ["Dm", "F/A", "G", "Em7", "Dm/F", "C", "G/D", "Dm"])
chord_span(29, ["Dm", "Dm", "G", "G", "F/A", "F/A", "C", "C",
                "Em7", "G/B", "Dm", "Dm", "C", "Am7", "G", "G/D"])
chord_span(45, ["Dmadd9", "Dmadd9", "Dm/F", "Dm/F", "Em7", "Em7", "G/D", "G/D", "Dm6", "Dm6"])
chord_span(55, base + ["Em7", "Em7", "G", "G", "C/D", "C/D", "G/D", "G/D"])
chord_span(71, ["Dm", "F", "G", "Dm", "Dm/F", "Am7", "G", "Dm",
                "Dm", "F/A", "G", "Em7", "Dm/F", "C", "G/D", "Dm6"])
chord_span(87, ["Dm", "Dm", "C/D", "C/D", "G/D", "G/D", "Dm", "Dm", "Dm", "Dm"])
assert len(HARMONY) == BARS


def candidates(pcs, low, high):
    return [p for p in range(low, high + 1) if p % 12 in pcs]


def nearest(pcs, target, low, high):
    return min(candidates(pcs, low, high), key=lambda p: (abs(p-target), p))


# Eight bars of theme: fifth leap answered by descending steps; B is the Dorian sixth.
THEME = [
    [(0, 74, 1.5), (1.5, 76, .5), (2, 77, 1)],
    [(0, 81, 1.5), (1.5, 79, .5), (2, 77, .5), (2.5, 76, .5)],
    [(0, 79, 1), (1, 83, .5), (1.5, 81, .5), (2, 79, 1)],
    [(0, 76, 1.5), (1.5, 74, 1.25)],
    [(0, 77, 1.5), (1.5, 76, .5), (2, 74, 1)],
    [(0, 76, .5), (.5, 79, .5), (1, 81, 1.75)],
    [(0, 83, 1), (1, 81, .5), (1.5, 79, .5), (2, 76, 1)],
    [(0, 77, .5), (.5, 76, .5), (1, 74, 1.5)],
]


def theme(ident, bar, transpose=0, vel=73, variant=0):
    for bi, events in enumerate(THEME):
        for ei, (offset, p, duration) in enumerate(events):
            if variant and bi == 3 and ei == 0:
                p, duration = 79, 1.5
            if variant and bi == 7 and ei == 0:
                p = 79
            gate = duration - (.10 if bi in (3, 7) else .018)
            accent = 4 if offset == 0 else (-5 if duration == .5 else 0)
            note(ident, p+transpose, bar+bi, offset, gate,
                 vel+accent+(2 if bi in (2, 6) else -2))


# Fantasy opening: sound enters in staggered pairs, never a full orchestra.
for bar in range(1, 13):
    root, pcs = CHORDS[HARMONY[bar]]
    if bar % 2:
        note("s06-violas-long", nearest(pcs, 57, 50, 65), bar, duration=5.78, velocity=49)
    if bar >= 5 and bar % 2:
        note("s03-violins2-long", nearest(pcs, 69, 62, 77), bar, duration=5.7, velocity=48)
    if bar >= 3:
        for off, pitch in [(0, root+12), (1.5, nearest(pcs, root+19, 45, 60))]:
            note("s10-cellos-pizzicato", pitch, bar, off, .42, 48 if off else 56)
    for ei, off in enumerate([0, .5, 1, 1.5, 2, 2.5] if bar >= 5 else [0, 1, 2]):
        arp = sorted(candidates(pcs, 57, 81))
        p = arp[[0, 2, 3, 5, 3, 2][ei]]
        note("k01-harp", p, bar, off, 1.1, 44+(5 if off == 0 else 0)+ei%3)
for b, p, duration in [(5, 74, 1.5), (5, 76, .5), (6, 77, 1.5), (6, 81, 1),
                       (7, 79, 1.5), (7, 83, .5), (8, 81, 1.5), (8, 74, 1)]:
    off = 1.5 if duration in (.5, 1) else 0
    note("w01-flutes-long", p, b, off, duration-.08, 65)
for b, p, off, dur in [(9, 67, 0, 1.5), (9, 69, 1.5, .5), (10, 72, 0, 2.25),
                        (11, 71, 0, 1.5), (11, 69, 1.5, .5), (12, 62, 0, 2.5)]:
    note("w03-oboes-long", p, b, off, dur-.07, 62)
for b, p in [(2, 86), (4, 81), (7, 83), (10, 88), (12, 86)]:
    note("k02-celeste", p, b, 1.5, 1.1, 43)
for b in [4, 11]:
    note("p07-triangle", 52, b, 0, .6, 42)


# Theme statement, with solo-colour dialogue rather than constant doubling.
theme("w01-flutes-long", 13, vel=71)
theme("w03-oboes-long", 21, transpose=-12, vel=73, variant=1)
for bar in range(13, 29):
    root, pcs = CHORDS[HARMONY[bar]]
    for ident, target, lo, hi, vel in [("s03-violins2-long", 70, 62, 77, 58),
        ("s06-violas-long", 58, 50, 65, 60), ("s11-basses-long", root-12, 26, 45, 52)]:
        note(ident, nearest(pcs if ident != "s11-basses-long" else [root%12], target, lo, hi),
             bar, duration=2.9 if bar%4 else 2.62, velocity=vel)
    for i, off in enumerate([0, 1, 1.5, 2.5]):
        p = nearest(pcs, 67+[0, 5, 3, 7][i], 60, 79)
        note("s05-violins2-pizzicato", p, bar, off, .27, 55+(5 if i==0 else -4))
    for off in [0, 1.5]:
        note("s10-cellos-pizzicato", root+12, bar, off, .38, 58+(4 if off==0 else -5))
    if bar % 2:
        for i in range(6):
            arp = sorted(candidates(pcs, 57, 81))
            note("k01-harp", arp[[0, 2, 4, 5, 4, 2][i]], bar, i*.5, .92, 54+i%3)
for bar, pitch in [(16, 69), (20, 67), (24, 71), (28, 69)]:
    note("w04-clarinets-long", pitch, bar, 1.5, 1.2, 61)
for bar, pitch in [(15, 83), (23, 83), (27, 86)]:
    note("k03-glockenspiel", pitch, bar, 0, .7, 44)


# Quest: theme comes to strings; upper and lower short strings interlock.
theme("s01-violins1-long", 29, vel=79)
theme("s01-violins1-long", 37, vel=82, variant=1)
for bar in list(range(29, 45)) + list(range(55, 93)):
    root, pcs = CHORDS[HARMONY[bar]]
    intensity = 67 if bar < 45 else 65+(bar-55)*.55 if bar < 71 else 83+(bar-71)*.28
    if bar in [36, 44, 62, 70, 78, 86, 92]:
        offsets = [0, .5, 1, 1.5]  # Last pulse rests so the ensemble can breathe.
    else:
        offsets = [0, .5, 1, 1.5, 2, 2.5]
    arp = sorted(candidates(pcs, 62, 79))
    for i, off in enumerate(offsets):
        index = [0, 2, 1, 3, 2, 4][i] if bar%2 else [1, 3, 2, 4, 2, 0][i]
        note("s04-violins2-spiccato", arp[index % len(arp)], bar, off,
             .21 + RNG.choice([0, .025, .04]), intensity+(6 if i in (0,3) else -7))
        if bar >= 33 and (bar < 45 or bar >= 59):
            note("s07-violas-spiccato", nearest(pcs, 55+[0,5,7,3,7,5][i], 50, 67),
                 bar, off, .24, intensity-8+(6 if i==3 else 0))
    if bar >= 37:
        for i, off in enumerate([0, 1.5, 2.5] if bar%2 else [0, 1.5]):
            pitch = root+12 if i!=2 else nearest(pcs, root+19, 43, 62)
            note("s09-cellos-spiccato", pitch, bar, off, .35 if i<2 else .23, intensity+2-6*i)


# Legato-like connected Long samples: no unavailable recorded Legato is required.
previous = {"s03-violins2-long": 69, "s06-violas-long": 57}
for bar in list(range(29,45)) + list(range(55,93)):
    root, pcs = CHORDS[HARMONY[bar]]
    vel = 66 if bar<45 else 64+(bar-55)*.7 if bar<71 else 80
    for ident, lo, hi in [("s03-violins2-long", 62, 76), ("s06-violas-long", 50, 65)]:
        p = nearest(pcs, previous[ident], lo, hi)
        # Select an alternative nearby chord tone every other bar for moving inner lines.
        if bar%4==2:
            p = nearest(pcs, p+3 if ident.startswith("s03") else p-2, lo, hi)
        previous[ident] = p
        note(ident, p, bar, duration=2.8 if bar in [44,70,86,92] else 2.97, velocity=vel)
    note("s11-basses-long", root-12 if root>=38 else root, bar, duration=2.84, velocity=vel-4)
    if bar < 37 or bar >= 71:
        note("s08-cellos-long", root+12, bar, duration=2.82, velocity=vel-1)
    if bar < 45 and bar%2:
        note("w05-bassoons-long", root+12, bar, 0, 1.35, 66)
        note("w05-bassoons-long", nearest(pcs, root+19, 45, 64), bar, 1.5, 1.2, 60)


# Brass peeks out before the retreat; avoids a flat crescendo for the whole piece.
for b, p, off, dur in [(39,62,0,1.5),(39,65,1.5,1.3),(40,67,0,2.4),
                       (41,69,0,1.5),(42,67,0,2.4),(43,71,0,1.5),(44,69,0,1.5)]:
    note("b01-horns-long", p, b, off, dur-.05, 74)
for bar in [37, 41, 44]:
    note("p01-timpani-hits", 38 if bar!=44 else 45, bar, 0, .6, 68)
note("p04-suspended-cymbal",41,44,1.5,.8,53)


# Ten-bar sanctuary: withdraw short strings, brass and drums; clarify the Dorian B.
theme("w04-clarinets-long",45,transpose=-12,vel=61,variant=1)
for bar in range(45,55):
    root,pcs=CHORDS[HARMONY[bar]]
    if bar%2:
        note("s06-violas-long",nearest(pcs,57,50,65),bar,duration=5.65,velocity=49)
        note("s08-cellos-long",root+12,bar,duration=5.55,velocity=48)
    for i,off in enumerate([0,.75,1.5,2.25]):
        arp=sorted(candidates(pcs,57,81))
        note("k01-harp",arp[[0,2,4,3][i]],bar,off,1.1,43+i%2)
for b,p in [(46,86),(49,83),(52,81),(54,86)]:
    note("k02-celeste",p,b,1.5,1.25,42)
note("w04-clarinets-long",71,53,0,1.4,62)
note("w04-clarinets-long",69,53,1.5,1.4,57)
note("w04-clarinets-long",62,54,0,2.3,56)


# Ascent: the same material is handed to horns at a lower octave.
theme("s01-violins1-long",55,vel=77,variant=1)
for i,events in enumerate(THEME[:4]):
    for off,p,dur in events:
        note("b01-horns-long",p-12,63+i,off,dur-.1,78+i*2)
for bar in range(63,71):
    root,pcs=CHORDS[HARMONY[bar]]
    note("w05-bassoons-long",root+12,bar,0,2.66,70)
    for i,off in enumerate([0,1.5]):
        note("p01-timpani-hits",38 if i==0 else 45,bar,off,.6,70+(bar-63)*3-i*8)
for bar in range(67,71):
    root,pcs=CHORDS[HARMONY[bar]]
    note("s02-violins1-tremolo",nearest(pcs,81,74,86),bar,duration=2.9,velocity=79+(bar-67)*4)
    for i in range(6):
        asc=[74,76,77,79,81,83,84,86,88,89,91,93]
        p=asc[min(i+(bar-67)*2,len(asc)-1)]
        note("w02-flutes-staccatissimo",p,bar,i*.5,.22,69+(bar-67)*4+i)
    for off in [0,1,1.5,2.5]:
        note("b02-horns-staccatissimo",nearest(pcs,62,55,72),bar,off,.27,76+(bar-67)*3)
note("p05-suspended-cymbal-roll",43,69,0,5.8,59)
for bar in [68,70]:
    for i in range(12):
        note("p03-snare",40,bar,i*.25,.1,43+i*3+(8 if bar==70 else 0))


# Epic statement, with countermelody and phrase breaths preserved.
theme("s01-violins1-long",71,vel=91)
theme("s01-violins1-long",79,vel=96,variant=1)
theme("b01-horns-long",71,transpose=-12,vel=86)
theme("b03-trumpets-long",79,transpose=-12,vel=91,variant=1)
for bar in range(71,93):
    root,pcs=CHORDS[HARMONY[bar]]
    if bar >= 79:
        # Horns now support, letting trumpets carry the late phrase.
        note("b01-horns-long",nearest(pcs,62,52,72),bar,0,2.63,83)
    for ident,target,lo,hi,vel in [
        ("b05-tenor-trombones-long",root+19,43,62,83),
        ("b06-bass-trombones-long",root+7,34,55,81),
        ("b07-tuba-long",root-12 if root>=40 else root,28,43,82),
    ]:
        if ident=="b07-tuba-long" and bar%2==0 and bar not in [86,92]:
            continue
        note(ident,nearest(pcs,target,lo,hi),bar,0,2.55 if bar%4==0 else 2.82,vel)
    if bar in [71,75,79,83,87,91]:
        note("p02-bass-drum",36,bar,0,.45,92+(bar-71)//4)
    elif bar%2:
        note("p02-bass-drum",36,bar,1.5,.38,78)
    for off,p,vel in [(0,38,89),(1.5,45,79)]:
        note("p01-timpani-hits",p,bar,off,.58,vel+(bar-71)//4)
    if bar not in [78,86,92]:
        for off,vel in [(0,72),(1,47),(1.5,79),(2.5,51)]:
            if bar==85 and off>=1.5:
                continue
            note("p03-snare",40,bar,off,.14,vel)
    if bar in [78,85,92]:
        for i in range(6):
            note("p03-snare",40,bar,1.5+i*.25,.10,54+i*5)
    if bar in [71,79,87]:
        note("p06-piatti",59,bar,0,.8,84+(bar-71)//4)
    if bar%4==1:
        for i,off in enumerate([0,.5,1,1.5,2,2.5]):
            arp=sorted(candidates(pcs,62,86))
            note("k01-harp",arp[[0,2,4,5,4,2][i]],bar,off,.85,64+i%3)
for b,p,dur in [(73,91,1.2),(77,95,1.2),(81,91,1.5),(85,93,1.5),
                (87,86,2.4),(89,88,2.4),(91,95,2.5)]:
    note("w06-piccolo-long",p,b,0,dur,79)
for b,p in [(73,83),(77,83),(81,86),(85,88),(87,86),(91,95)]:
    note("k03-glockenspiel",p,b,0,.8,66)
for b in [71,87]:
    note("k04-tubular-bells",62,b,0,2.5,81)
for bar in [74,78]:
    for off,p in [(1.5,69),(2,71),(2.5,74)]:
        note("b04-trumpets-staccatissimo",p,bar,off,.24,86)
for bar in [82,86]:
    for off,p in [(1.5,62),(2,65),(2.5,69)]:
        note("b02-horns-staccatissimo",p,bar,off,.26,87)


# Broad final six-bar arc, not a third copy of the eight-bar melody.
for b,p,off,dur in [(87,86,0,2.9),(88,89,0,2.9),(89,88,0,2.9),
                    (90,86,0,2.9),(91,95,0,1.5),(91,93,1.5,1.5),
                    (92,91,0,1.5),(92,88,1.5,1.5)]:
    note("s01-violins1-long",p,b,off,dur-.02,100)
    note("b03-trumpets-long",p-12,b,off,dur-.10,96)
    if b in [87,89,91]:
        note("w01-flutes-long",p,b,off,min(dur-.1,2.7),88)
note("p05-suspended-cymbal-roll",43,91,0,5.8,75)


# Final D minor tonic. Its arrival is the epic ending; two bars then allow release.
for ident,p,vel in [
    ("s01-violins1-long",86,105),("s03-violins2-long",81,95),
    ("s06-violas-long",65,93),("s08-cellos-long",50,95),("s11-basses-long",38,92),
    ("w01-flutes-long",86,92),("w03-oboes-long",77,84),("w04-clarinets-long",69,84),
    ("w05-bassoons-long",50,84),("w06-piccolo-long",86,84),
    ("b01-horns-long",69,99),("b03-trumpets-long",74,102),
    ("b05-tenor-trombones-long",65,97),("b06-bass-trombones-long",50,95),
    ("b07-tuba-long",38,95),
]:
    note(ident,p,93,0,5.55 if ident.startswith("s") else 5.3,vel)
for ident,p,vel,dur in [("p01-timpani-hits",38,108,.9),("p02-bass-drum",36,112,.7),
    ("p06-piatti",59,107,1),("k04-tubular-bells",62,94,3),
    ("k03-glockenspiel",86,77,1.2)]:
    note(ident,p,93,0,dur,vel)
for i,p in enumerate([50,57,62,65,69,74,77,81]):
    note("k01-harp",p,93,i*.25,2.0,76-i)


# CC1 carries the large arc; CC11 only a restrained phrase envelope. In Discover
# both affect level, so two deep identical curves would double-attenuate the sound.
ENERGY_POINTS = [(0,50),(33,60),(36,64),(81,71),(84,76),(126,81),(129,72),
    (132,49),(159,54),(162,66),(192,79),(207,98),(210,103),
    (231,107),(234,109),(255,113),(258,114),(273,119),(276,122),
    (278,117),(281.5,104),(288,104)]


def lerp(points,t):
    for (a,va),(b,vb) in zip(points,points[1:]):
        if a<=t<=b:
            x=(t-a)/(b-a)
            x=x*x*(3-2*x)
            return va+(vb-va)*x
    return points[-1][1]


GATE_ADJUSTMENTS=[]
for li,(ident,raw) in enumerate(LAYERS.items()):
    raw["notes"].sort(key=lambda n:(n["start"],n["pitch"]))
    assert raw["notes"], ident
    # A repeated pluck retriggers the same voice; release it before the next hit.
    next_start={}
    for n in reversed(raw["notes"]):
        p=n["pitch"]
        if p in next_start and n["start"]+n["duration"]>next_start[p]:
            assert BINDINGS[ident]["family"] == "keys", (ident,n)
            before=n["duration"]
            n["duration"]=round(next_start[p]-n["start"]-.02,5)
            assert n["duration"]>0
            GATE_ADJUSTMENTS.append(dict(layer=ident,pitch=p,start=n["start"],
                                         before=before,after=n["duration"]))
        next_start[p]=n["start"]
    # Curves cover active phrases plus their short releases; no random CC jitter.
    spans=[(n["start"],min(TOTAL,n["start"]+n["duration"]+.28)) for n in raw["notes"]]
    merged=[]
    for a,b in sorted(spans):
        if merged and a<=merged[-1][1]+.5:
            merged[-1][1]=max(merged[-1][1],b)
        else:
            merged.append([a,b])
    points={0.0}
    for a,b in merged:
        points.add(round(max(0,a-.125),5))
        for step in range(math.ceil(a*8),math.floor(b*8)+1):
            points.add(step/8)
    changes=[]
    last={}
    is_long=BINDINGS[ident]["articulation"] in ("Long","Tremolo")
    is_roll=ident=="p05-suspended-cymbal-roll"
    for t in sorted(points):
        phase=(t+li*.33)/12*2*math.pi
        base=lerp(ENERGY_POINTS,t)
        c1=round(base+(3*math.sin(phase) if is_long else 0))
        c11=round(108+8*math.sin(phase-.4)) if is_long else 116
        if is_roll:
            note_start=max([n["start"] for n in raw["notes"] if n["start"]<=t] or [0])
            x=max(0,min(1,(t-note_start)/5.8))
            c1=round(45+70*x)
            c11=round(102+12*x)
        for control,value in [(1,c1),(11,c11)]:
            value=max(28,min(124,value))
            if last.get(control)!=value:
                changes.append(dict(start=t,control=control,value=value))
                last[control]=value
    raw["control_changes"]=changes


SECTIONS=[("Whispering Lanterns",1,12,"fragment",2),
    ("The Hidden Path",13,16,"new",4),("The Quest",29,16,"vary",6),
    ("Sanctuary",45,10,"vary",2),("The Gate Awakens",55,16,"fragment",7),
    ("Banner of Dawn",71,16,"recap",9),("The Lantern Gate",87,8,"extend",10),
    ("Hall Release",95,2,"contract",0)]
source=dict(version=1,title="The Lantern Gate",tempo_bpm=BPM,time_signature=[6,8],
    bars=BARS,ticks_per_beat=PPQN,timing=dict(mode="strict",grid_division=16),
    description="BBCSO Discover orchestral fantasy in D Dorian, with a thematic epic ending.",
    prompt="Orkestra dinamis dan natural; Dorian; awal fantasy, akhir epic; MIDI saja. Discover gratis; satu track khusus setiap artikulasi.",
    assumptions=["D Dorian: D E F G A B C; final chord D minor.",
        "108 quarter-note BPM = 72 dotted-quarter BPM in 6/8; 96 bars = 160 seconds.",
        "Strict on-grid without swing; natural shaping through phrase rests, velocity, gate, CC1/CC11 and changing orchestration.",
        "BBCSO Discover only; separate fixed-articulation instances; no keyswitch or native presets requested.",
        "Untuned Percussion follows Discover's documented map, standard middle C=60; local plugin preference defaultMiddleCIsC4=1.",
        "Final two bars are release space; no MIDI notes begin after bar 93.",
        "Seed 20261014; no audio render, live Cubase import or listening claim."],
    sections=[dict(name=name,start=(start-1)*3) for name,start,_,_,_ in SECTIONS],
    layers=list(LAYERS.values()))
(HERE/"composition.json").write_text(json.dumps(source,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
(HERE/"bbcso-bindings.json").write_text(json.dumps(BINDINGS,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
(HERE/"harmony.json").write_text(json.dumps(HARMONY,indent=2)+"\n",encoding="utf-8")
(HERE/"gate-adjustments.json").write_text(json.dumps(GATE_ADJUSTMENTS,indent=2)+"\n",encoding="utf-8")
print(json.dumps(dict(layers=len(LAYERS),notes=sum(len(x["notes"]) for x in LAYERS.values()),
    cc_events=sum(len(x["control_changes"]) for x in LAYERS.values()),bars=BARS,seconds=160)))
