"""Publish native presets/sources and audit the requested musical performance."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess, sys
import mido
SOURCE = Path(__file__).resolve().parent
PROJECT = SOURCE.parent.parent
OUT = PROJECT/'v001'
spec = json.loads((SOURCE/'composition.json').read_text(encoding='utf-8'))
save = lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
presets = ['sub-bass','bass-grit','shadow-pad','ghost-bell','tension-rise']
(OUT/'Presets').mkdir(exist_ok=True)
bindings = {'piano':{'instrument':'User-selected piano','preset':None,'pitch_range':[36,80]}}
receipts = {}
for id in presets:
    folder = PROJECT/'_internal'/('preset-check-'+id+('-retry' if id=='bass-grit' else ''))
    r = json.loads((folder/'receipt.json').read_text(encoding='utf-8'))
    assert r['ok'] and all(r['preset']['structural_readback'].values())
    path = OUT/'Presets'/(id+'.SerumPreset')
    if not path.exists():
        shutil.copy2(folder/path.name,path)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==r['preset']['sha256']
    receipts[id]=r
    bindings[id]={'instrument':'Serum 2','preset':'Presets/'+path.name,'plugin_loaded':False,'auditioned':False}
drums={'kick':36,'snare':38,'rim':41,'closed-hat':54,'open-hat':57,'crash':64,'floor-tom':47}
for id,pitch in drums.items():
    bindings[id]={'instrument':'User-selected drum sampler','pitch':pitch,'channel':10,'sample':None}
save(SOURCE/'bindings.json',bindings)
save(OUT/'_internal'/'preset-receipts.json',receipts)
shutil.copytree(SOURCE,OUT/'_internal'/'source',dirs_exist_ok=True)
for command,args in [('validate',[str(SOURCE/'composition.json')]),('verify',[str(OUT)])]:
    run=subprocess.run([sys.executable,'-m','midi_creator',command,*args],capture_output=True,text=True)
    assert run.returncode==0,(run.stdout,run.stderr)
    report=json.loads(run.stdout)
    assert report['ok']
    save(OUT/'_internal'/(command+'-receipt.json'),report)
layers={x['id']:x for x in spec['layers']}
inventory={}
for id,item in layers.items():
    mf=mido.MidiFile(OUT/'MIDI'/(id+'.mid'))
    assert mf.type==1 and len(mf.tracks)==1 and mf.ticks_per_beat==480
    assert sum(m.time for m in mf.tracks[0])==215040
    assert not any(m.type in ['sysex','program_change','text','key_signature','marker'] for m in mf.tracks[0])
    hits=[m for m in mf.tracks[0] if m.type=='note_on' and m.velocity]
    if id in drums:
        assert {m.note for m in hits}=={drums[id]} and {m.channel for m in hits}=={9}
    inventory[id]={'tracks':1,'end_tick':215040,'notes':len(hits),
        'pitch_range':[min(m.note for m in hits),max(m.note for m in hits)],
        'velocity_range':[min(m.velocity for m in hits),max(m.velocity for m in hits)]}
choruses=[(128,192),(304,368),(400,432)]
assert all(any(a<=n['start']<b for a,b in choruses) for n in layers['bass-grit']['notes'])
for beat in [128,304,400]:
    assert any(n['start']==beat and n['pitch']==29 and n['velocity']>=120 for n in layers['sub-bass']['notes'])
    for id in ['bass-grit','kick','crash']:
        assert any(n['start']==beat for n in layers[id]['notes'])
    for item in layers.values():
        assert not any(n['start']<beat and n['start']+n['duration']>beat-1+0.0001 for n in item['notes']),(item['id'],beat)
piano=layers['piano']['notes']
vels=[n['velocity'] for n in piano]
assert max(vels)-min(vels)>=80 and len(set(vels))>=60
assert len({n['duration'] for n in piano})>=100
mean=lambda a:sum(a)/len(a)
sub=layers['sub-bass']['notes']
verse_v=mean([n['velocity'] for n in sub if any(a<=n['start']<b for a,b in [(32,96),(208,272)])])
chorus_v=mean([n['velocity'] for n in sub if any(a<=n['start']<b for a,b in choruses)])
assert chorus_v-verse_v>40
assert {p.name for p in OUT.iterdir()}=={'README.md','MIDI','Presets','_internal'}
audit={'ok':True,'files':inventory,'seed':20261012,'drop_bars':[33,77,101],
    'pre_drop_silence_beats':1,'piano_unique_velocities':len(set(vels)),
    'piano_unique_durations':len({n['duration'] for n in piano}),
    'verse_sub_mean_velocity':round(verse_v,2),'chorus_sub_mean_velocity':round(chorus_v,2),
    'preset_structure_readback':True,'preset_count':5,'all_readme_links_exist':True,
    'plugin_loaded':False,'cubase_import_tested':False,'audio_rendered':False,'listened':False}
save(OUT/'_internal'/'performance-audit.json',audit)
for path in [OUT/'README.md',PROJECT/'README.md']:
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        if '://' not in target and not target.startswith('#'):
            assert (path.parent/target).exists(),(path,target)
print(json.dumps({k:v for k,v in audit.items() if k!='files'},indent=2))
