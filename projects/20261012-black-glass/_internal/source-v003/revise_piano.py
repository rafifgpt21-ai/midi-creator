"""Chord-led piano revision; all other musical layers stay byte-for-byte reproducible."""
from pathlib import Path
from collections import Counter,defaultdict
import copy,json,random

SOURCE=Path(__file__).resolve().parent
PROJECT=next(p for p in SOURCE.parents if (p/'v002').is_dir())
original=json.loads((PROJECT/'v002/_internal/composition.json').read_text(encoding='utf-8'))
spec=copy.deepcopy(original)
piano=next(x for x in spec['layers'] if x['id']=='piano')
piano['name']='Chord Piano'
piano['role']='chord-focused harmony with sparse melodic improvisation'
piano['notes']=[]
SEED=2026101203
rng=random.Random(SEED)
FORM=[('Intro',0,8),('Verse 1',8,16),('Pre-chorus 1',24,8),('Chorus 1',32,16),
      ('Aftershock',48,4),('Verse 2',52,16),('Pre-chorus 2',68,8),('Chorus 2',76,16),
      ('Bridge',92,8),('Final chorus',100,8),('Outro',108,4)]
roots=[41,49,46,48]
voicings=[[[56,60,63,67],[60,63,65,68]], # Fm9 / Fm7 inversion
          [[56,60,63,65],[60,63,65,68]], # Dbmaj9
          [[56,60,61,65],[60,61,65,68]], # Bbm9
          [[55,58,61,65],[58,61,64,67]]] # Csus4(b9) / C7(b9)
fills=[]
gestures=[]

def add(pitch,t,gate,vel,limit):
    gate=min(gate,limit-t)
    if gate>0:
        piano['notes'].append({'pitch':pitch,'start':round(t,5),'duration':round(gate,5),
            'velocity':max(26,min(114,round(vel)))})

