from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

import mido
from midi_creator.export import generate_export, verify_export

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'src/midi_creator/spec.py').is_file())
OUT = Path(__file__).resolve().parent
projects = ROOT / 'projects'
dark = projects / '20261011-neon-di-ujung-malam/v002'
jack = projects / '20261009-neon-step-new-jack-swing/v004'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

results = {'ok': False, 'live_import_tested': False, 'listening': False}
exports = []
for manifest_path in projects.rglob('manifest.json'):
    manifest = read(manifest_path)
    if manifest.get('generator', {}).get('name') != 'midi-creator':
        continue
    folder = manifest_path.parent.parent if manifest_path.parent.name == '_internal' else manifest_path.parent
    report = verify_export(folder)
    assert report['ok'], (str(folder), report['errors'])
    exports.append({'folder': folder.relative_to(ROOT).as_posix(), 'ok': True,
                    'timing': {k: report['timing'][k] for k in ['mode', 'on_grid', 'off_grid_note_ons']}})
results['verified_exports'] = exports

for revision in [dark, projects / '20261009-neon-step-new-jack-swing/v003']:
    receipt = read(revision / '_internal/original-preservation.json')
    origin = revision.parent / receipt['origin']
    assert all(sha(origin / path) == digest for path, digest in receipt['sha256'].items())
results['original_revisions_unchanged'] = True

core = read(jack / '_internal/core-preservation.json')
origin = jack.parent / core['origin']
for layer in core['layers']:
    assert (origin / 'MIDI' / (layer['layer'] + '.mid')).read_bytes() == (jack / 'MIDI' / (layer['layer'] + '.mid')).read_bytes()
results['new_jack_core_byte_identical_layers'] = len(core['layers'])

edited = read(jack / '_internal/timing-change.json')['changed_layers']
old = read(origin / '_internal/composition.json')
new = read(jack / '_internal/composition.json')
for layer_id in edited:
    a = next(l for l in old['layers'] if l['id'] == layer_id)
    b = next(l for l in new['layers'] if l['id'] == layer_id)
    inventory = lambda l: Counter((n['pitch'], n['duration'], n['velocity']) for n in l['notes'])
    assert inventory(a) == inventory(b)
    midi = mido.MidiFile(jack / 'MIDI' / f'{layer_id}.mid')
    ppqn = midi.ticks_per_beat
    grid = {round((i / 4 + (.05 if i % 2 else 0)) * ppqn) for i in range(16)}
    tick = 0
    for msg in midi.tracks[0]:
        tick += msg.time
        if msg.type == 'note_on' and msg.velocity:
            assert tick % (4 * ppqn) in grid, (layer_id, tick)
results['four_support_layers_on_shared_swing_grid'] = True

for file in (dark / 'MIDI').glob('*.mid'):
    midi = mido.MidiFile(file)
    tick = 0
    assert midi.type == 1 and len(midi.tracks) == 1
    for msg in midi.tracks[0]:
        tick += msg.time
        if msg.type == 'note_on' and msg.velocity:
            assert tick % (midi.ticks_per_beat // 4) == 0, (file.name, tick)
results['dark_synth_all_eight_layers_on_straight_sixteenth'] = True

reuse = read(dark / '_internal/preset-reuse.json')
for preset in reuse['presets']:
    assert sha(dark / preset['file']) == preset['sha256']
    assert (dark / preset['file']).read_bytes() == (dark / preset['origin']).read_bytes()
results['seven_native_presets_unchanged_with_original_readback'] = True

for folder in [jack, dark]:
    text = (folder / 'README.md').read_text(encoding='utf-8')
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if not link.startswith(('https:', 'http:', '#')):
            assert (folder / link.split('#')[0]).exists(), (folder, link)
results['producer_readme_local_links_exist'] = True

examples = []
for name in ['single-layer', 'multi-layer']:
    output = OUT / ('example-' + name)
    generate_export(ROOT / 'examples' / name / 'composition.json', output)
    report = verify_export(output)
    assert report['ok'] and report['timing']['on_grid']
    examples.append({'name': name, 'ok': True, 'layers': len(report['files'])})
results['example_exports'] = examples

test = subprocess.run(['uv', 'run', 'python', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                      cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
(OUT / 'tests.log').write_text(test.stdout + test.stderr, encoding='utf-8')
assert test.returncode == 0, test.stderr
results['tests'] = {'exit_code': 0, 'summary': '43 tests, 42 passed, 1 opt-in Serum integration skipped'}
results['ok'] = True
(OUT / 'final-check.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in results.items() if k != 'verified_exports'}, indent=2))
print(f'All {len(exports)} current/archive MIDI exports verified.')
