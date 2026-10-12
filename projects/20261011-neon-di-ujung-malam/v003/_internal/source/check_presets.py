"""Readback reused native presets with the same upstream modules as Serum MCP."""
import hashlib
import json
from pathlib import Path
import sys
from serum_mcp.preset.introspect import extract_spec
from serum_mcp.preset.packer import unpack_file
from serum_mcp.preset.safety import scan_wire_types

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'integrations/check_serum_mcp.py').is_file())
sys.path.insert(0, str(ROOT / 'integrations'))
from check_serum_mcp import contains

project = ROOT / 'projects/20261011-neon-di-ujung-malam'
output = project / 'v003'
origin = project / 'v002'
check = output / '_internal/preset-check'
check.mkdir(parents=True,exist_ok=True)
specs = json.loads((HERE / 'preset-spec.json').read_text(encoding='utf-8'))
receipt = {'ok':False, 'origin':'v002', 'upstream':'Celian-mrc/serum-mcp',
           'commit':'7299f2eea1acd2ae5a863965f5bd4beedf107ee8',
           'plugin_loaded':False,'auditioned':False,'presets':[]}
for wanted in specs:
    path = output / 'Presets' / (wanted['name']+'.SerumPreset')
    assert path.read_bytes() == (origin / 'Presets' / path.name).read_bytes()
    native = unpack_file(path)
    issues = scan_wire_types(native.data)
    assert not issues, issues
    actual = extract_spec(native.data).model_dump(by_alias=True)
    comparison = {field:contains(actual[field],wanted[field]) for field in
                  ['oscillators','filters','envelopes','lfos','macros','fx_chain','global']}
    comparison['mod_routes'] = all(any(contains(r,w) for r in actual['mod_routes']) for w in wanted['mod_routes'])
    comparison['name'] = native.metadata.get('presetName') == wanted['name']
    assert all(comparison.values()), (path.name,comparison)
    (check / (wanted['name']+'-decoded-spec.json')).write_text(json.dumps(actual,indent=2)+'\n',encoding='utf-8')
    receipt['presets'].append({'layer':wanted['name'],'file':'Presets/'+path.name,
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'byte_identical_to_v002':True,
        'wire_type_issues':[],'structural_readback':comparison})
receipt['ok'] = True
(check / 'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print('PASS: seven unchanged native presets, exact requested readback and wire-type scan.')
