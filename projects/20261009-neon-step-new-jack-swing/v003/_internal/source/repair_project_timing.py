"""Publish immutable timing revisions from composition snapshots.

Pitch, velocity, instrument, sections, tempo, meter, PPQN and total length are
preserved. All attacks use a shared straight 1/16-note grid. In the new dark
synth song, the arp's constant 1/32-note lag is explicitly removed first.
"""
from collections import defaultdict
from copy import deepcopy
from decimal import Decimal,ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

from midi_creator.export import generate_export,verify_export
from midi_creator.spec import compile_composition
from midi_creator.timing import timing_report

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'src'/'midi_creator'/'spec.py').is_file())
PLAN=[('20261009-neon-step-new-jack-swing','v002','v003'),
      ('20261011-neon-di-ujung-malam','v001','v002')]

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def checksum(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(folder): return {p.relative_to(folder).as_posix():checksum(p) for p in folder.rglob('*') if p.is_file()}
def run_cli(*args):
    result=subprocess.run(['uv','run','midi-creator',*map(str,args)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if result.returncode: raise RuntimeError(result.stderr)
    return json.loads(result.stdout)

def revise(slug,previous,revision):
    project=ROOT/'projects'/slug
    old=project/previous
    output=project/revision
    if output.exists(): raise FileExistsError(f'Preserve existing revision {output}')
    before_inventory=inventory(old)
    original=json.loads((old/'_internal'/'composition.json').read_text(encoding='utf-8'))
    repaired=deepcopy(original)
    repaired['timing']={'mode':'strict','grid_division':16}
    repairs={}
    for layer in repaired['layers']:
        if layer.get('clips'): raise ValueError('This repair expects the audited, expanded note snapshots')
        changed=0
        by_pitch=defaultdict(list)
        for note in layer['notes']:
            start=Decimal(str(note['start']))
            if slug.endswith('neon-di-ujung-malam') and layer['id']=='glass-arp':
                start-=Decimal('.125')
            snapped=(start*4).to_integral_value(rounding=ROUND_HALF_UP)/4
            changed+=snapped!=Decimal(str(note['start']))
            note['start']=float(snapped)
            by_pitch[note['pitch']].append(note)
        shortened=0
        for notes in by_pitch.values():
            notes.sort(key=lambda n:n['start'])
            for a,b in zip(notes,notes[1:]):
                if a['start']==b['start']:
                    raise ValueError(f"{layer['id']}: quantization collides on pitch {a['pitch']}")
                if Decimal(str(a['start']))+Decimal(str(a['duration']))>Decimal(str(b['start'])):
                    a['duration']=float(Decimal(str(b['start']))-Decimal(str(a['start'])))
                    shortened+=1
        repairs[layer['id']]={'shifted_note_ons':changed,'shortened_gates_to_avoid_overlap':shortened}
    # Assert every property outside the authorized timing fields stays identical.
    restored=deepcopy(repaired)
    restored.pop('timing')
    for old_layer,new_layer in zip(original['layers'],restored['layers']):
        assert len(old_layer['notes'])==len(new_layer['notes'])
        for a,b in zip(old_layer['notes'],new_layer['notes']):
            b['start']=a['start']; b['duration']=a['duration']
    assert restored==original
    compiled=compile_composition(repaired,strict_timing=True)
    assert timing_report(compiled)['on_grid']
    old_compiled=compile_composition(original)
    assert (compiled.tempo,compiled.ppqn,compiled.end_tick)==(old_compiled.tempo,old_compiled.ppqn,old_compiled.end_tick)
    source=project/'_internal'/('source-'+revision)
    source.mkdir(parents=True,exist_ok=False)
    save(source/'composition.json',repaired)
    validate=run_cli('validate',source/'composition.json')
    result=generate_export(source/'composition.json',output)
    save(output/'_internal'/'validate-receipt.json',validate)
    if (old/'Presets').is_dir():
        shutil.copytree(old/'Presets',output/'Presets')
        if (old/'_internal'/'preset-check').is_dir():
            shutil.copytree(old/'_internal'/'preset-check',output/'_internal'/'preset-origin')
        receipts=[]
        for p in sorted((output/'Presets').iterdir()):
            assert checksum(p)==checksum(old/'Presets'/p.name)
            receipts.append({'file':p.relative_to(output).as_posix(),'origin':f'../{previous}/Presets/{p.name}',
                             'sha256':checksum(p),'unchanged':True})
        save(output/'_internal'/'preset-reuse.json',{'ok':True,'presets':receipts,
             'structural_readback':'unchanged files; original readback evidence in preset-origin',
             'plugin_loaded':False,'auditioned':False})
    if (old/'_internal'/'source'/'bindings.json').is_file():
        shutil.copy2(old/'_internal'/'source'/'bindings.json',source/'bindings.json')
    save(source/'timing-change.json',{'origin':previous,'revision':revision,'grid_division':16,'layers':repairs,
         'tempo_meter_ppqn_length_preserved':True,'pitch_velocity_instruments_sections_preserved':True,
         'arp_fixed_offset_removed_beats':.125 if slug.endswith('neon-di-ujung-malam') else 0})
    shutil.copy2(Path(__file__).resolve(),source/'repair_project_timing.py')
    # This shared reproduction script is retained as evidence; its executable
    # integration copy finds ROOT and the original revisions deterministically.
    (source/'request.md').write_text(
        '# Revisi timing\n\n'
        f'- Proyek: {original["title"]}\n- Revisi: {revision}; asal {previous}\n- Tanggal: 2026-10-11\n\n'
        '## Permintaan asli\n\n'
        '“hampir di semua projek, file midi ... temponya tidak rapih dan tidak konsisten antar layer ... tidak on grid ... telusuri kenapa dan perbaiki”\n\n'
        'Steering: seluruh layer sudah di-drop di grid yang sama; lead/arp terasa tidak menyambung dengan piano/pad.\n\n'
        '## Keputusan dan perubahan\n\n'
        'Semua onset pada grid straight 1/16, tanpa jitter, swing baked-in, strum delay atau clap flam. '
        'Dark synth arp kehilangan offset tetap 1/32 sehingga pulsa eighth-note sejajar dengan groove. '
        'Nada, velocity, sound, mixer, tempo, meter, PPQN, bagian dan panjang tetap. '
        'Durasi/gate hanya dipendekkan bila onset baru menyebabkan overlap pitch yang sama; detail pada timing-change.json. '
        'Revisi lama tetap utuh. Versi New Jack Swing ini merupakan alternatif straight; versi swing tersedia pada revisi asal.\n\n'
        '## Penerimaan\n\n'
        'Validate/generate/verify dan audit MIDI independen lulus; zero off-grid onset pada 1/16. '
        'Preset yang sudah ada dipakai ulang byte-identik. Pemuatan plugin/listening serta impor live belum diuji. '
        'Ekspor ulang dari Cubase masih diperlukan untuk membandingkan posisi part/note sesudah drop.\n',encoding='utf-8')
    text=(old/'README.md').read_text(encoding='utf-8')
    if slug.endswith('neon-di-ujung-malam'):
        text=text.replace('Clap stereo tipis, sekitar 9 ms setelah snare di chorus','Clap stereo tipis, tepat bersama snare di chorus')
        text=text.replace('velocity berselang-seling dan timing offbeat kecil','velocity berselang-seling; onset eighth-note lurus')
    else:
        text=text.replace('Swung sixteenth pulse','Straight sixteenth pulse').replace('Swung percussion','Straight percussion')
        text=text.replace('agar swing sixteenth 108 BPM tetap jelas','agar pulsa sixteenth 108 BPM tetap jelas')
        text=text.replace('Swing pasangan not 1/16 sebesar 60:40; variasi velocity memakai seed 108960 tanpa jitter onset tambahan.',
                          'Revisi timing: onset straight 1/16; swing, clap delay dan strum delay dilepas. Velocity asal seed 108960 dipertahankan.')
        text=text.replace('nada/velocity/timing/mixer tetap sama seperti v001','nada/velocity/mixer dipertahankan; timing diperbaiki pada revisi ini')
    correction=(f'## Koreksi timing — {revision}\n\n'
        f'Revisi asal: [{previous}]({"../"+previous+"/README.md"}). '
        '**Semua onset kini tepat pada satu grid straight 1/16**, termasuk chord, lead, arp dan drum. '
        'Jitter, baked-in swing, strum delay dan clap flam dihapus. '
        + ('Offset tetap 1/32 pada arp juga dihapus sehingga pulsa arp sejajar dengan beat. ' if slug.endswith('neon-di-ujung-malam') else
           'Feel versi ini lebih lurus; versi 60:40 tetap tersedia pada revisi asal. ')
        + 'Pitch, velocity, mixer, tempo, meter dan panjang lagu dipertahankan. Note-off/gate tetap untuk artikulasi, dengan trimming hanya bila diperlukan untuk mencegah overlap. '
        'Preset yang sudah ada dipakai ulang tanpa perubahan sound.\n\n'
        'Di Cubase, gunakan **Musical Time Base** (ikon not), tempo tetap sesuai judul, left locator **1.1.1.0**, '
        '**Import to Left Locator**, **Import Dropped File as Single Part** dan **Ignore Master Track Events on Merge**. '
        'Periksa posisi awal part melalui Info Line; file yang masuk belakangan tetap mempertahankan keheningan awal. '
        'Snap hanya menentukan posisi drop; Snap tidak mengkuantisasi isi nada. Ruler/key editor gunakan Bars+Beats, grid 1/16. '
        'Pemeriksaan akhir perlu membandingkan part/note hasil impor dengan file asli, bukan memindahkan nada pertama ke bar 1.\n\n'
        '**Status:** validate/generate/verify lulus, audit onset 1/16 lulus. Impor live, pemuatan preset dan listening belum diuji untuk revisi ini.\n\n')
    first_break=text.index('\n\n')+2
    text=text[:first_break]+correction+text[first_break:]
    (output/'README.md').write_text(text,encoding='utf-8')
    report=run_cli('verify',output)
    assert report['ok'] and report['timing']['on_grid']
    save(output/'_internal'/'verification.json',report)
    assert inventory(old)==before_inventory,'Original revision changed'
    save(output/'_internal'/'original-preservation.json',{'ok':True,'origin':previous,'sha256':before_inventory})
    target=output/'_internal'/'source'
    assert source.resolve().is_relative_to(project.resolve()) and target.resolve().is_relative_to(project.resolve())
    assert not target.exists()
    shutil.move(str(source),str(target))
    (project/'README.md').write_text(f'# {original["title"]}\n\n'
        f'[Revisi terbaru {revision} — onset tepat pada grid]({revision}/README.md)\n\n'
        f'[Revisi asal {previous}]({previous}/README.md) tetap utuh. Semua sumber/bukti berada di `_internal/` revisi.\n',encoding='utf-8')
    print(f'{slug}/{revision}: {len(repaired["layers"])} layers; shifted {sum(r["shifted_note_ons"] for r in repairs.values())} attacks; '
          f'trimmed {sum(r["shortened_gates_to_avoid_overlap"] for r in repairs.values())} gates; PASS',flush=True)

if __name__=='__main__':
    for item in PLAN: revise(*item)
