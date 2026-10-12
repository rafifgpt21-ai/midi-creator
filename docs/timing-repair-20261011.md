# Diagnosis dan perbaikan timing — 11 Oktober 2026

File MIDI asli diperiksa menggunakan Mido, tanpa memakai renderer untuk menghitung posisi note-on. Tempo, meter, PPQN dan end-of-track sama antarlayer di setiap komposisi yang diperiksa. Tidak ditemukan drift akibat konversi tempo atau akumulasi delta time. Posisi nada pecahan berasal dari spesifikasi dan dipertahankan oleh renderer; validator lama memeriksa struktur, tetapi belum membedakan grid dan humanization.

## Bukti sebelum perbaikan

| Komposisi / revisi | Kesalahan tempo/alignment | Onset di luar straight 1/32 | Makna |
| --- | --- | --- | --- |
| Afterglow Circuit v002 | 0 | 0 | Lead/arp dan layer lain sudah pada grid file asli |
| Neon Step v002 | 0 | 3335 | Sebagian besar swing 60:40 disengaja, ditambah clap flam dan strum |
| Synthwave Starter v002 | 0 | 0 | Semua onset sudah pada grid file asli |
| Neon di Ujung Malam v001 | 0 | 1613 | Jitter/offset pada bass, chord dan drum |

Glass Arp pada lagu dark synth juga memakai offset tetap **0.125 quarter beat**, setara 1/32 note: secara teknis on-grid 1/32, tetapi bergeser dari pulsa eighth-note yang menjadi target revisi. Night Hook, pad dan keys lagu itu sudah pada grid. Karena itu, jitter kecil tidak dapat menjelaskan seluruh keluhan lead/arp di semua proyek.

[Audit MIDI asli](../_internal/timing-repair-20261011/before.json) mencatat offset aktual per layer. [Repro satu nada](../_internal/timing-repair-20261011/minimized/) menunjukkan onset 1.002 beat yang lolos validator lama tetapi audit grid gagal. Tes regresi dibuat gagal terlebih dahulu, lalu lulus setelah pemeriksaan onset ditambahkan.

## Hasil yang dipakai

- [Neon Step v004](../projects/20261009-neon-step-new-jack-swing/v004/README.md): **11 MIDI core byte-identik** dengan v002, termasuk seluruh drum, slap bass, electric piano, synth stabs dan pad. Lead, muted guitar, brass dan bell disusun ulang onset-nya agar mengikuti anchor core; empat layer memakai transform swing yang sama, 60:40. Pitch, velocity, gate, sound, mixer, tempo dan panjang dipertahankan. Offset clap asli tetap ada karena pengguna menilai core tersebut sudah menyatu dengan baik. [Bukti core](../projects/20261009-neon-step-new-jack-swing/v004/_internal/core-preservation.json), [perubahan](../projects/20261009-neon-step-new-jack-swing/v004/_internal/timing-change.json).
- [Neon di Ujung Malam v002](../projects/20261011-neon-di-ujung-malam/v002/README.md): seluruh delapan layer pada straight 1/16, jitter dihapus, dan offset arp 1/32 dihapus. 2181 onset berubah; tidak ada gate dipangkas. Tujuh preset native disalin byte-identik dari preset yang sudah lulus readback. [Perubahan](../projects/20261011-neon-di-ujung-malam/v002/_internal/source/timing-change.json), [reuse preset](../projects/20261011-neon-di-ujung-malam/v002/_internal/preset-reuse.json).

Neon Step v003 adalah percobaan semua-layer straight sebelum feedback tentang core yang sudah cocok. Versi itu tetap disimpan sebagai alternatif; **v004 adalah rekomendasi**. Proyek yang sudah on-grid tidak diubah tanpa bukti penyebab baru. Revisi asli dipertahankan.

## Pencegahan dan verifikasi

Implementasi CLI/MCP validate, generate, serta studio prepare kini menolak onset off-grid yang tidak dinyatakan disengaja. `timing.mode=strict` memilih grid; `free` mempertahankan swing/humanization yang didokumentasikan. Durasi/gate tidak harus terkuantisasi. Tidak ada koreksi diam-diam saat ekspor. CLI dan server MCP baru memakai implementasi ini; server MCP yang sudah berjalan sebelum perubahan perlu reconnect/restart untuk memuat kode baru. `verify` arsip tetap memeriksa integritas dan melaporkan timing terpisah. [Kontrak timing](composition-guide.md#pemeriksaan-grid-onset) menjelaskan penggunaan.

[Audit setelah perbaikan](../_internal/timing-repair-20261011/after.json) menunjukkan nol kesalahan tempo/alignment. Dark synth memiliki nol onset off-grid; New Jack tetap memiliki offset swing/core yang disengaja. [Pemeriksaan akhir](../_internal/timing-repair-20261011/final-check.json) memeriksa langsung MIDI pada grid 1/16 dark synth, grid swing keempat pelengkap New Jack, kesamaan byte core, preservasi pitch/velocity/gate, checksum preset dan revisi asli, serta tautan README. Contoh single dan multi-layer diekspor/verifikasi; suite menjalankan 43 tes, 42 lulus dan satu integrasi Serum opt-in dilewati. [Log tes](../_internal/timing-repair-20261011/tests.log).

## Batas pemeriksaan Cubase

Bridge Cubase terhubung, tetapi tidak menyediakan impor MIDI atau posisi/edit part/nada. Inisialisasi kontrol desktop gagal dengan `Module not found: @oai/sky`. Tidak ada perubahan live, ekspor dari Cubase, `.cpr`, atau listening yang dilakukan. Penyebab perbedaan antara file yang sudah on-grid dan posisi yang tersimpan setelah drop Cubase masih belum terkonfirmasi.

README baru menyertakan locator bar 1, Musical Time Base, serta opsi impor untuk project bertempo tetap. [Panduan impor](cubase-studio.md#timing-saat-impor-cubase) mengacu pada dokumentasi Steinberg. Single Part/Snap tidak membuktikan isi nada terkuantisasi; pemeriksaan offline dan pengujian impor live merupakan dua hal berbeda.
