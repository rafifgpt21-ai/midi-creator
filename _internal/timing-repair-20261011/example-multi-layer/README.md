# Multi layer - A minor groove

92 BPM | 4/4 | Am | 8 bar

## Memakai MIDI di Cubase

1. Atur tempo/meter project sesuai keterangan di atas dan gunakan Musical Time Base (ikon not).
2. Buat satu instrument track Serum 2 untuk setiap instrumen melodi. Pilih preset sesuai fungsi pada tabel.
3. Impor semua file dari bar 1; untuk File > Import > MIDI File gunakan left locator 1.1.1.0 dan Import to Left Locator. Pertahankan keheningan awal/akhir.
4. Untuk drum, pilih sendiri kit/sample dan cocokkan pitch pada tabel drum di bawah.

Setiap file berisi tepat satu track instrumen dan mencakup seluruh panjang lagu. File baru memakai SMF format 1, tanpa SysEx, teks/marker tambahan, atau Program Change. Preset dipilih di Serum, bukan oleh MIDI.

## Instrumen

| Track | Fungsi | Sound awal | MIDI |
| --- | --- | --- | --- |
| Electric Piano | harmony | Serum 2; pilih preset sesuai fungsi | [keys.mid](MIDI/keys.mid) |
| Finger Bass | bass | Serum 2; pilih preset sesuai fungsi | [bass.mid](MIDI/bass.mid) |
| Piano Lead | melody | Serum 2; pilih preset sesuai fungsi | [lead.mid](MIDI/lead.mid) |
| Kick | rhythm | Kit/sample pilihan Anda | [kick.mid](MIDI/kick.mid) |
| Snare | rhythm | Kit/sample pilihan Anda | [snare.mid](MIDI/snare.mid) |
| Closed Hi-hat | rhythm | Kit/sample pilihan Anda | [hihat.mid](MIDI/hihat.mid) |

## Drum yang disarankan

Pilih kit yang sesuai warna lagu: kick dengan low-end yang menyisakan ruang bass; snare/clap untuk backbeat; hi-hat pendek agar groove tetap jelas. Sesuaikan karakter dan panjang tail terhadap tempo serta kepadatan aransemen. Sample belum dipilih atau disertakan dalam ekspor MIDI ini.

| Track drum | Pitch MIDI |
| --- | --- |
| Kick | 36 |
| Snare | 38 |
| Closed Hi-hat | 42 |

Jika beberapa bagian drum memakai channel 10 dan satu kit bersama, filter CC7/CC10 saat impor lalu atur volume/pan per pad, atau gunakan track sampler terpisah.

## Instrumen di luar Serum

Default semua instrumen melodi menggunakan Serum 2; drum memakai sampler/kit pilihan Anda. Belum ada plugin atau library melodi eksternal yang dikonfigurasikan dalam ekspor ini. Ekspor MIDI saja belum membuktikan adanya preset atau plugin yang berhasil dimuat.

## Timing

Onset memakai grid straight 1/32. Durasi/gate dapat lebih pendek dari grid.
Snap posisi part tidak mengkuantisasi isi nada. Periksa part pada bar 1 dan nada dalam Key Editor Bars+Beats; jangan memindahkan nada pertama layer yang masuk belakangan ke bar 1.

## Bagian lagu

| Bagian | Mulai bar |
| --- | --- |
| Theme A | 1 |
| Theme A repeat | 5 |

## Asumsi

- Tempo konstan; instrumen menggunakan program General MIDI 0-based.

## Keterangan hasil

Verifikasi struktur MIDI lulus. Status sound/preset dan listening perlu dicatat sesuai pemeriksaan yang benar-benar dilakukan. Data teknis dan snapshot komposisi ada di `_internal/`.

Untuk impor Cubase, buka Preferences > MIDI > MIDI File: aktifkan **Import Dropped File as Single Part** dan nonaktifkan **Auto Dissolve Format 0** untuk file lama. Pada project bertempo tetap sesuai lagu, Ignore Master Track Events on Merge mempertahankan tempo project. Keberhasilan drag-and-drop perlu diperiksa di Cubase Anda.

[Panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html)
