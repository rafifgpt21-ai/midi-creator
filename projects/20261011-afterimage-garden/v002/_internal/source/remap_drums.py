"""Reproduce the drum-only v002 by remapping v001 articulations, with no timing edits."""
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROJECT=next(p for p in HERE.parents if (p/'v001/_internal/composition.json').is_file())
SOURCE=PROJECT/'v001/_internal/composition.json'
old=json.loads(SOURCE.read_text(encoding='utf-8'))
original=next(layer for layer in old['layers'] if layer['id']=='disco-kit')
MAPPING={17:53,21:56,36:36,37:41,38:38,40:40,41:47,42:54,
         44:60,45:46,46:57,47:45,49:64,53:73,55:70,56:88}
DEFAULT={36:'Kick Hit',38:'Snare Hit (Center)',40:'Snare Rimshot',41:'Snare Rim',
         45:'Rack Tom High',46:'Rack Tom Low',47:'Floor Tom',
         53:'Hi-Hat Tight',54:'Hi-Hat Closed',55:'Hi-Hat Loose',
         56:'Hi-Hat Loose / Semi-Open',57:'Hi-Hat Open',58:'Hi-Hat Open',
         59:'Hi-Hat Open',60:'Hi-Hat Pedal',64:'Crash 1 Left',65:'Crash 1 Choke',
         70:'Crash 2 Right',71:'Crash 2 Choke',73:'Ride Bell',74:'Ride Bow',
         75:'Ride Edge / Crash Ride',77:'Shaker',78:'Shaker',
         86:'Hand Tambourine',87:'Hand Tambourine',88:'Stick'}
new=copy.deepcopy(old)
new['layers']=[copy.deepcopy(original)]
new['description']='Drum-only remap of Afterimage Garden v001 using the new user-supplied default map. All performance timing, velocities, gates and global duration preserved.'
new['prompt']='Regenerate only the drum MIDI using the new guide; create a Markdown default drum guide.'
new['assumptions']=[
    'Drum-only v002 supplement to the unchanged six Serum layers in v001.',
    '108 BPM, 4/4, 104 bars, 480 PPQN, strict straight sixteenth grid retained.',
    'Preserve every onset, duration and velocity; change drum pitches by articulation only.',
    'Old sidestick 37 becomes new snare rim 41; old cowbell 56 becomes stick 88 because the new map omits these exact articulations.',
    'Open hats use 57; alternatives 58 and 59 remain unused.',
    'No kit/sample selected or copied.']
for before,after in zip(original['notes'],new['layers'][0]['notes'],strict=True):
    after['pitch']=MAPPING[before['pitch']]
    assert after['pitch'] in DEFAULT
    assert all(after[k]==before[k] for k in ('start','duration','velocity'))
assert len(set(MAPPING.values()))==len(MAPPING)
(HERE/'composition.json').write_text(json.dumps(new,indent=2)+'\n',encoding='utf-8')
(HERE/'drum-map.json').write_text(json.dumps(dict(source='User default drum map supplied 2026-10-12',
    channel=10,selected_kit=None,samples_copied=False,mapping=DEFAULT,
    previous_to_new=MAPPING,used_pitches=sorted({n['pitch'] for n in new['layers'][0]['notes']})),indent=2)+'\n',encoding='utf-8')
hashes={str(p.relative_to(PROJECT/'v001')):hashlib.sha256(p.read_bytes()).hexdigest()
        for folder in ('MIDI','Presets') for p in (PROJECT/'v001'/folder).iterdir() if p.is_file()}
(HERE/'source-checksums.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(notes=len(original['notes']),mapping=MAPPING,timing_velocity_gate_preserved=True)))
