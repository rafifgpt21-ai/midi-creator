"""Publish v003 and verify piano-only scope, phrasing and preserved sound files."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,shutil,subprocess,sys
import mido

SOURCE=Path(__file__).resolve().parent
WORKSPACE=next(p for p in SOURCE.parents if (p/'integrations/serum-mcp').is_dir())
PROJECT=next(p for p in SOURCE.parents if (p/'v002').is_dir())
OUT=PROJECT/'v003'
OLD=PROJECT/'v002'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
new=json.loads((OUT/'_internal/composition.json').read_text(encoding='utf-8'))
old=json.loads((OLD/'_internal/composition.json').read_text(encoding='utf-8'))
newlayers={x['id']:x for x in new['layers']}
oldlayers={x['id']:x for x in old['layers']}
assert len(newlayers)==13
preserved=[]
for id in newlayers:
    if id!='piano':
        assert newlayers[id]==oldlayers[id]
        assert sha(OUT/'MIDI'/(id+'.mid'))==sha(OLD/'MIDI'/(id+'.mid'))
        preserved.append(id)
assert sha(OUT/'MIDI/piano.mid')!=sha(OLD/'MIDI/piano.mid')
for field in ['tempo_bpm','time_signature','bars','ticks_per_beat','timing','key_signature','sections']:
    assert new[field]==old[field]
for field in ['volume','pan','program','kind','channel']:
    assert newlayers['piano'].get(field)==oldlayers['piano'].get(field)

(OUT/'Presets').mkdir(exist_ok=True)
native_paths=[]
for path in sorted((OLD/'Presets').glob('*.SerumPreset')):
    dest=OUT/'Presets'/path.name
    if dest.exists():
        assert sha(dest)==sha(path)
    else:
        shutil.copy2(path,dest)
    assert sha(dest)==sha(path)
    native_paths.append(str(dest))
assert len(native_paths)==5
upstream=WORKSPACE/'integrations/serum-mcp/.venv/Scripts/python.exe'
wire=subprocess.run([str(upstream),str(WORKSPACE/'integrations/serum-mcp/scripts/check_preset.py'),*native_paths],
    capture_output=True,text=True,encoding='utf-8',cwd=WORKSPACE)
(OUT/'_internal/preset-wire-check.log').write_text(wire.stdout+wire.stderr,encoding='utf-8')
assert wire.returncode==0,wire.stderr
for name in ['preset-receipts.json','resource-manifest.json']:
    shutil.copy2(OLD/'_internal'/name,OUT/'_internal'/name)
bindings=json.loads((OLD/'_internal/source/bindings.json').read_text(encoding='utf-8'))
bindings['piano']['pitch_range']=[36,75]
bindings['piano']['performance_revision']='v003'
save(SOURCE/'bindings.json',bindings)
shutil.copytree(OLD/'_internal/source/preset-specs',SOURCE/'preset-specs',dirs_exist_ok=True)
shutil.copy2(SOURCE/'producer-readme.md',OUT/'README.md')

for command,args in [('validate',[str(SOURCE/'composition.json')]),('verify',[str(OUT)])]:
    run=subprocess.run([sys.executable,'-m','midi_creator',command,*args],capture_output=True,text=True,encoding='utf-8')
    assert run.returncode==0,(run.stdout,run.stderr)
    report=json.loads(run.stdout)
    assert report['ok']
    save(OUT/'_internal'/(command+'-receipt.json'),report)

piano=newlayers['piano']['notes']
counts=Counter(n['start'] for n in piano)
fraction=sum(v for v in counts.values() if v>=4)/len(piano)
assert fraction>=.90
design=json.loads((SOURCE/'piano-performance-design.json').read_text(encoding='utf-8'))
assert design['stats']['improvised_phrase_count']==19
assert len({n['velocity'] for n in piano})>=60
assert max(n['velocity'] for n in piano)-min(n['velocity'] for n in piano)>=70
for beat in [128,304,400]:
    assert all(not(n['start']<beat and n['start']+n['duration']>beat-1+.0001)
        for layer in new['layers'] for n in layer['notes']),beat
inventory={}
for path in sorted((OUT/'MIDI').glob('*.mid')):
    midi=mido.MidiFile(path)
    assert midi.type==1 and len(midi.tracks)==1 and midi.ticks_per_beat==480
    assert sum(m.time for m in midi.tracks[0])==215040
    inventory[path.name]={'sha256':sha(path),'tracks':1,'end_tick':215040,
        'preserved_from_v002':path.stem!='piano'}
audit={'ok':True,'revision':'v003','origin_revision':'v002','changed_layers':['piano'],
    'preserved_layers':preserved,'midi':inventory,'piano':design['stats'],
    'presets_identical_to_v002':True,'native_wire_scan':'pass',
    'pre_drop_gaps_preserved':True,'plugin_loaded':False,'cubase_import_tested':False,
    'rendered_audio_analyzed':False,'listened':False}
save(OUT/'_internal/revision-audit.json',audit)
shutil.copytree(SOURCE,OUT/'_internal/source',dirs_exist_ok=True)
for target in re.findall(r'\]\(([^)]+)\)',(OUT/'README.md').read_text(encoding='utf-8')):
    if '://' not in target and not target.startswith('#'):
        assert (OUT/target).exists(),target
assert {x.name for x in OUT.iterdir()}=={'README.md','MIDI','Presets','_internal'}
(PROJECT/'README.md').write_text('''# Black Glass

Dark trap R&B with expressive piano and heavy chorus bass drops.

[Open latest v003](v003/README.md) — chord-focused piano with restrained improvisation. 136 BPM, F minor, 4/4, 112 bars, 13 layers. Other instruments and five v002 Serum sounds are preserved.

Previous revisions: [v002 preset refinement](v002/README.md) · [v001 original piano](v001/README.md).

Producer files are in each revision's `MIDI/` and `Presets/`; sources and receipts are in `_internal/`.
''',encoding='utf-8')
catalog=WORKSPACE/'projects/README.md'
catalog.write_text(catalog.read_text(encoding='utf-8').replace(
    '[v002](20261012-black-glass/v002/README.md)','[v003](20261012-black-glass/v003/README.md)'),encoding='utf-8')
print(json.dumps({'ok':True,'changed_layer':'piano','preserved_layers':len(preserved),
    'chord_attack_note_fraction':round(fraction,4),'improvised_phrases':19,
    'preset_copies_verified':5,'midi_verification':'pass','listened':False},indent=2))
