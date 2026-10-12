# Neon di Ujung Malam

**118 BPM · F# minor · 4/4 · 112 bar · 3:47.797 · 960 PPQN**

Instrumental dark synth-pop dengan bass berdenyut, pad hangat, chord sinkopasi, arp kaca dan hook melankolis. Intro dan breakdown memberi ruang sinematik; chorus membuka beat dansa. Terinspirasi atmosfer *Dawn FM* dan *After Hours*, dengan motif serta aransemen baru. Delapan MIDI dan tujuh preset native Serum 2; tanpa vokal/lirik.

## Mulai di Cubase

1. Atur project pada **118 BPM, 4/4**. Buat tujuh instrument track **Serum 2** dan satu track sampler drum.
2. Pada setiap instance Serum, buka browser preset: `User > MIDI Creator > 20261011-neon-di-ujung-malam > v001`. Ketujuh preset sudah disimpan di folder User lokal itu. Cocokkan nama pada tabel dan mulai dengan macro default 0%.
3. Salinan preset ada di `Presets/`. Untuk komputer lain, salin `.SerumPreset` ke subfolder baru pada folder User Serum 2 lalu rescan browser jika perlu. Factory wavetables Serum 2 harus tersedia; tidak ada wavetable/sample tambahan.
4. Muat preset sebelum MIDI. Drag semua file ke track pasangannya mulai **bar 1**, termasuk layer yang masuk belakangan. Pertahankan keheningan dan panjang penuh 112 bar.
5. Muat kit/sample drum pilihan Anda, lalu cocokkan tujuh pitch pada tabel drum. Sample belum dipilih atau disalin.
6. Di Preferences > MIDI > MIDI File, aktifkan **Import Dropped File as Single Part**. Ekspor ini SMF format 1 dengan tepat satu track per file. [Panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html).

MIDI mempertahankan tempo, meter, velocity, CC7/CC10 dan end-of-track global, tanpa Program Change, Bank Select, SysEx atau metadata key/marker tambahan. Key dan bagian lagu tercantum di sini. File synth masing-masing memakai channel 1; drum channel 10.

## Track dan sound

Angka register memakai **C4 = MIDI 60**; nama octave di Cubase dapat berbeda. Semua sound dalam tabel memakai Serum 2 kecuali drum.

| Track | Fungsi / register MIDI | MIDI | Preset | Macro 1–4 |
| --- | --- | --- | --- | --- |
| Pulse Bass | Bass mono analog, pendek; 30–52 | [MIDI](MIDI/pulse-bass.mid) | [pulse-bass.SerumPreset](Presets/pulse-bass.SerumPreset) | OPEN: cutoff; SNAP: decay filter; WARMTH: tape wet; SUB: body rendah |
| Midnight Pad | Harmoni PWM hangat, drift lambat; 56–68 | [MIDI](MIDI/midnight-pad.mid) | [midnight-pad.SerumPreset](Presets/midnight-pad.SerumPreset) | OPEN: cutoff; DRIFT: kecepatan motion; SPACE: hall; GLOW: lapisan atas |
| Neon Chords | Brass-like stabs sinkopasi; 64–76 | [MIDI](MIDI/neon-chords.mid) | [neon-chords.SerumPreset](Presets/neon-chords.SerumPreset) | BITE: cutoff; BODY: octave bawah; WIDTH: chorus; ROOM: hall |
| Glass Arp | Pluck kaca, eighth-note saat chorus; 76–88 | [MIDI](MIDI/glass-arp.mid) | [glass-arp.SerumPreset](Presets/glass-arp.SerumPreset) | GLASS: warna digital; DECAY: panjang pluck; ECHO: delay; HALO: hall |
| Night Hook | Lead mono, vibrato tertunda; 66–78 | [MIDI](MIDI/night-hook.mid) | [night-hook.SerumPreset](Presets/night-hook.SerumPreset) | OPEN: cutoff; BODY: pulse layer; ECHO: delay; SPACE: hall |
| Rain Keys | Electric bell keys menjawab frase; 64–76 | [MIDI](MIDI/rain-keys.mid) | [rain-keys.SerumPreset](Presets/rain-keys.SerumPreset) | TINE: warna tine; LENGTH: decay; CHORUS: wet; ROOM: hall |
| Radio Haze | Tekstur tonal, brown noise terfilter; 76–80 | [MIDI](MIDI/radio-haze.mid) | [radio-haze.SerumPreset](Presets/radio-haze.SerumPreset) | TUNE: warna filter; DUST: noise; DRIFT: motion; SPACE: hall |
| Retro Drum Kit | Kick/snare/clap/hat/crash/shaker; channel 10 | [MIDI](MIDI/retro-drums.mid) | Sampler/kit pilihan Anda | Gain dan pan per pad pada sampler |

