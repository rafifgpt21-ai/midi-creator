# Panduan timing MIDI: on-grid tanpa swing

Gunakan panduan ini saat membuat lagu, mengadaptasi referensi, atau merevisi ritme MIDI. Aturan default berlaku pada semua layer, termasuk melodi, arp, chord, bass, drum, dan percussion. Field serta perhitungan tick mengikuti [kontrak komposisi](composition-guide.md#pemeriksaan-grid-onset) dan schema di `src/midi_creator/composition.schema.json`.

## Default dan pengecualian

- Tulis semua onset pada satu grid bersama dengan `timing.mode: "strict"`. Gunakan subdivision yang diperlukan pola musik; default generator adalah 1/32. Pilih grid sebelum menyusun layer, bukan memperhalus grid hanya agar offset yang tidak direncanakan lolos validasi.
- Gunakan subdivisi yang rata, tanpa swing sama sekali. Swing hanya diterapkan jika pengguna memintanya; genre, mood, atau referensi yang memiliki swing tidak otomatis menjadi izin. Untuk referensi tanpa permintaan swing, adaptasikan ritmenya ke grid tanpa swing dan catat keputusan itu.
- Humanization default melalui velocity dan gate/durasi. Pertahankan onset pada grid; strum, flam, jitter, atau offset timing lain memerlukan permintaan eksplisit pengguna.
- Dotted note, sinkopasi, jeda, tie yang ditulis sebagai durasi panjang, dan triplet pada grid yang sesuai tetap diizinkan jika dibutuhkan musik. On-grid mengatur posisi note-on, bukan mewajibkan setiap nada berdurasi sama.
- Meter selain 4/4 tetap diizinkan sesuai permintaan atau kebutuhan musik. Pilih meter berdasarkan frasa dan pengelompokan aksen, lalu catat asumsi bila pengguna belum menentukannya.

## Dotted note dan meter

Dotted note bernilai 1,5 kali durasi dasar. Dalam quarter-note beats yang dipakai spesifikasi:

| Nilai nada | `duration` nominal |
| --- | ---: |
| Dotted half note | 3 |
| Dotted quarter note | 1.5 |
| Dotted eighth note | 0.75 |
| Dotted sixteenth note | 0.375 |

Gunakan grid yang menampung onset berikutnya; dotted sixteenth berulang, misalnya, memerlukan grid 1/32 atau lebih rapat yang kompatibel. Gate boleh memperpendek bunyi untuk artikulasi tanpa menggeser onset berikutnya. Pola dotted yang memang ditulis sebagai ritme berbeda dari swing yang mengubah pembagian pasangan subdivisi rata menjadi panjang–pendek.

`time_signature` tidak harus `[4, 4]`. Satu bar = `numerator × 4 / denominator` quarter-note beats: 3/4 = 3, 6/8 = 3, 7/8 = 3.5, dan 5/4 = 5. Semua layer memakai meter dan panjang global yang sama. Meter 6/8 dapat memakai aksen 3+3 eighth notes dengan setiap eighth tetap berjarak 0.5 beat; pengelompokan ini bukan swing. Triplet rata juga bukan swing; pilih division triplet yang didukung schema bila diperlukan. Kontrak v1 memakai satu meter konstan sepanjang komposisi.

Contoh timing eksplisit untuk pola straight 1/16:

```json
"timing": {"mode": "strict", "grid_division": 16}
```

Jika pengguna meminta swing, gunakan `timing.mode: "free"` sesuai kontrak komposisi. Catat permintaan, rasio swing, subdivision, anchor bersama, layer yang terpengaruh, dan toleransi dalam `request.md` serta README. Terapkan transform yang konsisten pada layer yang berbagi pulsa. Mode free juga hanya dipakai untuk offset timing lain jika diminta eksplisit.

## Pemeriksaan sebelum penyerahan

1. Catat grid, meter, penggunaan dotted note/triplet bila relevan, serta asumsi dalam spesifikasi dan README. Untuk default, nyatakan **on-grid, tanpa swing**.
2. Periksa semua onset absolut, termasuk hasil `clip.start + indeks_pengulangan × every + note.start`. Nilai lead/arp bersama bass, drum, dan chord untuk memastikan satu pulsa yang sesuai brief.
3. Jalankan `validate`, `generate`, lalu `verify` sesuai [alur agent](agent-workflow.md). Untuk default, semua layer harus lolos mode strict dan laporan timing harus menunjukkan `on_grid: true` tanpa offset.
4. Audit pola secara musikal: grid yang sangat rapat dapat menampung swing sehingga `on_grid: true` saja tidak membuktikan tanpa swing. Pastikan subdivisi yang dimaksud rata tidak diberi transform swing atau offset humanization. Dotted note dan pengelompokan meter yang memang direncanakan tetap sah.

Selesai jika pemeriksaan teknis lulus, ritme memenuhi aturan default atau pengecualian yang diminta pengguna, dan README menjelaskan timing secara akurat. Verifikasi MIDI tidak membuktikan playback atau listening; laporkan keduanya terpisah.
