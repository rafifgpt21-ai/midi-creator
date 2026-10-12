# Brief komposisi

- Proyek: Afterglow Circuit — Progressive House
- Revisi: v001
- Revisi asal (jika ada): tidak ada; lagu baru, terpisah dari Neon Step.
- Tanggal: 2026-10-09

## Permintaan asli

> buatkan lagu baru seperti lagu deadmau5

## Keputusan musik

- Gaya / mood: melodic progressive house atmosferik; hipnotik, hangat, melankolis, dengan perkembangan panjang.
- Tempo (quarter-note BPM): 126.
- Meter: 4/4.
- Key / scale / pusat tonal: F minor / F natural minor.
- Jumlah bar / panjang: 160 bar, 640 beat, sekitar 5:04.762; PPQN 960.
- Bentuk dan bagian: intro 1–16; groove 17–32; theme 33–48; breakdown 49–64; build 1 65–72; drop 1 73–96; interlude 97–112; build 2 113–120; final drop 121–144; outro 145–160.
- Progresi / pendekatan harmoni: Fm9–Dbmaj9–Abmaj9–Ebadd9, masing-masing dua bar. Voicing menengah dengan voice leading dekat; kembali ke Fm9 pada bar 159–160.
- Groove / densitas / dinamika: straight 1/16, four-on-the-floor, clap 2/4, open hat offbeat, bass offbeat; arp tumbuh dari quarter/eighth ke sixteenth; snare roll 1/8 → 1/16 → 1/32. Satu beat hening sebelum drop.
- DAW / plugin / drum mapping: tidak ditentukan. GM sebagai mapping/penanda awal; target synth khusus dan efek diatur di DAW.

| Layer ID | Instrumen / sound target | Fungsi | Program GM 0-based / pitch drum |
| --- | --- | --- | --- |
| kick | Deep electronic kick | Fondasi four-on-the-floor | 36 |
| clap | Electronic clap | Backbeat | 39 |
| snare-roll | Electronic snare | Build-up dan fill | 38 |
| closed-hat | Closed hi-hat | Pulse 1/16 | 42 |
| open-hat | Open hi-hat | Offbeat | 46 |
| ride | Ride cymbal | Lift puncak drop | 51 |
| shaker | Shaker / maracas | Percussion ringan | 70 |
| synth-bass | Deep mono synth bass | Low-end offbeat | 38 |
| poly-synth | Wide saw poly synth | Hook chord utama | 81 |
| pluck-arp | Plucked synth | Arpeggio berulang | 80 |
| warm-pad | Warm atmospheric pad | Ruang harmoni | 89 |
| lead-synth | Melodic saw lead | Motif utama 8 bar | 81 |

## Asumsi dan referensi

- Pengguna menyebut artis tanpa judul lagu atau file referensi. Arah yang dipilih adalah progressive house melodis/atmosferik; bukan analisis audio lagu tertentu.
- Semua melodi, pola MIDI dan aransemen dibuat baru. Referensi artis merupakan arahan estetika umum.
- Instrumental, dengan 12 layer untuk aransemen lengkap. Tempo, key dan panjang dipilih agent.
- Lagu sebelumnya dipertahankan; ini proyek baru, bukan revisi new jack swing.
- Generator reproduksi: `build_composition.py`; seed velocity 126160. Onset grid lurus tanpa jitter.
- Setiap instrumen memakai satu program tetap dan satu file type 0/satu track; semua file mencakup 0–614400 tick, termasuk keheningan sebelum masuk.
- File drum channel 10; file synth masing-masing channel 1. Impor tiap file ke track/instrumen terpisah.
- Synth preset GM bersifat representatif. Gunakan synth pluck dengan envelope pendek, saw poly chord dengan low-pass, mono sub/bass, warm pad dan saw lead.
- Automation filter, delay, reverb, stereo widening, riser audio dan sidechain pumping dibuat di DAW; schema MIDI saat ini menyimpan not/velocity dan mixer awal, bukan automation efek.
- ZIP berisi seluruh MIDI terpisah dan dokumentasi; tidak ada file MIDI gabungan.

## Perubahan revisi

Komposisi baru v001; tidak ada bagian lagu sebelumnya yang diubah.

## Kriteria penerimaan dan hasil

- 12 file `.mid` tersedia; satu track/instrumen per file.
- Tempo, meter, PPQN, timeline awal dan panjang total sama.
- `validate`, `generate`, dan `verify` lulus dengan exit code 0 dan `ok: true`.
- Audit musikal: harmony/scale, register, fungsi layer, ritme, dinamika, perkembangan dan ruang frase; bass/arp/lead monofonik, tanpa overlap pitch sama.
- Lokasi output: `output/`, termasuk snapshot `composition.json`, `manifest.json`, `validation.json`, dan `summary.md`.
- Penilaian musikal: `musical-review.md`.
- Playback yang benar-benar dilakukan: belum ada; audio belum didengarkan.
- Status teknis akhir: validate, generate dan verify lulus dengan exit code 0 dan `ok: true`; 12 file, masing-masing satu track, PPQN 960, end tick 614400, 7823 nada total. Tidak ada error atau warning; ekspor cocok dengan snapshot sumber. Receipt terpisah tersedia di `verification.json`.
