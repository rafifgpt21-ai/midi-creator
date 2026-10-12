"""Final inventory, link, preset checksum and MIDI checks; save an evidence receipt."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
REV=HERE.parents[1]
WORKSPACE=next(p for p in HERE.parents if (p/'src/midi_creator').is_dir())
result=subprocess.run(['uv','run','midi-creator','verify',str(REV)],cwd=WORKSPACE,
                      capture_output=True,text=True,check=True)
report=json.loads(result.stdout)
assert report['ok'],report
(REV/'_internal/midi-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

composition=json.loads((REV/'_internal/composition.json').read_text(encoding='utf-8'))
assert composition==json.loads((HERE/'composition.json').read_text(encoding='utf-8'))
scale={0,2,4,5,7,9,10}
allowed_drums=set(map(int,json.loads((REV/'_internal/drum-map.json').read_text(encoding='utf-8'))['mapping']))
for layer in composition['layers']:
    if layer['kind']=='melodic':
        assert all(n['pitch']%12 in scale for n in layer['notes']),layer['id']
    else:
        assert all(n['pitch'] in allowed_drums for n in layer['notes'])
assert len(list((REV/'MIDI').glob('*.mid')))==7
assert len(list((REV/'Presets').glob('*.SerumPreset')))==6

preset_receipt=json.loads((REV/'_internal/preset-receipt.json').read_text(encoding='utf-8'))
assert preset_receipt['ok']
for patch in preset_receipt['presets']:
    assert all(patch['structural_readback'].values())
    assert hashlib.sha256((REV/patch['file']).read_bytes()).hexdigest()==patch['sha256']

links=[]
for readme in (REV/'README.md',REV.parent/'README.md'):
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',readme.read_text(encoding='utf-8')):
        if not target.startswith(('https:','http:')):
            path=readme.parent/target
            assert path.is_file(),path
            links.append(str(path.relative_to(REV.parent)))
assert set(p.name for p in REV.iterdir())=={'README.md','MIDI','Presets','_internal'}
receipt=dict(ok=True,checked_at=datetime.now(timezone.utc).isoformat(),
    midi_ok=report['ok'],layers=7,native_presets=6,notes=sum(len(x['notes']) for x in composition['layers']),
    all_links_exist=True,link_count=len(links),source_matches_snapshot=True,
    all_melodic_notes_in_D_natural_minor=True,drums_use_user_map=True,
    preset_checksums_match=True,producer_layout_ok=True,
    plugin_loaded=False,cubase_import_tested=False,audio_rendered=False,audio_listened=False)
(REV/'_internal/final-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
