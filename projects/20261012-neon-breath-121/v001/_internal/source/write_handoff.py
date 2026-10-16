"""Write complete producer documentation from the exact accepted source specs."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

HERE=Path(__file__).resolve().parent
WORKSPACE=next(p for p in HERE.parents if (p/'studio.local.json').exists())
PROJECT=WORKSPACE/'projects/20261012-neon-breath-121'
OUT=PROJECT/'v001'
comp=json.loads((HERE/'composition.json').read_text(encoding='utf-8'))
specs=json.loads((HERE/'preset-specs.json').read_text(encoding='utf-8'))
manifest=json.loads((OUT/'_internal/serum/manifest.json').read_text(encoding='utf-8'))
assert manifest['ok'] and len(manifest['presets'])==10
sub_id='layer01-sub-bass'
NAMES=['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
def pitch(n):return f'{NAMES[n%12]}{n//12-2} ({n})'
def num(n):return f'{n:.6f}'.rstrip('0').rstrip('.')
def pos(start):
    step=round(start*4)
    return f'{step//16+1}.{(step%16)//4+1}.{step%4+1}'
def envtext(e):return f"{num(e['attack']*1000)} / {num(e['decay']*1000)} / {num(e['sustain']*100)}% / {num(e['release']*1000)}"
def events(item):
    grouped=defaultdict(list)
    for n in item['notes']:grouped[(n['start'],n['duration'])].append(n)
    rows=['| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |',
          '| --- | ---: | --- | --- | ---: | ---: |']
    for (s,d),ns in sorted(grouped.items()):
        ns=sorted(ns,key=lambda n:n['pitch'])
        rows.append(f"| {pos(s)} | {round(s*4)%16+1} | {' + '.join(pitch(n['pitch']) for n in ns)} | {'/'.join(str(n['velocity']) for n in ns)} | {num(d)} | {num(d*4)} |")
    return '\n'.join(rows)

effects_names={'FXDistortion':'Distortion','FXChorus':'Chorus','FXDelay':'Delay','FXReverb':'Reverb','FXComp':'Compression','FXUtils':'Utility / band-limit'}
wave_names={'default':'S2 Tables/Default Shapes.wav','analog_basic':'Analog/Basic Shapes.wav',
            'analog_mini':'Analog/Basic Mini.wav','pwm':'Analog/PWM Juno.wav'}
summaries={
 'layer01-sub-bass':'Root panjang satu bar; Sub triangle mono ke Direct. Fundamental 32,70 / 43,65 / 51,91 / 58,27 Hz. Terapkan LP 80 Hz sesudah Serum agar harmonik triangle ikut dibatasi.',
 'layer02-octave-bass':'Saw punchy, tiap 16th berganti oktav. Gate 72% dari satu step; filter decay 72 ms, saturasi dan HP 95 Hz menjaga pemisahan dari sub.',
 'layer03-chord-stabs':'Dual saw dengan 3+2 unison, chorus vintage, stab pada step 3/7/10/15. Voicing bar 1 Cm7, bar 2 Fm7, bar 3 Abmaj7; bar 4 upper voicing Bb/G: G–Bb–D–F. Dengan sub Bb, harmoni gabungan berbunyi Bb6.',
 'layer04-synth-brass':'Saw 5 voices + square 3 voices, swell filter 35 ms. Chord di downbeat tiap bar, ditahan dua beat, dengan hall besar untuk lift.',
 'layer05-bright-arp':'Up/down triad 16th, gate 66%. Filter pluck membuka singkat; LFO1 menggerakkan cutoff lembut, LFO2 menggerakkan posisi PWM. Volume lebih rendah dari hook.',
 'layer06-glass-bells':'Glassy bell: carrier sine A, B sine +7 semitone aktif dengan volume 0 sebagai sumber FM. C5–C6 Cubase/MIDI84–96. Pola eighth-grid dengan jeda; Space reverb menghasilkan atmosfer tanpa pitch-shift shimmer.',
 'layer07-warm-pad':'Voicing penuh satu bar per chord. Nada yang sama pada chord berurutan diikat: C3/MIDI60 berlangsung bar 1–3, Ab2/MIDI56 bar 2–3. Attack 620 ms dan release 650 ms sesuai pergantian chord sekitar 1,98 detik.',
 'layer08-main-lead':'Hook baru dalam C natural minor. Mono/legato, portamento 50 ms; overlap antar nada dalam frase 0,07 beat (≈34,7 ms). Bar 2/4 berhenti tepat pada beat 3-and agar respons whistle punya ruang.',
 'layer09-synth-whistle':'Sine lead dengan lapisan square pelan dan vibrato tertunda. Menjawab pada beat 3-and, 4, 4-and di bar 2/4; keheningan bar 1/3 tetap dalam file.',
 'layer10-transition-fx':'Satu preset poly dengan dua gesture. C3/MIDI60 velocity1 ditahan 16 beat untuk noise riser; C2/MIDI48 velocity127 di 1.1.1 ditahan satu beat untuk impact sine pitch-down. Jangan menormalisasi velocity layer ini.'
}
sidechain={
 'layer01-sub-bass':'Native LFO1 pump 1/4, kedalaman via PUMP=100. Untuk sidechain audio kick: PUMP=0; host compressor ratio 6:1, attack 1 ms, release 150 ms, threshold sampai reduction ≈8–10 dB. LP 24 dB/oct 80 Hz dan HP 24 Hz setelah Serum.',
 'layer02-octave-bass':'Host sidechain dari kick: ratio 4:1, attack 1 ms, release 85 ms, reduction awal 3–5 dB; atur threshold menurut sample kick.',
 'layer03-chord-stabs':'Host duck ringan 2–3 dB, attack 2 ms, release 110 ms bila stab terasa menutup kick.',
 'layer04-synth-brass':'Host duck 3–4 dB, attack 2 ms, release 130 ms; jaga transient brass.',
 'layer05-bright-arp':'Host duck 2 dB, attack 2 ms, release 85 ms; prioritas jelasnya hook dan hi-hat.',
 'layer06-glass-bells':'Host sidechain OFF sebagai awal; volume rendah dan HP membatasi interferensi.',
 'layer07-warm-pad':'Host duck 3–4 dB, attack 3 ms, release 160 ms bila perlu gerak disco; native compressor OFF.',
 'layer08-main-lead':'Host sidechain OFF sebagai awal; bila diperlukan duck 1–2 dB, attack 3 ms, release 100 ms.',
 'layer09-synth-whistle':'Host sidechain OFF sebagai awal; biarkan jawaban tetap terbaca.',
 'layer10-transition-fx':'Host duck 3–5 dB dari kick, attack 1 ms, release 110 ms; jaga impact tidak menutupi pukulan pertama.'
}

lines=['# Neon Breath — 121 BPM Nu-Disco / Synthwave',
       '', '**121 BPM · C minor · 4/4 · 4 bar · 7,933888 detik · 480 PPQN · straight 1/16, tanpa swing.**',
       '', 'Progresi: **Cm → Fm → Ab → Bb**, satu chord per bar. Paket berisi **10 MIDI synth + 10 preset native Serum 2 + 7 MIDI drum terpisah**. Setiap MIDI SMF format 1, tepat satu track, mulai di bar 1 dan berakhir pada tick 7680. Hook dan susunan nada merupakan komposisi baru mengikuti brief.',
       '', '## Mulai di Cubase', '',
       '1. Set project ke 121 BPM, 4/4, Musical Time Base; left locator **1.1.1.0**, right locator **5.1.1.0**.',
       '2. Buat 10 Instrument Tracks Serum 2. Preset juga sudah dipasang di browser **User → MIDI Creator → 20261012-neon-breath-121 → v001**. Pilih preset dengan ID yang sama seperti MIDI. Untuk salinan paket, gunakan menu Serum **Load Preset** pada file `.SerumPreset` di `Presets/`.',
       '3. Impor setiap MIDI dari tabel ke track yang sesuai dengan **Import to Left Locator**. Aktifkan **Import Dropped File as Single Part** bila drag-and-drop. Pertahankan keheningan awal semua part. Pada project bertempo tetap, **Ignore Master Track Events on Merge** menjaga tempo project.',
       '4. Buat tujuh Sampler Tracks drum terpisah. Muat sample pilihan Anda, root **C3 (MIDI60)**, channel MIDI10. Semua drum sengaja memakai pitch yang sama karena instrumennya terpisah; jangan masukkan tujuh MIDI ini ke satu kit tanpa remap.',
       '5. Untuk Sub Direct, pasang EQ low-pass **80 Hz / 24 dB per oktav**, HP sekitar **24 Hz**, dan compressor sidechain dari kick pada channel Cubase. Untuk sidechain audio, putar macro PUMP ke 0 agar tidak mendobelkan pump LFO.',
       '6. Internal arp/clip Serum dimatikan; file MIDI sudah berisi setiap nada arp. Gunakan voicing poly untuk chord/pad, mono untuk bass/lead sesuai preset. Loop bar 1–4; release dan FX tail boleh melampaui batas loop saat playback.',
       '', '## Track, MIDI, dan preset', '',
       '| Track | Fungsi | MIDI | Preset native / instrumen | Nada | CC7 / CC10 |',
       '| --- | --- | --- | --- | ---: | --- |']
for l in comp['layers']:
    ident=l['id'];presetlink=f'[Serum 2](Presets/{ident}.SerumPreset)' if ident in specs else 'Cubase Sampler — sample Anda'
    lines.append(f"| {l['name']} | {l['role']} | [{ident}.mid](MIDI/{ident}.mid) | {presetlink} | {len(l['notes'])} | {l['volume']} / {l['pan']} |")
lines += ['', '## Bentuk 4 bar dan ruang frase', '',
          '| Bar | Chord / bass | Perkembangan |', '| --- | --- | --- |',
          '| 1 | Cm / C0 | Downbeat kick, crash, brass, impact; bass/arp mulai; hook memperkenalkan motif. Riser mulai pelan. |',
          '| 2 | Fm / F0 | Hook beralih F–Ab lalu berhenti; whistle menjawab di setengah bar terakhir. |',
          '| 3 | Ab / Ab0 | Hook mencapai C4; pad mempertahankan C dan Ab dari bar sebelumnya; riser makin membuka. |',
          '| 4 | Bb / Bb0 | Hook turun; whistle mengantisipasi C pada akhir loop. Riser mencapai terang tepat di batas bar5. |',
          '', 'Pad mempertahankan harmoni per bar, bukan satu chord statis sepanjang empat bar. Riser empat bar cocok sebagai build menuju pengulangan berikutnya; bila loop diulang terus, mute riser pada pengulangan yang tidak memerlukan transisi. Pan/volume MIDI adalah titik awal balance, bukan hasil mix audio terukur.',
          '', '## Konvensi parameter dan notasi', '',
          '- **Nama nada selalu Cubase: C3=MIDI60.** Angka MIDI di kurung adalah acuan utama. Penamaan standar C4=MIDI60 menyebut semua nada satu oktaf lebih tinggi.',
          '- **Posisi `bar.beat.16th`**: `2.3.3` = bar2, beat3, subdivision ketiga, yaitu beat3-and. Step bar 1–16 ditampilkan juga. Satu step = 0,25 beat ≈123,967 ms =120 tick. Durasi beat dan durasi step adalah gate MIDI, bukan tail reverb.',
          '- Envelope ditulis **A/D/S/R**: attack, decay, release dalam ms; sustain dalam persen. Hold=0; curve attack=50%, decay/release=66,6% mengikuti schema.',
          '- Oscillator detune dan level memakai nilai native/tool **0–1**; octave relatif ke nada MIDI, fine dalam cent. Pan0=tengah. Table position adalah nilai tersimpan `kParamTablePos` 0–256. Default Shapes frame0=saw, sekitar128=square; Basic Shapes frame0=sine, Basic Mini frame0=rounded saw. Identitas frame diperiksa offline dari WAV factory, bukan melalui listening plugin.',
          '- Cutoff filter adalah nilai tersimpan normalized **0–1**, **bukan Hz**. Resonance/drive/wet memakai persen; `level_out=0.5`, stereo50 netral menurut schema. File native memuat nilai ini langsung. Nilai cutoff Hz pada EQ/Utility dan instruksi host ditulis terpisah.',
          '- Label UI ENV1/ENV2 = schema env0/env1; LFO1/LFO2 = lfo0/lfo1. Depth matrix dalam persen normalized, **bukan langsung semitone/cent/Hz**. Bipolar berarti gerak dua arah; depth satu arah jika tidak ditandai.',
          '- LFO `beat_sync=true, rate=0` menggunakan default **1/4** tersimpan tanpa key rate. Untuk `beat_sync=false`, rate eksplisit adalah Hz. Semua kurva LFO ordinary di paket ini triangle 0→1→0; Sub memakai kurva duck khusus.',
          '- FX berikut ditulis dalam urutan rack Main. `kParamTimeL/R` delay dalam detik, chorus depth/delay kira-kira ms, compressor attack/release ms, makeup gain multiplier. FX yang tidak terdaftar **OFF**.',
          '- Compression internal mengatur dinamika sound sendiri. **Sidechain kick audio adalah insert host**, tidak otomatis tersimpan di preset Serum. Semua angka gain-reduction host adalah target awal untuk disetel saat audition.',
          '', '## Parameter Serum dan MIDI lengkap per layer']

for l in comp['layers'][:10]:
    ident=l['id'];s=specs[ident]
    lines += ['',f"### {l['name']}",'',summaries[ident], '',
              f"[MIDI](MIDI/{ident}.mid) · [Preset native](Presets/{ident}.SerumPreset)", '',
              '**Oscillator dan routing**', '',
              '| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |',
              '| --- | --- | --- | --- | --- | --- |']
    for label,i in [('A',0),('B',1),('C',2),('Noise',3),('Sub',4)]:
        o=s['oscillators'][i]
        if not o['enabled']:
            lines.append(f'| {label} | OFF | 0 / 0 | 1 / 0 | 0 | none |');continue
        wave=(f"{o.get('noise_type','White')}" if i==3 else f"{o.get('sub_shape','saw')}" if i==4 else
              f"{wave_names.get(o['wavetable'],o['wavetable'])}; WT pos {num(o.get('table_position',0))}")
        if i<3 and o.get('warp_amount',0):wave+=f"; warp {o.get('warp_mode','fm')} {num(o['warp_amount']*100)}%"
        lines.append(f"| {label} | ON: {wave} | {num(o['octave'])} / {num(o.get('fine',0))} cent; semitone {num(o.get('semitone',0))} | {num(o['unison'])} / {num(o['detune'])} | {num(o['volume'])} | {o['filter_routing']}; F1 balance {num(o.get('filter_balance',0))} |")
    lines += ['', '**Filter dan envelope**', '',
              '| Modul | Nilai eksplisit |', '| --- | --- |']
    for i,f in enumerate(s['filters'],1):
        lines.append(f"| Filter{i} | {'ON' if f['enabled'] else 'OFF'}; {f['type']}; cutoff {num(f['cutoff'])}; resonance {num(f['resonance'])}%; drive {num(f['drive'])}%; key track {f['key_track']}; wet {num(f['wet'])}%; output {f['output_routing']} |")
    for i,e in enumerate(s['envelopes'][:3],1):lines.append(f'| ENV{i} A/D/S/R | {envtext(e)} |')
    g=s['global']
    lines.append(f"| Global | master {num(g['master_volume'])}; mono {g['mono']}; poly {num(g['poly_count'])}; legato {g['legato']}; glide {num(g['portamento_time']*1000)} ms; Porta Always OFF; swing0; internal arp OFF |")
    lines += ['', '**LFO1, LFO2, dan matrix**', '',
              '| LFO | Clock / trigger / shape | Assignment |', '| --- | --- | --- |']
    for i,f in enumerate(s['lfos'][:2]):
        rts=[r for r in s['mod_routes'] if r['source']==f'lfo{i}']
        assigns=[]
        for r in rts:
            aux=f"; aux {r['aux_source']}{' inverted' if r.get('aux_inverted') else ''}" if r.get('aux_source') else ''
            assigns.append(f"{r['destination']} {r['amount']:+g}%{' bipolar' if r.get('bipolar') else ''}{aux}")
        rate='1/4, default rate0' if f.get('beat_sync') and f['rate']==0 else f"{num(f['rate'])} Hz"
        shape='duck: (0,1), (0.075,1), (0.45,0.1), (0.75,0), (1,0)' if ident==sub_id and i==0 else 'triangle (0,0)→(0.5,1)→(1,0)'
        lines.append(f"| LFO{i+1} | {rate}; {f['mode']}, mono/shared {f['mono']}; delay {num(f.get('delay',0)*1000)} ms; rise {num(f.get('rise',0)*1000)} ms; {shape} | {'; '.join(assigns) if assigns else 'OFF: tidak dirutekan'} |")
    lines += ['', '| Sumber matrix lain | Tujuan | Depth / polarity / aux |','| --- | --- | --- |']
    for r in s['mod_routes']:
        if r['source'].startswith('lfo'):continue
        src=r['source']
        if src.startswith('env'):src=f'ENV{int(src[3:])+1}'
        if src.startswith('macro'):src=f"Macro{int(src[5:])+1} ({s['macros'][int(src[5:])]['name']})"
        aux=f"; aux {r['aux_source']}{' inverted' if r.get('aux_inverted') else ''}" if r.get('aux_source') else ''
        lines.append(f"| {src} | {r['destination']} | {r['amount']:+g}%{' bipolar' if r.get('bipolar') else ' unipolar'}{aux} |")
    lines += ['', '**FX rack**', '', '| Urutan / modul | Wet | Parameter |', '| --- | --- | --- |']
    for i,f in enumerate(s['fx_chain'],1):
        parms='; '.join(f'{k}={num(v) if isinstance(v,(int,float)) else v}' for k,v in f['params'].items())
        lines.append(f"| {i}. {effects_names.get(f['type'],f['type'])} | {num(f['wet'])}% | {parms} |")
    for typ in ['FXDistortion','FXChorus','FXDelay','FXReverb','FXComp']:
        if not any(f['type']==typ for f in s['fx_chain']):lines.append(f'| {effects_names[typ]} | OFF | Tidak digunakan |')
    lines += ['',f"Macro defaults: {', '.join(f'{i+1} {m["name"]}={m["value"]}%' for i,m in enumerate(s['macros']))}. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.",
              '',f'**Sidechain / insert DAW:** {sidechain[ident]}', '',
              '<details>',f'<summary>MIDI DATA lengkap — {len(l["notes"])} nada, 4 bar</summary>','',events(l),'','</details>']

lines += ['', '## Drum per layer / per file', '',
          'Sample konkret belum dipilih atau disalin. Berikut karakter awal yang cocok untuk brief dan mapping Sampler Track; pitch **MIDI60 = C3 Cubase** berlaku untuk seluruh note di masing-masing file. CC7/CC10 pada tabel track merupakan level/pan independen per instrumen.', '',
          '| File | Karakter sample yang dipilih di DAW | Performa / mapping |', '| --- | --- | --- |',
          '| [Kick](MIDI/drum-kick.mid) | Kick disco padat, fundamental sekitar 45–65 Hz, attack jelas, tail sekitar 100–160 ms; hindari tail bass panjang yang menutup sub. | C3/MIDI60, channel10; beats1/2/3/4 setiap bar. |',
          '| [Snare](MIDI/drum-snare.mid) | Snare elektronik 80s: body terkontrol dan snap terang; tail sekitar 120–200 ms. | C3/MIDI60; beats2 dan4. |',
          '| [Clap](MIDI/drum-clap.mid) | Clap disco agak lebar, HP sekitar200 Hz; layer lebih pelan daripada snare. | C3/MIDI60; tepat serempak snare, tanpa offset flam. |',
          '| [Closed hat](MIDI/drum-closed-hat.mid) | Hat terang pendek, tail sekitar30–60 ms. | C3/MIDI60; pola16th, ruang pada step3/7/11/15 untuk open hat. |',
          '| [Open hat](MIDI/drum-open-hat.mid) | Open hat airy offbeat; atur tail sekitar100–150 ms. | C3/MIDI60; step3/7/11/15. Bila dua sampler dapat memakai choke bersama, closed hat memotong open hat berikutnya; jika tidak, pendekkan tail sample. |',
          '| [Shaker](MIDI/drum-shaker.mid) | Shaker lembut pendek, aksen offbeat, pan kanan ringan. | C3/MIDI60; straight16th dengan variasi velocity, tanpa swing. |',
          '| [Crash](MIDI/drum-crash.mid) | Crash tipis berfilter, tail sekitar0,8–1,5 detik; tidak menutup attack kick. | C3/MIDI60; hanya downbeat bar1. |']
for l in comp['layers'][10:]:lines += ['', '<details>',f'<summary>{l["name"]}: MIDI lengkap — {len(l["notes"])} hit</summary>','',events(l),'','</details>']
lines += ['', '## Batas implementasi yang perlu diperhatikan', '',
          '- **Sub Direct vs low-pass:** Direct sengaja melewati filter/FX Serum. Filter LP24 disimpan OFF sebagai acuan, sehingga low-pass80 Hz yang diminta berada pada insert DAW. Pilihan triangle memenuhi opsi waveform brief; kandungan harmonik sebelum insert LP tetap ada. PUMP internal merupakan LFO beat-sync dan belum diuji phase terhadap transport; compressor sidechain host mengikuti kick sebenarnya.',
          '- **Delay stereo/ping-pong:** file menyimpan L=0,247934 s (1/8), R=0,123967 s (1/16), beat syncOFF dan `kParamMode=1`, nilai yang ditemukan dalam preset Factory ARP–Aardvark. Arti UI mode1 belum diverifikasi; untuk ping-pong persis, pilih **Ping-Pong** di UI Serum dan konfirmasi interval saat playback. Waktu delay native ditetapkan untuk121 BPM, sehingga harus disetel ulang bila tempo diubah.',
          '- **Bell shimmer:** file menggunakan FM + Space reverb + stereo delay. Tidak ada pitch-shift shimmer yang tersimpan. Ini memenuhi pilihan atmosfer Space; bila memerlukan shimmer beroktaf, tambah pitch-shift reverb/return di DAW.',
          '- **Layer10:** selector velocity berupa scaling aux matrix, bukan hard split. Pada velocity1 carrier impact masih menerima sekitar1/127 scaling dan bisa bocor sangat pelan; pada velocity127 noise inverted-velocity menjadi0. Riser ENV2 attack=7,933884 s, impact ENV3 decay380 ms. Route ENV3→pitch depth+50% memberi pitch turun saat envelope turun; besaran semitone efektif belum diuji di plugin. Tetap gunakan velocity1/127 yang sudah ditulis.',
          '- **EQ, macro dan balance:** titik awal sound sudah tersimpan; belum ada pengukuran level, peak, mono compatibility, envelope Direct, atau hasil macro ekstrem melalui audio. Mulai playback dengan fader rendah, lalu balance sesuai sample drum dan register tiap sound.',
          '', '## Instrumen eksternal dan dependency', '',
          'Semua instrumen synth memakai **Serum 2**. Instrumen eksternal hanya drum: **Cubase Sampler Track** atau sampler one-shot pilihan Anda. Set root C3/MIDI60, channel10, satu sample per track, one-shot untuk drum; gunakan note-gated jika ingin durasi MIDI mengontrol tail. Tidak ada keyswitch atau Program Change.',
          'Preset memakai wavetable factory **Default Shapes**, **Basic Mini**, **Basic Shapes**, dan **PWM Juno**. Semua path dependency ditemukan di instalasi lokal. Tidak ada custom wavetable/sample/IR yang perlu disalin. Saat berpindah komputer, instal factory content Serum 2 yang sama. File native sudah berada di `Presets/`; registry/resource manifest, hash dan readback tersimpan di `_internal/serum/`.',
          '', '## Verifikasi, asumsi, dan referensi', '',
          '- **MIDI — PASS:** validate/generate/verify exit0 dan `ok:true`; 17 file SMF1 dengan tepat satu track/instrumen, 480 PPQN, tempo495868 µs/quarter, meter4/4, end tick7680. Total436 note-on, pasangan note-off lengkap, tidak ada overlap pitch sama atau offset onset. Lead memiliki overlap pitch berbeda untuk legato.',
          '- **Preset native — PASS struktural:** 10 `.SerumPreset` benar-benar dibangun melalui server serum-mcp; container XferJson/Zstd/CBOR dapat didecode; source/filter/envelope/LFO/macro/FX/global/matrix cocok dengan spec; arp disabled diperiksa melalui raw switch. Nol unsafe wire type. Hash salinan sama dengan file yang dipasang; dependency ditemukan.',
          '- **Audit musikal offline — selesai:** scale C natural minor, voice-leading, root/progresi, posisi drum, artikulasi 16th, chord polyphony dan jeda call/response diperiksa. Ini penilaian berdasarkan MIDI/spec, belum penilaian mix audio.',
          '- **Pemuatan native dalam plugin — BELUM DIUJI.** Impor/drag-and-drop Cubase — BELUM DIUJI. Render/analisis audio — BELUM DILAKUKAN. Listening aktual — BELUM DILAKUKAN. Tidak ada klaim `.cpr` atau preview audio.',
          '- **Asumsi berdampak:** register Sub disetujui C0/F0/Ab0/Bb0; 4-bar loop sesuai panjang eksplisit; warna chord7 dan Bb6 di bar4; common-tone pad ties; 7 drum dipilih sebagai bagian performa, sample tetap pilihan pengguna.',
          '- Referensi karakter produksi: [Synth Ctrl — Take My Breath Breakdown](https://synthctrl.com/blogs/blog/the-weeknd-take-my-breath-breakdown), terutama envelope filter, velocity dan ruang synth; [Resident Advisor — ulasan Take My Breath](https://ra.co/reviews/34172) untuk konteks arp Moroder/disco. Artikel merupakan referensi pendekatan, bukan bukti patch asli rekaman.',
          '- Referensi parameter lokal: Factory **BA–Eighty** (filter envelope cepat/drive), **PD–Analog Butter** (independent pad movement/space). Hanya struktur yang diperiksa; preset referensi tidak diaudisi pada run ini.',
          '', 'Untuk audit teknis: [_internal/source/composition.json](_internal/source/composition.json), [_internal/source/preset-specs.json](_internal/source/preset-specs.json), [receipt preset](_internal/serum/manifest.json), dan [receipt final](_internal/final-receipt.json).']

# sub_id is used only by the LFO table renderer above.

def finish():
    text='\n'.join(lines)+'\n'
    (OUT/'README.md').write_text(text,encoding='utf-8')
    (PROJECT/'README.md').write_text('# Neon Breath — Nu-Disco / Synthwave\n\n121 BPM · C minor · 4/4 · 4 bar.\n\n[Revisi siap pakai v001: README, semua MIDI dan preset Serum 2](v001/README.md).\n\nBahan teknis berada dalam `v001/_internal/`; tidak ada revisi lama yang diganti.\n',encoding='utf-8')
    source=OUT/'_internal/source';source.mkdir(exist_ok=True)
    for p in HERE.iterdir():
        if p.is_file():shutil.copy2(p,source/p.name)
    result=subprocess.run(['uv','run','midi-creator','verify',str(OUT)],cwd=WORKSPACE,text=True,capture_output=True)
    verification=json.loads(result.stdout)
    assert result.returncode==0 and verification['ok']
    (OUT/'_internal/final-midi-verification.json').write_text(result.stdout,encoding='utf-8')
    links=re.findall(r'\]\(([^)]+)\)',text)
    broken=[v for v in links if not v.startswith('http') and not (OUT/v).exists() and v!='_internal/final-receipt.json']
    assert not broken,broken
    assert len(list((OUT/'MIDI').glob('*.mid')))==17
    assert len(list((OUT/'Presets').glob('*.SerumPreset')))==10
    receipt=dict(ok=True,midi_ok=True,preset_structure_ok=True,readme_links_ok=True,
                 midi_files=17,native_presets=10,note_count=436,end_tick=7680,
                 grid='straight 1/16',plugin_loaded=False,cubase_import_tested=False,
                 audio_rendered=False,auditioned=False,
                 files={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in list((OUT/'MIDI').glob('*.mid'))+list((OUT/'Presets').glob('*.SerumPreset'))})
    (OUT/'_internal/final-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in receipt.items() if k!='files'},indent=2))

if __name__=='__main__':finish()
