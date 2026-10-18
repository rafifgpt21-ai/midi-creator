# Brief komposisi

- Proyek: Neon Orbits
- Revisi: v002, hasil audit pra-penyerahan; berasal dari v001 dalam proyek baru ini.
- Tanggal: 2026-10-16

## Permintaan asli

> buatkan musik retro synthwave edm, dengan beat 4 on the floor beat dan menggunakan polyrithm dan polymeter ala deadmau5, dengan mode minor harmonic, gunakan semua skill yang terkait dengan ini, terutama /skill:mc dan skill di dalam repo

## Keputusan musik

- Gaya: retro synthwave dengan bentuk progressive EDM instrumental; kick 4/4, sequence yang berkembang melalui penambahan/pengurangan layer.
- Tempo: 124 quarter-note BPM. Meter: 4/4 global. Durasi: 164 bar / 317.419 detik, termasuk release.
- Tangga nada: E harmonic minor, E F# G A B C D#. Tidak memakai D natural atau tangga nada lain.
- Harmoni utama: Emadd9 - Cmaj7 - Amadd9 - B7b9, umumnya dua bar per chord. Breakdown memakai Cmaj7 - Amadd9 - F#m7b5 - B7b9, kemudian Emadd9 - Cmaj7 - Amadd9 - D#dim7 - B7b9. Coda Em.
- Bentuk: intro 1-16; groove 17-32; build 33-48; drop 49-80; breakdown 81-96; rebuild 97-112; drop kedua 113-144; outro 145-160; coda/release 161-164.
- Polimeter: tujuh eighth notes/7/8, aksen 2+2+3, siklus 3.5 quarter beats terhadap bar 4 quarter beats. Pertemuan kembali setiap 28 beats = tujuh bar utama = delapan siklus 7/8. Pola tidak diulang dari awal pada setiap bar; reset hanya di awal span yang tertulis di script.
- Poliritme: tiga onset merata per dua quarter beats, berjarak 2/3 beat, melawan dua kick quarter-note. Aktif bar 57-72 dan 121-136.
- Timing strict, grid 1/48 whole note = 1/12 quarter beat, 960 PPQN. Grid dipilih sejak desain untuk menampung 16th lurus dan triplet. Tidak ada swing/jitter onset.
- Ekspresi melalui velocity, gate, CC1 cutoff, keheningan, serta perubahan lapisan. Bukan klaim sidechain compressor yang sudah terpasang dalam DAW.
- Synth memakai Serum 2. Drum per layer memakai root Cubase C3, angka MIDI 60, channel 10; sample belum dipilih.

| Layer | Target / fungsi | Program hint atau pitch |
| --- | --- | --- |
| mono-bass | Bass saw/triangle, mono, menjawab kick pada offbeat | 38 |
| juno-pad | Pad DCO-family, sumber PWM-table tunggal dan chorus | 89 |
| phase-seven-pluck | Pluck saw berfilter, siklus 7/8 | 81 |
| three-two-pulse | Pulse square/triangle, poliritme 3:2 | 80 |
| analog-lead | Lead saw/pulse dua VCO, motif utama | 81 |
| poly-brass | Brass synth polifonik, jawaban di sela frase | 62 |
| glass-keys | Synth digital kaca untuk breakdown, bukan piano akustik | 98 |
| kick | Four-on-the-floor | 60 |
| snare-clap | Backbeat 2 dan 4 | 60 |
| closed-hat | Eighth/16th lurus | 60 |
| open-hat | Offbeat, bergantian dengan closed hat | 60 |
| synth-tom | Fill pendek | 60 |
| crash | Aksen bagian | 60 |

## Asumsi dan referensi

Nama lagu, key, tempo, durasi, serta jumlah layer dipilih agent. Rujukan deadmau5 ditafsirkan sebagai arahan sequence berlapis dan perkembangan filter; tidak ada rekaman referensi yang diberikan atau ditranskripsi. Materi nada dibuat orisinal. Tidak ada vokal, combined MIDI, pilihan sample, ekspor audio, atau proyek .cpr yang diminta.

Skill terkait dipilih lewat mc-workflow; daftar dan pembagian tugas tersimpan dalam skill-usage.json. ARR-SPEC mengikuti template MC; composition.json menjadi sumber performa yang diekspor. Mode harmonic minor tidak tersedia dalam enum ARR-SPEC; mode minor disertai koleksi nada eksplisit. Pedoman MC yang menganjurkan onset tidak terkuantisasi atau chord di luar tangga nada dikecualikan sesuai AGENTS.md dan permintaan pengguna.

Seed tetap 20261016, hanya untuk variasi velocity hat. Script compose.py dapat membangun ulang source, harmoni, dan preset specs. Referensi wavetable factory diperiksa secara numerik; library pabrik Serum diperlukan. Tidak ada custom sample/wavetable/IR.

## Perubahan revisi

v001 adalah materi baru. Saat validasi sumber, pickup bass 3.875 beat ditemukan berada di luar grid 1/48; pickup diperbaiki ke beat 3.75 sebelum ekspor v001. Audit berikutnya menemukan delapan overlap bass sebelum pickup serta lompatan oktaf lead pada bar 139 dan 141. Source diperbaiki dan diekspor ulang ke folder baru v002: gate bass dipendekkan 0.27 menjadi 0.20 beat sebelum pickup, dan pitch frase lead diperbaiki tanpa menggeser onset/velocity. Sebelas layer lain, seluruh controller, tempo/meter, serta preset dipertahankan. Tidak ada MIDI hasil ekspor yang diedit langsung.

## Kriteria penerimaan dan hasil

- 13 MIDI, satu instrumen dan satu track SMF1 per file; semuanya mulai timeline global bar 1 dan berakhir di 164 bar.
- 7 preset native .SerumPreset yang namanya cocok dengan layer synth, dibangun dengan serum-mcp dan diperiksa readback serta tipe wire.
- validate, generate, verify harus berhasil. Audit tambahan memastikan semua nada mengikuti harmonic minor, siklus 7/8 dan 3:2 benar, dan drum terpisah selalu pitch 60.
- README menautkan setiap MIDI/preset, menjelaskan impor Cubase, mapping dan karakter drum, serta membedakan struktur, plugin loading, render, dan listening.
- Status akhir dan hasil terukur dicatat di musical-audit.json dan receipt bank dalam _internal revisi.
- Playback, pemuatan preset native di plugin, impor Cubase live, dan listening tidak dilakukan; jangan dianggap teruji dari hasil offline.

Hasil akhir: v002 validate/generate/verify lulus; 13 MIDI, 7 preset, 4.182 nada, 79 pemeriksaan khusus lulus. Tidak ada nada di luar koleksi harmonic minor atau onset di luar grid. Semua file berakhir di 629.760 tick. Source final dipindahkan ke v002/_internal/source/; v001 dipertahankan di _internal/previous-revisions/v001/.
