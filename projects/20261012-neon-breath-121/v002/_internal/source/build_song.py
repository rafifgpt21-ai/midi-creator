"""Develop v001 into a deterministic 168-bar instrumental song at 121 BPM."""
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = next(p for p in HERE.parents if (p/'v001/_internal/composition.json').exists())
BASE = json.loads((PROJECT/'v001/_internal/composition.json').read_text(encoding='utf-8'))
LAYERS = deepcopy(BASE['layers'])
BY_ID = {l['id']: l for l in LAYERS}
for layer in LAYERS: layer['notes'] = []
IDS = [l['id'] for l in LAYERS]
SUB, BASS, STAB, BRASS, ARP, BELL, PAD, LEAD, ANSWER, FX = IDS[:10]
KICK, SNARE, CLAP, CH, OH, SHAKER, CRASH = IDS[10:]
BASE_NOTES = {l['id']: l['notes'] for l in BASE['layers']}

# Boundaries always start on the Cm of the original four-bar progression.
SECTIONS = [
    ('Intro', 1, 16, 'intro', .62),
    ('Verse 1', 17, 32, 'verse', .76),
    ('Pre-Chorus 1', 33, 40, 'pre', .88),
    ('Chorus 1', 41, 56, 'chorus', 1.00),
    ('Post-Chorus', 57, 64, 'post', .84),
    ('Verse 2', 65, 80, 'verse2', .82),
    ('Pre-Chorus 2', 81, 88, 'pre2', .94),
    ('Chorus 2', 89, 104, 'chorus2', 1.03),
    ('Breakdown', 105, 120, 'break', .63),
    ('Build', 121, 128, 'build', .90),
    ('Final Chorus', 129, 152, 'final', 1.06),
    ('Outro', 153, 168, 'outro', .68),
]
ROOTS = [24, 29, 32, 34]
BASS_PAIRS = [(36,48), (29,41), (32,44), (34,46)]
STAB_VOICES = [[48,55,58,63], [48,53,56,63], [48,55,56,63], [55,58,62,65]]
BRASS_VOICES = [[48,51,55], [48,53,56], [48,51,56], [50,53,58]]
ARP_VOICES = [[60,63,67,72], [65,68,72,77], [68,72,75,80], [70,74,77,82]]
PAD_VOICES = [[51,55,60], [53,56,60], [51,56,60], [53,58,62]]
PAD_BARS = {}
EVENTS = {ident: {} for ident in IDS}

def put(ident, pitch, bar, step, duration, velocity):
    start = (bar-1)*4 + step*.25
    assert 1 <= velocity <= 127 and duration > 0
    key = (pitch, start)
    event = dict(pitch=pitch, start=start, duration=round(duration,6), velocity=int(velocity))
    if key in EVENTS[ident]:
        # A fill can accent an existing backbeat without duplicating it.
        prior = EVENTS[ident][key]
        prior['velocity'] = max(prior['velocity'], event['velocity'])
        prior['duration'] = max(prior['duration'], event['duration'])
    else: EVENTS[ident][key] = event

def chord(ident, notes, bar, step, duration, velocity):
    for i,pitch in enumerate(notes): put(ident,pitch,bar,step,duration,max(1,velocity-i*2))

def vel(base, intensity): return max(1,min(127,round(base*intensity)))

