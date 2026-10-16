"""Package retained presets, audit the full arrangement, and publish producer docs."""
from collections import Counter,defaultdict
import csv
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
PROJECT=next(p for p in HERE.parents if (p/'v001/_internal/composition.json').exists())
WORKSPACE=next(p for p in HERE.parents if (p/'studio.local.json').exists())
OLD=PROJECT/'v001';OUT=PROJECT/'v002'
sys.path.insert(0,str(WORKSPACE/'integrations/serum-mcp/src'))
from serum_mcp.preset.packer import unpack_file
from serum_mcp.preset.introspect import extract_spec
from serum_mcp.preset.safety import scan_wire_types

def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def matches(a,b):
    if isinstance(b,dict):return isinstance(a,dict) and all(k in a and matches(a[k],v) for k,v in b.items())
    if isinstance(b,list):return isinstance(a,list) and len(a)>=len(b) and all(matches(a[i],v) for i,v in enumerate(b))
    if type(a) in (int,float) and type(b) in (int,float):return math.isclose(a,b,abs_tol=1e-5,rel_tol=1e-5)
    return a==b
def clock(seconds):return f'{int(seconds)//60}:{seconds%60:05.2f}'
def position(start):
    s=round(start*4);return f'{s//16+1}.{s%16//4+1}.{s%4+1}'

c=json.loads((HERE/'composition.json').read_text(encoding='utf-8'))
assert c==json.loads((OUT/'_internal/composition.json').read_text(encoding='utf-8'))
plan=json.loads((HERE/'arrangement-plan.json').read_text(encoding='utf-8'))
specs=json.loads((OLD/'_internal/source/preset-specs.json').read_text(encoding='utf-8'))
old_manifest=json.loads((OLD/'_internal/serum/manifest.json').read_text(encoding='utf-8'))
assert old_manifest['ok']
source=OUT/'_internal/source';source.mkdir(exist_ok=True)
for p in HERE.iterdir():
    if p.is_file():shutil.copy2(p,source/p.name)
for name in ['preset-specs.json','sound-design.json']:
    shutil.copy2(OLD/'_internal/source'/name,source/name)
shutil.copytree(OLD/'_internal/serum',OUT/'_internal/serum',dirs_exist_ok=True)
(OUT/'Presets').mkdir(exist_ok=True)
cfg=json.loads((WORKSPACE/'studio.local.json').read_text(encoding='utf-8'))
serum_root=Path(cfg['serum_presets']).parent
receipts=[]
for ident,spec in specs.items():
    old=OLD/'Presets'/f'{ident}.SerumPreset';new=OUT/'Presets'/old.name
    if new.exists():assert digest(new)==digest(old)
    else:shutil.copy2(old,new)
    native=unpack_file(new)
    recovered=extract_spec(native.data).model_dump(by_alias=True)
    checks={k:matches(recovered[k],spec[k]) for k in ['oscillators','filters','envelopes','lfos','macros','fx_chain','global']}
    checks['mod_routes']=all(any(matches(a,w) for a in recovered['mod_routes']) for w in spec['mod_routes'])
    checks['arp_disabled']=native.data['Arp0']['plainParams']['kParamEnabled']==0.0
    checks['name']=native.metadata['presetName']==spec['name']
    issues=[str(v) for v in scan_wire_types(native.data)]
    deps=[]
    for i in range(3):
        rel=native.data.get(f'Oscillator{i}',{}).get(f'WTOsc{i}',{}).get('relativePathToWT')
        if rel:
            resource=serum_root/'Tables'/rel
            deps.append(dict(kind='factory_wavetable',relative_path=rel,exists=resource.is_file(),sha256=digest(resource)))
    assert all(checks.values()) and not issues and all(d['exists'] for d in deps)
    receipt=dict(layer=ident,ok=True,file=str(new),reused_from=str(old),sha256=digest(new),
                 unchanged_from_v001=digest(new)==digest(old),structural_readback=checks,
                 wire_type_issues=issues,dependencies=deps,plugin_loaded=False,auditioned=False)
    receipts.append(receipt)
    save(OUT/'_internal/serum'/ident/'decoded-spec.json',recovered)
    save(OUT/'_internal/serum'/ident/'receipt.json',receipt)
save(OUT/'_internal/serum/manifest.json',dict(ok=True,checked_at=datetime.now(timezone.utc).isoformat(),
    mode='unchanged native files reused from v001, decoded and checked again',commit=old_manifest['commit'],
    presets=receipts,custom_dependencies=[],plugin_loaded=False,audio_rendered=False,auditioned=False,
    limitations=old_manifest['limitations']))

