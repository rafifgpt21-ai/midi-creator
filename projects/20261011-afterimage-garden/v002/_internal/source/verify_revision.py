"""Verify the drum-only export and event-level preservation of v001."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import mido

HERE=Path(__file__).resolve().parent
PROJECT=next(p for p in HERE.parents if (p/'v001/_internal/composition.json').is_file())
REV=PROJECT/'v002'
WORKSPACE=next(p for p in HERE.parents if (p/'src/midi_creator').is_dir())

def events(path):
    mf=mido.MidiFile(path)
    assert mf.type==1 and len(mf.tracks)==1 and mf.ticks_per_beat==480
    tick=0
    active={}
    notes=[]
    other=[]
    for msg in mf.tracks[0]:
        tick+=msg.time
        if msg.type=='note_on' and msg.velocity>0:
            key=(msg.channel,msg.note)
            assert key not in active
            active[key]=(tick,msg.velocity)
        elif msg.type=='note_off' or (msg.type=='note_on' and msg.velocity==0):
            start,vel=active.pop((msg.channel,msg.note))
            notes.append((start,tick,msg.channel,msg.note,vel))
        else:
            obj=msg.dict()
            obj.pop('time')
            other.append((tick,obj))
    assert not active
    return notes,other

result=subprocess.run(['uv','run','midi-creator','verify',str(REV)],cwd=WORKSPACE,
                       capture_output=True,text=True,check=True)
report=json.loads(result.stdout)
assert report['ok'] and report['timing']['on_grid']
(REV/'_internal/midi-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
old,old_meta=events(PROJECT/'v001/MIDI/disco-kit.mid')
new,new_meta=events(REV/'MIDI/disco-kit.mid')
mapping=json.loads((HERE/'drum-map.json').read_text(encoding='utf-8'))
remap={int(k):v for k,v in mapping['previous_to_new'].items()}
assert Counter((a,b,c,remap[p],v) for a,b,c,p,v in old)==Counter(new)
assert old_meta==new_meta
assert len(new)==1375
assert all(c==9 and str(p) in mapping['mapping'] for a,b,c,p,v in new)
assert len(list((REV/'MIDI').glob('*.mid')))==1
assert not (REV/'Presets').exists()
for relative,digest in json.loads((HERE/'source-checksums.json').read_text(encoding='utf-8')).items():
    assert hashlib.sha256((PROJECT/'v001'/relative).read_bytes()).hexdigest()==digest
for readme in (REV/'README.md',PROJECT/'README.md'):
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',readme.read_text(encoding='utf-8')):
        assert (readme.parent/target).is_file(),target
guide=WORKSPACE/'docs/default-drum-map.md'
documented=set(int(p) for p in re.findall(r'^\|[^|]+\|\s*(\d+)\s*\|',guide.read_text(encoding='utf-8'),re.M))
assert documented==set(map(int,mapping['mapping']))
assert 'docs/default-drum-map.md' in (WORKSPACE/'AGENTS.md').read_text(encoding='utf-8')
receipt=dict(ok=True,checked_at=datetime.now(timezone.utc).isoformat(),
    revision='v002',source_revision='v001',midi_files=1,tracks=1,notes=len(new),
    note_events_match_remapped_v001=True,non_note_events_unchanged=True,
    prior_MIDI_and_presets_unchanged=True,only_drum_exported=True,all_pitches_in_default_map=True,
    default_map_entries=len(documented),readme_links_exist=True,on_grid=True,
    audio_rendered=False,audio_listened=False,cubase_import_tested=False)
(REV/'_internal/revision-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