def copy_bar(ident, source_index, bar, intensity=1, predicate=None, transform=None):
    for n in BASE_NOTES[ident]:
        if int(n['start']//4) != source_index: continue
        local = n['start'] - source_index*4
        if predicate and not predicate(n, local): continue
        pitch = transform(n['pitch'], local) if transform else n['pitch']
        put(ident,pitch,bar,round(local*4),n['duration'],vel(n['velocity'],intensity))

def bass_bar(bar, ci, rate, intensity, variant=0, fill=False):
    lo,hi = BASS_PAIRS[ci]
    steps = list(range(0,16,2)) if rate==8 else list(range(16))
    pattern = [0,1]*8 if variant%3==0 else [0,1,0,1,0,0,1,1,0,1,0,1,0,1,1,0]
    for j,s in enumerate(steps):
        pitch = [lo,hi][pattern[j]]
        if fill and s >= 12: pitch = [lo,lo+7,hi,lo+7][s-12]
        put(BASS,pitch,bar,s,.18 if rate==16 else .34,vel([108,84,96,86][j%4],intensity))

def arp_bar(bar, ci, mode, intensity, variant=0):
    patterns = [[0,1,2,3,2,1,0,1,2,3,2,1,0,1,2,1],
                [0,2,1,3,2,1,0,2,1,3,2,0,1,2,3,2],
                [3,2,1,0,1,2,3,2,1,0,1,2,3,2,1,2]]
    steps = range(16) if mode=='full' else range(0,16,2) if mode=='eighth' else [2,6,10,14]
    for s in steps:
        p = ARP_VOICES[ci][patterns[variant%3][s]]
        put(ARP,p,bar,s,.165,vel([84,65,73,67][s%4],intensity))

def hook_bar(bar,ci,intensity,variation):
    def change(p,local):
        if variation=='lift' and ci in (0,2) and local in (.75,1.0,2.0):
            return p+12 if p<=67 else p
        if variation=='answer' and ci==2 and local==3.5: return 68
        if variation=='answer' and ci==0 and local==3.5: return 67
        return p
    copy_bar(LEAD,ci,bar,intensity,transform=change)
    copy_bar(ANSWER,ci,bar,intensity)

def verse_lead(bar,ci,intensity,second=False):
    if ci in (0,2):
        copy_bar(LEAD,ci,bar,intensity,predicate=lambda n,t:t<1.75,
                 transform=(lambda p,t:p+12 if second and p==63 and t==.5 else p))
    elif (bar//4)%2==0 or second:
        copy_bar(ANSWER,ci,bar,intensity*.9)

def drums(bar,kind,local,total,intensity):
    kick_on = not (kind=='intro' and local<4) and not (kind=='break' and local<12) and not (kind=='outro' and local>=12)
    backbeat = not (kind=='intro' and local<8) and kind!='break' and not (kind=='outro' and local>=8)
    hats = kick_on
    full_hat = kind in ('pre','pre2','chorus','chorus2','final','build') or (kind=='verse2' and local>=8)
    open_hat = backbeat and not (kind=='intro' and local<12)
    shaker_on = kind in ('pre','pre2','chorus','chorus2','post','final') or (kind in ('verse2','build') and local>=4)
    if kick_on:
        for beat in range(4):
            if kind=='build' and local==total-1 and beat==3:continue
            put(KICK,60,bar,beat*4,.175,vel([117,109,113,108][beat],max(.84,intensity)))
    if backbeat:
        for s,v in [(4,105),(12,111)]:
            put(SNARE,60,bar,s,.1375,vel(v,intensity))
            if kind!='outro':put(CLAP,60,bar,s,.1375,vel(v-20,intensity))
    if kind=='build' and local>=4:
        for s in range(0,16,4):put(SNARE,60,bar,s,.12,vel(74+local*3,intensity))
    if hats:
        closed_steps=range(16) if full_hat else range(0,16,2)
        for s in closed_steps:
            if open_hat and s%4==2:continue
            put(CH,60,bar,s,.08,vel([72,49,68,56][s%4],intensity))
    if open_hat:
        for s in [2,6,10,14]:put(OH,60,bar,s,.175,vel(77 if s in [6,14] else 69,intensity))
    if shaker_on:
        for s in range(16):put(SHAKER,60,bar,s,.07,vel([43,34,61,39][s%4],intensity))
    # Phrase-end fills, all on the same straight 1/16 grid.
    if backbeat and local==total-1:
        for s in [10,11,12,13,14,15]:put(SNARE,60,bar,s,.12,vel(72+(s-10)*7,intensity))
        if kind in ('pre','pre2','build'):
            for s in [9,11,13,15]:put(CLAP,60,bar,s,.10,vel(63+s,intensity))

for name, first, last, kind, energy in SECTIONS:
    total=last-first+1
    for bar in range(first,last+1):
        local=bar-first;ci=(bar-1)%4;cycle=local//4
        intensity=energy
        if kind in ('pre','pre2','build'):intensity*=.87+.13*local/max(1,total-1)
        drums(bar,kind,local,total,intensity)
        pad_on=True;sub_on=True;rate=16;stab_steps=[2,6,9,14];arp_mode='full';bell_count=2;brass_on=False
        if kind=='intro':
            sub_on=local>=4;rate=8 if local<8 else 16
            stab_steps=[] if local<8 else [6,14]
            arp_mode=None if local<8 else 'eighth';bell_count=2 if local%2==0 else 0
            if local>=12 and ci in (0,2):
                copy_bar(LEAD,ci,bar,.67,predicate=lambda n,t:t<1.0)
        elif kind in ('verse','verse2'):
            rate=8 if kind=='verse2' and local<8 else 16
            stab_steps=[6,14] if cycle%2==0 else [2,9,14]
            arp_mode='space' if cycle%2==0 else 'eighth';bell_count=2 if ci in (1,3) else 0
            verse_lead(bar,ci,.80 if kind=='verse' else .87,kind=='verse2')
        elif kind in ('pre','pre2'):
            arp_mode='eighth' if local<4 else 'full';bell_count=0
            brass_on=local>=total-2
            # Rising chord tones, with the response window preserved.
            tones=ARP_VOICES[ci][:3]
            for s,p,d in [(0,tones[0],.57),(4,tones[1],.57),(8,tones[2],.50)]:
                put(LEAD,p,bar,s,d,vel(96,intensity))
            if ci in (1,3):copy_bar(ANSWER,ci,bar,intensity*.92)
        elif kind in ('chorus','chorus2','final'):
            brass_on=True;bell_count=3 if ci in (1,3) else 2
            variation='original' if cycle%3==0 else 'answer' if cycle%3==1 else 'lift'
            if kind=='chorus' and cycle<2:variation='original' if cycle==0 else 'answer'
            hook_bar(bar,ci,min(1.06,intensity),variation)
        elif kind=='post':
            brass_on=local==0;bell_count=4;arp_mode='full'
            if ci in (1,3):copy_bar(ANSWER,ci,bar,.92)
        elif kind=='break':
            sub_on=local>=8;rate=None;stab_steps=[];arp_mode=None if local<8 else 'space';bell_count=3
            if local in (0,4,8):
                put(LEAD,[67,68,72][local//4],bar,0,2,77)
            if local>=12:
                stab_steps=[6,14]
                if ci in (1,3):copy_bar(ANSWER,ci,bar,.76)
        elif kind=='build':
            rate=8 if local<4 else 16;arp_mode='eighth' if local<4 else 'full';bell_count=0
            stab_steps=[6,14] if local<4 else [2,6,9,14]
            brass_on=local==6
            # Reserve the last beat of the build for the upcoming final chorus.
            if local<6:
                for s,p in [(0,ARP_VOICES[ci][0]),(8,ARP_VOICES[ci][2])]:put(LEAD,p,bar,s,.70,vel(90,intensity))
        elif kind=='outro':
            if local>=13:continue
            rate=16 if local<4 else 8 if local<8 else None
            stab_steps=[6,14] if local<8 else []
            arp_mode='eighth' if local<4 else None;bell_count=2 if local<8 else 0
            if local<4 and ci in (0,2):copy_bar(LEAD,ci,bar,.82,predicate=lambda n,t:t<1.0)
            if local==12:
                # Final Cm at bar165, then three complete silent bars for tails.
                ci=0;brass_on=True;stab_steps=[0];rate=None;bell_count=0
                put(KICK,60,bar,0,.175,101)
                put(CRASH,60,bar,0,.25,66)
        if pad_on:PAD_BARS[bar]=(PAD_VOICES[ci],vel(70,max(.78,intensity)))
        if sub_on:put(SUB,ROOTS[ci],bar,0,4,100)
        if rate:bass_bar(bar,ci,rate,intensity,cycle,fill=local%8==7 and kind not in ('intro','outro'))
        for j,s in enumerate(stab_steps):chord(STAB,STAB_VOICES[ci],bar,s,.2875,vel([94,86,92,103][j%4],intensity))
        if brass_on:
            chord(BRASS,BRASS_VOICES[ci],bar,0,2 if kind!='outro' else 1.5,vel(104,intensity))
            if kind in ('chorus2','final') and local%8==7:
                chord(BRASS,BRASS_VOICES[ci],bar,10,.5,vel(91,intensity))
        if arp_mode:arp_bar(bar,ci,arp_mode,intensity,cycle)
        if bell_count:
            allowed=([.75,2.75] if bell_count==2 else [.25,1.75,3.75] if bell_count==3 else [.25,.75,2.25,3.75])
            copy_bar(BELL,ci,bar,max(.70,intensity*.90),predicate=lambda n,t:t in allowed)

# Tie unchanged common pad tones globally, splitting at section dynamics changes.
for p in sorted({pitch for voices,v in PAD_BARS.values() for pitch in voices}):
    bar=1
    while bar<=168:
        if bar not in PAD_BARS or p not in PAD_BARS[bar][0]:bar+=1;continue
        velocity=PAD_BARS[bar][1];end=bar+1
        while end in PAD_BARS and p in PAD_BARS[end][0] and PAD_BARS[end][1]==velocity:end+=1
        put(PAD,p,bar,0,(end-bar)*4,velocity)
        bar=end

# The retained native FX envelope rises for four bars: trigger only at transitions.
for bar in [13,37,85,101,125]:put(FX,60,bar,0,16,1)
for bar in [1,17,41,57,65,89,105,129,153,165]:put(FX,48,bar,0,1,127)
for bar in [9,17,41,57,65,89,129,153]:put(CRASH,60,bar,0,.25,98 if bar in [41,89,129] else 78)

for ident,layer in BY_ID.items():layer['notes']=sorted(EVENTS[ident].values(),key=lambda n:(n['start'],n['pitch']))
assumptions=[
    'Revision v002 develops the original v001 four-bar study into an instrumental song, 168 bars / approximately 5:33.',
    'Tempo121 BPM, Cm,4/4,480PPQN, strict straight1/16; no swing/randomization. Chord cycle Cm/Fm/Ab/Bb retained.',
    'Original ten native Serum2 presets are copied byte-for-byte; no sound/plugin parameters changed. Lead arrangement reaches MIDI79 in selected lifts.',
    'Cubase C3=MIDI60; approved sub C0/F0/Ab0/Bb0 remains MIDI24/29/32/34.',
    'Seven drum layers remain separate files, MIDI60/channel10; samples remain user-selected.',
    'Hook identity retained in choruses; verse fragments, answer variation and occasional octave lift create development.',
    'Kick is four-on-the-floor in groove sections; intro/breakdown have intentional rests, and build bar128 omits beat4 for the drop.',
    'Four-bar risers only before major transitions. FX velocity1/127 preserved; the native four-bar envelope is not stretched to song length.',
    'Final cadence Cm at bar165, note-offs by bar166, bars166-168 reserved for tails; every MIDI ends at bar169.',
    'Direct Sub still requires host LP80 and actual kick sidechain; delay topology and native audio behavior have not been auditioned.',
    'No CC fade automation or combined MIDI; outro reduces instruments and ends on Cm. No audio preview requested.'
]
composition=dict(version=1,title='Neon Breath — Full Song',description='168-bar Nu-Disco/Synthwave instrumental arrangement with section development, retained v001 synth sounds and separate drum files.',
    tempo_bpm=121,time_signature=[4,4],bars=168,ticks_per_beat=480,key_signature='Cm',timing=dict(mode='strict',grid_division=16),
    sections=[dict(name=name,start=(first-1)*4) for name,first,last,kind,energy in SECTIONS],
    assumptions=assumptions,layers=LAYERS)

def save(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save('composition.json',composition)
save('arrangement-plan.json',[dict(name=name,first_bar=first,last_bar=last,kind=kind,intensity=energy) for name,first,last,kind,energy in SECTIONS])
save('bindings.json',{ident:dict(plugin='Serum 2',preset=f'Presets/{ident}.SerumPreset') for ident in IDS[:10]})
print(json.dumps(dict(bars=168,seconds=168*4*60/121,layers=len(LAYERS),notes=sum(len(l['notes']) for l in LAYERS),
                     per_layer={l['id']:len(l['notes']) for l in LAYERS}),indent=2))
