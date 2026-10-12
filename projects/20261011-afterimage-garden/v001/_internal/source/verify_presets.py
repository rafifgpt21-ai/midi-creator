"""Verify native serum-mcp patches and copy their exact bytes into the revision."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
WORKSPACE = next(p for p in HERE.parents if (p/'integrations/serum-mcp').is_dir())
sys.path.insert(0, str(WORKSPACE))
from integrations.check_serum_mcp import contains
from serum_mcp.generation.spec import PresetSpec
from serum_mcp.preset.introspect import extract_spec
from serum_mcp.preset.packer import unpack_file
from serum_mcp.preset.schema import SIMPLE_WAVETABLES


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--revision',type=Path,required=True)
    args=parser.parse_args()
    rev=args.revision.resolve()
    out=rev/'Presets'
    out.mkdir(exist_ok=True)
    conf=json.loads((WORKSPACE/'studio.local.json').read_text(encoding='utf-8'))
    root=Path(conf['serum_presets']).parent
    bank=root/'Presets/User/MIDI Creator/20261011-afterimage-garden/v001'
    tables=root/'Tables'
    records=[]
    for raw in json.loads((HERE/'preset-specs.json').read_text(encoding='utf-8')):
        spec=PresetSpec.model_validate(raw)
        src=bank/(spec.name+'.SerumPreset')
        dest=out/src.name
        assert src.is_file(),src
        unpacked=unpack_file(src)
        actual=extract_spec(unpacked.data).model_dump(by_alias=True)
        comparisons={field: contains(actual[field],raw[field]) for field in
            ('oscillators','filters','envelopes','lfos','macros','fx_chain','global') if field in raw}
        comparisons['mod_routes']=all(any(contains(route,wanted) for route in actual['mod_routes']) for wanted in raw.get('mod_routes',[]))
        comparisons['name']=unpacked.metadata.get('presetName')==spec.name
        if 'arp' in raw:
            if raw['arp']=={'enabled': False}:
                # Upstream intentionally returns None for disabled arps. Check wire state.
                comparisons['arp_disabled']=unpacked.data['Arp0']['plainParams']['kParamEnabled'] == 0.0
            else:
                comparisons['arp']=contains(actual['arp'],raw['arp'])
        (HERE/(spec.name+'-readback.json')).write_text(json.dumps(actual,indent=2)+'\n',encoding='utf-8')
        if not all(comparisons.values()):
            raise ValueError(f'{spec.name}: {comparisons}')
        dependencies=[]
        for i,o in enumerate(raw['oscillators'][:3]):
            if o.get('enabled'):
                dependency=tables/SIMPLE_WAVETABLES[o['wavetable']].relative_path
                assert dependency.is_file(),dependency
                dependencies.append(str(dependency))
        if dest.exists():
            assert dest.read_bytes()==src.read_bytes(), 'Preserve changed destination preset'
        else:
            shutil.copy2(src,dest)
        records.append(dict(layer_id=spec.name,file='Presets/'+src.name,installed=str(src),
            bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
            structural_readback=comparisons,factory_wavetables=dependencies))
    bindings={r['layer_id']:dict(plugin='Serum 2',native_preset=r['file'],
              installed=r['installed']) for r in records}
    bindings['disco-kit']=dict(plugin='User-selected external drum kit',midi_channel=10,
        sample_selection='pending user kit',numeric_mapping='drum-map.json')
    (rev/'_internal/bindings.json').write_text(json.dumps(bindings,indent=2)+'\n',encoding='utf-8')
    receipt=dict(ok=True,checked_at=datetime.now(timezone.utc).isoformat(),
        repository='https://github.com/Celian-mrc/serum-mcp',
        commit=subprocess.check_output(['git','-C',str(WORKSPACE/'integrations/serum-mcp'),'rev-parse','HEAD'],text=True).strip(),
        generated_via='mcp__serum_mcp__generate_preset',described_via='mcp__serum_mcp__describe_preset',
        plugin_loaded=False,audio_rendered=False,audio_listened=False,cubase_import_tested=False,
        presets=records)
    (rev/'_internal/preset-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(ok=True,presets=len(records),all_readbacks_match=True,factory_dependencies_exist=True)))


if __name__=='__main__': main()
