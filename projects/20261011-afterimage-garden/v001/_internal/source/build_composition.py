"""Reproduce Afterimage Garden v001. Run with the workspace uv environment."""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
RNG = random.Random(108104)
TOTAL = 104 * 4
SECTIONS = [
    (0, 8, 'Intro', 'intro'), (8, 24, 'Verse 1', 'verse'),
    (24, 32, 'Lift 1', 'lift'), (32, 48, 'Chorus 1', 'chorus'),
    (48, 56, 'Prismatic interlude', 'interlude'),
    (56, 64, 'Verse 2', 'verse2'), (64, 72, 'Lift 2', 'lift'),
    (72, 88, 'Final chorus', 'final'), (88, 100, 'Outro', 'outro'),
    (100, 104, 'Release tail', 'tail'),
]
CHORDS = {
    'Dm9': {'root': 38, 'pad': [53, 57, 60, 62, 64], 'arp': [62, 65, 69, 72, 76], 'hook': [81, 79, 77, 76, 74]},
    'Bbmaj7': {'root': 34, 'pad': [53, 57, 58, 62, 65], 'arp': [62, 65, 69, 70, 74], 'hook': [77, 81, 79, 77, 74]},
    'Fmaj9': {'root': 41, 'pad': [53, 57, 60, 64, 67], 'arp': [60, 64, 65, 69, 72], 'hook': [79, 77, 76, 72, 69]},
    'Cadd9': {'root': 36, 'pad': [55, 60, 62, 64, 67], 'arp': [60, 62, 64, 67, 72], 'hook': [79, 76, 74, 72, 74]},
    'Gm9': {'root': 31, 'pad': [53, 57, 58, 62, 65], 'arp': [58, 62, 65, 69, 74], 'hook': [77, 74, 72, 70, 69]},
    'F/A': {'root': 33, 'pad': [53, 57, 60, 64, 67], 'arp': [60, 64, 65, 69, 72], 'hook': [79, 77, 76, 72, 69]},
}
LAYERS = [
    ('juno-pad', 'Juno Memory Pad', 'harmony', 89, 79, 59),
    ('phase-bass', 'Hypnotic Phase Bass', 'bass', 38, 106, 64),
    ('prism-arp', 'Prismatic Arpeggio', 'arpeggio', 81, 78, 78),
    ('afterimage-lead', 'Afterimage Hook Lead', 'melody', 80, 91, 64),
    ('velvet-keys', 'Velvet Synth Keys', 'rhythmic harmony', 4, 72, 49),
    ('halo-texture', 'Halo Air Texture', 'texture', 91, 55, 68),
]
tracks = {ident: dict(id=ident, name=name, kind='melodic', role=role,
                      program=program, volume=volume, pan=pan, notes=[])
          for ident, name, role, program, volume, pan in LAYERS}
tracks['disco-kit'] = dict(id='disco-kit', name='Disco Funk Kit', kind='drums',
                          role='drums', channel=10, volume=101, pan=64, notes=[])


def note(layer, pitch, start, duration, velocity):
    assert start % .25 == 0, (layer, start)
    assert start + duration <= TOTAL
    tracks[layer]['notes'].append(dict(pitch=pitch, start=start,
        duration=round(duration, 4), velocity=max(1, min(127, velocity))))


def human(base, spread=4):
    return base + RNG.randint(-spread, spread)


def section(bar):
    return next(s for s in SECTIONS if s[0] <= bar < s[1])


