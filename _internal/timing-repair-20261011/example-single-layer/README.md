# Single layer - piano motif

100 BPM | 4/4 | C | 4 bar

## Memakai MIDI di Cubase

1. Atur tempo/meter project sesuai keterangan di atas dan gunakan Musical Time Base (ikon not).
2. Buat satu instrument track Serum 2 untuk setiap instrumen melodi. Pilih preset sesuai fungsi pada tabel.
3. Impor semua file dari bar 1; untuk File > Import > MIDI File gunakan left locator 1.1.1.0 dan Import to Left Locator. Pertahankan keheningan awal/akhir.
4. Untuk drum, pilih sendiri kit/sample dan cocokkan pitch pada tabel drum di bawah.

Setiap file berisi tepat satu track instrumen dan mencakup seluruh panjang lagu. File baru memakai SMF format 1, tanpa SysEx, teks/marker tambahan, atau Program Change. Preset dipilih di Serum, bukan oleh MIDI.

## Instrumen

| Track | Fungsi | Sound awal | MIDI |
| --- | --- | --- | --- |
| Piano | melody | Serum 2; pilih preset sesuai fungsi | [piano.mid](MIDI/piano.mid) |

## Drum yang disarankan

Pilih kit yang sesuai warna lagu: kick dengan low-end yang menyisakan ruang bass; snare/clap untuk backbeat; hi-hat pendek agar groove tetap jelas. Sesuaikan karakter dan panjang tail terhadap tempo serta kepadatan aransemen. Sample belum dipilih atau disertakan dalam ekspor MIDI ini.

| Track drum | Pitch MIDI |
| --- | --- |
| Belum ada layer drum dalam aransemen ini | — |

Jika beberapa bagian drum memakai channel 10 dan satu kit bersama, filter CC7/CC10 saat impor lalu atur volume/pan per pad, atau gunakan track sampler terpisah.

## Instrumen di luar Serum

Default semua instrumen melodi menggunakan Serum 2; drum memakai sampler/kit pilihan Anda. Belum ada plugin atau library melodi eksternal yang dikonfigurasikan dalam ekspor ini. Ekspor MIDI saja belum membuktikan adanya preset atau plugin yang berhasil dimuat.

## Timing

Onset memakai grid straight 1/32. Durasi/gate dapat lebih pendek dari grid.
Snap posisi part tidak mengkuantisasi isi nada. Periksa part pada bar 1 dan nada dalam Key Editor Bars+Beats; jangan memindahkan nada pertama layer yang masuk belakangan ke bar 1.

## Bagian lagu

| Bagian | Mulai bar |
| --- | --- |
| Motif A | 1 |
| Motif A repeat | 3 |

## Asumsi

- Satu beat adalah quarter note; C4 = MIDI 60.

## Keterangan hasil

Verifikasi struktur MIDI lulus. Status sound/preset dan listening perlu dicatat sesuai pemeriksaan yang benar-benar dilakukan. Data teknis dan snapshot komposisi ada di `_internal/`.

Untuk impor Cubase, buka Preferences > MIDI > MIDI File: aktifkan **Import Dropped File as Single Part** dan nonaktifkan **Auto Dissolve Format 0** untuk file lama. Pada project bertempo tetap sesuai lagu, Ignore Master Track Events on Merge mempertahankan tempo project. Keberhasilan drag-and-drop perlu diperiksa di Cubase Anda.

[Panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html)
