"""Original dark trap R&B; deterministic performance and expressive piano."""
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parent
SEED = 20261012
rng = random.Random(SEED)
BPM = 136
BARS = 112
FORM = [
    ('Intro', 0, 8), ('Verse 1', 8, 16), ('Pre-chorus 1', 24, 8),
    ('Chorus 1', 32, 16), ('Aftershock', 48, 4), ('Verse 2', 52, 16),
    ('Pre-chorus 2', 68, 8), ('Chorus 2', 76, 16), ('Bridge', 92, 8),
    ('Final chorus', 100, 8), ('Outro', 108, 4),
]
layers = {}

def layer(id, name, role, volume, pan=64, program=None):
    item = dict(id=id, name=name, role=role, kind='drums' if program is None else 'melodic',
                volume=volume, pan=pan, notes=[])
    if program is not None:
        item['program'] = program
    else:
        item['channel'] = 10
    layers[id] = item

layer('piano', 'Expressive Piano', 'harmony and original melodic hook', 105, 62, 0)
layer('sub-bass', 'Sub Bass', 'restrained verse bass and deep chorus foundation', 107, 64, 38)
layer('bass-grit', 'Chorus Bass Grit', 'chorus-only distorted bass octave', 91, 64, 38)
layer('shadow-pad', 'Shadow Pad', 'wide dark harmonic atmosphere', 66, 64, 89)
layer('ghost-bell', 'Ghost Bell', 'sparse high response melody', 74, 79, 98)
layer('tension-rise', 'Tension Rise', 'two-bar noise/filter swell before drops', 80, 64, 97)
for args in [
    ('kick', 'Kick', 'short kick supporting the bass', 112, 64),
    ('snare', 'Snare', 'half-time backbeat', 101, 64),
    ('rim', 'Rim', 'quiet verse accents and ghost notes', 73, 53),
    ('closed-hat', 'Closed Hat', 'straight eighths, sixteenths and 32nd rolls', 82, 72),
    ('open-hat', 'Open Hat', 'offbeat lift', 79, 80),
    ('crash', 'Crash', 'chorus and transition punctuation', 88, 48),
    ('floor-tom', 'Floor Tom', 'sparse transition fills', 88, 57),
]:
    layer(*args)

def note(id, pitch, beat, length, velocity):
    layers[id]['notes'].append(dict(pitch=int(pitch), start=round(beat, 5),
        duration=round(min(length, BARS*4-beat), 5), velocity=max(1, min(127, round(velocity)))))

def section_at(bar):
    return next((name, start, length) for name,start,length in FORM if start <= bar < start+length)

# An original eight-bar harmonic phrase. C7(b9) resolves the harmonic-minor E to F.
ROOTS = [29, 37, 34, 36]
VOICE = [[56,60,63,67,72], [56,60,65,68,75], [56,60,61,65,72], [55,58,61,65,73]]
HOOK = [[79,77,75,72,70,68,67], [80,77,75,72,68,65,67],
        [77,75,72,70,68,65,60], [79,77,73,72,70,68,64]]

