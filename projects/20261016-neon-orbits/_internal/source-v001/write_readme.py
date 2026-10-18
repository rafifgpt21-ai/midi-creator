"""Producer documentation and copy-provenance finalization for Neon Orbits v002."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path.cwd().resolve()
PROJECT=ROOT/'projects/20261016-neon-orbits'
REV=PROJECT/'v002'
audit=json.loads((REV/'_internal/musical-audit.json').read_text())
spec=json.loads((REV/'_internal/composition.json').read_text())
layers={l['id']:l for l in spec['layers']}
sound={
 'mono-bass':('Bass mono saw/triangle, low end tengah; offbeat menjawab kick','Mini-family VCO approximation; release 65 ms; tanpa chorus'),
 'juno-pad':('Pad hangat, sumber PWM tunggal dan chorus','DCO-family approximation; tanpa pitch drift; attack 550 ms/release 1.45 s'),
 'phase-seven-pluck':('Pluck 7/8 beraksen 2+2+3, melewati garis bar','Saw berfilter, decay pendek; echo eighth-note ringan'),
 'three-two-pulse':('Pulse hollow, tiga serangan melawan dua quarter beats','Square/triangle; pendek dan lebih sempit dari pad'),
 'analog-lead':('Motif E–B–F#–G, frase berjeda dan jawaban berbeda di drop kedua','Dua sumber saw/pulse -2/+2 cents; mono dan retrigger'),
 'poly-brass':('Brass synth yang menjawab ruang kosong lead','Dua sumber saw -3/+3 cents, filter swell; bukan brass akustik'),
 'glass-keys':('Synth digital berkaca untuk breakdown dan coda','OPL + Dying Sine; bukan piano akustik'),
}
rows=[]
for lid,(role,loading) in sound.items():
    inv=audit['inventory'][lid]
    rows.append(f"| {layers[lid]['name']} | {role} | {inv['pitch_min']}–{inv['pitch_max']} | [{lid}.mid](MIDI/{lid}.mid) | [{lid}.SerumPreset](Presets/{lid}.SerumPreset) | {loading} |")
drums={
 'kick':('Kick four-on-the-floor','Kick elektronik bulat dan tegas, attack singkat; body sekitar 100–180 ms agar bass offbeat tetap jelas. Jika dituning, E sekitar 41/82 Hz dapat dicoba setelah mendengar sampelnya.'),
 'snare-clap':('Backbeat 2 dan 4','Satu sample snare/clap berlapis, karakter gated era 80-an, tail sekitar 120–250 ms. Nama layer ini satu instrumen/sample, bukan dua file tersembunyi.'),
 'closed-hat':('Eighth lurus, tambahan 16th pada drop kedua','Hat kering dan pendek 30–70 ms, lebih lembut pada 16th tambahan. Jangan jadikan top end paling keras.'),
 'open-hat':('Offbeat eighth','Hat terbuka 100–200 ms, berpasangan dengan closed hat. Sampler one-shot boleh mengabaikan gate MIDI; atur choke sesuai panjang sample.'),
 'synth-tom':('Fill terpilih','Satu tom elektronik rendah/menengah, decay 150–300 ms. Jika bernada, E atau B masuk ke pusat tonal; MIDI 60 tetap root pemicu, bukan permintaan bunyi C.'),
 'crash':('Aksen awal bagian','Crash/splash terang yang terkendali, tail 0.8–1.8 detik; jangan menutup pluck saat drop masuk.'),
}
drows=[f"| {layers[lid]['name']} | [{lid}.mid](MIDI/{lid}.mid) | C3 / **60** | 10 | {role}. {char} |" for lid,(role,char) in drums.items()]
text=f'''# Neon Orbits — retro synthwave / progressive EDM

**124 BPM · E harmonic minor · 4/4 · 164 bar · 5:17.419 · 13 layer · 7 preset native Serum 2.**

Aransemen instrumental lengkap: kick four-on-the-floor menjadi jangkar, sementara sequence 7/8 dan poliritme 3:2 bergeser di atasnya. Materi melodinya orisinal. Arahan deadmau5 diterapkan pada perkembangan sequence dan filter; tidak ada lagu referensi yang ditranskripsi.

Revisi siap pakai: **v002**. Audit sebelum penyerahan merapikan lompatan register lead pada bar 139/141 dan memperpendek delapan gate bass sebelum pickup. Onset, velocity, tempo, serta sebelas layer lain dipertahankan dari v001. Versi awal disimpan di arsip internal.

## Mulai di Cubase

1. Buat project **124 BPM, 4/4**. Aktifkan **Musical Time Base** pada track dan atur left locator ke **1.1.1.0**. Gunakan **Import to Left Locator** saat impor MIDI. Untuk drag-and-drop, aktifkan **Import Dropped File as Single Part**, lalu tempatkan setiap part di bar 1. Pada project bertempo tetap, **Ignore Master Track Events on Merge** mempertahankan tempo project yang sudah diatur.
2. Buat tujuh instrument track Serum 2. Muat preset yang berpasangan pada tabel, lalu impor MIDI yang sama namanya. Semua file menyimpan keheningan awal; **jangan geser nada pertama ke bar 1**. Setiap file SMF format 1 berisi tepat satu track dan panjang global yang sama.
3. Preset dapat dibuka melalui menu preset Serum **Load Preset** dengan memilih `.SerumPreset` dari `Presets/`. Alternatifnya, salin ketujuh file ke folder User Serum, lalu rescan browser. Salinan juga sudah dibuat pada `Presets/User/MIDI Creator/20261016-neon-orbits/v001/` di library Serum komputer ini; bank v001 tersebut berisi sound yang sama dengan salinan final v002.
4. Buat enam **Sampler Track terpisah**, pilih sendiri sample untuk masing-masing bagian drum, atur root sample **C3 di Cubase = MIDI 60**, lalu impor MIDI drum yang sesuai. Semua drum memakai channel 10. Set instrumen agar menerima channel tersebut.
5. Pertahankan data **CC1**: semua preset memetakan mod wheel ke cutoff untuk perkembangan filter sepanjang lagu. CC7/CC10 awal memberi volume/pan per layer; jika host tidak menerapkannya pada instrumen, gunakan angka mixer di bawah sebagai titik awal, lalu atur gain dengan mendengar hasilnya. Jangan arahkan seluruh drum ke satu instrumen shared tanpa merancang ulang mapping dan mixer.

## Track synth dan preset

Angka rentang adalah **MIDI numerik**, sehingga tidak berubah walaupun label oktaf DAW berbeda. Tidak ada Program Change yang mengubah preset secara otomatis.

| Track | Fungsi / karakter | Rentang MIDI | MIDI | Serum 2 | Cara memainkan / artikulasi |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

Setiap preset mempunyai **Tone** default 15/100 dan **Contour** default 20/100. Tone menambah pembukaan filter; Contour memperpanjang envelope timbre. Rentang 0–100 tersedia, tetapi ekstrem serta gabungan macro belum diaudisi; default adalah titik mulai. CC1 memberi gerak cutoff tambahan tanpa mengubah pitch. Arpeggiator internal dimatikan pada semua sound karena seluruh nada sudah ditulis dalam MIDI.

Delay pada lead, pluck, dan glass keys memakai **241.935 ms**, setara eighth note pada 124 BPM, dengan feedback rendah. Ini adalah waktu dalam detik yang sengaja disetel free, bukan klaim BPM-sync yang sudah diuji. Jika tempo diubah, sesuaikan delay menjadi **30 / BPM detik**. Tidak ada sidechain compressor DAW yang dikonfigurasi oleh file ini; ruang kick/bass sudah dibentuk lewat onset dan gate. Sidechain bisa ditambahkan saat mixing setelah sample kick dipilih.

## Bentuk lagu

| Bar | Bagian | Perkembangan |
| --- | --- | --- |
| 1–16 | Intro | Pad dan kilatan glass keys; hat masuk bar 5, kick/bass bar 9. |
| 17–32 | Groove | Arp 7/8 masuk; backbeat dan offbeat hat membuka groove. |
| 33–48 | Build | Fragmen lead, cutoff naik; bass keluar bar 45–48, beat terakhir sebelum drop dikosongkan. |
| 49–80 | Drop 1 | Lead lengkap dan jawaban brass; poliritme 3:2 aktif bar 57–72. Pad dikurangi di sela frase. |
| 81–96 | Breakdown | Seluruh drum dan bass diam; glass keys membawa harmoni lebih renggang. Arp tipis kembali bar 89. |
| 97–112 | Rebuild | Motif dipotong dan filter dibuka; kick kembali bar 105, bass ditarik lagi bar 109–112. |
| 113–144 | Drop 2 | Motif kembali dengan variasi, tambahan hat, filter lebih terbuka; 3:2 bar 121–136. Frase akhir lead diperbarui. |
| 145–160 | Outro | Lead/brass/3:2 keluar. Arp berhenti setelah bar 152, hat setelah 156; kick/bass menyisakan jalan keluar. |
| 161–164 | Coda / release | Em dan nada E terakhir pada bar 161; bar 162–164 tanpa note-on baru untuk release. |

Koleksi nada: **E, F#, G, A, B, C, D#**. Progresi utama **Emadd9 – Cmaj7 – Amadd9 – B7b9**, umumnya dua bar per chord. Breakdown berawal **Cmaj7 – Amadd9 – F#m7b5 – B7b9**, kemudian **Emadd9 – Cmaj7 – Amadd9 – D#dim7 – B7b9**. Dua chord terakhir breakdown masing-masing satu bar. D# sebagai leading tone dan C sebagai b9 memberi warna harmonic minor. Coda menetap pada Em.

## Cara kerja pola silang

**Polimeter 7/8:** Phase Seven Pluck berisi siklus tujuh eighth notes, aksen **2+2+3**, berdurasi 3.5 quarter beats. Kick tetap dalam bar empat quarter beats. Awal siklus bergeser setengah beat terhadap bar utama; keduanya bertemu kembali setelah **28 beats = 7 bar 4/4 = 8 siklus 7/8**. MIDI tetap memiliki meter global 4/4 agar seluruh file sejajar; meter kedua diwujudkan melalui panjang dan aksen pola. Sequence melewati garis bar tanpa reset. Reset struktural hanya di bar 17, 49, 89, 97, 113, dan 145; voice chord menyesuaikan harmoni tanpa mengulang fase tiap bar.

**Poliritme 3:2:** Three Two Pulse menyerang pada **0, 2/3, 4/3 beat** dalam jendela dua quarter beats, sementara kick menyerang **0 dan 1**. Ini tiga pembagian rata melawan dua; bukan hanya aksen tiga nada pada grid eighth. Part aktif pada dua span di tabel, agar kompleksitas tidak memenuhi seluruh lagu.

Timing **strict, tanpa swing**, 960 PPQN. Grid **1/48 whole note = 1/12 quarter beat** menampung straight 16th dan triplet dalam satu lattice. Variasi manusiawi terbatas pada velocity, panjang gate, frase, dan evolusi timbre; onset tidak diberi jitter.

## Drum yang cocok dan mapping

**Belum ada sample/kit yang dipilih atau disalin.** Tabel ini menjelaskan karakter yang mendukung lagu. Load sample milik Anda pada sampler masing-masing. Trigger semua bagian adalah 60, bukan mapping General MIDI. Root Cubase C3 dan angka MIDI 60 adalah acuan; generator menamai angka yang sama C4.

| Track | MIDI | Root / trigger | Channel | Peran dan saran karakter |
| --- | --- | --- | --- | --- |
{chr(10).join(drows)}

Closed/open hat tidak menyerang bersamaan; bila memakai instrumen dengan choke bersama, closed hat menutup open hat. Jika memakai dua Sampler Track terpisah, kendalikan tail open-hat dengan envelope sampler karena choke antarinstrumen tidak otomatis ada. Fill ditempatkan pada bar **31, 46, 48, 63, 78, 103, 110, 112, 127, 142, 158**. Kick tetap four-on-the-floor pada seluruh groove/drop; breakdown serta penarikan menjelang drop adalah keheningan yang disengaja.

Mixer awal MIDI (CC7/CC10): {', '.join(f"{l['id']} {l['volume']}/{l['pan']}" for l in spec['layers'])}. Pan 64 berarti tengah. Karena tiap drum memakai file/instrumen terpisah, setting ini independen.

## Library, batas implementasi, dan pemeriksaan

Semua instrumen bernada memakai Serum 2; instrumen luar hanya sampler drum pilihan pengguna. Diperlukan factory wavetable library Serum 2: **Basic Shapes, Basic Mini, PWM Juno, Default Shapes, DM - OSCAR, Basic OPL, Dying Sine**. Semua resource ditemukan di komputer ini dan hash dicatat. Tidak ada sample, wavetable custom, atau IR tambahan yang perlu dipasang.

Karakter analog adalah **pendekatan keluarga instrumen terawat**, bukan klaim emulasi sirkuit yang telah dibandingkan. Pad memakai satu sumber tabel PWM dengan pitch stabil dan chorus; dua sumber lead/brass memakai offset tuning kecil. Noise FM, noise AM, pola kalibrasi voice, tape, dan pitch drift kontinu tidak ditambahkan tanpa kebutuhan. Phase memory tetap mengikuti Init. Macro cutoff tidak diterjemahkan menjadi frekuensi Hz yang belum diukur.

- **MIDI:** validate/generate/verify berhasil, `ok: true`; **4.182 nada**, 13 file, satu track SMF1 per file, **629.760 tick** total masing-masing, nol onset di luar grid. Tidak ada SysEx, Bank Select, Program Change, atau metadata key/marker tambahan dalam MIDI per layer.
- **Preset native:** tujuh `.SerumPreset` berhasil dibuat melalui serum-mcp; seluruh oscillator/filter/envelope/LFO/macro/FX/routing yang diminta diperiksa readback, scan tipe wire bersih, dan hash salinan cocok. Arp disabled dibaca sebagai `null` oleh extractor, sehingga status off dikonfirmasi dari payload native.
- **Audit musikal offline:** 79 pemeriksaan lulus, termasuk koleksi nada, aksen 7/8 lintas bar, rasio 3:2, kick tiap quarter beat pada bagian aktif, drum root 60, bass mono tanpa overlap, perubahan v002 yang terbatas, serta ruang akhir.
- **Pemuatan native dalam Serum, impor Cubase live, rendering audio, mono/stereo audio, dan listening:** **belum diuji/dilakukan**. Status instalasi Serum 2.0.23 ditemukan, tetapi itu bukan bukti preset final telah dimuat. Ini paket MIDI dan preset, bukan mix audio yang sudah didengarkan.

Brief, ARR-SPEC MC, script, preset specs, daftar skill, checksum, resource manifest, dan receipt ada di `_internal/`. Rangkaian skill yang dipakai mencakup workflow, bentuk, perkembangan motif, harmoni, melodi, groove, rhythm section, orkestrasi, tekstur, desain suara, mix intent, kompilasi MIDI, gaya EDM, dan audit MC, disertai enam skill Serum terkait. Pedoman MC untuk swing/onset bebas atau chord di luar mode dikecualikan sesuai timing repo dan permintaan harmonic minor.
'''
(REV/'README.md').write_text(text,encoding='utf8')

receipt_path=REV/'_internal/serum-bank/receipt.json'
receipt=json.loads(receipt_path.read_text())
for p in receipt['presets']:
    p['build_delivered_original']=p['delivered']
    p['delivered']=str(REV/'Presets'/f"{p['id']}.SerumPreset")
    assert hashlib.sha256(Path(p['delivered']).read_bytes()).hexdigest()==p['sha256']
receipt['copied_to_revision']='v002; identical native sounds, composition-only audit corrections'
receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
for target in re.findall(r'\]\(([^)]+)\)',text):
    assert (REV/target).exists(),target
print('README: 20 MIDI/preset links resolve; native copied hashes match.')
