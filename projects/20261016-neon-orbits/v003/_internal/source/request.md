# Brief komposisi — revisi koherensi

- Proyek: Neon Orbits
- Revisi: v003; asal: v002
- Tanggal: 2026-10-16

## Permintaan asli dan umpan balik

"buatkan musik retro synthwave edm, dengan beat 4 on the floor beat dan menggunakan polyrithm dan polymeter ala deadmau5, dengan mode minor harmonic, gunakan semua skill yang terkait dengan ini, terutama /skill:mc dan skill di dalam repo"

"koherensi antar intrument tidak baik, sepertinya penggunaan polymeter/polyrthm tidak terdengar harmonis antar instrumen, terdengar kacau dan tidak terdengar bagus"

## Diagnosis dan keputusan musik

Inspeksi simbolik v002: pola 7/8 dan 3:2 ditumpuk dengan lead sinkopatif pada register berdekatan; pad memiliki cluster F#–G, B–C atau B–C pada chord minor/add9 dan major7. C menjadi b9 berulang pada B7b9. Fragmen lead B–D#–F# tidak selalu mengikuti chord build; glass keys pada bar 95 melewati pergantian chord satu bar. Release pad 1.45 detik bisa melewati pergantian harmoni. Ini diagnosis dari partitur/preset, bukan klaim telah mendengar audio pengguna.

Prioritas: satu foreground, akor mudah dikenali, motif konsisten, pola silang sebagai jawaban. Pertahankan 124 BPM, 4/4, E harmonic minor, 164 bar, 960 PPQN dan batas semua bagian. Tetap strict/no swing, grid 1/48 untuk eighths, quarter/eighth lead dan triplet 2/3 beat.

Harmoni utama Em–C–Am–B, dua bar per chord. Hilangkan extension rapat dan rute diminished tambahan. Bass hanya root offbeat. Pad tiga suara dengan voice leading pendek. Lead memakai chord tones; C–D# sebagai augmented second tidak dipaksakan menjadi motif tetap. D# dominan bergerak ke E pada kembali ke tonik.

7/8: lima serangan dan dua jeda dalam tujuh slot eighth, aksen 2+2+3. Fase tetap berjalan melintasi garis bar dan pergantian chord; pitch mengikuti chord. Jendela jawaban tujuh bar memuat delapan siklus utuh. 3:2 hanya bar 69–72 dan 133–136, satu pitch stabil per chord; lead, arp, brass diam. Lead, arp dan pulse tidak bermain bersamaan. Brass mengisi jendela kosong. Glass keys sendiri di foreground breakdown.

Kurangi hat tambahan, tom cukup dua serangan per fill. Pertahankan kick, snare/clap dan crash tepat dari v002. Sample tetap pilihan pengguna; seluruh trigger drum MIDI 60, channel 10, satu Sampler Track per file.

## Sound dan asumsi

Tujuh layer Serum 2, enam drum; nama file sama agar pergantian versi mudah. Pertahankan arsitektur retro analog/DCO/VCO, osilator, filter, routing dan detune. Kurangi release pad, pluck, pulse, lead, glass keys; hilangkan delay pluck/lead/keys, kecilkan wet reverb. Bass dan brass tidak diubah secara semantik. Semua preset dibangun ulang di bank v003 baru, tidak menimpa bank lama. Tidak ada humanization acak: seed tidak diperlukan.

`compose.py` memakai snapshot v002 dan spesifikasi preset asli yang dibekukan di source ini. `composition.json` hasil adalah source of truth. Tidak ada referensi audio tambahan; referensi artis tetap arahan konseptual.

## Kriteria penerimaan

- MIDI validate/generate/verify sukses; 13 file format 1, satu track, total panjang sama.
- Semua pitch synth anggota E harmonic minor dan chord yang berlangsung, tanpa nada melewati pergantian harmoni.
- Tidak ada foreground lead/arp/pulse/brass bertumpuk, termasuk budget release amp terprogram; glass keys hanya intro/breakdown/coda.
- Tidak ada interval semiton vertikal pada note gate synth; pad minimum tiga semiton antarsuara.
- 7/8 tidak di-reset setiap bar; 3:2 tepat 640 tick dan tetap bersandar pada kick quarter-note 960 tick.
- Kick, snare/clap, crash tidak berubah; density melodic berkurang dan register tercatat.
- Tujuh native preset dibangun lewat MCP, readback, dependency dan wire-type scan; tautan README valid.
- Preset loading di plugin, live import Cubase, render, dan actual listening dinyatakan terpisah. Belum dapat menilai sukses bunyi tanpa audition; hasil offline tidak menggantikan pendengaran pengguna.

Output: `projects/20261016-neon-orbits/v003/`. v002 dipertahankan utuh.