# MIDI/source audit: harmony, arrangement contrast, response windows and resolution.
byid={l['id']:l for l in c['layers']};scale={0,2,3,5,7,8,10}
assert all(n['pitch']%12 in scale for l in c['layers'] if l['kind']=='melodic' for n in l['notes'])
assert all(n['pitch']==60 for l in c['layers'] if l['kind']=='drums' for n in l['notes'])
assert all(abs(n['start']*4-round(n['start']*4))<1e-9 for l in c['layers'] for n in l['notes'])
lead=byid['layer08-main-lead']['notes'];answer=byid['layer09-synth-whistle']['notes']
overlaps=[(a['start'],b['start']) for a in lead for b in answer if a['start']<b['start']+b['duration'] and b['start']<a['start']+a['duration']]
assert not overlaps,overlaps[:3]
assert all(n['start']+n['duration']<=660 for l in c['layers'] for n in l['notes'])
assert next(n for n in byid['layer01-sub-bass']['notes'] if n['start']==656)['pitch']==24
expected=[24,29,32,34]
assert all(n['pitch']==expected[int(n['start']//4)%4] for n in byid['layer01-sub-bass']['notes'])
padvoices=[{51,55,60},{53,56,60},{51,56,60},{53,58,62}]
for bar in range(165):
    active={n['pitch'] for n in byid['layer07-warm-pad']['notes'] if n['start']<=bar*4<n['start']+n['duration']}
    assert active==padvoices[bar%4],(bar,active)
density={}
for s in plan:
    start=(s['first_bar']-1)*4;end=s['last_bar']*4
    density[s['name']]={l['id']:sum(start<=n['start']<end for n in l['notes']) for l in c['layers']}
assert density['Chorus 1']['layer08-main-lead']>density['Verse 1']['layer08-main-lead']
assert density['Breakdown']['drum-kick']<density['Chorus 2']['drum-kick']
assert density['Outro']['layer02-octave-bass']<density['Final Chorus']['layer02-octave-bass']
signatures=[]
for b in range(0,164,4):
    signatures.append(tuple((l['id'],tuple((n['pitch'],n['start']-b*4,n['duration'],n['velocity']) for n in l['notes'] if b*4<=n['start']<(b+4)*4)) for l in c['layers']))
assert len(set(signatures))>=20
for first,last in [(41,56),(89,104),(129,152)]:
    actual={n['start'] for n in byid['drum-kick']['notes'] if (first-1)*4<=n['start']<last*4}
    assert actual==set(range((first-1)*4,last*4))
audit=dict(ok=True,scale_ok=True,sub_progression_ok=True,pad_voice_leading_ok=True,lead_response_overlap_count=len(overlaps),
           chorus_kick_four_on_floor=True,sections=len(plan),unique_four_bar_blocks=len(set(signatures)),
           total_four_bar_blocks=len(signatures),last_note_off_beat=660,silent_tail_bars=3,section_note_counts=density,auditioned=False)
save(OUT/'_internal/musical-audit.json',audit)

# Export all exact note events for inspection without crowding the producer README.
eventdir=OUT/'_internal/midi-events';eventdir.mkdir(exist_ok=True)
for l in c['layers']:
    with (eventdir/(l['id']+'.csv')).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['position_bar_beat_16th','pitch_midi','velocity','start_beat','duration_beat','duration_sixteenth_steps'])
        for n in l['notes']:w.writerow([position(n['start']),n['pitch'],n['velocity'],n['start'],n['duration'],round(n['duration']*4,6)])

result=subprocess.run(['uv','run','midi-creator','verify',str(OUT)],cwd=WORKSPACE,text=True,capture_output=True)
assert result.returncode==0,result.stderr
v=json.loads(result.stdout);assert v['ok']
save(OUT/'_internal/final-midi-verification.json',v)
endtick=168*4*480;duration=round(495868/1e6*672,6)
assert v['end_tick']==endtick if 'end_tick' in v else all(f['end_tick']==endtick for f in v['files'].values())

details={
 'Intro':'Pad/bell dahulu; sub dan kick masuk bar5, stabs/arp bar9, cuplikan hook bar13. Riser13–16 menuju verse.',
 'Verse 1':'Bass berjalan, stabs lebih jarang, arp berjarak; hook dipotong menjadi call pendek dan jawaban whistle.',
 'Pre-Chorus 1':'Arp eighth menjadi16th, hat/shaker lebih rapat, lead memakai chord tones naik. Riser37–40.',
 'Chorus 1':'Hook utama, brass tiap downbeat, groove penuh. Setiap siklus memakai variasi arp dan ending hook.',
 'Post-Chorus':'Lead utama beristirahat; arp/bell/whistle meneruskan motif di atas bass dan drum.',
 'Verse 2':'Bass eighth pada delapan bar pertama lalu16th; countertexture dan fragment lead lebih aktif.',
 'Pre-Chorus 2':'Build harmoni lebih kuat, brass akhir frase, riser85–88 dan snare/clap fill.',
 'Chorus 2':'Full groove, tambahan brass accent setiap delapan bar; riser101–104 melepas energi ke breakdown.',
 'Breakdown':'Kick berhenti selama12 bar, bass rhythm diam; pad/FM bells/lead panjang. Sub kembali bar113, kick bar117.',
 'Build':'Bass eighth→16th, arp bertambah rapat, snare makin aktif. Riser125–128; beat4 bar128 dibiarkan kosong pada kick.',
 'Final Chorus':'24 bar klimaks: motif asli, ending alternatif dan lift oktaf pilihan, brass/fill drum berulang dengan variasi.',
 'Outro':'Layer dilepas bertahap; cadence Cm bar165. Note-off terakhir di166.1.1; bar166–168 memberi ruang tail.'
}
readme=['# Neon Breath — Lagu Penuh v002','',
    f'**121 BPM · C minor · 4/4 · 168 bar · {clock(duration)} ({duration:.6f} detik).**','',
    'Revisi ini mengembangkan loop empat bar menjadi lagu instrumental penuh dengan 12 bagian. **10 layer synth Serum 2 + 7 drum terpisah**. Semua 17 MIDI mulai di bar1 dan berakhir di bar169, dengan tepat satu track/instrumen per file. Versi v001 tetap disimpan.', '',
    '## Import versi lagu penuh di Cubase','',
    '1. Gunakan file dari **`v002/MIDI/`** pada tabel di bawah. Ganti part loop lama dengan file lagu penuh pada track yang sama; jangan menumpuk kedua versi pada track yang sama.',
    '2. Set tempo121 BPM, meter4/4, Musical Time Base. Left locator **1.1.1.0**, right locator **169.1.1.0**. Setelah impor, zoom seluruh part untuk melihat168 bar; panjang tiap file termasuk keheningan awal dan akhir.',
    '3. Gunakan **Import to Left Locator** untuk memasukkan dari bar1; **Import Dropped File as Single Part** bila drag-and-drop. Pada project bertempo tetap, **Ignore Master Track Events on Merge** menjaga tempo project.',
    '4. Sepuluh preset pada `Presets/` identik dengan v001. Jika preset v001 sudah dimuat, gunakan sound yang sama; untuk memuat dari paket pilih **Load Preset** di Serum2 dan file native yang sesuai. Browser instalasi v001 tetap berada di User/MIDI Creator/20261012-neon-breath-121/v001.',
    '5. Drum tetap satu sample per Sampler Track: root **C3 Cubase/MIDI60**, channel10. Semua MIDI drum memakai pitch60, sehingga perlu tujuh sampler terpisah. Sample tetap pilihan Anda.',
    '6. Sub Direct membutuhkan insert **LP80 Hz/24 dB per oktav** serta sidechain audio dari kick. Bila memakai sidechain host, set macro PUMP=0 agar pumping LFO tidak ikut mendobel. Internal arp Serum tetapOFF karena semua event arp sudah ada dalam MIDI.',
    '', '## Bentuk lagu dan cue waktu','',
    '| Bagian | Bar | Waktu awal–akhir | Perkembangan |','| --- | --- | --- | --- |']
for s in plan:
    readme.append(f"| {s['name']} | {s['first_bar']}–{s['last_bar']} | {clock((s['first_bar']-1)*4*60/121)}–{clock(s['last_bar']*4*60/121)} | {details[s['name']]} |")
readme += ['', 'Cm–Fm–Ab–Bb tetap satu chord per bar; siklus dimulai dari Cm pada setiap bagian. Stab memakai warna Cm7/Fm7/Abmaj7; voicing G–Bb–D–F di atas bass Bb menghasilkan Bb6. Pada bar165 lagu kembali ke Cm untuk penutup. Intro/outro dan breakdown mempunyai keheningan yang sengaja ditulis; chorus memakai four-on-the-floor penuh.', '',
    '## Track, MIDI, preset dan pemakaian','',
    '| Track | MIDI lagu168 bar | Native preset / instrumen | Jumlah nada | CC7 / CC10 |','| --- | --- | --- | ---: | --- |']
for l in c['layers']:
    ident=l['id'];p=f'[Preset](Presets/{ident}.SerumPreset)' if ident in specs else 'Sampler Track / sample Anda'
    readme.append(f"| {l['name']} | [{ident}.mid](MIDI/{ident}.mid) | {p} | {len(l['notes'])} | {l['volume']} / {l['pan']} |")
readme += ['', '## Drum, sample dan mapping','',
    'Ketujuh MIDI drum memakai **pitch60 (C3 Cubase), channel10**. CC7/CC10 independen berlaku pada masing-masing sampler. Snare/clap berada pada beats2/4, dengan fill straight16th di akhir frase; open hat mengisi offbeat. Closed hat lebih rapat pada chorus/pre/build, shaker bervariasi velocity. Kick menjaga empat ketukan di setiap bar chorus, dengan jeda yang disengaja pada intro/breakdown/build.',
    '', 'Pilih kick disco padat dengan tail sekitar100–160 ms; snare elektronik80s dengan body terkontrol dan snap; clap lebar dengan low-end dikurangi; closed hat pendek30–60 ms; open hat airy100–150 ms; shaker lembut; crash tipis sekitar0,8–1,5 detik. Sample belum dipilih/disalin. Untuk choke hat antar sampler, gunakan routing choke yang didukung atau pendekkan open-hat tail. One-shot playback tidak selalu mengikuti note-off MIDI.',
    '', 'Instrumen eksternal hanya sampler drum (**Cubase Sampler Track** atau sampler one-shot pilihan Anda); root60/channel10, tanpa keyswitch/program change. Tidak ada synth di luar Serum2.',
    '', '## Perubahan musikal dan sound','',
    'Seluruh preset native dipertahankan byte-for-byte. Perubahan v002 ada pada aransemen: density bass/arp, fragmen hook, ending alternatif, lift register, rhythm fills, transition trigger dan outro. Macro default, envelope, LFO dan FX tidak diganti. Jumlah/posisi note berubah; 121 BPM, key, meter, channel, CC7/CC10 dan IDs tetap.',
    '', 'Label nada mengikuti Cubase **C3=MIDI60**. Sub tetap MIDI24/29/32/34 = C0/F0/Ab0/Bb0. Lead pilihan mencapai MIDI79/G4 Cubase; respons whistle berada MIDI72–80, bell MIDI84–96. Onset strict straight1/16, tanpa swing atau random timing; durasi gate tidak harus tepat sepanjang grid.',
    '', 'Semua event lengkap ada dalam MIDI dan [composition source](_internal/source/composition.json). Untuk inspeksi piano-roll, [CSV event per layer](_internal/midi-events/) memuat pitch numerik, bar.beat.16th, velocity dan durasi. Native resource memakai empat factory wavetables Serum2 yang sama; dependency diverifikasi, tanpa custom sample/table/IR.',
    '', '### Batas implementasi yang tetap berlaku','',
    '- Direct Sub melewati filter/FX Serum: LP80 Hz dan real sidechain dari kick berada di DAW. Native PUMP adalah quarter-note LFO, belum diuji phase transport.',
    '- Delay menyimpan eighth L dan sixteenth R pada121 BPM, `kParamMode=1` dari observed factory state. Arti UI ping-pong belum diuji; bila diperlukan pilih Ping-Pong di UI dan periksa timing saat playback.',
    '- FM bell memakai Space reverb; pitch-shift shimmer tidak tersimpan. FX layer10 menggunakan velocity1 riser/127 impact sebagai aux scaling, bukan hard split. Jangan normalize velocity FX; small carrier leakage pada velocity1 tetap mungkin.',
    '- Lima riser berdurasi4 bar memakai envelope asli sekitar7,934 s. Tiga bar tail di akhir merupakan ruang MIDI; panjang decay audio sebenarnya belum diukur. Outro mengurangi layer dan memberi cadence, tanpa CC/fader fade otomatis.',
    '', '## Verifikasi dan asumsi','',
    f'- **MIDI PASS:** validate/generate/verify exit0, ok:true. 17 file SMF1, satu track,480 PPQN, tempo495868 µs/quarter, endtick322560, total{sum(len(l["notes"]) for l in c["layers"]):,} note-on; seluruh onset grid1/16 dan panjang sama. Note-on/off lengkap; no same-pitch overlap.',
    '- **Preset PASS struktural:** 10 native `.SerumPreset` tersedia, hash identik dengan v001, decode/readback diperiksa ulang, zero unsafe wire type, semua dependency factory ditemukan. Native files awal dibangun melalui serum-mcp; revisi ini memakai salinan yang sama.',
    f'- **Audit musikal offline:** scale/root/pad voice-leading lulus, lead/whistle tidak beririsan secara MIDI, kick chorus four-on-the-floor; {len(set(signatures))} blok4 bar berbeda dari{len(signatures)} blok aktif menunjukkan perkembangan aransemen. Cadence Cm bar165 dan tiga bar tail tersedia.',
    '- **Native plugin load, import live Cubase, render/analisis audio dan listening aktual BELUM DIUJI** pada revisi ini. Screenshot pengguna menunjukkan penggunaan Cubase, tetapi tidak membuktikan setiap file/preset v002 sudah dimuat. Tidak ada `.cpr` atau audio preview dibuat.',
    '- Durasi dipilih5:33 dalam rentang5–6 menit; bentuk instrumental tanpa vokal. Progresi/tempo/register sub disetujui tetap dipakai. Sample drum masih pilihan pengguna.',
    '', '[Receipt final](_internal/final-receipt.json) · [MIDI verification](_internal/final-midi-verification.json) · [Musical audit](_internal/musical-audit.json) · [Preset readback](_internal/serum/manifest.json) · [Revisi asal v001](../v001/README.md)',
    '', '## Parameter Serum yang dipertahankan','',
    'Tabel berikut berasal dari preset yang sama dengan v001. Assignment/modulation dan nilai FX berlaku untuk MIDI lagu penuh v002. Bagian MIDI empat bar pada dokumentasi lama tidak disalin; file pada tabel track di atas berisi aransemen168 bar.']

# Reuse exact parameter tables while replacing four-bar performance commentary.
oldreadme=(OLD/'README.md').read_text(encoding='utf-8')
conventions=oldreadme.split('## Konvensi parameter dan notasi',1)[1].split('## Parameter Serum dan MIDI lengkap per layer',1)[0]
readme += ['', conventions.strip()]
parameter_area=oldreadme.split('## Parameter Serum dan MIDI lengkap per layer',1)[1].split('## Drum per layer / per file',1)[0]
blocks=re.split(r'(?m)^### ',parameter_area)[1:]
assert len(blocks)==10
for block in blocks:
    title=block.splitlines()[0]
    params=block.split('**Oscillator dan routing**',1)[1].split('<details>',1)[0]
    readme += ['',f'### {title}', '', '**Oscillator dan routing**'+params.rstrip()]
text='\n'.join(readme)+'\n'
(OUT/'README.md').write_text(text,encoding='utf-8')

reference=OUT/'_internal/reference';reference.mkdir(exist_ok=True)
attachment=Path('C:/Users/rafif/.t3/userdata/attachments/2c70e49e-62ed-4adf-9eef-a553dec80a5f-0225b25b-f345-4596-9b7c-b3d76413b250.png')
if attachment.exists():shutil.copy2(attachment,reference/'cubase-four-bars.png')
previous_hashes={str(p.relative_to(OLD)):digest(p) for p in [OLD/'README.md']+list((OLD/'MIDI').glob('*.mid'))+list((OLD/'Presets').glob('*.SerumPreset'))}
save(OUT/'_internal/previous-revision-hashes.json',previous_hashes)
links=re.findall(r'\]\(([^)]+)\)',text)
broken=[l for l in links if not l.startswith('http') and not (OUT/l).exists() and l!='_internal/final-receipt.json']
assert not broken,broken
assert len(list((OUT/'MIDI').glob('*.mid')))==17 and len(list((OUT/'Presets').glob('*.SerumPreset')))==10
receipt=dict(ok=True,revision='v002',revised_from='v001',duration_seconds=duration,bars=168,
             midi_files=17,native_presets=10,presets_unchanged=True,notes=sum(len(l['notes']) for l in c['layers']),
             end_tick=322560,readme_links_ok=True,midi_ok=True,preset_structure_ok=True,musical_audit_ok=True,
             plugin_loaded=False,cubase_import_tested=False,audio_rendered=False,auditioned=False,
             files={str(p.relative_to(OUT)):digest(p) for p in list((OUT/'MIDI').glob('*.mid'))+list((OUT/'Presets').glob('*.SerumPreset'))})
save(OUT/'_internal/final-receipt.json',receipt)
(PROJECT/'README.md').write_text('# Neon Breath — Nu-Disco / Synthwave\n\n121 BPM · C minor ·4/4.\n\n[**Terbaru: v002 — lagu penuh168 bar / 5:33**](v002/README.md)\n\n[Versi asal v001 — loop4 bar](v001/README.md) tetap disimpan utuh. Bahan teknis setiap versi berada dalam `_internal/`.\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k!='files'},indent=2))
