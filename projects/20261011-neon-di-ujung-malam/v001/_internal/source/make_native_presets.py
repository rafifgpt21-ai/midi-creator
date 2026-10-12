"""Generate native sounds through the upstream Serum MCP, then decode/read back.

Run with integrations/serum-mcp/.venv/Scripts/python.exe. Existing outputs are
never overwritten: a resumed run verifies their full requested state instead.
"""
import asyncio
from datetime import datetime,timedelta,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
from serum_mcp.generation.spec import PresetSpec
from serum_mcp.preset.introspect import extract_spec
from serum_mcp.preset.packer import unpack_file
from serum_mcp.tools._naming import sanitize_subfolder,slugify_preset_name

HERE=Path(__file__).resolve().parent
WORKSPACE=next(p for p in HERE.parents if (p/'integrations'/'check_serum_mcp.py').is_file())
sys.path.insert(0,str(WORKSPACE/'integrations'))
from check_serum_mcp import contains
PROJECT=WORKSPACE/'projects'/'20261011-neon-di-ujung-malam'
OUTPUT=PROJECT/'v001'
CHECK=OUTPUT/'_internal'/'preset-check'
BANK='MIDI Creator/20261011-neon-di-ujung-malam/v001'

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

async def main():
    rawspecs=json.loads((HERE/'preset-spec.json').read_text(encoding='utf-8'))
    specs=[PresetSpec.model_validate(raw) for raw in rawspecs]
    config=json.loads((WORKSPACE/'studio.local.json').read_text(encoding='utf-8'))
    repo=WORKSPACE/'integrations'/'serum-mcp'
    root=Path(config['serum_presets']).parent
    presets=root/'Presets'/'User'
    params=StdioServerParameters(command=str(repo/'.venv'/'Scripts'/'python.exe'),
        args=['-m','serum_mcp.server'],cwd=str(repo),env={'SERUM_PRESETS_PATH':str(presets),
        'SERUM_TABLES_PATH':str(root/'Tables'),'SERUM_SAMPLES_PATH':str(root/'Samples')})
    receipt=dict(ok=False,checked_at=datetime.now(timezone.utc).isoformat(),
        repository='https://github.com/Celian-mrc/serum-mcp',
        commit=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),
        bank=BANK,plugin_loaded=False,audio_rendered=False,auditioned=False,presets=[])
    CHECK.mkdir(parents=True,exist_ok=True)
    (OUTPUT/'Presets').mkdir(exist_ok=True)
    try:
        async with stdio_client(params) as (reader,writer):
            async with ClientSession(reader,writer,read_timeout_seconds=timedelta(seconds=90)) as client:
                initialized=await client.initialize()
                receipt['server']=initialized.serverInfo.model_dump()
                available=await client.list_tools()
                save(CHECK/'tool-schemas.json',[t.model_dump() for t in available.tools])
                async def call(name,args):
                    result=await client.call_tool(name,args)
                    if result.isError: raise RuntimeError(f'{name}: {result.content}')
                    return '\n'.join(b.text for b in result.content if b.type=='text')
                save(CHECK/'parameters.json',json.loads(await call('list_parameters',{})))
                refs=json.loads(await call('find_reference_presets',{'query':'synthwave','limit':5}))
                save(CHECK/'references.json',refs)
                for ref in refs.get('results',[])[:1]+refs.get('results',[])[-1:]:
                    desc=await call('describe_preset',{'preset_path':ref['path']})
                    (CHECK/('reference-'+Path(ref['path']).stem+'.txt')).write_text(desc,encoding='utf-8')
                for raw,spec in zip(rawspecs,specs):
                    target=presets/sanitize_subfolder(BANK)/(slugify_preset_name(spec.name)+'.SerumPreset')
                    generated_now=False
                    if not target.exists():
                        reply=await call('generate_preset',{'spec':raw,'subfolder':BANK})
                        (CHECK/(spec.name+'-generation.txt')).write_text(reply,encoding='utf-8')
                        returned=Path(reply.splitlines()[0]).resolve()
                        if returned!=target.resolve(): raise ValueError('Unexpected generated preset path')
                        generated_now=True
                    desc=await call('describe_preset',{'preset_path':str(target)})
                    (CHECK/(spec.name+'-description.txt')).write_text(desc,encoding='utf-8')
                    native=unpack_file(target)
                    actual=extract_spec(native.data).model_dump(by_alias=True)
                    save(CHECK/(spec.name+'-decoded-spec.json'),actual)
                    comparisons={field:contains(actual[field],raw[field]) for field in
                        ('oscillators','filters','envelopes','lfos','macros','fx_chain','global')}
                    comparisons['mod_routes']=all(any(contains(route,wanted) for route in actual['mod_routes'])
                        for wanted in raw['mod_routes'])
                    comparisons['name']=native.metadata.get('presetName')==spec.name
                    save(CHECK/(spec.name+'-comparison.json'),comparisons)
                    if not all(comparisons.values()): raise ValueError(f'{spec.name} readback mismatch: {comparisons}')
                    digest=hashlib.sha256(target.read_bytes()).hexdigest()
                    destination=OUTPUT/'Presets'/(spec.name+'.SerumPreset')
                    if destination.exists():
                        if hashlib.sha256(destination.read_bytes()).hexdigest()!=digest:
                            raise FileExistsError(f'Preserve different existing preset {destination}')
                    else: shutil.copy2(target,destination)
                    receipt['presets'].append(dict(layer=spec.name,file=str(destination),installed=str(target),
                        generated_now=generated_now,sha256=digest,structural_readback=comparisons))
                    save(CHECK/'receipt.json',receipt)
                    print(f'{spec.name}: native preset + exact requested readback PASS',flush=True)
                receipt['ok']=True
    except BaseException as error:
        receipt['error']=str(error)
        raise
    finally: save(CHECK/'receipt.json',receipt)

if __name__=='__main__': asyncio.run(main())