Arp sudah berupa nada MIDI; jangan menambah arpeggiator kedua. Delay Glass Arp/Night Hook memakai waktu literal **254.237 ms**, setara 1/8 pada 118 BPM; sesuaikan jika tempo berubah. Macro adalah kontrol manual, tanpa automation macro di MIDI. Octave penunjang internal oscillator sudah tersimpan dalam preset.

## Bentuk lagu

| Bar | Bagian | Perkembangan |
| --- | --- | --- |
| 1–8 | Intro | Pad/haze, bass dan arp masuk bar 5, teaser hook bar 7 |
| 9–24 | Verse 1 | Kick sinkopasi, bass mono, chord jarang, keys mengisi celah |
| 25–32 | Pre-chorus 1 | Bm7–Dmaj7–E6–C#7; arp rapat, lead naik sampai E#5, snare pickup |
| 33–48 | Chorus 1 | Kick empat ketukan, bass offbeat, clap, chord lebar, motif lead delapan bar |
| 49–56 | Interlude | Beat turun, haze/keys; groove perlahan kembali bar 53 |
| 57–72 | Verse 2 | Keys bervariasi, shaker muncul bar 65 |
| 73–80 | Pre-chorus 2 | Dominant build lalu beralih ke breakdown |
| 81–88 | Breakdown | Lead lebih rendah, Bm7–F#m9–Dmaj7–C#7; drum kembali bar 85 |
| 89–104 | Final chorus | Velocity lebih kuat dan shaker; bar 101–104 memakai Bm7–C#7–F#m–F#m |
| 105–108 | Outro | Tonic F#m9, drum mereda, pad/haze menutup |
| 109–112 | Release | Tanpa nada MIDI baru atau yang masih ditahan; sekitar 8.14 detik untuk release/FX |

Harmoni dasar **F#m9–Dmaj7–Aadd9–E6**, dua bar per chord. Pad berada di register rendah-menengah, stabs lebih tinggi, arp di atas lead. Melodi memakai extension sebagai warna dan E# pada C#7 sebagai leading tone ke F#.

## Drum yang cocok

Pilih kit elektronik retro dengan transient jelas dan top-end halus. Kick chorus stabil empat ketukan; verse memakai kick sinkopasi dan snare pada ketukan 2/4. Clap memberi lebar chorus. Rekomendasi berikut adalah karakter sound, bukan sample yang sudah dipilih.

| Pitch MIDI | Bagian | Karakter / mapping |
| --- | --- | --- |
| 36 | Kick | Bulat dan punchy, tail kira-kira 100–180 ms; low-end terkontrol agar bass F#1 jelas |
| 38 | Snare | Snare 80-an, body singkat dengan gated room; ghost note lebih lembut |
| 39 | Clap | Clap stereo tipis, sekitar 9 ms setelah snare di chorus |
| 42 | Closed hat | Hat pendek, agak gelap; velocity berselang-seling dan timing offbeat kecil |
| 46 | Open hat | Open hat ringkas di offbeat chorus; choke bersama closed hat bila kit mendukung |
| 49 | Crash | Crash lembut di awal blok chorus, wash tidak terlalu panjang/tajam |
| 82 | Shaker | Shaker/cabasa halus pada verse 2 dan final chorus; petakan angka 82 manual |

