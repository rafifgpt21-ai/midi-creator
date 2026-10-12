# Neon Step - New Jack Swing

## Revisi groove v004

**Bass, seluruh drum, electric piano, synth stabs dan string pad dipertahankan byte-identik dengan v002.** Swing 1/16 **60:40** tetap digunakan karena core tersebut sudah cocok menurut Anda. Lead mengikuti serangan piano pada chorus dan piano/bass pada verse; muted guitar mengikuti accent kick/bass/chord dan tidak lagi memakai strum delay. Brass dan bell menjawab pada akhir frase yang mengikuti pulsa core. Nada, velocity, durasi, mixer, tempo dan panjang tetap.

Gunakan **108 BPM**, 4/4, Musical Time Base (ikon not), left locator **1.1.1.0**, **Import to Left Locator**, **Import Dropped File as Single Part**, **Ignore Master Track Events on Merge**. Baked-in swing disengaja: nada sixteenth ganjil berada pada offset .30/.80 beat, bukan .25/.75. Jangan kuantisasi ulang core dengan straight 1/16. Semua part harus mempertahankan keheningan awal dari bar 1.

[v002 — core asal](../v002/README.md) tetap tersedia. [v003 — percobaan semua-layer straight](../v003/README.md) disimpan sebagai alternatif, tetapi **v004 adalah revisi yang direkomendasikan** berdasarkan feedback terbaru.

**Verifikasi:** validate/generate/verify PASS; 11 MIDI core byte-identik; empat pelengkap pada grid groove 60:40. Impor live, pemuatan preset dan listening belum diuji. Sound/preset mengikuti versi asal; tidak ada native preset baru dibuat pada revisi timing ini.

108 BPM | 4/4 | F#m | 96 bar

## Memakai MIDI di Cubase

1. Atur tempo dan meter project sesuai keterangan di atas.
2. Buat satu instrument track Serum 2 untuk setiap instrumen melodi. Pilih preset sesuai fungsi pada tabel.
3. Drag file di `MIDI/` ke track yang sesuai, semuanya mulai bar 1. Pertahankan keheningan awal/akhir.
4. Untuk drum, pilih sendiri kit/sample dan cocokkan pitch pada tabel drum di bawah.

Setiap file berisi tepat satu track instrumen dan mencakup seluruh panjang lagu. File baru memakai SMF format 1, tanpa SysEx, teks/marker tambahan, atau Program Change. Preset dipilih di Serum, bukan oleh MIDI.

## Instrumen

| Track | Fungsi | Sound awal | MIDI |
| --- | --- | --- | --- |
| Kick - punchy drum machine | Groove foundation | Kit/sample pilihan Anda | [kick.mid](MIDI/kick.mid) |
| Snare - gated backbeat | Backbeat and ghost notes | Kit/sample pilihan Anda | [snare.mid](MIDI/snare.mid) |
| Hand clap | Chorus backbeat reinforcement | Kit/sample pilihan Anda | [clap.mid](MIDI/clap.mid) |
| Hi-hat - closed and open | Swung sixteenth pulse | Kit/sample pilihan Anda | [hihat.mid](MIDI/hihat.mid) |
| Shaker | Swung percussion | Kit/sample pilihan Anda | [shaker.mid](MIDI/shaker.mid) |
| Tambourine | Chorus lift | Kit/sample pilihan Anda | [tambourine.mid](MIDI/tambourine.mid) |
| Electronic toms | Section transition fills | Kit/sample pilihan Anda | [toms.mid](MIDI/toms.mid) |
| Slap bass | Syncopated bassline | Serum 2; pilih preset sesuai fungsi | [slap-bass.mid](MIDI/slap-bass.mid) |
| Electric piano | Extended chord harmony | Serum 2; pilih preset sesuai fungsi | [electric-piano.mid](MIDI/electric-piano.mid) |
| Poly synth stabs | Rhythmic harmony | Serum 2; pilih preset sesuai fungsi | [synth-stabs.mid](MIDI/synth-stabs.mid) |
| Muted funk guitar | Offbeat chord scratches | Serum 2; pilih preset sesuai fungsi | [muted-guitar.mid](MIDI/muted-guitar.mid) |
| Synth brass | Call-and-response accents | Serum 2; pilih preset sesuai fungsi | [synth-brass.mid](MIDI/synth-brass.mid) |
| Saw synth lead | Main instrumental hook | Serum 2; pilih preset sesuai fungsi | [lead-synth.mid](MIDI/lead-synth.mid) |
| Warm string pad | Pre-chorus and bridge sustain | Serum 2; pilih preset sesuai fungsi | [string-pad.mid](MIDI/string-pad.mid) |
| FM bell keys | Phrase-end sparkle | Serum 2; pilih preset sesuai fungsi | [bell-keys.mid](MIDI/bell-keys.mid) |