for name,start,count in FORM:
    chorus=name in ['Chorus 1','Chorus 2','Final chorus']
    pre=name.startswith('Pre')
    verse=name.startswith('Verse')
    intro=name=='Intro'
    bridge=name=='Bridge'
    outro=name=='Outro'
    for rel in range(count):
        bar=start+rel
        t=bar*4
        ch=0 if outro else rel%8//2
        # Each two-bar harmonic unit retains the existing arrangement's harmony.
        resolved=(ch==3 and rel%2==1)
        variant=1 if (resolved or (chorus and rel%4 in [0,1]) or (name=='Verse 2' and rel%4==1)) else 0
        rh=voicings[ch][variant].copy()
        if ch==3 and not resolved:
            rh=voicings[3][0].copy()
        lh=roots[ch]
        if chorus and ch==0:
            lh+=12
        phrase=[-3,0,2,-2,1,4,3,-5][rel%8]
        base=88 if name=='Final chorus' else 83 if chorus else 68 if pre else 57 if verse else 47 if intro else 52 if bridge else 55
        if outro:
            base-=rel*7
        cutoff=(pre or bridge) and rel==7
        unit_end=(start+(rel//2+1)*2)*4
        limit=min(unit_end,(start+count)*4,442)
        if ch==3 and not resolved:
            limit=min(limit,t+3.82) # Release suspended F before the following C7 E.
        if cutoff:
            limit=min(limit,t+2.75)
        if intro or bridge:
            # Long chord holds and deliberate rests; no sequential broken-chord attacks.
            hits=[(0,5.7,0)] if rel%2==0 else ([(1.5,1.8,-7)] if rel%4==3 else [])
            if cutoff:
                hits=[(0,2.4,-3)]
        elif outro:
            hits=[(0,5.4,-2)] if rel%2==0 else []
        elif chorus:
            hits=([(0,2.28,4),(2.75,.94,-6)] if rel%2==0 else
                  [(0,1.27,-1),(1.5,1.84,1)])
            if name=='Chorus 2' and rel%4==1:
                hits=[(0,1.01,0),(1.25,2.1,-3)]
        elif pre:
            hits=[(0,2.1,0),(2.5,1.05,-5)] if rel%2==0 else [(0.5,2.7,1)]
            if cutoff:
                hits=[(0,2.4,-2)]
        elif name=='Aftershock':
            hits=[(0,3.35,-2)] if rel%2==0 else [(1,2.2,-8)]
        else:
            hits=([(0,2.28,0),(2.75,.98,-9)] if rel%2==0 else [(1,2.48,-3)])
            if name=='Verse 2' and rel%4==2:
                hits=[(0,2.12,1),(2.5,1.22,-8)]
        for at,gate,accent in hits:
            beat=t+at
            dynamic=base+phrase+accent+rng.randint(-4,4)
            # A whole chord is played together. Natural hand weighting and unequal releases
            # preserve expression without turning chords into an arpeggio or adding swing.
            add(lh,beat,gate+rng.uniform(-.12,.12),dynamic-14+rng.randint(-3,3),limit)
            if at==0 and rel%2==0 and not outro:
                lower_fifth=lh-5
                if lower_fifth<36:
                    lower_fifth+=12
                add(lower_fifth,beat,gate+rng.uniform(-.18,.06),dynamic-22+rng.randint(-3,3),limit)
            for index,pitch in enumerate(rh):
                weight=7 if index==len(rh)-1 else -11 if index==0 else -6
                add(pitch,beat,gate+rng.uniform(-.14,.13),dynamic+weight+rng.randint(-5,4),limit)
            gestures.append({'bar':bar+1,'beat':at,'pitches':[lh]+rh,'velocity_center':dynamic})

        # Hand-written, short melodic answers occur only at selected phrase endings.
        # They move mostly by step/chord-neighbor motion, never through repeated chord ladders.
        fragment=None
        if verse and rel in ([3,11] if name=='Verse 1' else [3,7,11,15]):
            fragment=([(2.75,68,.30),(3.25,65,.28),(3.5,63,.32)] if ch==1 else
                      [(2.75,67,.28),(3.25,65,.28),(3.5,64,.33)])
        elif chorus and rel in [3,11]:
            fragment=[(3.0,75,.22),(3.25,73,.22),(3.5,72,.32)]
        elif chorus and rel in [7,15]:
            fragment=[(3.0,73,.22),(3.25,72,.22),(3.5,70,.28)]
        elif intro and rel==3:
            fragment=[(3.0,68,.34),(3.5,65,.38)]
        elif bridge and rel==3:
            fragment=[(2.75,68,.34),(3.5,63,.36)]
        elif name=='Aftershock' and rel==3:
            fragment=[(3.0,65,.34),(3.5,63,.34)]
        if fragment:
            for index,(at,pitch,gate) in enumerate(fragment):
                vel=base+phrase+2-index*4+rng.randint(-4,3)
                add(pitch,t+at,gate+rng.uniform(-.04,.04),vel,limit)
            fills.append({'bar':bar+1,'pitches':[x[1] for x in fragment]})

# Lift a repeated key before retrigger; same-time duplicates combine into one key strike.
by_pitch=defaultdict(list)
for n in sorted(piano['notes'],key=lambda x:(x['start'],x['pitch'])):
    group=by_pitch[n['pitch']]
    if group and group[-1]['start']==n['start']:
        group[-1]['duration']=max(group[-1]['duration'],n['duration'])
        group[-1]['velocity']=max(group[-1]['velocity'],n['velocity'])
    else:
        group.append(n)
for group in by_pitch.values():
    for a,b in zip(group,group[1:]):
        a['duration']=round(min(a['duration'],b['start']-a['start']-.03),5)
piano['notes']=sorted([n for group in by_pitch.values() for n in group],key=lambda x:(x['start'],x['pitch']))
spec['description']='Dark trap R&B with chord-led expressive piano, sparse improvisation, and the preserved v002 bass/synth/drum arrangement.'
spec['prompt']+=' New revision: more chord-focused piano instead of arpeggios, natural dynamics and tasteful improvisation.'
spec['assumptions']=[x for x in spec['assumptions'] if 'broken chords' not in x and 'Deterministic seed' not in x]
spec['assumptions'] += ['Piano chord attacks are simultaneous on the strict straight grid; natural expression comes from voicing, hand balance, varied velocities/gates and phrase space. No swing or timing jitter.',
    'Only piano notes/name/role changed from v002; all other musical layers, mixer settings and five Serum presets are preserved.',
    f'Piano revision seed {SEED}; original other-layer seed 20261012. No combined MIDI or audio requested.']
SOURCE.joinpath('composition.json').write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')
counts=Counter(n['start'] for n in piano['notes'])
stats={'seed':SEED,'notes':len(piano['notes']),'chord_strikes':len(gestures),'improvised_phrase_count':len(fills),
    'fill_bars':[x['bar'] for x in fills],'pitches':[min(by_pitch),max(by_pitch)],
    'velocity_range':[min(n['velocity'] for n in piano['notes']),max(n['velocity'] for n in piano['notes'])],
    'notes_on_chord_attacks_fraction':round(sum(v for v in counts.values() if v>=4)/len(piano['notes']),4),
    'unique_velocities':len({n['velocity'] for n in piano['notes']}),
    'unique_gates':len({n['duration'] for n in piano['notes']})}
SOURCE.joinpath('piano-performance-design.json').write_text(json.dumps({'stats':stats,'chord_gestures':gestures,'improvised_fragments':fills},indent=2)+'\n',encoding='utf-8')
print(json.dumps(stats,indent=2))
