"""Reduce the observed off-grid output to one actual source note."""
import json
from pathlib import Path
import subprocess
source=Path('projects/20261011-neon-di-ujung-malam/v001/_internal/composition.json')
spec=json.loads(source.read_text(encoding='utf-8'))
drums=next(l for l in spec['layers'] if l['id']=='retro-drums')
bad=next(n for n in drums['notes'] if abs(n['start']*8-round(n['start']*8))>.01)
single=dict(bad,start=round(bad['start']%4,6))
small=dict(version=1,title='One-note grid repro',tempo_bpm=118,time_signature=[4,4],bars=1,ticks_per_beat=960,
           layers=[dict(id='retro-drums',name='One note',kind='drums',notes=[single])])
root=Path('_internal/timing-repair-20261011/minimized')
root.mkdir(exist_ok=False)
path=root/'composition.json'
path.write_text(json.dumps(small,indent=2)+'\n',encoding='utf-8')
subprocess.run(['uv','run','midi-creator','generate',str(path),'--out',str(root/'v001')],check=True)
print('Original observed source note:',bad)
print('Minimal source note:',single)
raise SystemExit(subprocess.run(['uv','run','python','integrations/audit_midi_timing.py',str(root/'v001'),'--strict',
                                '--out',str(root/'audit.json')]).returncode)
