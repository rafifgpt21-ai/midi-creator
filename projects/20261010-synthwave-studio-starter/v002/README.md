# Neon Workshop - Serum Synthwave Starter

110 BPM | 4/4 | Am | 16 bar

## Memakai MIDI di Cubase

1. Atur tempo dan meter project sesuai keterangan di atas.
2. Buat satu instrument track Serum 2 untuk setiap instrumen melodi. Pilih preset sesuai fungsi pada tabel.
3. Drag file di `MIDI/` ke track yang sesuai, semuanya mulai bar 1. Pertahankan keheningan awal/akhir.
4. Untuk drum, pilih sendiri kit/sample dan cocokkan pitch pada tabel drum di bawah.

Setiap file berisi tepat satu track instrumen dan mencakup seluruh panjang lagu. File baru memakai SMF format 1, tanpa SysEx, teks/marker tambahan, atau Program Change. Preset dipilih di Serum, bukan oleh MIDI.

## Instrumen

| Track | Fungsi | Sound awal | MIDI |
| --- | --- | --- | --- |
| Serum - Warm Neon Pad | harmony | Serum 2; pilih preset sesuai fungsi | [pad.mid](MIDI/pad.mid) |
| Serum - Night Drive Bass | bass | Serum 2; pilih preset sesuai fungsi | [bass.mid](MIDI/bass.mid) |
| Serum - Skyline Arp | arpeggio | Serum 2; pilih preset sesuai fungsi | [arp.mid](MIDI/arp.mid) |
| Serum - Midnight Lead | melody | Serum 2; pilih preset sesuai fungsi | [lead.mid](MIDI/lead.mid) |
| Serum - Retro Brass | synth brass | Serum 2; pilih preset sesuai fungsi | [brass.mid](MIDI/brass.mid) |
| Serum - Glass Keys | keys accents | Serum 2; pilih preset sesuai fungsi | [keys.mid](MIDI/keys.mid) |
| Drums - Kick | percussion | Kit/sample pilihan Anda | [kick.mid](MIDI/kick.mid) |
| Drums - Snare | percussion | Kit/sample pilihan Anda | [snare.mid](MIDI/snare.mid) |
| Drums - Closed Hat | percussion | Kit/sample pilihan Anda | [closed-hat.mid](MIDI/closed-hat.mid) |
| Drums - Open Hat | percussion | Kit/sample pilihan Anda | [open-hat.mid](MIDI/open-hat.mid) |

## Drum yang disarankan

Kick drum-machine dengan low-end padat dan tail pendek, snare elektronik dengan body sedang yang dapat diberi gated reverb, closed hat kering, dan open hat terang dengan decay terkendali untuk eighth-note groove 110 BPM. Kit lama ikut disalin sebagai pilihan yang sudah ada; Anda boleh mengganti sample pada pitch yang sama. Kit lama menggunakan 36 kick, 38 snare, 42 closed hat, dan 46 open hat.

| Track drum | Pitch MIDI |
| --- | --- |
| Drums - Kick | 36 |
| Drums - Snare | 38 |
| Drums - Closed Hat | 42 |
| Drums - Open Hat | 46 |

Jika beberapa bagian drum memakai channel 10 dan satu kit bersama, filter CC7/CC10 saat impor lalu atur volume/pan per pad, atau gunakan track sampler terpisah.

## Instrumen di luar Serum

Default semua instrumen melodi menggunakan Serum 2; drum memakai sampler/kit pilihan Anda. Belum ada plugin atau library melodi eksternal yang dikonfigurasikan dalam ekspor ini. Ekspor MIDI saja belum membuktikan adanya preset atau plugin yang berhasil dimuat.

## Bagian lagu

| Bagian | Mulai bar |
| --- | --- |
| Atmosphere | 1 |
| Bass and drums | 3 |
| Arp | 5 |
| Lead and brass | 9 |
| Release | 15.5 |

## Asumsi

- 110 BPM and A minor are starting values, not a requested finished song.
- Dry synth patches leave room for Cubase chorus, delay, and reverb.
- The final bar provides release space; no combined MIDI was requested.

## Keterangan hasil

Verifikasi struktur MIDI lulus. Status sound/preset dan listening perlu dicatat sesuai pemeriksaan yang benar-benar dilakukan. Data teknis dan snapshot komposisi ada di `_internal/`.

Untuk impor Cubase, buka Preferences > MIDI > MIDI File: aktifkan **Import Dropped File as Single Part** dan nonaktifkan **Auto Dissolve Format 0** untuk file lama. Keberhasilan drag-and-drop perlu diperiksa di Cubase Anda.

[Panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html)

## Preset dan audio yang ikut paket

Preset VST3 dan stem dari starter v001 dipertahankan tanpa perubahan sound. Di MediaBay Cubase, browse `Presets/` lalu buat instrument track dari `.vstpreset`. Import MIDI yang namanya sama di bar 1. Untuk native Serum MCP lihat proyek demo terpisah.

| Track | Preset | Audio |
| --- | --- | --- |
| pad | [VST3](Presets/pad.vstpreset) | [stem](Audio/pad.wav) |
| bass | [VST3](Presets/bass.vstpreset) | [stem](Audio/bass.wav) |
| arp | [VST3](Presets/arp.vstpreset) | [stem](Audio/arp.wav) |
| lead | [VST3](Presets/lead.vstpreset) | [stem](Audio/lead.wav) |
| brass | [VST3](Presets/brass.vstpreset) | [stem](Audio/brass.wav) |
| keys | [VST3](Presets/keys.vstpreset) | [stem](Audio/keys.wav) |
| kick | Drums/ | [stem](Audio/kick.wav) |
| snare | Drums/ | [stem](Audio/snare.wav) |
| closed-hat | Drums/ | [stem](Audio/closed-hat.wav) |
| open-hat | Drums/ | [stem](Audio/open-hat.wav) |

Gunakan audio ATAU MIDI untuk setiap part agar tidak terdengar ganda. Stem lama sudah diverifikasi sejajar dan tidak dirender ulang dalam revisi ini. Drums/kit.sfz dapat dibuka di sampler SFZ; untuk Groove Agent SE muat WAV ke pad 36/38/42/46. Audio belum didengarkan.