def chord(bar):
    a, _, _, typ = section(bar)
    if typ in ('chorus', 'final'):
        progression = ['Bbmaj7', 'F/A', 'Cadd9', 'Dm9']
    elif typ == 'lift':
        progression = ['Gm9', 'Bbmaj7', 'Dm9', 'Cadd9']
    elif typ == 'interlude':
        progression = ['Gm9', 'Bbmaj7', 'Fmaj9', 'Cadd9']
    else:
        progression = ['Dm9', 'Bbmaj7', 'Fmaj9', 'Cadd9']
    if typ == 'outro' and bar >= 96:
        return 'Dm9'
    return progression[((bar-a)//2) % 4]


# Pads move every two bars; high texture appears only at selected transitions.
for bar in range(0, 100, 2):
    typ = section(bar)[3]
    c = CHORDS[chord(bar)]
    base = {'intro': 57, 'verse': 66, 'verse2': 69, 'lift': 76,
            'chorus': 85, 'final': 91, 'interlude': 60, 'outro': 68}[typ]
    if typ == 'outro':
        base -= (bar-88)*2
    for p in c['pad']:
        note('juno-pad', p, bar*4, 7.75, human(base, 3))
    if (typ in ('intro', 'interlude', 'outro') or bar % 8 == 0):
        for p in [c['pad'][2]+24, c['pad'][-1]+24]:
            note('halo-texture', p, bar*4, 7.5, human(48 if typ!='final' else 62, 3))

# Bass locks roots to the downbeat and pushes into hats with short offbeat pickups.
for bar in range(4, 98):
    a, b, _, typ = section(bar)
    c = CHORDS[chord(bar)]
    root = c['root']
    if typ == 'intro':
        pattern = [(0,0,1.3), (2.5,0,.4), (3.5,7,.3)]
    elif typ == 'interlude' and bar < 52:
        pattern = [(0,0,1.75), (2.75,7,.45)]
    elif typ == 'outro' and bar >= 94:
        pattern = [(0,0,2.7), (3,12,.65)]
    else:
        pattern = [(0,0,.65), (.75,0,.2), (1.5,12,.35),
                   (2,0,.65), (2.75,7,.2), (3.5,0,.4)]
        if bar % 2:
            pattern = [(0,0,.85), (1.25,7,.2), (1.75,12,.2),
                       (2.5,0,.65), (3.25,7,.2), (3.75,0,.2)]
        if typ == 'lift':
            pattern = [(0,0,.9), (1.5,7,.35), (2,0,.6), (3,12,.35), (3.5,7,.3)]
    for off, interval, dur in pattern:
        note('phase-bass', root+interval, bar*4+off, dur,
             human(96 if off in (0,2) else 77))
    # Diatonic approach only at the end of an eight-bar phrase.
    if (bar-a) % 8 == 7 and typ not in ('intro','interlude','outro'):
        end = tracks['phase-bass']['notes'][-1]
        end['duration'] = min(end['duration'], .2)
        # Replace the last step rather than add a colliding note.
        end['pitch'] = CHORDS[chord(bar+1)]['root']+2

# Written MIDI arp, not Serum's internal arp; sixteenth runs are reserved for lifts.
for bar in range(4, 96):
    a, b, _, typ = section(bar)
    if typ == 'verse' and (bar-a) % 8 < 2:
        continue
    if typ == 'interlude' and bar < 52:
        continue
    tones = CHORDS[chord(bar)]['arp']
    indices = [0,2,1,3,2,4,3,1] if bar % 2 == 0 else [0,1,3,2,4,2,1,3]
    sixteenths = typ == 'lift' and bar-a >= 4
    steps = 16 if sixteenths else 8
    for step in range(steps):
        off = step*(.25 if sixteenths else .5)
        if typ in ('verse','verse2','intro','outro') and step in (0,6):
            continue
        if typ in ('chorus','final') and bar % 4 == 3 and off >= 3:
            continue
        p = tones[indices[step % 8]]+12
        note('prism-arp', p, bar*4+off, .16 if sixteenths else .28,
             human((76 if typ in ('chorus','final') else 62)+(8 if step%4==0 else 0)))

# Chord stabs create a second rhythmic conversation without filling every beat.
for bar in range(8, 94):
    a,b,_,typ = section(bar)
    if typ == 'interlude' or (typ == 'outro' and bar >= 92):
        continue
    offsets = [(.5,.28), (2.5,.4)]
    if typ in ('chorus','final'):
        offsets = [(.5,.28), (1.75,.2), (2.5,.35), (3.5,.25)]
    if typ == 'lift':
        offsets = [(1.5,.45), (3,.6)]
    voicing = CHORDS[chord(bar)]['pad'][1:]
    for off,dur in offsets:
        for p in voicing:
            note('velvet-keys', p, bar*4+off, dur, human(71 if typ in ('chorus','final') else 58,3))

# Two-bar, chord-aware hook cells. Repeated phrases have space, answers, and endings.
hook_rhythm = [(0,0,.65), (.75,0,.2), (1.5,1,.35), (2.5,2,.6),
               (3.5,3,.35), (4.5,4,1.1), (6.5,2,.7)]
for first, last in [(32,48), (72,88)]:
    for bar in range(first,last,2):
        tones = CHORDS[chord(bar)]['hook']
        for off,idx,dur in hook_rhythm:
            p = tones[idx]
            # The second half answers lower; final two-bar phrase resolves D.
            if bar-first >= 8 and off == 6.5:
                p = 74 if chord(bar)=='Dm9' else tones[4]
            note('afterimage-lead',p,bar*4+off,dur,human(90 if first==72 else 83,4))
        if first==72 and bar in (78,86):
            note('afterimage-lead',tones[1],bar*4+7.5,.3,human(72,3))
# Sparing preview of the hook and a descending interlude response.
for bar in (20,22,60,62,90,94):
    tones=CHORDS[chord(bar)]['hook']
    for off,idx,dur in [(1.5,2,.75),(3,3,.6),(5,4,1.4)]:
        note('afterimage-lead',tones[idx]-12,bar*4+off,dur,human(66,3))
for bar in (48,50,52,54):
    tones=CHORDS[chord(bar)]['hook']
    for off,idx,dur in [(.5,0,1.2),(2.5,2,.7),(4.5,4,2)]:
        note('afterimage-lead',tones[idx],bar*4+off,dur,human(70,3))

# One drum kit, using the user's numeric map exclusively. No timing swing/jitter.
drums = 'disco-kit'
for bar in range(4,98):
    a,b,_,typ=section(bar)
    full=typ in ('chorus','final','lift')
    sparse=(typ=='intro' or (typ=='interlude' and bar<52) or (typ=='outro' and bar>=94))
    final_fill=bar in (23,31,47,55,63,71,87,93)
    if sparse:
        kicks=[0,2] if typ!='interlude' else [0]
    elif full:
        kicks=[0,1,2,3]
        if bar%4==2:
            kicks.append(2.75)
    else:
        kicks=[0,1.5,2,3.5] if bar%2==0 else [0,.75,2,2.75]
    if final_fill:
        kicks=[k for k in kicks if k<3]
    for off in kicks:
        note(drums,36,bar*4+off,.1,human(108 if off in (0,2) else 92,3))
    if typ=='intro':
        if bar>=6:
            for off in (1,3): note(drums,37,bar*4+off,.1,human(67,3))
    elif typ=='interlude' and bar<52:
        note(drums,37,bar*4+3,.1,human(64,3))
    else:
        for off in (1,3):
            note(drums,40 if typ=='final' and bar%4==3 else 38,
                 bar*4+off,.1,human(103 if full else 93,3))
        if not sparse and bar%2==1:
            note(drums,37,bar*4+2.75,.08,human(41,3))
    # Hat slots are mutually exclusive; don't double closed/open hats on one onset.
    for step in range(8):
        off=step*.5
        if final_fill and off>=3.25: continue
        if sparse and step%2==0: continue
        pitch=42
        if step in (3,7) and full: pitch=46
        elif step==7 and not sparse: pitch=21
        elif sparse: pitch=17
        vel=human(76 if step%2 else 53,4)
        note(drums,pitch,bar*4+off,.22 if pitch in (21,46) else .1,vel)
    if full and not final_fill and bar%2==0:
        for off in (.75,2.75): note(drums,17,bar*4+off,.08,human(39,3))
    if typ in ('chorus','final') and (bar-a)%4==2:
        for off in (.5,2.5): note(drums,56,bar*4+off,.12,human(57,3))
    if typ=='final' and bar>=80 and bar%2==0:
        note(drums,53,bar*4+2,.18,human(66,3))
    if final_fill:
        for off,p in [(3.25,47),(3.5,45),(3.75,41)]:
            note(drums,p,bar*4+off,.12,human(78+int((off-3.25)*24),3))
for bar in (8,24,32,56,64,72,80,88):
    note(drums,49 if bar!=80 else 55,bar*4,.45,96 if bar in (32,72) else 80)
note(drums,49,96*4,.5,65)
note(drums,44,98*4,.1,47)

for t in tracks.values():
    t['notes'].sort(key=lambda n:(n['start'],n['pitch']))
    ends={}
    for n in t['notes']:
        assert n['start'] >= ends.get(n['pitch'],0), ('overlap',t['id'],n)
        ends[n['pitch']] = n['start']+n['duration']

composition=dict(version=1,title='Afterimage Garden',
    description='Original atmospheric psychedelic synthpop instrumental: warm extended harmony, analog sweeps, hook-and-answer lead, phasing mono bass and a disco-funk kit.',
    prompt='Tame Impala inspired atmospheric synth-heavy psychedelic pop with 80s analog synthpop / modern neo-psychedelia; lush Juno-style pads, bright arps, thick hypnotic phaser bass and groovy compressed 70s/80s disco-funk drums. Nostalgic, introspective, warm and euphoric. User-provided drum map.',
    tempo_bpm=108,time_signature=[4,4],bars=104,key_signature='Dm',ticks_per_beat=480,
    timing=dict(mode='strict',grid_division=16),
    assumptions=['Original instrumental; no vocal requested.','108 BPM, D natural minor, 104 bars including four bars of release space.',
                 'Straight sixteenth onset grid; no swing or timing jitter. Velocity and gate variation only.',
                 'Six Serum 2 synth layers and one external drum kit MIDI; native presets provided.',
                 'Numeric drum mapping supplied by user. Sample kit selection remains with user; no samples copied.'],
    sections=[dict(name=name,start=a*4) for a,b,name,typ in SECTIONS],layers=list(tracks.values()))
(HERE/'composition.json').write_text(json.dumps(composition,indent=2)+'\n',encoding='utf-8')
audit=dict(seed=108104,tempo_bpm=108,bars=104,seconds=TOTAL*60/108,
    harmony=[dict(bar=bar+1,chord=chord(bar)) for bar in range(0,100,2)],
    layers={k:dict(notes=len(v['notes']),range=[min(n['pitch'] for n in v['notes']),max(n['pitch'] for n in v['notes'])],
        first_beat=v['notes'][0]['start'],last_note_end=max(n['start']+n['duration'] for n in v['notes'])) for k,v in tracks.items()},
    drum_pitches=sorted({n['pitch'] for n in tracks[drums]['notes']}),
    musical_review=['Pad moves on two-bar chord boundaries with shared tones and extensions above bass.',
        'Bass roots anchor kick; short octave/fifth syncopation leaves room for snare.',
        'Eighth arp and occasional sixteenth lift share the same strict grid.',
        'Lead chorus uses repeating two-bar cells, lower answers, and phrase-end rests.',
        'Intro/interlude/outro reduce density; second chorus adds accents, cowbell and ride bell.',
        'All pitched notes use D natural minor; percussion follows user numeric map.',
        'Last note ends before bar 101; four final bars are silent MIDI for release/effects.'],
    audio_listened=False)
(HERE/'musical-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
print(json.dumps(audit,indent=2))
