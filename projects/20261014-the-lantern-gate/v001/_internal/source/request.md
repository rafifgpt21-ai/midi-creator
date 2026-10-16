# Brief komposisi

- Proyek: The Lantern Gate / 20261014-the-lantern-gate
- Revisi: v001
- Revisi asal: komposisi baru
- Tanggal: 2026-10-14

## Permintaan asli

“buatkan musik orchestra yang terdengar dinamic dan natural; gunakan dorian mode untuk musiknya, vibe nya fantasy di awal dan di akhir terdengar epic; saya menggunakan BBC Symphony Orchestra sebagai VST, kamu tinggal buat midi per track nya saja.”

Pengguna memberi kategori Strings, Woodwinds, Brass, Percussion & Keyboards serta contoh instrumen/artikulasi. Klarifikasi: **versi gratis (Discover)**. “jika ingin menggunakan mode berbeda dari instrumen yang sama, buat track khusus untuk mode berbeda.” Instruksi tambahan: “gunakan skill yang tersedia dan yang cocok.”

## Keputusan musik

- Gaya/mood: fantasy orkestra, kemudian heroik, dengan sanctuary yang tenang di tengah.
- Tempo quarter-note: 108 BPM. Meter: 6/8, dotted-quarter 72.
- Pusat tonal: D Dorian (D E F G A B C). Final D minor.
- Panjang: 96 bar, sekitar 160 detik; 94 bar musik dan 2 bar release.
- Bentuk: intro 12 / tema 16 / quest 16 / sanctuary 10 / ascent 16 / epic recap 16 / coda 8 / release 2.
- Harmoni: chord modal, inversion dekat dan pedal D; ganti harmoni dua/empat bar maupun per bar. B natural menegaskan sixth Dorian.
- Natural: rests/breaths, aksen, variasi velocity/gate, smooth CC1/CC11, handoff instrumen, rentang konser yang wajar. Tanpa random onset jitter/swing, sesuai kontrak timing.
- Plugin: BBC Symphony Orchestra Discover, semua 35 instrumen-artikulasi memakai instance terpisah; lihat bbcso-bindings.json dan README.
- Drum: Discover Untuned Percussion; numeric 36 Bass Drum, 40 Snare, 41 Sus Cymbal Hit, 43 Sus Cymbal Roll, 59 Piatti, 52 Triangle. Timpani Hits bertonal 38/45 pada patch sendiri. Mapping merujuk manual; middle C lokal = C4/MIDI60; live trigger belum diuji.

## Asumsi dan referensi

Durasi/tempo/key/meter dipilih agent. Harp dan Celeste tersedia pada Discover menurut manual. Tidak memakai Legato, Marcato, Col Legno atau solo winds Core/Professional. Long digunakan untuk garis connected tanpa mengklaim sampled legato. Long+short seksi strings dapat berjalan sebagai fungsi divisi; README menjelaskan dampak full-section samples.

Skill: mc-workflow, mc-development, mc-melody, mc-harmony, mc-orchestration, mc-arrangement-arch, mc-ai-tell-audit. Internal arrangement-plan.json mencatat motif, perkembangan, roster, arc serta alasan pengecualian chromatic chords/timing offsets. composition.json tetap sumber nada/CC yang otoritatif.

Seed 20261014; build_composition.py mereproduksi nada, velocity, gate dan CC. Gate retrigger harp diselesaikan sebelum ekspor, disimpan di gate-adjustments.json. Generator ditambah field CC1/CC11 untuk memenuhi dinamika Long; schema, compiler, render, readback, dokumentasi serta tes diubah bersama. 46 tes: 45 passed, 1 opt-in Serum skipped; single/multi-layer examples covered.

Sumber primer: manual Discover Appendix B/C, artikel Spitfire tentang perbedaan edisi dan map Untuned Percussion. Tautan ada di README. Tidak ada karya musik atau audio pengguna yang ditiru.

## Perubahan revisi

Komposisi baru, belum ada revisi asal; proyek pengguna lain dan revisi lama dipertahankan.

## Kriteria penerimaan dan hasil

- 35 MIDI dengan satu track format 1/instrumen-artikulasi per file; tanpa combined atau preset/audio sesuai request.
- 108 BPM, 6/8, 960 PPQN, EOT tick 276480 sama; semua posisi awal global tetap bar 1.
- Validate, generate, verify PASS; on_grid true.
- Readback 1.966 nada, 7.024 CC sesuai komposisi; tidak ada note stuck/overlap pitch sama.
- Seluruh nada bertonal dalam D Dorian; final D minor; retreat tengah dan epic final diperiksa pada data komposisi.
- Output: v001/README.md, v001/MIDI/*.mid.
- Pemuatan patch, live Cubase import, render dan actual listening: belum dilakukan; tidak diklaim.
