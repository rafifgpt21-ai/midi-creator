# Afterglow Circuit - Progressive House

126 BPM | 4/4 | Fm | 160 bar

## Memakai MIDI di Cubase

1. Atur tempo dan meter project sesuai keterangan di atas.
2. Buat satu instrument track Serum 2 untuk setiap instrumen melodi. Pilih preset sesuai fungsi pada tabel.
3. Drag file di `MIDI/` ke track yang sesuai, semuanya mulai bar 1. Pertahankan keheningan awal/akhir.
4. Untuk drum, pilih sendiri kit/sample dan cocokkan pitch pada tabel drum di bawah.

Setiap file berisi tepat satu track instrumen dan mencakup seluruh panjang lagu. File baru memakai SMF format 1, tanpa SysEx, teks/marker tambahan, atau Program Change. Preset dipilih di Serum, bukan oleh MIDI.

## Instrumen

| Track | Fungsi | Sound awal | MIDI |
| --- | --- | --- | --- |
| Electronic kick | Four-on-the-floor foundation | Kit/sample pilihan Anda | [kick.mid](MIDI/kick.mid) |
| Electronic clap | Beats 2 and 4 | Kit/sample pilihan Anda | [clap.mid](MIDI/clap.mid) |
| Snare build and fills | Accelerating build-up rolls | Kit/sample pilihan Anda | [snare-roll.mid](MIDI/snare-roll.mid) |
| Closed hi-hat | Sixteenth pulse | Kit/sample pilihan Anda | [closed-hat.mid](MIDI/closed-hat.mid) |
| Open hi-hat | Offbeat lift | Kit/sample pilihan Anda | [open-hat.mid](MIDI/open-hat.mid) |
| Ride cymbal | Final drop lift | Kit/sample pilihan Anda | [ride.mid](MIDI/ride.mid) |
| Shaker / maracas | Subtle percussion syncopation | Kit/sample pilihan Anda | [shaker.mid](MIDI/shaker.mid) |
| Deep mono synth bass | Offbeat low-end pulse | Serum 2; pilih preset sesuai fungsi | [synth-bass.mid](MIDI/synth-bass.mid) |
| Wide saw poly synth | Main chord hook | Serum 2; pilih preset sesuai fungsi | [poly-synth.mid](MIDI/poly-synth.mid) |
| Plucked synth arpeggio | Repeating evolving motif | Serum 2; pilih preset sesuai fungsi | [pluck-arp.mid](MIDI/pluck-arp.mid) |
| Warm atmospheric pad | Sustained harmonic space | Serum 2; pilih preset sesuai fungsi | [warm-pad.mid](MIDI/warm-pad.mid) |
| Melodic saw lead | Original eight-bar melodic hook | Serum 2; pilih preset sesuai fungsi | [lead-synth.mid](MIDI/lead-synth.mid) |

## Drum yang disarankan

Kick elektronik tebal dengan transient jelas dan tail pendek/sedang untuk four-on-the-floor 126 BPM. Clap lebar untuk backbeat; snare tajam yang tetap bersih saat roll makin rapat. Closed hat pendek untuk sixteenth, open hat lebih terang di offbeat, ride tipis di final drop, serta shaker ringan. Hindari kick yang tail-nya menutup bass offbeat. Sample/kit masih dipilih Anda.

| Track drum | Pitch MIDI |
| --- | --- |
| Electronic kick | 36 |
| Electronic clap | 39 |
| Snare build and fills | 38 |
| Closed hi-hat | 42 |
| Open hi-hat | 46 |
| Ride cymbal | 51 |
| Shaker / maracas | 70 |

Jika beberapa bagian drum memakai channel 10 dan satu kit bersama, filter CC7/CC10 saat impor lalu atur volume/pan per pad, atau gunakan track sampler terpisah.

## Instrumen di luar Serum

Default semua instrumen melodi menggunakan Serum 2; drum memakai sampler/kit pilihan Anda. Belum ada plugin atau library melodi eksternal yang dikonfigurasikan dalam ekspor ini. Ekspor MIDI saja belum membuktikan adanya preset atau plugin yang berhasil dimuat.

## Bagian lagu

| Bagian | Mulai bar |
| --- | --- |
| Intro | 1 |
| Groove | 17 |
| Theme | 33 |
| Breakdown | 49 |
| Build 1 | 65 |
| Drop 1 | 73 |
| Interlude | 97 |
| Build 2 | 113 |
| Final drop | 121 |
| Outro | 145 |

## Asumsi

- Memilih arah melodic/atmospheric progressive house dari referensi artis umum; tidak ada lagu tertentu atau bahan audio/MIDI yang diberikan.
- Komposisi baru orisinal dan instrumental; 126 BPM, F minor, 4/4, 160 bar, sekitar 5:04.76.
- 12 layer lengkap: kick, clap, snare-roll, closed-hat, open-hat, ride, shaker/maracas, synth bass, saw chords, pluck arp, warm pad, saw lead.
- Groove lurus not 1/16 tanpa swing; variasi velocity kecil memakai seed 126160.
- Loop harmoni Fm9 - Dbmaj9 - Abmaj9 - Ebadd9, dua bar per chord; dua bar terakhir kembali ke Fm9.
- Drum mapping GM: kick 36, clap 39, snare 38, closed hat 42, open hat 46, ride 51, shaker/maracas 70.
- Program GM hanya penanda instrumen. Filter automation, sidechain, stereo widening, delay, reverb dan riser audio diatur di DAW; tidak terkandung dalam file MIDI.
- Satu file MIDI per instrumen, timeline global sama; tidak membuat MIDI gabungan.

## Keterangan hasil

Verifikasi struktur MIDI lulus. Status sound/preset dan listening perlu dicatat sesuai pemeriksaan yang benar-benar dilakukan. Data teknis dan snapshot komposisi ada di `_internal/`.

Untuk impor Cubase, buka Preferences > MIDI > MIDI File: aktifkan **Import Dropped File as Single Part** dan nonaktifkan **Auto Dissolve Format 0** untuk file lama. Keberhasilan drag-and-drop perlu diperiksa di Cubase Anda.

[Panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html)

## Sound untuk revisi ini

Revisi ini memperbarui struktur folder dan file impor; nada/velocity/timing/mixer tetap sama seperti v001. Preset Serum baru belum dibuat untuk lagu arsip ini. Gunakan Serum 2 dengan karakter sesuai nama/fungsi track, atau sound sebelumnya.