## Drum yang disarankan

Kick drum-machine yang padat dan pendek, snare elektronik dengan gated tail untuk backbeat, clap sebagai lapisan chorus, closed hat kering dan open hat pendek agar swing sixteenth 108 BPM tetap jelas. Shaker ringan, tambourine terang di chorus, serta tom elektronik bernada untuk fill. Gunakan velocity ghost snare yang lebih lembut, bukan sample besar pada setiap pukulan. Sample/kit masih dipilih Anda.

| Track drum | Pitch MIDI |
| --- | --- |
| Kick - punchy drum machine | 36 |
| Snare - gated backbeat | 38 |
| Hand clap | 39 |
| Hi-hat - closed and open | 42, 46 |
| Shaker | 82 |
| Tambourine | 54 |
| Electronic toms | 45, 47, 50 |

Jika beberapa bagian drum memakai channel 10 dan satu kit bersama, filter CC7/CC10 saat impor lalu atur volume/pan per pad, atau gunakan track sampler terpisah.

## Instrumen di luar Serum

Default semua instrumen melodi menggunakan Serum 2; drum memakai sampler/kit pilihan Anda. Belum ada plugin atau library melodi eksternal yang dikonfigurasikan dalam ekspor ini. Ekspor MIDI saja belum membuktikan adanya preset atau plugin yang berhasil dimuat.

## Bagian lagu

| Bagian | Mulai bar |
| --- | --- |
| Intro | 1 |
| Verse 1 | 9 |
| Pre-chorus | 25 |
| Chorus 1 | 33 |
| Verse 2 | 49 |
| Bridge | 65 |
| Final chorus | 73 |
| Outro | 89 |

## Asumsi

- Komposisi instrumental orisinal; synth lead menjalankan fungsi melodi utama karena vokal/lirik tidak diminta.
- 108 BPM, F# minor, 4/4, 96 bar; durasi 213.333 detik.
- Swing pasangan not 1/16 sebesar 60:40; seed velocity asal 108960. Offset core asli, termasuk clap flam, dipertahankan; strum delay pada muted guitar dihapus.
- 15 layer: tujuh bagian drum/percussion dan delapan instrumen melodi/harmoni; satu file MIDI per layer.
- Drum map General MIDI: kick 36, snare 38, clap 39, hi-hat 42/46, shaker 82, tambourine 54, toms 50/47/45.
- Preset GM adalah petunjuk sound; gunakan drum machine dengan gated snare, slap bass, Rhodes dan synth era 1990-an di DAW.
- Tidak ada file MIDI gabungan; semua layer tetap mulai pada tick 0 dan berakhir di panjang global.

## Keterangan hasil

Verifikasi struktur MIDI lulus. Status sound/preset dan listening perlu dicatat sesuai pemeriksaan yang benar-benar dilakukan. Data teknis dan snapshot komposisi ada di `_internal/`.

Untuk impor Cubase, buka Preferences > MIDI > MIDI File: aktifkan **Import Dropped File as Single Part** dan nonaktifkan **Auto Dissolve Format 0** untuk file lama. Keberhasilan drag-and-drop perlu diperiksa di Cubase Anda.

[Panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html)

## Sound untuk revisi ini

Revisi v004 mempertahankan core v002 dan memperbaiki onset empat layer pelengkap seperti dijelaskan di atas. Pitch/velocity/durasi/mixer tetap sama. Preset Serum baru belum dibuat untuk lagu arsip ini. Gunakan Serum 2 dengan karakter sesuai nama/fungsi track, atau sound sebelumnya.

Untuk electric piano dan muted guitar, gunakan engine multisample Serum 2 (epiano_suitcase / guitar_ac) sebagai titik awal, envelope pendek untuk guitar scratches. Untuk slap bass realistis, bila suara Serum tidak mencukupi gunakan library bass yang Anda sudah miliki: buat instrument track terpisah, muat patch slap, import `slap-bass.mid` di bar 1, cek rentang pitch pada `_internal/validation.json`, lalu sesuaikan keyswitch menurut manual library. MIDI ini belum mengandung keyswitch. Sound eksternal ini opsional dan belum dipasang atau diuji.
