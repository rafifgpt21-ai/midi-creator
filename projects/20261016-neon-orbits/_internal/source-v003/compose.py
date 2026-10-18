"""Coherence revision. Run from workspace root; baseline is immutable v002 input."""
from pathlib import Path
from fractions import Fraction
from copy import deepcopy
import json

HERE = Path(__file__).resolve().parent
def save(name, obj):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

spec = json.loads((HERE/'baseline-v002.json').read_text(encoding='utf8'))
layers = {x['id']: x for x in spec['layers']}
SCALE = {4,6,7,9,11,0,3}
CHORDS = {
    'Em': {'root':28, 'pad':[55,59,64], 'arp':[64,67,71]},
    'C':  {'root':36, 'pad':[55,60,64], 'arp':[64,67,72]},
    'Am': {'root':33, 'pad':[57,60,64], 'arp':[64,69,72]},
    'B':  {'root':35, 'pad':[54,59,63], 'arp':[63,66,71]},
}
def harmony(bar):
    if bar >= 161: return 'Em'
    if 33 <= bar <= 48 or 97 <= bar <= 112:
        first = 33 if bar < 81 else 97
        local = bar-first
        return 'B' if local >= 12 else ['Am','C','B','B'][(local//2)%4]
    if 81 <= bar <= 96:
        return ['C','Am','Em','B','Em','C','Am','B'][(bar-81)//2]
    first = next(s['start']/4+1 for s in reversed(spec['sections']) if s['start'] <= (bar-1)*4)
    return ['Em','C','Am','B'][((bar-int(first))//2)%4]

def add(lid, pitch, start, gate, vel):
    if layers[lid]['kind'] == 'melodic': assert pitch % 12 in SCALE
    layers[lid]['notes'].append(dict(pitch=pitch,start=round(float(start),9),duration=round(float(gate),9),velocity=vel))
def chord(lid, pitches, start, gate, vel):
    for p in pitches: add(lid,p,start,gate,vel)

# Kick, snare and crash retain every event and controller from the preceding version.
for x in layers.values():
    if x['kind'] == 'melodic': x['notes'] = []
volumes={'mono-bass':101,'juno-pad':66,'phase-seven-pluck':78,'three-two-pulse':68,'analog-lead':95,'poly-brass':70,'glass-keys':80}
for lid,vol in volumes.items(): layers[lid]['volume']=vol

# Remove optional 16th hats, and retain only two offbeat open hats per drop bar.
layers['closed-hat']['notes'] = [n for n in layers['closed-hat']['notes'] if abs(n['start']*2-round(n['start']*2))<1e-7]
old_open=layers['open-hat']['notes']
layers['open-hat']['notes']=[]
for n in old_open:
    if n['start'] % 4 in (1.5,3.5): layers['open-hat']['notes'].append(n)
    else:
        q=deepcopy(n); q['duration']=.09; q['velocity']=62
        layers['closed-hat']['notes'].append(q)
layers['synth-tom']['notes']=[]
FILL_BARS=[31,46,48,63,78,103,110,112,127,142,158]
for bar in FILL_BARS:
    for i,at in enumerate((2,2.5) if bar in (48,112) else (3,3.5)):
        add('synth-tom',60,(bar-1)*4+at,.12,72+i*6)

# Constant offbeat roots: no competing octave figures or sixteenth pickups.
for bar in range(9,161):
    if 81<=bar<=96 or 45<=bar<=48 or 109<=bar<=112: continue
    ats=(.5,2.5) if bar<17 or bar>=153 else (.5,1.5,2.5,3.5)
    for i,at in enumerate(ats): add('mono-bass',CHORDS[harmony(bar)]['root'],(bar-1)*4+at,.30,98-i*3)

# Three voices in a compact but non-clustered midrange. Each voice moves <=3
# semitones in the main loop. Note-offs and shorter release precede chord changes.
for bar in range(1,161,2):
    if 45<=bar<=48 or 109<=bar<=112 or bar>=153: continue
    in_drop=49<=bar<=80 or 113<=bar<=144
    chord('juno-pad',CHORDS[harmony(bar)]['pad'],(bar-1)*4,7.25,53 if in_drop else 62)
chord('juno-pad',CHORDS['Em']['pad'],640,3,60)

# Seven-eighth meter is foregrounded in separate answer windows. The two
# shorter drop spans are exactly seven global bars = eight complete 7/8 cycles.
# Two rests make 2+2+3 grouping legible without an unbroken stream of attacks.
ARP_SPANS=[(17,33),(37,45),(57,64),(73,80),(101,109),(121,128),(137,144),(145,152)]
arp_steps={0:(0,82),1:(1,57),2:(2,68),4:(1,74),5:(0,56)}
for first,after in ARP_SPANS:
    begin=(first-1)*4
    for step in range((after-first)*8):
        phase=step%7
        if phase not in arp_steps: continue
        t=begin+step*.5
        index,vel=arp_steps[phase]
        add('phase-seven-pluck',CHORDS[harmony(int(t//4)+1)]['arp'][index],t,.22,vel)

# 3:2 is a four-bar response, with one stable pitch per harmony. Neither lead,
# brass nor 7/8 pluck plays here. The anchor is still four quarter-note kicks.
PULSE_SPANS=[(69,73),(133,137)]
for first,after in PULSE_SPANS:
    begin=Fraction((first-1)*4)
    for k in range((after-first)*6):
        t=begin+Fraction(k*2,3)
        bar=int(t//4)+1
        p=76 if harmony(bar)=='Am' else 78
        add('three-two-pulse',p,t,.20,76 if k%3==0 else 56)

# One readily identified, mostly quarter/eighth-note phrase. Chord tones carry
# every sustained melody note; G/C/E map back to the same contour. D# resolves
# into E at the next tonic call. Rested backbeats expose the snare and groove.
HOOK=[
    [(0,76,.70),(1.5,79,.70),(2.5,83,1.0)],
    [(0,79,1.10),(2,76,1.25)],
    [(0,76,.70),(1.5,79,.70),(2.5,84,1.0)],
    [(0,79,1.10),(2,76,1.25)],
    [(0,76,.70),(1.5,81,.70),(2.5,84,1.0)],
    [(0,81,1.10),(2,76,1.25)],
    [(0,78,.70),(1.5,75,.70),(2.5,71,.80)],
    [(0,78,.70),(2,75,.60)],
]
for first in (49,113):
    for local in range(8):
        for i,(at,p,gate) in enumerate(HOOK[local]):
            add('analog-lead',p,(first+local-1)*4+at,gate,98-i*5+(3 if first==113 else 0))
    # Return only the first half of the hook; second-drop change is one contour,
    # never a new busy line layered over either cross-rhythm.
    for local in range(4):
        for i,(at,p,gate) in enumerate(HOOK[local]):
            if first==113 and local==2 and at==2.5: p=79
            add('analog-lead',p,(first+16+local-1)*4+at,gate,96-i*5)
    for at,p,gate in [(0,78,.7),(2,75,.6)]:
        add('analog-lead',p,(first+31-1)*4+at,gate,88)

# Two build calls precede, rather than accompany, the rotating answer.
for bar in (33,35,97,99):
    ps=[76,81] if harmony(bar)=='Am' else [76,79]
    for at,p in zip((0,2),ps): add('analog-lead',p,(bar-1)*4+at,.65,73)

# Short chord punctuation only in windows left empty by the three foregrounds.
for bar in (36,48,64,100,112,128,160):
    chord('poly-brass',[p+12 for p in CHORDS[harmony(bar)]['pad']],(bar-1)*4,1.25,68)

# Breakdown has a single foreground. This uses the same upward-third contour
# in longer values; no arp, triplet or lead competes with the glass keys.
for bar in range(81,97,2):
    ps=[p+12 for p in CHORDS[harmony(bar)]['pad']]
    for i,(at,index) in enumerate([(0,2),(2,0),(4,1),(6,2)]):
        add('glass-keys',ps[index],(bar-1)*4+at,1.0,76-i*4)
for bar,p in [(4,76),(8,75),(12,76),(16,75)]: add('glass-keys',p,(bar-1)*4+2,1.0,56)
add('glass-keys',76,640,2,65)

# Replace dense CC1 ramps with phrase-level movement kept below the previous
# maxima; expression still opens filters, never modulates pitch or note timing.
for lid,x in layers.items():
    if x['kind']!='melodic': continue
    old=x.get('control_changes',[])
    x['control_changes']=[dict(n,value=round(n['value']*.70)) for n in old if n['start']%2==0]
    x['notes'].sort(key=lambda n:(n['start'],n['pitch']))
for x in layers.values(): x['notes'].sort(key=lambda n:(n['start'],n['pitch']))
spec['description']='v003 coherence revision: unified chord-tone hook; 7/8 and 3:2 take separate turns above a steady 4/4 rhythm section.'
spec['prompt']+='\nRevision feedback: koherensi antar instrument tidak baik; polymeter/polyrhythm terdengar kacau. Prioritize coherent harmony and shared groove.'
spec['assumptions']=[
    '124 BPM, E harmonic minor (E F# G A B C D#), 4/4, 164 bars and 960 PPQN retained.',
    'Strict 1/48 grid without swing; cyclic eighths and true 2/3-beat divisions share the lattice.',
    'Harmony simplified to Em-C-Am-B triads; builds and breakdown use the same four chord vocabulary. D# is expressed in the dominant, never a permanent dissonant layer.',
    'The 7/8 pluck, 3:2 pulse and lead use separate foreground windows; all harmony follows the same two-bar chord changes.',
    'User drum samples remain unselected. Separate sampler tracks, every drum trigger 60, channel 10.',
    'Seven Serum 2 layers, with new native presets and compact tails. No combined MIDI or audio requested.',
    'Offline verification does not establish audible success. No plugin loading, rendering or actual listening performed.'
]
save('composition.json',spec)
save('harmonic-plan.json',[dict(bar=b,chord=harmony(b),**CHORDS[harmony(b)]) for b in range(1,165)])
save('arrangement-plan.json',dict(revision='v003',source='v002',tempo=124,meter='4/4',bars=164,seed=None,
    principle='One foreground at a time; harmony defines stable anchors; cross-rhythms supply contrast between calls.',
    arp_spans=ARP_SPANS,pulse_spans=PULSE_SPANS,
    lead_calls=[[49,57],[65,69],[80,81],[113,121],[129,133],[144,145]],
    rhythm=dict(kick='Quarter-note floor',bass='Unchanging eighth offbeats, root only',snare='Backbeats 2 and 4',lead='Calls rest or soften around backbeats'),
    harmonic_rhythm='Two bars per chord throughout; no extra diminished detour',
    motif='E-G-B / G-E; transferred to C and Am; F#-D#-B answers on the dominant',
    registers={lid:[min(n['pitch'] for n in layers[lid]['notes']),max(n['pitch'] for n in layers[lid]['notes'])] for lid in volumes},
    preserved=['tempo','meter','length','PPQN','section boundaries','kick','snare-clap','crash'],
    changed=['all seven melodic performances','harmonic voicings','foreground windows','hat density','tom fills','five preset envelopes/FX','seven CC1 curves'],
    listening_status='untested; symbolic and native structure only'))

# Preserve the original architecture, oscillator choices, detune and routing.
# Revise only articulation/space that could smear rhythm or chord changes.
bank={p.stem:json.loads(p.read_text(encoding='utf8')) for p in (HERE/'baseline-preset-specs').glob('*.json')}
patch_changes={
    'juno-pad':dict(amp=dict(attack=.35,release=.22),wet={'FXReverb':6}),
    'phase-seven-pluck':dict(amp=dict(decay=.24,release=.06),remove=['FXDelay'],wet={'FXReverb':4}),
    'three-two-pulse':dict(amp=dict(decay=.20,release=.055),wet={'FXReverb':4}),
    'analog-lead':dict(amp=dict(release=.10),remove=['FXDelay'],wet={'FXReverb':6}),
    'glass-keys':dict(amp=dict(release=.25),remove=['FXDelay'],wet={'FXReverb':12}),
}
for lid,p in bank.items():
    change=patch_changes.get(lid,{})
    p['envelopes'][0].update(change.get('amp',{}))
    p['fx_chain']=[f for f in p['fx_chain'] if f['type'] not in change.get('remove',[])]
    for f in p['fx_chain']:
        if f['type'] in change.get('wet',{}): f['wet']=change['wet'][f['type']]
    if change: p['description']+=' v003: compact articulation and reduced space for arrangement coherence; no extra note-generating echo.'
    save(f'preset-specs/{lid}.json',p)
save('sound-design-changes.json',dict(changes=patch_changes,unchanged=['mono-bass','poly-brass'],
    preserved_architecture='Maintained analog-family approximations, stable DCO pad, static VCO detune; all oscillators/filters/routes preserved.',
    limitation='Shorter stored releases and lower wet values are design evidence; true plugin tails and perceptual blend remain unauditioned.'))
save('bindings.json',{lid:f'Presets/{lid}.SerumPreset' for lid in bank})
save('skill-usage.json',dict(applied=['mc-workflow','mc-harmony','mc-rhythm-groove','mc-texture-layering','serum-sound-design','serum-modulation','serum-effects','serum-preset-build','serum-preset-qa'],
    applications=['Harmonic function before color; triad tones as anchors','Melody makes gaps for backbeat','Foreground competition resolved by alternation and register','Preserve retro oscillator architecture; shorten envelopes and remove echoes'],
    precedence='Strict repo grid and user harmonic-minor request override generic humanization or chromatic-color suggestions.'))
print(json.dumps(dict(revision='v003',notes={lid:len(l['notes']) for lid,l in layers.items()},total=sum(len(l['notes']) for l in layers.values())),indent=2))
