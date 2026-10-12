"""Align supporting phrases to the approved core; preserve core MIDI byte-for-byte."""
from copy import deepcopy
from decimal import Decimal,ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from midi_creator.export import generate_export,verify_export
from midi_creator.spec import compile_composition

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'src'/'midi_creator'/'spec.py').is_file())
PROJECT=ROOT/'projects'/'20261009-neon-step-new-jack-swing'
ORIGIN=PROJECT/'v002'
OUTPUT=PROJECT/'v004'
PROTECTED={'kick','snare','clap','hihat','shaker','tambourine','toms',
           'slap-bass','electric-piano','synth-stabs','string-pad'}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def swing(beat):
    index=int((Decimal(str(beat))*4).to_integral_value(rounding=ROUND_HALF_UP))
    return index/4+(.05 if index%2 else 0)
def family_at(spec,bar):
    current=max((s for s in spec['sections'] if s['start']<=bar*4),key=lambda s:s['start'])
    name=current['name']
    family='Verse' if name.startswith('Verse') else 'Chorus' if 'chorus' in name.lower() and name!='Pre-chorus' else name
    return family

if __name__=='__main__':
    if OUTPUT.exists(): raise FileExistsError(OUTPUT)
    original=json.loads((ORIGIN/'_internal'/'composition.json').read_text(encoding='utf-8'))
    spec=deepcopy(original)
    spec['timing']={'mode':'free','grid_division':16}
    spec['assumptions'].append('Revisi v004: core bass/drum/chord/pad asli dipertahankan, pelengkap mengikuti anchor groove core; 60:40 tetap disengaja.')
    changes={}
    for layer in spec['layers']:
        if layer['id'] in PROTECTED: continue
        shifted=0
        for note in layer['notes']:
            bar=int(note['start']//4)
            off=note['start']-bar*4
            family=family_at(spec,bar)
            # Decode original swung 1/16 positions, removing only strum offsets.
            straight=min((i/4 for i in range(16)),key=lambda b:abs(swing(b)-off))
            if layer['id']=='lead-synth':
                mapping=({1.25:1.5} if family=='Chorus' else
                         {1.25:1.75,2.0:2.5,2.75:3.5} if family=='Verse' else
                         {.5:1.5} if family=='Bridge' else
                         {1.25:1.5,2.0:2.5} if family=='Intro' else
                         {1.25:1.5} if family=='Outro' else {})
            elif layer['id']=='muted-guitar':
                mapping={.5:.75,1.25:1.5,2.25:2.5,2.5:2.75,3.25:3.5} if family=='Chorus' else {.5:.75,2.25:2.5,3.25:3.5}
            elif layer['id']=='synth-brass': mapping={3.25:3.5}
            elif layer['id']=='bell-keys': mapping={2.75:2.5,3.25:3.5}
            else: raise ValueError(layer['id'])
            new=round(bar*4+swing(mapping.get(straight,straight)),5)
            shifted+=abs(new-note['start'])>1e-7
            note['start']=new
        changes[layer['id']]={'shifted_note_ons':shifted,'notes':len(layer['notes'])}
        layer['notes'].sort(key=lambda n:(n['start'],n['pitch']))
    compiled=compile_composition(spec)
    # Keep the original pitch/velocity/duration inventory on edited layers.
    for a,b in zip(original['layers'],spec['layers']):
        if a['id'] in PROTECTED: assert a==b
        else:
            assert sorted((n['pitch'],n['velocity'],n['duration']) for n in a['notes'])==sorted((n['pitch'],n['velocity'],n['duration']) for n in b['notes'])
            assert all(abs((n['start']%4)-swing(min((i/4 for i in range(16)),key=lambda t:abs(swing(t)-n['start']%4))))<1e-7 for n in b['notes'])
    source=PROJECT/'_internal'/'source-v004'
    source.mkdir(parents=True,exist_ok=False)
    save(source/'composition.json',spec)
    validate=subprocess.run(['uv','run','midi-creator','validate',str(source/'composition.json')],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',check=True)
    generate_export(source/'composition.json',OUTPUT)
    protected=[]
    for id in sorted(PROTECTED):
        old=ORIGIN/'MIDI'/(id+'.mid');new=OUTPUT/'MIDI'/(id+'.mid')
        assert old.read_bytes()==new.read_bytes(),id
        protected.append({'layer':id,'sha256':sha(new),'byte_identical_to_v002':True})
    save(OUTPUT/'_internal'/'core-preservation.json',{'ok':True,'origin':'v002','layers':protected})
    save(OUTPUT/'_internal'/'timing-change.json',{'origin':'v002','revision':'v004','protected_layers':sorted(PROTECTED),
         'changed_layers':changes,'swing_ratio':'60:40','pitch_velocity_gates_preserved':True,
         'tempo_meter_ppqn_end_preserved':True,'listening':False})
    save(OUTPUT/'_internal'/'validate-receipt.json',json.loads(validate.stdout))
    report=verify_export(OUTPUT)
    assert report['ok']
    save(OUTPUT/'_internal'/'verification.json',report)
    shutil.copy2(Path(__file__).resolve(),source/'repair_neon_step_groove.py')
    (source/'request.md').write_text('# Revisi groove Neon Step\n\nRevisi v004 dari v002, 2026-10-11.\n\n'
        'Permintaan: perbaiki ketidakselarasan antar-layer. Steering: bass, drum dan chord New Jack Swing sudah menyatu sangat baik; layer lain terasa kurang bagus.\n\n'
        'Keputusan: 11 layer core (drum, bass, piano/chord stabs dan pad) dipertahankan termasuk seluruh timing, velocity, note/gate/mixer. '
        'Empat pelengkap (lead, muted guitar, brass, bell) menempatkan frase pada anchor piano/bass/drum, bukan memakai aksen yang berdiri sendiri. '
        'Guitar strum delay dihapus; swing core 60:40 dipertahankan. Pitch, velocity, jumlah note dan durasi tetap. '
        'v003 adalah percobaan straight yang tidak menjadi rekomendasi utama; tetap disimpan.\n\n'
        'Kriteria: 11 MIDI core byte-identik dengan v002, layer pelengkap tepat pada grid groove 60:40, validate/generate/verify lulus. '
        'Pemuatan plugin dan listening belum diuji. Tidak ada preset baru karena revisi ini menjaga sound yang sudah digunakan pengguna.\n',encoding='utf-8')
    text=(ORIGIN/'README.md').read_text(encoding='utf-8')
    insert=('## Revisi groove v004\n\n'
        '**Bass, seluruh drum, electric piano, synth stabs dan string pad dipertahankan byte-identik dengan v002.** '
        'Swing 1/16 **60:40** tetap digunakan karena core tersebut sudah cocok menurut Anda. '
        'Lead mengikuti serangan piano pada chorus dan piano/bass pada verse; muted guitar mengikuti accent kick/bass/chord dan tidak lagi memakai strum delay. '
        'Brass dan bell menjawab pada akhir frase yang mengikuti pulsa core. Nada, velocity, durasi, mixer, tempo dan panjang tetap.\n\n'
        'Gunakan **108 BPM**, 4/4, Musical Time Base (ikon not), left locator **1.1.1.0**, '
        '**Import to Left Locator**, **Import Dropped File as Single Part**, **Ignore Master Track Events on Merge**. '
        'Baked-in swing disengaja: nada sixteenth ganjil berada pada offset .30/.80 beat, bukan .25/.75. '
        'Jangan kuantisasi ulang core dengan straight 1/16. Semua part harus mempertahankan keheningan awal dari bar 1.\n\n'
        '[v002 — core asal](../v002/README.md) tetap tersedia. [v003 — percobaan semua-layer straight](../v003/README.md) '
        'disimpan sebagai alternatif, tetapi **v004 adalah revisi yang direkomendasikan** berdasarkan feedback terbaru.\n\n'
        '**Verifikasi:** validate/generate/verify PASS; 11 MIDI core byte-identik; empat pelengkap pada grid groove 60:40. '
        'Impor live, pemuatan preset dan listening belum diuji. Sound/preset mengikuti versi asal; tidak ada native preset baru dibuat pada revisi timing ini.\n\n')
    at=text.index('\n\n')+2
    (OUTPUT/'README.md').write_text(text[:at]+insert+text[at:],encoding='utf-8')
    target=OUTPUT/'_internal'/'source'
    assert source.resolve().is_relative_to(PROJECT.resolve()) and target.resolve().is_relative_to(PROJECT.resolve()) and not target.exists()
    shutil.move(str(source),str(target))
    (PROJECT/'README.md').write_text('# Neon Step — New Jack Swing\n\n[Revisi terbaru v004 — core asli, pelengkap lebih selaras](v004/README.md).\n\n'
        '[v002 — asal](v002/README.md) dan [v003 — percobaan straight](v003/README.md) dipertahankan. Bahan teknis berada di `_internal/` masing-masing revisi.\n',encoding='utf-8')
    print('PASS: v004; 11 core MIDI byte-identical; 4 supporting layers aligned to their 60:40 groove.')
