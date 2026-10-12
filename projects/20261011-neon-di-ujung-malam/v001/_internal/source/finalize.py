"""Save verification, structural musical audit, and link/inventory checks."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE=Path(__file__).resolve().parent
WORKSPACE=next(p for p in HERE.parents if (p/'src'/'midi_creator'/'composition.schema.json').is_file())
PROJECT=WORKSPACE/'projects'/'20261011-neon-di-ujung-malam'
OUTPUT=PROJECT/'v001'
INTERNAL=OUTPUT/'_internal'
def save(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

(OUTPUT/'README.md').write_text((HERE/'producer-readme.md').read_text(encoding='utf-8'),encoding='utf-8')

verified=subprocess.run(['uv','run','midi-creator','verify',str(OUTPUT)],cwd=WORKSPACE,capture_output=True,text=True,encoding='utf-8')
save(INTERNAL/'verification.json',json.loads(verified.stdout))
if verified.returncode: raise RuntimeError(verified.stderr)
spec=json.loads((INTERNAL/'composition.json').read_text(encoding='utf-8'))
assert spec['bars']==112 and spec['tempo_bpm']==118 and len(spec['layers'])==8
receipt=json.loads((INTERNAL/'preset-check'/'receipt.json').read_text(encoding='utf-8'))
assert receipt['ok'] and len(receipt['presets'])==7
for item in receipt['presets']:
    assert all(item['structural_readback'].values())
    assert hashlib.sha256(Path(item['file']).read_bytes()).hexdigest()==item['sha256']
audit={'ok':True,'method':'score/specification inspection plus event analysis; no playback',
       'auditioned':False,'layer_ranges':{},'sections':[]}
for layer in spec['layers']:
    notes=layer['notes']
    if layer['kind']=='melodic':
        assert (OUTPUT/'Presets'/(layer['id']+'.SerumPreset')).is_file()
        # F# natural minor; E# is an intentional leading tone in the dominant.
        allowed={1,2,4,6,8,9,11,5}
        assert all(n['pitch']%12 in allowed for n in notes)
    else:
        assert {n['pitch'] for n in notes}=={36,38,39,42,46,49,82}
    assert all(n['start']+n['duration']<=432 for n in notes),'Last four bars reserved for tails'
    audit['layer_ranges'][layer['id']]={'min':min(n['pitch'] for n in notes),'max':max(n['pitch'] for n in notes),
        'notes':len(notes),'first_beat':min(n['start'] for n in notes),'last_note_end_beat':max(n['start']+n['duration'] for n in notes)}
for i,section in enumerate(spec['sections']):
    end=spec['sections'][i+1]['start'] if i+1<len(spec['sections']) else 448
    counts={layer['id']:sum(section['start']<=n['start']<end for n in layer['notes']) for layer in spec['layers']}
    audit['sections'].append({'name':section['name'],'first_bar':int(section['start']/4+1),
                              'last_bar':int(end/4),'note_on_counts':counts})
audit['musical_review']=['Close-voiced extended minor harmony with C#7/E# dominant movement.',
    'Bass and lead monophonic; pad and chords kept in separate registers.',
    'Lead rests and key answers; original chorus motif with cadence variation.',
    'Sparse intro/interlude/breakdown contrast with four-on-the-floor choruses.',
    'Verse two/final chorus add shaker and stronger velocity; ending resolves to F# minor.',
    'No new note in last four bars; Serum release tails have room.']
save(INTERNAL/'musical-review.json',audit)
missing=[]
for readme in (PROJECT/'README.md',OUTPUT/'README.md'):
    for target in re.findall(r'\]\(([^)]+)\)',readme.read_text(encoding='utf-8')):
        if target.startswith(('http://','https://','#')): continue
        if not (readme.parent/target).is_file(): missing.append(str(readme.parent/target))
assert not missing,missing
top={p.name for p in OUTPUT.iterdir()}
assert top=={'README.md','MIDI','Presets','_internal'},top
assert len(list((OUTPUT/'MIDI').glob('*.mid')))==8
assert len(list((OUTPUT/'Presets').glob('*.SerumPreset')))==7
save(INTERNAL/'delivery-check.json',{'ok':True,'midi_files':8,'native_presets':7,'readme_links_exist':True,
    'producer_layout_ok':True,'musical_review':'specification reviewed; not auditioned',
    'plugin_loaded':False,'cubase_import_tested':False,'audio_rendered':False,'auditioned':False})
print('PASS: 8 aligned MIDI files, 7 verified native presets, musical event audit, README links and producer layout.')
