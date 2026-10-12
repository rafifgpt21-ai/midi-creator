# Brief komposisi

- Proyek: Neon Step — New Jack Swing
- Revisi: v001
- Revisi asal (jika ada): tidak ada; komposisi baru.
- Tanggal: 2026-10-09

## Permintaan asli

> buatkan lagu untuk genre new jack swing (semua instrumenya)

## Keputusan musik

- Gaya / mood: new jack swing instrumental, danceable, cerah dengan harmoni R&B minor dan synth era 1990-an.
- Tempo (quarter-note BPM): 108.
- Meter: 4/4.
- Key / scale / pusat tonal: F# minor; E# digunakan pada C#7b9.
- Jumlah bar / panjang: 96 bar, 384 beat, sekitar 3:33.333; PPQN 960.
- Bentuk dan bagian: intro 1–8, verse 1 9–24, pre-chorus 25–32, chorus 1 33–48, verse 2 49–64, bridge 65–72, final chorus 73–88, outro 89–96.
- Progresi / pendekatan harmoni: verse F#m9–F#m9–Bm9–C#7b9–F#m9–Amaj9–Dmaj9–C#7b9; chorus F#m9–Bm9–E13–Amaj9–Dmaj9–Bm9–C#7sus–C#7b9. Voicing tanpa root pada keys memberi ruang untuk bass.
- Groove / densitas / dinamika: swing not 1/16 60:40; kick sinkopasi, snare beat 2/4, ghost note ringan, clap berlapis di bagian penuh, bass staccato dan octave pop, gitar muted, motif synth, respons brass, half-time di awal bridge, akhir tonic dengan ruang tail.
- DAW / plugin / drum mapping: DAW tidak ditentukan; General MIDI/GM2 sebagai mapping awal (shaker pitch 82 mengikuti ekstensi GM2). Sound target kick drum machine, gated electronic snare, slap bass, Rhodes, poly synth, muted funk guitar, synth brass, saw lead, warm string pad, FM bell.

| Layer ID | Instrumen / sound target | Fungsi | Program GM 0-based / pitch drum |
| --- | --- | --- | --- |
| kick | Kick drum machine | Fondasi groove | 36 |
| snare | Gated snare | Backbeat dan ghost notes | 38 |
| clap | Hand clap | Lapisan backbeat | 39 |
| hihat | Closed/open hi-hat | Pulse swing | 42 / 46 |
| shaker | Shaker | Gerak percussion | 82 |
| tambourine | Tambourine | Lift chorus | 54 |
| toms | Electronic toms | Fill transisi | 50 / 47 / 45 |
| slap-bass | Slap bass | Bassline sinkopasi | 36 |
| electric-piano | Rhodes / electric piano | Harmoni chord extended | 4 |
| synth-stabs | Poly synth | Chord stabs | 90 |
| muted-guitar | Muted electric guitar | Scratch chord funk | 28 |
| synth-brass | Synth brass | Respons melodi / aksen | 62 |
| lead-synth | Saw synth lead | Hook utama | 81 |
| string-pad | Warm string pad | Sustain dan transisi | 50 |
| bell-keys | FM bell keys | Ornamen frase | 10 |

## Asumsi dan referensi

- Semua instrumen ditafsirkan sebagai aransemen band lengkap, dengan tujuh bagian drum/percussion dan delapan instrumen bernada.
- Komposisi orisinal tanpa referensi atau meniru lagu tertentu.
- Instrumental; melodi utama dimainkan synth karena vokal/lirik tidak diminta.
- Tempo, key, durasi, dan struktur dipilih agent karena belum ditentukan pengguna.
- Seed velocity: 108960; script reproduksi: `build_composition.py`. Timing swing eksplisit, tidak ada jitter onset acak.
- Semua MIDI per-layer type 0, satu track, timeline global 0–368640 tick; diam sebelum instrumen masuk dipertahankan.
- Drum channel 10, instrumen bernada channel 1 pada file masing-masing. Tiap instrumen bernada mempunyai satu program tetap.
- Preset dan efek (termasuk gated snare) dipilih di DAW; MIDI menyimpan performa, bukan audio atau efek.
- Arsip ZIP disediakan untuk memudahkan pengambilan semua MIDI terpisah. Tidak membuat MIDI gabungan.

## Perubahan revisi

Komposisi baru v001; tidak ada revisi asal.

## Kriteria penerimaan dan hasil

- 15 file `.mid` tersedia; setiap file mempunyai tepat satu track/instrumen.
- Tempo, meter, resolusi, titik awal, dan panjang total seluruh layer sama.
- `validate`, `generate`, dan `verify` wajib exit code 0 dan `ok: true` sebelum penyerahan.
- Harmoni, register, groove, dinamika, perkembangan bagian, ruang frase, serta monofoni bass/lead dinilai; hasil event audit berada di `musical-review.md`.
- Lokasi output: `output/`; snapshot spec, `manifest.json`, `validation.json`, dan `summary.md` berada di output.
- Playback yang benar-benar dilakukan: belum ada; audio belum didengarkan.
- Status teknis akhir: validate, generate, dan verify lulus dengan exit code 0; `ok: true`, tanpa error atau warning. Seluruh 15 file type 0 mempunyai tepat satu track, PPQN 960 dan end tick 368640; 6541 nada secara total. Snapshot komposisi cocok dengan ekspor.
