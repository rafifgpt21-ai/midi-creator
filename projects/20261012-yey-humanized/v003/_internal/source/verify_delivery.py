"""Audit exported revision and prove all six BBC parts are byte-identical."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import mido

HERE = Path(__file__).resolve().parent
PROJECT = next(p for p in HERE.parents if p.name == '20261012-yey-humanized')
OUT = PROJECT / 'v003'
for name, args in [('validate', ['validate', str(OUT/'_internal/composition.json')]), ('verify', ['verify', str(OUT)])]:
    result = subprocess.run([sys.executable, '-m', 'midi_creator', *args], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, (name, result.stdout, result.stderr)
    value = json.loads(result.stdout)
    assert value['ok']
    (OUT/'_internal'/f'{name}-receipt.json').write_text(json.dumps({'exit_code': 0, 'result': value}, indent=2)+'\n', encoding='utf-8')

base = json.loads((PROJECT/'v002/_internal/composition.json').read_text(encoding='utf-8'))
new = json.loads((OUT/'_internal/composition.json').read_text(encoding='utf-8'))
for key in ('tempo_bpm', 'time_signature', 'bars', 'ticks_per_beat', 'timing', 'key_signature', 'sections'):
    assert base[key] == new[key], key
assert new == json.loads((HERE/'composition.json').read_text(encoding='utf-8'))
by_id = {l['id']: l for l in base['layers']}
files, preserved = [], []
for layer in new['layers']:
    path = OUT/'MIDI'/f"{layer['id']}.mid"
    midi = mido.MidiFile(path)
    assert midi.type == 1 and len(midi.tracks) == 1 and midi.ticks_per_beat == 480
    assert sum(m.time for m in midi.tracks[0]) == 145920
    assert not any(m.type in ('sysex', 'program_change', 'text', 'key_signature', 'marker') or m.type == 'control_change' and m.control in (0, 32) for m in midi.tracks[0])
    assert [m.value for m in midi.tracks[0] if m.type == 'control_change' and m.control == 10] == [layer['pan']]
    files.append({'layer': layer['id'], 'tracks': 1, 'end_tick': 145920, 'pan': layer['pan'],
                  'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'notes': sum(m.type == 'note_on' and m.velocity > 0 for m in midi.tracks[0])})
    if layer['id'].startswith('bbc-'):
        assert layer == by_id[layer['id']]
        assert (PROJECT/'v002/MIDI'/path.name).read_bytes() == path.read_bytes()
        preserved.append(layer['id'])
assert len(preserved) == 6 and len(files) == 9
pianos = new['layers'][:3]
assert [l['id'] for l in pianos] == ['piano-center', 'piano-left', 'piano-right']
assert max(n['duration'] for n in pianos[0]['notes']) <= 8
plan = json.loads((HERE/'performance-design.json').read_text(encoding='utf-8'))
for n in pianos[2]['notes']:
    assert n['pitch'] >= plan['center_anchors'][int(n['start']//4)][-1] + 2
cello = next(l['notes'] for l in new['layers'] if l['id'] == 'bbc-celli')
assert not [(l['id'], n, w) for l in pianos for n in l['notes'] for w in cello if abs(n['pitch']-w['pitch']) == 1 and n['start'] < w['start']+w['duration'] and w['start'] < n['start']+n['duration']]
links = []
for readme in (OUT/'README.md', PROJECT/'README.md'):
    for target in re.findall(r'\]\(([^)]+)\)', readme.read_text(encoding='utf-8-sig')):
        if '://' in target or target.startswith('#'):
            continue
        assert (readme.parent/target.split('#')[0]).resolve().exists(), (readme, target)
        links.append(target)
assert {p.name for p in OUT.iterdir()} == {'README.md', 'MIDI', '_internal'}
receipt = {'ok': True, 'global_timeline_identical': True, 'bbc_specs_and_midi_bytes_identical': preserved,
           'midi_files': files, 'readme_links_checked': links,
           'center_max_gate_beats': max(n['duration'] for n in pianos[0]['notes']),
           'right_above_center_upper_voice': True, 'piano_cello_adjacent_semitone_overlaps': 0,
           'plugin_loading_tested': False, 'live_cubase_import_tested': False, 'audio_rendered': False, 'actual_listening': False}
(OUT/'_internal/delivery-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'ok': True, 'unchanged_bbc': len(preserved), 'midi_files': len(files), 'notes': sum(f['notes'] for f in files), 'checked_readme_links': len(links)}, indent=2))