for bar in range(BARS):
    sec, begin, size = section_at(bar)
    rel = bar-begin
    ch = (rel % 8)//2
    if sec == 'Outro':
        ch = 0
    root = ROOTS[ch]
    vo = VOICE[ch].copy()
    if ch == 3 and rel % 2:
        vo[3] = 64
    t = bar*4
    chorus = 'chorus' in sec.lower() and not sec.startswith('Pre')
    pre = sec.startswith('Pre')
    verse = sec.startswith('Verse')
    bridge = sec == 'Bridge'
    intro = sec == 'Intro'
    outro = sec == 'Outro'
    cutoff = (pre and rel == 7) or (bridge and rel == 7)
    # Piano: separate hand velocities, phrase crescendos, melody accents and gate variation.
    # Broken chord onsets are intentional written 32nd/16th values, never timing jitter.
    phrase_arc = [0, 3, 1, 5, 2, 6, 4, -3][rel % 8]
    level = (88 if chorus else 68 if pre else 57 if verse else 50 if bridge else 45)
    if outro:
        level = 57-rel*7
    left_pitch = root + (24 if chorus else 12)
    note('piano', left_pitch, t, 2.3 if chorus else 2.8, level-14+rng.randint(-4,4))
    if rel % 2 == 0 and not outro:
        fifth = left_pitch-5
        if fifth in vo:
            fifth -= 12
        note('piano', fifth, t+0.5, 1.65, level-24+rng.randint(-3,3))
    inner_times = [0.125,0.375,0.75,1.25]
    if chorus:
        inner_times = [0,0.25,0.625,1.0]
    for i,at in enumerate(inner_times):
        p = vo[i]
        # Shallow inner voice gates leave the hook clear and avoid uniform block chords.
        note('piano', p, t+at, rng.uniform(0.56,1.24), level-15+i*2+phrase_arc+rng.randint(-7,5))
    if chorus:
        # Eight-bar singable response; rests and accented peaks make the phrase breathe.
        motif = HOOK[ch]
        hits = [(0.5,motif[0],0.65),(1.5,motif[1],0.36),(2.25,motif[2],0.60),
                (3.25,motif[3],0.56)] if rel % 2 == 0 else [
                (0.25,motif[4],0.73),(1.25,motif[5],0.48),(2.5,motif[6],0.62)]
        for idx,(at,p,dur) in enumerate(hits):
            note('piano',p,t+at,dur,level+phrase_arc+(13 if idx==0 else 1)+rng.randint(-6,5))
        if rel % 4 == 3:
            note('piano',vo[2],t+3.25,0.45,level-20)
    else:
        # Two-bar question/answer gestures, rather than the same ostinato repeated verbatim.
        gestures = [(1.75, vo[4],0.8),(3.0,vo[3]+12,0.58)] if rel%2==0 else [
            (1.5,vo[2]+12,0.7),(2.5,vo[1]+12,0.5),(3.5,vo[0]+12,0.3)]
        if (intro and rel < 2) or (outro and rel > 1):
            gestures = gestures[:1]
        if verse and rel%4==3:
            gestures = gestures[:2]
        for idx,(at,p,dur) in enumerate(gestures):
            if cutoff and at>=2.5:
                continue
            note('piano',p,t+at,dur+rng.uniform(-0.12,0.12),level+phrase_arc+6-idx*4+rng.randint(-5,6))
        if rel%4==2 and not cutoff and not outro:
            note('piano',vo[1],t+2.75,0.45,level-25)

    # Wide pad is quieter in verses; separate upper register leaves the sub and piano room.
    if rel%2==0 and not (intro and rel<4) and not (outro and rel>=2):
        duration = 5.45 if ((pre or bridge) and rel==6) else 7.4
        pad_pitches = [vo[0]+12,vo[1]+12,vo[3]+12]
        if ch==3:
            # Only the suspended fifth-bar voicing is sustained; E resolution is in piano/bell.
            duration = 3.45
        for p in pad_pitches:
            note('shadow-pad',p,t,duration,65 if chorus else 44 if verse else 51)
    if ch==3 and rel%2 and not cutoff and not outro:
        for p in [67,70,76]:
            note('shadow-pad',p,t,3.25,55 if chorus else 42)

    # Bass attacks are explicitly paired with the kick; verse is one octave higher and softer.
    kicks = []
    if chorus:
        patterns = [[0,1.5,2.75],[0,0.75,3.0,3.5],[0,1.75,2.5],[0,1.25,3.25]]
        kicks = patterns[rel%4].copy()
        # A long first root establishes weight; later stabs and octave pickups vary the answer.
        bass_hits = [0,2.75] if rel%4==0 else kicks.copy()
        if rel%4==3:
            bass_hits += [3.75]
        for idx,at in enumerate(bass_hits):
            next_at = bass_hits[idx+1] if idx+1<len(bass_hits) else 4
            p = root+12 if at==3.75 else root
            gate = max(0.10,next_at-at-0.07)
            vel = 123 if rel==0 and idx==0 else 117 if idx==0 else 108+rng.randint(-5,7)
            note('sub-bass',p,t+at,gate,vel)
            note('bass-grit',p+12,t+at,max(0.10,gate-0.03),vel-5)
    elif verse or (pre and rel<6) or (sec=='Aftershock' and rel<2):
        kicks = ([0,2.75] if rel%2==0 else [0,1.75,3.5]) if verse else [0,1.5,3.0]
        if verse and rel%8<2:
            kicks = [0,2.75] if rel%2==0 else [1.75]
        for idx,at in enumerate(kicks):
            nxt = kicks[idx+1] if idx+1<len(kicks) else 4
            note('sub-bass',root+12,t+at,min(1.65,nxt-at-0.12),62+(8 if pre else 0)+rng.randint(-5,5))
    elif intro and rel>=6:
        note('sub-bass',root+12,t,1.7,47)
    for idx,at in enumerate(kicks):
        note('kick',36,t+at,0.12,122 if chorus and rel==0 and idx==0 else
             (113 if chorus else 91)+rng.randint(-6,5))

    # Half-time snare beat 3; kick and snare are independent single-pitch drum files.
    beat_active = chorus or verse or pre or sec=='Aftershock'
    if beat_active and not (sec=='Aftershock' and rel>=2):
        note('snare',38,t+2,0.13,(112 if chorus else 94 if pre else 82)+rng.randint(-4,5))
        if verse and rel%4 in [1,3]:
            note('rim',41,t+3.25,0.10,44+rng.randint(-6,8))
        if chorus and rel%4==3:
            note('rim',41,t+1.75,0.10,54)
        if verse and rel%8==6:
            note('snare',38,t+3.75,0.10,42)

    hat_times = []
    if chorus or verse or pre:
        hat_times = [i*0.5 for i in range(8)]
        if verse and rel%8<4:
            hat_times = [0.5,1.5,2.5,3.5]
        if chorus and rel%2:
            hat_times += [1.25,1.75]
        if (chorus and rel%4==3) or (pre and rel in [5,6]):
            hat_times = [x for x in hat_times if x<3.0]+[3.0,3.125,3.25,3.375,3.5,3.625,3.75,3.875]
    elif intro and rel>=4:
        hat_times=[1.5,3.5]
    elif bridge and rel>=4:
        hat_times=[0.5,1.5,2.5,3.5]
    # Pre-drop beat 4 is empty for every MIDI layer, including the hat roll.
    if cutoff:
        hat_times = [x for x in hat_times if x<3]
    opens = []
    if chorus and rel%2==1:
        opens=[0.5]
    elif verse and rel%4==2:
        opens=[3.5]
    elif pre and rel in [3,5]:
        opens=[0.5]
    for at in sorted(set(hat_times)-set(opens)):
        v = (76 if chorus else 60 if pre else 51)+(4 if at%1==0 else -9)+rng.randint(-9,7)
        if at%0.25:
            v-=10
        note('closed-hat',54,t+at,0.075,v)
    for at in opens:
        note('open-hat',57,t+at,0.22,80 if chorus else 57)
    if chorus and rel in [0,8]:
        note('crash',64,t,0.25,113 if rel==0 else 83)
    if (verse and rel==15) or (chorus and rel in [7,15]) or (bridge and rel==6):
        for at,v in [(3.0,66),(3.5,83),(3.75,96)]:
            note('floor-tom',47,t+at,0.10,v)

    # A sparse bell answers the piano instead of filling every vocal gap.
    if chorus and rel%4 in [1,3]:
        p = [84,87,84,85][ch]
        if ch==3:
            p=88  # E6 over C7, resolves to F at the next phrase.
        note('ghost-bell',p,t+3.0,0.30,68+rng.randint(-4,6))
    elif (verse or intro or bridge) and rel%4==3 and not cutoff:
        note('ghost-bell',[79,80,77,76][ch],t+2.75,0.35,46+rng.randint(-5,6))

