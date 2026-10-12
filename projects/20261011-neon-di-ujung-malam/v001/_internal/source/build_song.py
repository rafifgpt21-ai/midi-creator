"""Reproduce Neon di Ujung Malam. Quarter-note beats; fixed seed 20261011."""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
RNG = random.Random(20261011)
BARS = 112
SECTIONS = [(0,8,'Intro'), (8,24,'Verse 1'), (24,32,'Pre-chorus 1'),
            (32,48,'Chorus 1'), (48,56,'Interlude'), (56,72,'Verse 2'),
            (72,80,'Pre-chorus 2'), (80,88,'Breakdown'),
            (88,104,'Final chorus'), (104,112,'Outro / release')]
CHORDS = {
    'F#m9': (30,[57,61,64,68],[66,69,73,76]),
    'Dmaj7': (38,[57,61,62,66],[66,69,73,74]),
    'Aadd9': (33,[57,59,61,64],[64,69,71,73]),
    'E6': (40,[56,59,61,64],[64,68,71,73]),
    'Bm7': (35,[57,59,62,66],[66,69,71,74]),
    'C#7': (37,[56,59,61,65],[65,68,71,73]),
    'F#m': (30,[57,61,66],[66,69,73]),
}
CORE = ['F#m9','Dmaj7','Aadd9','E6']
PRE = ['Bm7','Dmaj7','E6','C#7']
BRIDGE = ['Bm7','F#m9','Dmaj7','C#7']

def section(bar):
    return next((start,end,name) for start,end,name in SECTIONS if start<=bar<end)

