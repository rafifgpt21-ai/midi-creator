# One-note grid repro

118 BPM | 4/4 | pusat tonal mengikuti nada | 1 bar

## Memakai MIDI di Cubase

1. Atur tempo dan meter project sesuai keterangan di atas.
2. Buat satu instrument track Serum 2 untuk setiap instrumen melodi. Pilih preset sesuai fungsi pada tabel.
3. Drag file di `MIDI/` ke track yang sesuai, semuanya mulai bar 1. Pertahankan keheningan awal/akhir.
4. Untuk drum, pilih sendiri kit/sample dan cocokkan pitch pada tabel drum di bawah.

Setiap file berisi tepat satu track instrumen dan mencakup seluruh panjang lagu. File baru memakai SMF format 1, tanpa SysEx, teks/marker tambahan, atau Program Change. Preset dipilih di Serum, bukan oleh MIDI.

## Instrumen

| Track | Fungsi | Sound awal | MIDI |
| --- | --- | --- | --- |
| One note | mengikuti aransemen | Kit/sample pilihan Anda | [retro-drums.mid](MIDI/retro-drums.mid) |

## Drum yang disarankan

Pilih kit yang sesuai warna lagu: kick dengan low-end yang menyisakan ruang bass; snare/clap untuk backbeat; hi-hat pendek agar groove tetap jelas. Sesuaikan karakter dan panjang tail terhadap tempo serta kepadatan aransemen. Sample belum dipilih atau disertakan dalam ekspor MIDI ini.

| Track drum | Pitch MIDI |
| --- | --- |
| One note | 42 |

Jika beberapa bagian drum memakai channel 10 dan satu kit bersama, filter CC7/CC10 saat impor lalu atur volume/pan per pad, atau gunakan track sampler terpisah.

## Instrumen di luar Serum

Default semua instrumen melodi menggunakan Serum 2; drum memakai sampler/kit pilihan Anda. Belum ada plugin atau library melodi eksternal yang dikonfigurasikan dalam ekspor ini. Ekspor MIDI saja belum membuktikan adanya preset atau plugin yang berhasil dimuat.

## Keterangan hasil

Verifikasi struktur MIDI lulus. Status sound/preset dan listening perlu dicatat sesuai pemeriksaan yang benar-benar dilakukan. Data teknis dan snapshot komposisi ada di `_internal/`.

Untuk impor Cubase, buka Preferences > MIDI > MIDI File: aktifkan **Import Dropped File as Single Part** dan nonaktifkan **Auto Dissolve Format 0** untuk file lama. Keberhasilan drag-and-drop perlu diperiksa di Cubase Anda.

[Panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html)