# Seven beats of rise, then one full beat of MIDI silence at each major entry.
for first in [30,74,98]:
    note('tension-rise',77,first*4,7.0,96)

# Last 1.5 bars are silent in all layers, allowing release/reverb to decay.
end_limit = 110*4+2
for item in layers.values():
    item['notes'] = [n for n in item['notes'] if n['start']<end_limit]
    for n in item['notes']:
        n['duration'] = round(min(n['duration'],end_limit-n['start']),5)
    item['notes'].sort(key=lambda n:(n['start'],n['pitch']))

# When the melody and an inner hand share a key, the accented melody owns that key.
# Merge coincident attacks and lift the earlier note before any new attack.
keys = {}
for n in layers['piano']['notes']:
    group = keys.setdefault(n['pitch'], [])
    if group and group[-1]['start'] == n['start']:
        group[-1]['velocity'] = max(group[-1]['velocity'],n['velocity'])
        group[-1]['duration'] = max(group[-1]['duration'],n['duration'])
    else:
        group.append(n)
for group in keys.values():
    for a,b in zip(group,group[1:]):
        a['duration'] = round(min(a['duration'],b['start']-a['start']-0.035),5)
layers['piano']['notes'] = sorted([n for group in keys.values() for n in group],key=lambda n:(n['start'],n['pitch']))

spec = dict(version=1, title='Black Glass', tempo_bpm=BPM, time_signature=[4,4],
    bars=BARS,ticks_per_beat=480,key_signature='Fm',timing=dict(mode='strict',grid_division=32),
    description='Original dark trap R&B with expressive acoustic piano and deep layered chorus drops.',
    prompt='Dark trap R&B with piano; The Hills by The Weeknd as a mood reference; separate MIDI for each drum; huge chorus bass drop. Piano should feel human and highly dynamic; user selects its sound.',
    assumptions=[
        'Original composition inspired by broad mood, contrast and bass weight; no reference transcription or audio analysis.',
        '136 quarter-note BPM / 68 BPM half-time feel, F minor with harmonic-minor dominant, 112 bars.',
        'Strict straight 1/32 onset grid without swing or random timing jitter; piano expression uses velocity, gate, breathing room and intentionally broken chords.',
        'No piano preset; user selects a velocity-sensitive acoustic piano. All five other melodic layers use native Serum 2 presets.',
        'Seven separate drum sounds use the user default pitch map; sample choice remains with the user.',
        f'Deterministic seed {SEED}; no combined MIDI or audio requested.',
    ],sections=[dict(name=n,start=s*4) for n,s,_ in FORM],layers=list(layers.values()))
ROOT.joinpath('composition.json').write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'bars':BARS,'bpm':BPM,'seconds':BARS*4*60/BPM,
    'notes':{k:len(v['notes']) for k,v in layers.items()},
    'piano_velocity_range':[min(n['velocity'] for n in layers['piano']['notes']),max(n['velocity'] for n in layers['piano']['notes'])]},indent=2))
