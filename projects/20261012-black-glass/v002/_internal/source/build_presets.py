"""Build v002 through real serum-mcp and check semantic/schema and native types."""
from pathlib import Path
import json, subprocess, sys
from serum_mcp.generation.spec import PresetSpec
from serum_mcp.preset.packer import unpack_file
from serum_mcp.preset.introspect import extract_spec
from serum_mcp.preset.safety import scan_wire_types

SOURCE=Path(__file__).resolve().parent
WORKSPACE=next(p for p in SOURCE.parents if (p/'integrations/serum-mcp').is_dir())
schema=PresetSpec.model_json_schema(by_alias=True)
params=json.loads((SOURCE/'serum-parameters.json').read_text(encoding='utf-8'))

def check_keys(value,node,path='spec'):
    if '$ref' in node:
        node=schema['$defs'][node['$ref'].split('/')[-1]]
    if value is None:
        return
    if 'anyOf' in node:
        options=[n for n in node['anyOf'] if n.get('type')!='null']
        if len(options)==1:
            check_keys(value,options[0],path)
        return
    if isinstance(value,dict) and 'properties' in node:
        unknown=set(value)-set(node['properties'])
        assert not unknown,(path,unknown)
        for key,item in value.items():
            check_keys(item,node['properties'][key],path+'.'+key)
    elif isinstance(value,list) and 'items' in node:
        for index,item in enumerate(value):
            check_keys(item,node['items'],path+f'[{index}]')

for path in sorted((SOURCE/'preset-specs').glob('*.json')):
    raw=json.loads(path.read_text(encoding='utf-8'))
    check_keys(raw,schema)
    PresetSpec.model_validate(raw)
    for unit in raw['fx_chain']:
        assert not set(unit['params'])-set(params['fx_params'][unit['type']]),unit
    id=path.stem
    output=SOURCE/'checks'/id
    if output.exists():
        prior=json.loads((output/'receipt.json').read_text(encoding='utf-8'))
        assert prior['ok'] and json.loads((output/'preset-spec.json').read_text(encoding='utf-8'))==raw
    else:
        run=subprocess.run([sys.executable,str(WORKSPACE/'integrations/check_serum_mcp.py'),
            '--spec',str(path),'--subfolder','MIDI Creator/20261012-black-glass/v002',
            '--out',str(output),'--query','dark'],cwd=WORKSPACE,capture_output=True,text=True,encoding='utf-8')
        (SOURCE/(id+'-build.log')).write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
        if run.returncode:
            print(run.stdout+run.stderr)
            raise RuntimeError(f'Native build/readback failed: {id}')
    native=output/(id+'.SerumPreset')
    preset=unpack_file(native)
    issues=scan_wire_types(preset.data)
    assert not issues,(id,issues)
    actual=extract_spec(preset.data)
    assert preset.data['Arp0']['plainParams']['kParamEnabled']==0.0
    check=subprocess.run([sys.executable,str(WORKSPACE/'integrations/serum-mcp/scripts/check_preset.py'),str(native)],
        cwd=WORKSPACE,capture_output=True,text=True,encoding='utf-8')
    (output/'wire-check.log').write_text(check.stdout+check.stderr,encoding='utf-8')
    assert check.returncode==0,check.stderr
    evidence={'ok':True,'semantic_unknown_fields':[],'wire_issues':[],
        'arp_disabled':True,'plugin_loaded':False,'rendered':False,'listened':False}
    (output/'extended-readback.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'preset':id,**evidence}),flush=True)
