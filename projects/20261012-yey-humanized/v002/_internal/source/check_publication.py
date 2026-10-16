"""Persist CLI receipts and check the final producer package without editing MIDI."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent
PROJECT = OUT.parent
checks = {}
tasks = {
    'validate': ['validate', str(HERE / 'composition.json')],
    'verify': ['verify', str(OUT)],
    'verify_previous': ['verify', str(PROJECT / 'v001')],
}
for label, args in tasks.items():
    result = subprocess.run(['uv', 'run', 'midi-creator', *args], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, (label, result.stderr, result.stdout)
    data = json.loads(result.stdout)
    assert data['ok'], data
    checks[label] = {'exit_code': result.returncode, 'ok': data['ok']}
    (OUT / '_internal' / (label + '-receipt.json')).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

links = []
for doc in (OUT / 'README.md', PROJECT / 'README.md'):
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', doc.read_text(encoding='utf-8')):
        if target.startswith('https://'):
            continue
        destination = (doc.parent / target).resolve()
        assert destination.exists(), (doc, target)
        links.append({'document': str(doc.relative_to(PROJECT)), 'target': target, 'exists': True})
source = json.loads((HERE / 'composition.json').read_text(encoding='utf-8'))
snapshot = json.loads((OUT / '_internal/composition.json').read_text(encoding='utf-8'))
assert source == snapshot
assert {p.name for p in OUT.iterdir()} == {'README.md', 'MIDI', 'Presets', '_internal'}
hashes = {str(f.relative_to(OUT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((OUT / 'MIDI').glob('*.mid'))}
assert len(hashes) == 7
receipt = {
    'ok': True, 'checks': checks, 'source_equals_export_snapshot': True,
    'readme_links': links, 'midi_sha256': hashes,
    'live_import_tested': False, 'requested_patch_loading_tested': False,
    'audio_rendered': False, 'audio_listened': False,
}
(OUT / '_internal/delivery-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'ok': True, 'checks': checks, 'readme_local_links': len(links), 'midi_files': len(hashes), 'source_equals_snapshot': True}))
