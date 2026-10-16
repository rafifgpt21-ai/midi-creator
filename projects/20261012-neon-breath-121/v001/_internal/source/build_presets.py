"""Build through the real serum-mcp stdio server and audit delivered bytes."""
import asyncio
from datetime import timedelta, datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).resolve().parent
WORKSPACE = next(p for p in HERE.parents if (p/'studio.local.json').is_file())
PROJECT = WORKSPACE/'projects/20261012-neon-breath-121'
OUTPUT = PROJECT/'v001'
REPO = WORKSPACE/'integrations/serum-mcp'
sys.path.insert(0,str(REPO/'src'))
from serum_mcp.generation.spec import PresetSpec
from serum_mcp.preset.introspect import extract_spec
from serum_mcp.preset.packer import unpack_file
from serum_mcp.preset.safety import scan_wire_types
from serum_mcp.tools._naming import sanitize_subfolder,slugify_preset_name

def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def matches(a,b):
    if isinstance(b,dict):return isinstance(a,dict) and all(k in a and matches(a[k],v) for k,v in b.items())
    if isinstance(b,list):return isinstance(a,list) and len(a)>=len(b) and all(matches(a[i],v) for i,v in enumerate(b))
    if type(a) in (int,float) and type(b) in (int,float):return math.isclose(a,b,abs_tol=1e-5,rel_tol=1e-5)
    return a==b

async def main():
    specs=json.loads((HERE/'preset-specs.json').read_text(encoding='utf-8'))
    cfg=json.loads((WORKSPACE/'studio.local.json').read_text(encoding='utf-8'))
    root=Path(cfg['serum_presets']).parent
    bank='MIDI Creator/20261012-neon-breath-121/v001'
    receipt_dir=OUTPUT/'_internal/serum'
    receipt_dir.mkdir(parents=True,exist_ok=True)
    (OUTPUT/'Presets').mkdir(exist_ok=True)
    for ident,raw in specs.items():
        PresetSpec.model_validate(raw)
        target=root/'Presets/User'/sanitize_subfolder(bank)/(slugify_preset_name(raw['name'])+'.SerumPreset')
        if target.exists():
            prior=receipt_dir/ident/'preset-spec.json'
            if not prior.exists() or json.loads(prior.read_text(encoding='utf-8'))!=raw:
                raise FileExistsError(f'Preserve existing preset: {target}')
    env={'SERUM_PRESETS_PATH':str(root/'Presets/User'),'SERUM_TABLES_PATH':str(root/'Tables'),'SERUM_SAMPLES_PATH':str(root/'Samples')}
    params=StdioServerParameters(command=str(REPO/'.venv/Scripts/python.exe'),args=['-m','serum_mcp.server'],cwd=str(REPO),env=env)
    receipts=[]
    async with stdio_client(params) as (reader,writer):
        async with ClientSession(reader,writer,read_timeout_seconds=timedelta(seconds=90)) as client:
            await client.initialize()
            async def call(name,args):
                res=await client.call_tool(name,args)
                if res.isError:raise RuntimeError(f'{name}: {res.content}')
                return '\n'.join(v.text for v in res.content if v.type=='text')
            save(receipt_dir/'parameters.json',json.loads(await call('list_parameters',{})))
            save(receipt_dir/'semantic-schema.json',PresetSpec.model_json_schema())
            save(receipt_dir/'tool-schemas.json',[t.model_dump() for t in (await client.list_tools()).tools])
            for query in ['disco analog bass','analog brass pad pluck']:
                ref=json.loads(await call('find_reference_presets',{'query':query,'limit':3}))
                save(receipt_dir/(query.replace(' ','-')+'-references.json'),ref)
            for rel in ['Bass/Retro Analog/BA - Eighty.SerumPreset','Pad/PD - Analog Butter.SerumPreset']:
                desc=await call('describe_preset',{'preset_path':str(root/'Presets/Factory'/rel)})
                (receipt_dir/(Path(rel).stem+'-reference.txt')).write_text(desc,encoding='utf-8')
            for ident,raw in specs.items():
                out=receipt_dir/ident;out.mkdir(exist_ok=True)
                save(out/'preset-spec.json',raw)
                installed=root/'Presets/User'/sanitize_subfolder(bank)/(slugify_preset_name(raw['name'])+'.SerumPreset')
                if installed.exists():
                    res=(out/'generate-response.txt').read_text(encoding='utf-8')
                else:
                    res=await call('generate_preset',{'spec':raw,'subfolder':bank})
                    (out/'generate-response.txt').write_text(res,encoding='utf-8')
                source=Path(res.splitlines()[0])
                target=OUTPUT/'Presets'/f'{ident}.SerumPreset'
                if target.exists():
                    if target.read_bytes()!=source.read_bytes():raise FileExistsError(target)
                else:shutil.copy2(source,target)
                desc=await call('describe_preset',{'preset_path':str(target)})
                (out/'description.txt').write_text(desc,encoding='utf-8')
                native=unpack_file(target)
                recovered=extract_spec(native.data).model_dump(by_alias=True)
                save(out/'decoded-spec.json',recovered)
                comparisons={k:matches(recovered[k],raw[k]) for k in ['oscillators','filters','envelopes','lfos','macros','fx_chain','global']}
                # extract_spec returns None for disabled arp; inspect the stored switch.
                comparisons['arp']=not raw['arp']['enabled'] and native.data['Arp0']['plainParams']['kParamEnabled']==0.0
                comparisons['mod_routes']=all(any(matches(a,w) for a in recovered['mod_routes']) for w in raw['mod_routes'])
                comparisons['name']=native.metadata.get('presetName')==raw['name']
                issues=[str(v) for v in scan_wire_types(native.data)]
                save(out/'comparison.json',comparisons)
                dependency_paths=[]
                for i in range(3):
                    container=native.data.get(f'Oscillator{i}',{}).get(f'WTOsc{i}',{})
                    rel=container.get('relativePathToWT')
                    if rel:dependency_paths.append(dict(kind='factory_wavetable',relative_path=rel,exists=(root/'Tables'/rel).is_file()))
                ok=all(comparisons.values()) and not issues and all(d['exists'] for d in dependency_paths)
                receipt=dict(layer=ident,ok=ok,file=str(target),installed=str(source),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                    copy_hash_matches=hashlib.sha256(target.read_bytes()).digest()==hashlib.sha256(source.read_bytes()).digest(),
                    structural_readback=comparisons,wire_type_issues=issues,dependencies=dependency_paths,
                    plugin_loaded=False,audio_rendered=False,auditioned=False)
                save(out/'receipt.json',receipt);receipts.append(receipt)
                print(f'{ident}: structural_ok={ok}',flush=True)
                if not ok:raise ValueError(f'Readback failed: {ident}, {comparisons}, {issues}')
    manifest=dict(ok=all(r['ok'] for r in receipts),checked_at=datetime.now(timezone.utc).isoformat(),
        repository='https://github.com/Celian-mrc/serum-mcp',
        commit=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip(),
        presets=receipts,custom_dependencies=[],plugin_loaded=False,audio_rendered=False,auditioned=False,
        limitations=['Direct Sub requires host LP80 and real kick sidechain for the specified signal path.',
                     'Noise rise / impact is continuous velocity crossfade, not hard key split.',
                     'Delay mode=1 observed in Factory; ping-pong UI meaning not verified. Set ping-pong manually if desired.',
                     'Bell uses Space reverb; no pitch-shift shimmer is implemented.'])
    save(receipt_dir/'manifest.json',manifest)
    print('10 native presets generated and structurally verified.',flush=True)

if __name__=='__main__':asyncio.run(main())
