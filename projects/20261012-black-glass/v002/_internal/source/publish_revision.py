"""Publish the reviewed v002 presets, unchanged MIDI bundle and evidence."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,shutil,subprocess,sys
from serum_mcp.preset.packer import unpack_file
from serum_mcp.preset.safety import scan_wire_types
from serum_mcp.preset.wavetable import read_wav_mono

SOURCE=Path(__file__).resolve().parent
WORKSPACE=next(p for p in SOURCE.parents if (p/'integrations/serum-mcp').is_dir())
PROJECT=next(p for p in SOURCE.parents if (p/'v001').is_dir())
OUT=PROJECT/'v002'
OLD=PROJECT/'v001'
save=lambda p,v:p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (OUT/'_internal/composition.json').read_bytes()==(OLD/'_internal/composition.json').read_bytes()
spec=json.loads((SOURCE/'composition.json').read_text(encoding='utf-8'))
config=json.loads((WORKSPACE/'studio.local.json').read_text(encoding='utf-8'))
tables=Path(config['serum_presets']).parent/'Tables'
(OUT/'Presets').mkdir(exist_ok=True)
receipts={}
resources={}
inventory={}
bindings=json.loads((OLD/'_internal/source/bindings.json').read_text(encoding='utf-8'))

def native_resources(value,id):
    if isinstance(value,dict):
        if 'relativePathToWT' in value:
            relative=value['relativePathToWT'].lstrip('/\\')
            path=tables/relative
            assert path.is_file(),(id,path)
            samples,sr=read_wav_mono(path)
            assert len(samples)==value['numFrames'] and sr==value['sampleRate']
            item=resources.setdefault(relative,{'kind':'factory_wavetable','factory':True,
                'relative_install_path':relative,'resolved_path':str(path),'sha256':sha(path),
                'included_custom_file':None,'referenced_by':[]})
            if id not in item['referenced_by']:
                item['referenced_by'].append(id)
        for child in value.values():
            native_resources(child,id)
    elif isinstance(value,list):
        for child in value:
            native_resources(child,id)

for id in ['sub-bass','bass-grit','shadow-pad','ghost-bell','tension-rise']:
    folder=SOURCE/'checks'/id
    receipt=json.loads((folder/'receipt.json').read_text(encoding='utf-8'))
    extended=json.loads((folder/'extended-readback.json').read_text(encoding='utf-8'))
    assert receipt['ok'] and extended['ok'] and all(receipt['preset']['structural_readback'].values())
    native=folder/(id+'.SerumPreset')
    path=OUT/'Presets'/native.name
    if path.exists():
        assert sha(path)==sha(native)
    else:
        shutil.copy2(native,path)
    assert sha(path)==receipt['preset']['sha256']
    assert sha(path)!=sha(OLD/'Presets'/path.name)
    parsed=unpack_file(path)
    assert not scan_wire_types(parsed.data)
    requested=json.loads((SOURCE/'preset-specs'/(id+'.json')).read_text(encoding='utf-8'))
    assert parsed.metadata['presetDescription']==requested['description']
    assert parsed.data['Arp0']['plainParams']['kParamEnabled']==0.0
    native_resources(parsed.data,id)
    receipts[id]={'build':receipt,'extended_readback':extended,'delivered_file':'Presets/'+path.name,
        'sha256':sha(path),'description_readback':True,'resource_check':True}
    bindings[id]['preset']='Presets/'+path.name
    bindings[id]['revision']='v002'

for path in sorted((OUT/'MIDI').glob('*.mid')):
    assert sha(path)==sha(OLD/'MIDI'/path.name),path
    inventory[path.name]={'sha256':sha(path),'unchanged_from_v001':True}
assert len(inventory)==13
for command,args in [('validate',[str(SOURCE/'composition.json')]),('verify',[str(OUT)])]:
    run=subprocess.run([str(WORKSPACE/'.venv/Scripts/python.exe'),'-m','midi_creator',command,*args],
        cwd=WORKSPACE,capture_output=True,text=True,encoding='utf-8')
    assert run.returncode==0,(run.stdout,run.stderr)
    result=json.loads(run.stdout)
    assert result['ok']
    save(OUT/'_internal'/(command+'-receipt.json'),result)

# Full musical performance audit remains valid because the MIDI bytes are identical.
performance=json.loads((OLD/'_internal/performance-audit.json').read_text(encoding='utf-8'))
performance['origin_revision']='v001'
performance['revision']='v002'
performance['all_midi_unchanged_from_v001']=True
save(OUT/'_internal/performance-audit.json',performance)
save(OUT/'_internal/preset-receipts.json',receipts)
manifest={'ok':True,'custom_dependencies':[],'resources':list(resources.values()),
    'install_instruction':'Installed Serum 2 factory tables are required; no custom tables/samples/IRs to install.'}
save(OUT/'_internal/resource-manifest.json',manifest)
save(SOURCE/'bindings.json',bindings)

# Update the producer guide while retaining the complete import, piano, drum and form guidance.
guide=(OLD/'README.md').read_text(encoding='utf-8')
guide=guide.replace('# Black Glass','# Black Glass — v002',1)
insert='''
**Revisi preset v002:** kelima sound Serum didesain ulang untuk aransemen ini. Sub memakai sine bersih tanpa distorsi; grit memiliki serangan filter, saturasi tape dan EQ; pad bergerak pelan; bell memiliki partial atas yang cepat mereda; riser berubah dari gelap ke terang dengan release 20 ms. Seluruh 13 MIDI identik dengan v001, termasuk dinamika piano. Versi ini tetap 136 BPM, F minor, 4/4, 112 bar / 3:17.65.

Gunakan **User > MIDI Creator > 20261012-black-glass > v002**, atau **Load Preset** dari file `Presets/` di revisi ini. Cukup ganti lima preset pada track Serum yang sudah ada; MIDI lama juga dapat tetap dipakai. [v001](../v001/README.md) dipertahankan.

| Layer | Macro dan default | Rentang yang berguna |
| --- | --- | --- |
| Sub bass | BODY 15%; PUNCH 28% | BODY menambah level sine secara terbatas; PUNCH mengatur tambahan serangan singkat. Mulai di default |
| Bass grit | BITE 18%; TONE 25%; ATTACK 35% | BITE: blend distorsi 62–87%; TONE membuka LP; ATTACK menambah pembukaan singkat filter |
| Shadow pad | SHADE 18%; MOTION 24%; SPACE 12% | SHADE menggelapkan tone; MOTION mengatur gerakan filter/pan lambat; SPACE: wet reverb 18–40% |
| Ghost bell | GLASS 28%; ECHO 10%; SPACE 15% | GLASS mengatur partial serangan atas; ECHO: wet delay 13–35%; SPACE: wet reverb 9–23% |
| Tension rise | AIR 15%; TENSION 22%; LIFT 15% | AIR membuka sweep; TENSION menambah resonansi di akhir; LIFT menambah level noise |

Seluruh macro memakai rentang 0–100%. Default adalah titik awal; nilai ekstrem belum didengarkan. Cutoff filter memakai unit normalized, bukan frekuensi Hz yang sudah terkalibrasi. Bell memakai lapisan sine atas, tanpa FM. Pad memakai LFO free 0.085 dan 0.11 Hz; echo bell fixed 220.588 ms cocok dengan eighth note pada 136 BPM.

**Dependensi:** hanya factory wavetable Serum 2 yang telah terpasang (`Analog/Basic Shapes.wav`, `S2 Tables/Analog/DM - OSCAR.wav`, dan `S2 Tables/Default Shapes.wav`, termasuk slot nonaktif). Tidak ada file custom/sample/IR tambahan. [Manifest resource](_internal/resource-manifest.json).

**Status:** struktur/readback lima preset, wire-type scan, resource dan checksum **PASS**. MIDI validate/generate/verify **PASS**; seluruh file sama byte demi byte dengan v001. **Pemuatan plugin native, render/analisis audio dan listening aktual belum diuji.** Analisis FFT hanya memeriksa file wavetable sumber, bukan audio keluaran Serum. Perbaikan di atas adalah target desain; preferensi suara perlu dinilai saat dimuat dan dibandingkan pada level yang sama.

[Receipt QA v002](_internal/revision-qa.json) · [Desain dan rencana audition](_internal/source/sound-design.md)
'''
guide=guide.replace('## Import into Cubase',insert+'\n## Import into Cubase',1)
guide=guide.replace('20261012-black-glass > v001','20261012-black-glass > v002')
guide=guide.replace('BODY adds oscillator level; TAIL lengthens release. Start at saved values','BODY adds sine level; PUNCH controls a brief attack lift')
guide=guide.replace('BITE increases distortion blend; WEIGHT lowers the high-pass cutoff','BITE adds tape blend; TONE opens LP; ATTACK adds transient color')
guide=guide.replace('OPEN brightens the filter; SPACE adds reverb','SHADE darkens tone; MOTION adds slow movement; SPACE adds reverb')
guide=guide.replace('GLASS adds FM color; ECHO adds delay. Saved echo is an eighth note at 136 BPM','GLASS adds the short upper partial; ECHO/SPACE add dark delay/reverb')
guide=guide.replace('AIR raises the filter cutoff; LEVEL adds noise level','AIR opens the sweep; TENSION adds late resonance; LIFT adds noise level')
(OUT/'README.md').write_text(guide,encoding='utf-8')
qa={'ok':True,'revision':'v002','origin':'v001','checked_at':datetime.now(timezone.utc).isoformat(),
    'preset_count':5,'midi_count':13,'all_midi_unchanged':True,'midi':inventory,
    'structural':{'status':'pass','full_requested_readback':True,'wire_type_scan':True,'arp_off':True,
        'resource_resolution':True,'factory_waveform_analysis':True,'copied_hash_match':True},
    'plugin_load':{'status':'untested','installed_plugin_version':'2.0.23','reason':'Current studio tools report native_preset_loading=false.'},
    'render_analysis':{'status':'untested','audio_rendered':False},
    'listening':{'status':'untested','auditioned':False},
    'uncertain_controls':['source phase/randomness uses tool/default state; no general semantic setter',
        'two-filter balance exact scale and audible isolation untested',
        'macro endpoints, actual gain/peaks, filter Hz and stereo behavior require audio checks']}
save(OUT/'_internal/revision-qa.json',qa)
shutil.copytree(SOURCE,OUT/'_internal/source',dirs_exist_ok=True)
for file in [OUT/'README.md']:
    for target in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
        if '://' not in target and not target.startswith('#'):
            assert (file.parent/target).exists(),(file,target)
assert {p.name for p in OUT.iterdir()}=={'README.md','MIDI','Presets','_internal'}
index='''# Black Glass

Dark trap R&B dengan piano ekspresif dan bass drop chorus.

[Buka revisi terbaru v002](v002/README.md) — lima preset Serum diperbarui; MIDI tetap identik dengan v001. 136 BPM, F minor, 4/4, 112 bar, 13 layer.

[Revisi sebelumnya v001](v001/README.md) tetap tersedia. File produser ada di `MIDI/` dan `Presets/` masing-masing revisi; spesifikasi/receipt berada di `_internal/`.
'''
(PROJECT/'README.md').write_text(index,encoding='utf-8')
catalog=WORKSPACE/'projects/README.md'
catalog.write_text(catalog.read_text(encoding='utf-8').replace(
    '[v001](20261012-black-glass/v001/README.md)','[v002](20261012-black-glass/v002/README.md)'),encoding='utf-8')
print(json.dumps({'ok':True,'presets':5,'midi_files':13,'all_midi_identical_to_v001':True,
    'factory_dependencies':list(resources),'custom_dependencies':0,'structural_readback':'pass',
    'wire_scan':'pass','plugin_load':'untested','render_analysis':'untested','listening':'untested'},indent=2))