def chord(bar):
    start,end,name = section(bar)
    if bar>=104:
        return 'F#m9'
    if bar>=100:
        return ['Bm7','C#7','F#m','F#m'][bar-100]
    progression = PRE if name.startswith('Pre') else BRIDGE if name=='Breakdown' else CORE
    return progression[((bar-start)//2)%4]

LAYERS = {}
def layer(id,name,role,program,volume,pan):
    data = dict(id=id,name=name,kind='melodic',role=role,program=program,volume=volume,pan=pan,notes=[])
    LAYERS[id] = data

layer('pulse-bass','Pulse Bass','bass',38,101,64)
layer('midnight-pad','Midnight Pad','harmony',89,73,64)
layer('neon-chords','Neon Chords','harmony',62,82,58)
layer('glass-arp','Glass Arp','arpeggio',81,68,79)
layer('night-hook','Night Hook','melody',80,94,64)
layer('rain-keys','Rain Keys','countermelody',4,72,47)
layer('radio-haze','Radio Haze','texture',95,56,68)
LAYERS['retro-drums'] = dict(id='retro-drums',name='Retro Drum Kit',kind='drums',role='percussion',channel=10,volume=106,pan=64,notes=[])

def note(id,pitch,start,duration,velocity,jitter=False):
    if jitter:
        start += RNG.choice([0,.002,.004,.006])
    assert start>=0 and start+duration<=BARS*4
    LAYERS[id]['notes'].append(dict(pitch=pitch,start=round(start,6),duration=round(duration,6),velocity=max(1,min(127,velocity+RNG.randint(-3,3)))))

# Warm low-mid voicings leave the bass and hook their own registers.
for bar in range(0,108,2):
    _,end,name = section(bar)
    dur=7.52 if bar<100 else 3.52
    if 100<=bar<104:
        continue
    pitches = CHORDS[chord(bar)][1]
    vel=66 if name.startswith('Verse') else 76 if 'chorus' in name.lower() else 58
    for p in pitches:
        note('midnight-pad',p,bar*4,dur,vel)
# Exact cadence, followed by over eight seconds of empty MIDI tail.
for bar in (100,101,102,103):
    for p in CHORDS[chord(bar)][1]:
        note('midnight-pad',p,bar*4,3.52,70 if bar<102 else 61)

for bar in range(4,108):
    start,end,name=section(bar)
    root=CHORDS[chord(bar)][0]
    if bar>=104:
        if bar==104:
            note('pulse-bass',30,bar*4,11.2,65)
        continue
    if name=='Intro' or name=='Breakdown' or name=='Interlude':
        if bar%2==0:
            note('pulse-bass',root,bar*4+.08,6.8,70 if name=='Breakdown' else 76)
        continue
    dance='Chorus' in name or 'chorus'==name.lower().split()[-1] and name.startswith('Final')
    if dance:
        hits=[(.25,0),(.75,0),(1.25,12),(1.75,0),(2.25,0),(2.75,0),(3.25,12),(3.75,0)]
        if bar in (47,103): hits=hits[:6]
        for i,(off,octave) in enumerate(hits):
            note('pulse-bass',root+octave,bar*4+off,.23,100 if i%2==0 else 86)
    else:
        hits=[(0,.62,0),(.875,.35,0),(1.5,.45,12),(2.75,.42,0),(3.5,.32,0)]
        if name.startswith('Pre'): hits += [(2,.4,0)]
        for off,dur,octave in hits:
            note('pulse-bass',root+octave,bar*4+off,dur,85 if not octave else 74)

# Syncopated chord stabs enter gradually and become broad in the chorus.
for bar in range(8,104):
    _,_,name=section(bar)
    if name in ('Interlude','Breakdown'): continue
    pitches=CHORDS[chord(bar)][2]
    chorus='Chorus' in name or name=='Final chorus'
    if chorus: hits=[(.5,.52),(1.75,.38),(2.5,.55),(3.5,.3)]
    elif name.startswith('Pre'): hits=[(.5,.48),(2,.62),(3.25,.42)]
    elif bar%2: hits=[(1.5,.62),(3.25,.42)]
    else: hits=[(.75,.62)]
    for off,dur in hits:
        for p in pitches: note('neon-chords',p,bar*4+off,dur,86 if chorus else 62,jitter=True)

# Arp is explicit MIDI, not a second arpeggiator inside Serum.
for bar in range(4,108):
    _,_,name=section(bar)
    if name.startswith('Verse') and (bar%4<2): continue
    if name=='Breakdown' and bar<84: continue
    if bar>=106: continue
    pitches=CHORDS[chord(bar)][2]
    pattern=[0,2,1,3,2,1,3,1]
    if bar%4==3: pattern=[0,1,2,3,1,2,3,2]
    fast=name.startswith('Pre') or name in ('Chorus 1','Final chorus')
    steps=8 if fast else 4
    for i in range(steps):
        off=i*(.5 if fast else 1)+.125
        pitch=pitches[pattern[i]%len(pitches)]+12
        vel=(69 if i%2==0 else 53)+(8 if name=='Final chorus' else 0)
        note('glass-arp',pitch,bar*4+off,.18 if fast else .32,vel)

# Original eight-bar melodic arc: short call, held answer, breath, rising reply.
HOOK=[
 [(0.5,73,.5),(1.25,76,.5),(2,78,1.25),(3.5,76,.35)],
 [(.25,73,.75),(1.5,69,1.4)],
 [(.5,73,.5),(1.25,74,.5),(2,78,.65),(3,76,.6)],
 [(0,73,1.5),(2.25,71,.5),(3,69,.6)],
 [(.5,71,.5),(1.25,73,.5),(2,76,1.25)],
 [(.25,73,.7),(1.5,71,.5),(2.25,69,.6)],
 [(.5,68,.5),(1.25,71,.5),(2,73,.6),(3,76,.55)],
 [(0,73,1.2),(1.75,71,.5),(2.5,68,.9)],
]
for start in (32,40,88,96):
    for i,phrase in enumerate(HOOK):
        bar=start+i
        for off,p,dur in phrase:
            # The last four bars use a dominant-to-tonic cadence.
            if bar==100 and p==76: p=74
            if bar==101 and p==69: p=68
            if bar in (102,103) and p in (68,71): p=69 if p==68 else 73
            note('night-hook',p,bar*4+off,dur,96 if start>=88 else 88)
# Teasers and a different, less busy pre-chorus melody.
for start in (6,50):
    for off,p,dur in [(0,73,.6),(1,71,.6),(2.5,68,1.1)]:
        note('night-hook',p,start*4+off,dur,63)
for start in (24,72):
    for baroff,p in [(0,71),(2,73),(4,76),(6,77)]:
        note('night-hook',p,(start+baroff)*4+.5,2.4,75+baroff)
    note('night-hook',68,(start+7)*4+2,.65,78)
# Breakdown quotes just the contour in a lower register.
for off,p,dur in [(0,66,1.25),(2,69,1),(5,73,1.4),(9,71,1.8),(13,69,1.5)]:
    note('night-hook',p,80*4+off,dur,61)

# Bell-like electric keys answer in the gaps; verse two adds variation.
for start,end in [(8,24),(48,72),(80,88)]:
    for bar in range(start,end,2):
        pitches=CHORDS[chord(bar)][2]
        for off,p,dur in [(2.5,pitches[2],.75),(4.5,pitches[1],1.0),(6,pitches[0],1.2)]:
            note('rain-keys',p,bar*4+off,dur,65 if bar>=56 else 57)
        if 64<=bar<72: note('rain-keys',pitches[3],bar*4+7.25,.5,58)
for bar in (35,39,43,47,91,95,99,103):
    for off,p in [(3,CHORDS[chord(bar)][2][0]),(3.5,CHORDS[chord(bar)][2][1])]:
        note('rain-keys',p,bar*4+off,.3,50)

# Quiet tonal haze, not sampled speech or a copied radio intro.
for bar,dur in [(0,14),(4,13),(24,12),(48,14),(52,12),(72,12),(80,14),(84,12),(104,14)]:
    p=CHORDS[chord(bar)][1][-1]+12
    note('radio-haze',p,bar*4,dur,48 if bar<104 else 39)

def drum(p,b,off,vel,dur=.1): note('retro-drums',p,b*4+off,dur,vel,jitter=p in (38,39,42,46,82))
for bar in range(6,108):
    start,end,name=section(bar)
    if name=='Intro':
        for off in (1,3): drum(42,bar,off,43)
        continue
    if name=='Interlude':
        if bar>=52:
            for off in (0,2): drum(36,bar,off,78)
            drum(38,bar,3,70)
            for off in (.5,1.5,2.5,3.5): drum(42,bar,off,48)
        continue
    if name=='Breakdown':
        if bar>=84:
            drum(36,bar,0,78)
            drum(38,bar,3,76)
            for off in (0,.5,1,1.5,2,2.5,3,3.5): drum(42,bar,off,45+3*(bar-84))
        continue
    if name.startswith('Outro'):
        if bar<106:
            for off in (0,2): drum(36,bar,off,75)
            drum(38,bar,3,67)
            for off in (.5,1.5,2.5,3.5): drum(42,bar,off,44)
        continue
    chorus=name in ('Chorus 1','Final chorus')
    kickhits=[0,1,2,3] if chorus else [0,1.5,2.75]
    if name.startswith('Pre'): kickhits=[0,1,2,2.75]
    if bar in (31,79,87): kickhits=[0,1,2]
    for off in kickhits: drum(36,bar,off,110 if chorus else 94)
    for off in (1,3):
        drum(38,bar,off,105 if chorus else 89)
        if chorus: drum(39,bar,off+.018,76)
    for i in range(8):
        off=i*.5+(.018 if i%2 else 0)
        pitch=46 if chorus and i in (3,7) else 42
        drum(pitch,bar,off,72 if i%2 else 50,.18 if pitch==46 else .08)
    if name=='Final chorus' or (name=='Verse 2' and bar>=64):
        for i in range(8): drum(82,bar,i*.5+.25,48 if i%2 else 34,.055)
    if bar in (32,40,88,96): drum(49,bar,0,83,.4)
    if bar%8==7 and bar not in (31,79):
        drum(38,bar,2.5,43)
        # Four small snare pickups, with the ordinary backbeat retained.
        for off,vel in [(3.25,52),(3.5,62),(3.75,73)]: drum(38,bar,off,vel,.08)
    if bar in (31,79):
        for off,vel in [(2.5,52),(2.75,62),(3.25,71),(3.5,78),(3.75,85)]: drum(38,bar,off,vel,.08)

# Sort notes, enforce same-pitch non-overlap independently of the CLI.
for data in LAYERS.values():
    data['notes'].sort(key=lambda n:(n['start'],n['pitch']))
    ends={}
    for n in data['notes']:
        assert n['start']>=ends.get(n['pitch'],-1), (data['id'],n)
        ends[n['pitch']]=n['start']+n['duration']

spec=dict(version=1,title='Neon di Ujung Malam',tempo_bpm=118,time_signature=[4,4],
          bars=BARS,ticks_per_beat=960,key_signature='F#m',
          description='Original instrumental dark synth-pop: nocturnal space, analog pulse, restrained verses and dance choruses.',
          prompt='coba buatkan lagu seperti lagunya the weeknd pada album dawn FM dan after hour (dark synth music),',
          assumptions=['Instrumental, tanpa vokal atau lirik.', '118 BPM, F# minor, 112 bar; 4 bar akhir kosong untuk release.',
                       '7 instrumen Serum 2 dan satu kit drum MIDI; sample drum dipilih pengguna.',
                       'Referensi digunakan untuk atmosfer; motif dan aransemen ditulis baru.',
                       'Random seed 20261011; timing humanization kecil pada chord dan percussion.'],
          sections=[dict(name=name,start=start*4) for start,end,name in SECTIONS],layers=list(LAYERS.values()))
(HERE/'composition.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(title=spec['title'],bars=BARS,seconds=BARS*4*60/118,notes={k:len(v['notes']) for k,v in LAYERS.items()}),indent=2))
