"""Reharmonize/recompose v002 with unchanged instruments, presets and drums.

No random onset offsets. All attacks share a straight 1/16 grid.
Run with uv run python; writes only the source composition and harmonic plan.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'src/midi_creator/spec.py').is_file())
PROJECT = ROOT / 'projects/20261011-neon-di-ujung-malam'
ORIGIN = PROJECT / 'v002'
SEED = 2026101103
RNG = random.Random(SEED)
source = json.loads((ORIGIN / '_internal/composition.json').read_text(encoding='utf-8'))
spec = deepcopy(source)
layers = {layer['id']: layer for layer in spec['layers']}
for layer in spec['layers']:
    if layer['kind'] != 'drums':
        layer['notes'] = []

# Explicit voicings: descending chromatic verse bass, then diatonic descent
# into a raised-third dominant with a flat ninth. Registers avoid bass doubling.
CHORDS = {
    'F#m9': (30, [57,61,64,68], [64,68,69,73], [6,9,1,4,8]),
    'F#m(maj9)/E#': (29, [54,57,61,65,68], [65,68,69,73], [6,9,1,5,8]),
    'F#m7/E': (28, [57,61,64,66], [64,66,69,73], [6,9,1,4]),
    'E(add9)': (28, [56,59,64,66], [64,66,68,71], [4,8,11,6]),
    'Dmaj7': (26, [57,61,62,66], [62,66,69,73], [2,6,9,1]),
    'C#7(b9)': (25, [56,59,62,65], [61,65,71,74], [1,5,8,11,2]),
    'Bm9': (35, [57,61,62,66], [62,66,69,73], [11,2,6,9,1]),
    'Gmaj7(#11)': (31, [55,59,61,66], [62,66,67,71], [7,11,2,6,1]),
    'F#m(add9)/A': (33, [57,61,66,68], [61,66,68,69], [6,9,1,8]),
    'F#m(add9)': (30, [57,61,66,68], [61,66,68,69], [6,9,1,8]),
}
VERSE = ['F#m9', 'F#m(maj9)/E#', 'F#m7/E', 'Dmaj7']
CHORUS = ['F#m9', 'E(add9)', 'Dmaj7', 'C#7(b9)']
PRE = ['Bm9', 'Dmaj7', 'Gmaj7(#11)', 'C#7(b9)']
BRIDGE = ['Bm9', 'F#m(add9)/A', 'Gmaj7(#11)', 'C#7(b9)']

def section(bar):
    return max((s for s in spec['sections'] if s['start'] <= bar*4), key=lambda s: s['start'])

def chord(bar):
    name = section(bar)['name']
    start = section(bar)['start'] // 4
    if bar >= 104:
        return 'F#m(add9)' if bar in (104,105) else 'F#m9'
    if bar >= 100:
        return ['Bm9', 'Gmaj7(#11)', 'C#7(b9)', 'F#m9'][bar-100]
    progression = (VERSE if name.startswith('Verse') or name == 'Interlude' else
                   PRE if name.startswith('Pre') else BRIDGE if name == 'Breakdown' else CHORUS)
    return progression[((bar-int(start))//2)%4]

def note(layer, pitch, start, duration, velocity):
    assert abs(start*4-round(start*4)) < 1e-8, (layer, start)
    assert 0 <= start < 432 and start+duration <= 432, (layer, start, duration)
    layers[layer]['notes'].append(dict(pitch=pitch,start=start,duration=duration,
                                      velocity=max(1,min(127,velocity+RNG.randint(-3,3)))))

def chord_span(bar):
    return 1 if 100 <= bar <= 103 else 2

for bar in range(0,108):
    if bar < 100 and bar%2 or bar>=104 and bar%2:
        continue
    name = section(bar)['name']
    dur = 4*chord_span(bar)-.4
    vel = 63 if name.startswith('Verse') else 70 if 'chorus' in name.lower() else 55
    for pitch in CHORDS[chord(bar)][1]:
        note('midnight-pad', pitch, bar*4, dur, vel)

# Bass is rooted in the same harmonic map; verse line moves F#-E#-E-D.
for bar in range(4,108):
    name = section(bar)['name']
    root = CHORDS[chord(bar)][0]
    if bar >= 104:
        if bar == 104:
            note('pulse-bass',root,bar*4,15.4,61)
        continue
    if name in ('Intro','Interlude','Breakdown'):
        if bar%2 == 0:
            note('pulse-bass',root,bar*4,7.25,70)
        continue
    chorus = name in ('Chorus 1','Final chorus')
    hits = [(i*.5+.25, .22, 12 if i in (2,6) else 0) for i in range(8)] if chorus else [
        (0,.65,0),(.75,.32,0),(1.5,.42,12),(2.75,.42,0),(3.5,.32,0)]
    if name.startswith('Pre'):
        hits.append((2,.4,0))
    if bar in (47,103):
        hits = [h for h in hits if h[0] < 3]
    for i,(off,dur,octave) in enumerate(hits):
        note('pulse-bass',root+octave,bar*4+off,dur,94 if chorus and i%2==0 else 79)

for bar in range(8,104):
    name = section(bar)['name']
    if name in ('Interlude','Breakdown'):
        continue
    chorus = name in ('Chorus 1','Final chorus')
    hits = [(.5,.5),(1.75,.35),(2.5,.5),(3.5,.3)] if chorus else [(.5,.48),(2,.6),(3.25,.4)] if name.startswith('Pre') else [(1.5,.6),(3.25,.4)] if bar%2 else [(.75,.6)]
    for off,dur in hits:
        for pitch in CHORDS[chord(bar)][2]:
            note('neon-chords',pitch,bar*4+off,dur,80 if chorus else 59)

# Arp descending cells, shared eighth pulse, reduced on hook attacks.
for bar in range(4,106):
    name = section(bar)['name']
    if name.startswith('Verse') and bar%4 < 2 or name=='Breakdown' and bar<84:
        continue
    upper = CHORDS[chord(bar)][2]
    pattern = [3,2,1,0,2,1,0,1] if bar%2==0 else [2,1,3,1,0,1,2,0]
    fast = name.startswith('Pre') or name in ('Chorus 1','Final chorus')
    for i in range(8 if fast else 4):
        off = i*(.5 if fast else 1)
        # Choruses leave two eighths open each bar for the descending hook.
        if name in ('Chorus 1','Final chorus') and i in (1,4):
            continue
        note('glass-arp',upper[pattern[i]]+12,bar*4+off,.18 if fast else .3,
             61 if i%2==0 else 48)

# New eight-bar hook: downwards phrases, minor third and ninth, dominant
# D->C# / E#->F# resolution. It does not transpose the previous hook.
HOOK = [
    [(.5,73,.6),(1.5,69,.6),(2.5,68,1.0)],
    [(.5,69,.7),(1.75,66,1.35)],
    [(.5,71,.6),(1.5,68,.6),(2.5,66,.9)],
    [(.5,68,.65),(1.75,64,1.4)],
    [(.5,69,.6),(1.5,66,.6),(2.5,61,1.0)],
    [(.5,66,.65),(1.75,62,1.35)],
    [(.5,68,.6),(1.5,65,.65),(2.5,62,.65),(3.25,61,.45)],
    [(.5,65,.65),(1.75,68,.6),(3.25,65,.45)],
]
CADENCE = [
    [(.5,69,.6),(1.5,66,.6),(2.5,61,.9)],
    [(.5,67,.6),(1.5,66,.7),(2.75,62,.7)],
    [(.5,68,.6),(1.5,65,.65),(2.5,62,.5),(3.25,61,.4)],
    [(0,66,1.5),(2,68,.5),(3,66,.6)],
]
for start in (32,40,88,96):
    for i,phrase in enumerate(HOOK):
        bar = start+i
        if bar>=100:
            phrase = CADENCE[bar-100]
        for off,pitch,dur in phrase:
            note('night-hook',pitch,bar*4+off,dur,86 if start<88 else 91)

for bar in (6,50):
    teaser = [(.5,68,.65),(1.75,65,.8),(3,62,.6)] if bar==6 else [(.5,69,.65),(1.75,66,.8),(3,61,.6)]
    for off,pitch,dur in teaser:
        note('night-hook',pitch,bar*4+off,dur,58)
for start in (24,72):
    # Bm9 -> Dmaj7 -> borrowed Gmaj7 -> C#7b9, increasingly tense.
    for baroff,pitch in [(0,66),(2,69),(4,67),(6,65)]:
        note('night-hook',pitch,(start+baroff)*4+.5,2.4,68+baroff)
    note('night-hook',62,(start+7)*4+2,.65,73)
for bar,phrase in [(80,[(.5,66,1.3),(2.5,62,1)]),
                   (82,[(.5,68,1.2),(2.5,66,1)]),
                   (84,[(.5,67,1.4),(2.75,66,.8)]),
                   (86,[(.5,65,1.5),(2.75,62,.7)])]:
    for off,pitch,dur in phrase:
        note('night-hook',pitch,bar*4+off,dur,58)
note('night-hook',66,104*4+.5,2.5,55)

# Short answers in the harmonic cell where they begin; never cross a change.
for start,end in [(8,24),(48,72),(80,88)]:
    for bar in range(start,end,2):
        upper=CHORDS[chord(bar)][2]
        for off,pitch,dur in [(2.5,upper[2],.7),(4.5,upper[1],.9),(6.25,upper[0],1.1)]:
            note('rain-keys',pitch,bar*4+off,dur,60 if bar>=56 else 53)
for bar in (35,39,43,47,91,95,99,103):
    upper=CHORDS[chord(bar)][2]
    for off,pitch in [(3,upper[1]),(3.5,upper[0])]:
        note('rain-keys',pitch,bar*4+off,.3,47)

# C# is common to most chords; altered G section selects its fifth D instead.
for bar in (0,4,24,48,52,72,80,84,104):
    pitch = 74 if chord(bar)=='Gmaj7(#11)' else 73
    note('radio-haze',pitch,bar*4,7.5 if bar!=104 else 15.4,44 if bar<104 else 36)

for layer in spec['layers']:
    layer['notes'].sort(key=lambda n:(n['start'],n['pitch']))
spec.update(
    description='Rekomposisi dark synth-pop melankolis: bass kromatis menurun, minor-major colour, borrowed bII and dominant flat ninth; restrained descending original hook.',
    prompt='tulis ulang midi projek 20261011-neon-di-ujung-malam dengan menggunakan progresi yang lebih dark dan sedih ala the weeknd, tetap dengan instrumen yang sama',
    timing={'mode':'strict','grid_division':16},
    assumptions=[
        'Revisi v003 dari v002; tujuh layer tonal ditulis ulang, drum v002 dipertahankan byte-identik.',
        '118 BPM, F# minor, 4/4, 112 bar, 960 PPQN dan bentuk lagu tetap; empat bar akhir kosong untuk release.',
        'Tujuh preset native Serum 2 dipakai ulang tanpa modifikasi; kit/sample drum tetap pilihan pengguna.',
        'Referensi atmosfer dark synth-pop; harmoni dan motif asli, tanpa mengambil melodi lagu tertentu.',
        f'Seed velocity {SEED}; onset strict 1/16, tanpa jitter atau swing antarlayer.',
        'Verse memakai E# sebagai bass kromatis; Gmaj7(#11) pre/breakdown adalah borrowed bII, C#7(b9) memakai E# dan D sebagai tegangan.',
        'Register bass 25-47 lebih rendah pada jalur turun; mono pulse Serum yang sama digunakan.',
    ])

plan = [{'bar_start':bar+1,'bars':chord_span(bar),'chord':chord(bar),
         'bass_midi':CHORDS[chord(bar)][0],'pad_voicing':CHORDS[chord(bar)][1],
         'stab_voicing':CHORDS[chord(bar)][2], 'pitch_classes':CHORDS[chord(bar)][3]}
        for bar in range(108) if (bar%2==0 or 100<=bar<=103)]
(HERE/'composition.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'harmonic-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'revision-origin.json').write_text(json.dumps({
    'origin':'v002','seed':SEED,
    'sha256':{p.relative_to(ORIGIN).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
              for p in ORIGIN.rglob('*') if p.is_file()}},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'layers':{l['id']:len(l['notes']) for l in spec['layers']},'seed':SEED},indent=2))