**Sample belum dipilih atau disertakan; kit mengikuti pilihan Anda.** Groove Agent SE atau sampler Anda dapat memuat one-shot ke pitch numerik di atas; jangan mengandalkan nama octave atau preset GM. Karena satu kit, CC7=106 dan CC10=64 berlaku bagi seluruh kit. Atur gain dan pan per pad pada sampler. Note-off drum pendek bukan instruksi memotong sample: gunakan mode one-shot dan choke hat sesuai kit.

## Arahan produksi

Mulai dari balance CC, lalu sesuaikan gain setelah kit dimuat. Bass chorus masuk seperempat beat setelah kick dengan gate pendek untuk kesan pumping. Sidechain bass/pad ringan ke kick dapat ditambahkan di DAW; belum dibuat dalam file ini.

Lead di depan, arp di kanan ringan dan keys di kiri ringan. Pad/haze sudah memakai hall. Tambah send reverb setelah listening; pertahankan verse lebih rendah daripada chorus. Turunkan level outro bila menginginkan fade lebih panjang. Preset belum dinilai melalui audio, sehingga balance akhir perlu disesuaikan dengan kit pilihan Anda.

## Instrumen di luar Serum

Tidak ada instrumen melodi eksternal. Drum memakai sampler karena kit/sample mengikuti pilihan Anda. Groove Agent SE cocok untuk pad manual atau gunakan sampler kit sendiri; tidak ada library drum yang diwajibkan. Artikulasinya kick/snare/clap/hat/crash/shaker one-shot, channel 10, pitch 36–82 sesuai tabel, tanpa keyswitch.

## Verifikasi dan asumsi

| Pemeriksaan | Status |
| --- | --- |
| MIDI validate / generate / verify | **PASS**, exit code 0, `ok: true`, 3849 note, delapan file format 1 dengan satu track |
| Alignment | **PASS**, timeline bar 1, end-of-track 430080 tick, tempo/meter/960 PPQN sama |
| Note pairing / overlap / metadata | **PASS**, tanpa nada tertinggal, overlap pitch sama, SysEx, Bank Select atau Program Change |
| Native preset | **PASS**, tujuh `.SerumPreset` asli dibuat melalui repo serum-mcp |
| Decode / readback / checksum | **PASS**, oscillator/filter/envelope/LFO/macro/FX/global/mod routes/nama cocok dengan spesifikasi; checksum salinan sesuai |
| Penilaian musikal | Harmoni, register, fungsi layer, groove, frase, perkembangan dan ending diperiksa dari spesifikasi/event |
| Pemuatan tujuh preset di Serum 2 | **Belum diuji**; status studio mendeteksi instalasi Serum 2.0.23, API native-preset loading belum tersedia |
| Import / playback live Cubase | **Belum diuji**; tidak ada `.cpr` dibuat |
| Rendering / listening | **Belum dilakukan**; belum ada preview WAV atau audio yang didengarkan |

Tempo/key/panjang/bentuk dipilih untuk brief yang terbuka. Versi ini instrumental tanpa vokal, sample drum pilihan Anda, tanpa file gabungan karena tidak diminta. Keheningan awal tiap layer disengaja. Factory wavetables Serum 2 diperlukan; macro manual dan modulation internal tersimpan dalam preset.

Riset mengacu pada [wawancara Daniel Lopatin di Synth History](https://www.synthhistory.com/post/three-questions-with-oneohtrix-point-never), yang membahas Juno-60 dan penggunaan arp pada karyanya untuk The Weeknd. PWM pad dan arp di sini adalah interpretasi musikal. [Wawancara GQ](https://www.gq.com/story/oneohtrix-point-never-magic-oneohtrix-point-never-album-the-weeknd-interview) memberi konteks kolaborasi synth pada *After Hours*. Preset synthwave lokal hanya diperiksa sebagai pembanding; sound baru dibuat dari init.

Sumber, binding, spesifikasi, schema, audit, checksum dan receipt berada di `_internal/`. Upstream `Celian-mrc/serum-mcp`, commit `7299f2eea1acd2ae5a863965f5bd4beedf107ee8`.
