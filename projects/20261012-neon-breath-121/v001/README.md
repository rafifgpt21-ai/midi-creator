# Neon Breath — 121 BPM Nu-Disco / Synthwave

**121 BPM · C minor · 4/4 · 4 bar · 7,933888 detik · 480 PPQN · straight 1/16, tanpa swing.**

Progresi: **Cm → Fm → Ab → Bb**, satu chord per bar. Paket berisi **10 MIDI synth + 10 preset native Serum 2 + 7 MIDI drum terpisah**. Setiap MIDI SMF format 1, tepat satu track, mulai di bar 1 dan berakhir pada tick 7680. Hook dan susunan nada merupakan komposisi baru mengikuti brief.

## Mulai di Cubase

1. Set project ke 121 BPM, 4/4, Musical Time Base; left locator **1.1.1.0**, right locator **5.1.1.0**.
2. Buat 10 Instrument Tracks Serum 2. Preset juga sudah dipasang di browser **User → MIDI Creator → 20261012-neon-breath-121 → v001**. Pilih preset dengan ID yang sama seperti MIDI. Untuk salinan paket, gunakan menu Serum **Load Preset** pada file `.SerumPreset` di `Presets/`.
3. Impor setiap MIDI dari tabel ke track yang sesuai dengan **Import to Left Locator**. Aktifkan **Import Dropped File as Single Part** bila drag-and-drop. Pertahankan keheningan awal semua part. Pada project bertempo tetap, **Ignore Master Track Events on Merge** menjaga tempo project.
4. Buat tujuh Sampler Tracks drum terpisah. Muat sample pilihan Anda, root **C3 (MIDI60)**, channel MIDI10. Semua drum sengaja memakai pitch yang sama karena instrumennya terpisah; jangan masukkan tujuh MIDI ini ke satu kit tanpa remap.
5. Untuk Sub Direct, pasang EQ low-pass **80 Hz / 24 dB per oktav**, HP sekitar **24 Hz**, dan compressor sidechain dari kick pada channel Cubase. Untuk sidechain audio, putar macro PUMP ke 0 agar tidak mendobelkan pump LFO.
6. Internal arp/clip Serum dimatikan; file MIDI sudah berisi setiap nada arp. Gunakan voicing poly untuk chord/pad, mono untuk bass/lead sesuai preset. Loop bar 1–4; release dan FX tail boleh melampaui batas loop saat playback.

## Track, MIDI, dan preset

| Track | Fungsi | MIDI | Preset native / instrumen | Nada | CC7 / CC10 |
| --- | --- | --- | --- | ---: | --- |
| 01 Sub Bass | low-end foundation | [layer01-sub-bass.mid](MIDI/layer01-sub-bass.mid) | [Serum 2](Presets/layer01-sub-bass.SerumPreset) | 4 | 99 / 64 |
| 02 Moroder Octave Bass | rhythmic bass | [layer02-octave-bass.mid](MIDI/layer02-octave-bass.mid) | [Serum 2](Presets/layer02-octave-bass.SerumPreset) | 64 | 95 / 64 |
| 03 Analog Chord Stabs | offbeat harmony | [layer03-chord-stabs.mid](MIDI/layer03-chord-stabs.mid) | [Serum 2](Presets/layer03-chord-stabs.SerumPreset) | 64 | 87 / 61 |
| 04 Synth Brass Accents | chorus lift | [layer04-synth-brass.mid](MIDI/layer04-synth-brass.mid) | [Serum 2](Presets/layer04-synth-brass.SerumPreset) | 12 | 79 / 64 |
| 05 Bright Up Down Arp | main arp | [layer05-bright-arp.mid](MIDI/layer05-bright-arp.mid) | [Serum 2](Presets/layer05-bright-arp.SerumPreset) | 64 | 72 / 72 |
| 06 Glass Bell Counter Arp | high texture | [layer06-glass-bells.mid](MIDI/layer06-glass-bells.mid) | [Serum 2](Presets/layer06-glass-bells.SerumPreset) | 24 | 60 / 52 |
| 07 Warm Ambient Pad | background glue | [layer07-warm-pad.mid](MIDI/layer07-warm-pad.mid) | [Serum 2](Presets/layer07-warm-pad.SerumPreset) | 9 | 67 / 64 |
| 08 Main Retro Hook | primary hook | [layer08-main-lead.mid](MIDI/layer08-main-lead.mid) | [Serum 2](Presets/layer08-main-lead.SerumPreset) | 26 | 94 / 64 |
| 09 Whistle Response | call and response | [layer09-synth-whistle.mid](MIDI/layer09-synth-whistle.mid) | [Serum 2](Presets/layer09-synth-whistle.SerumPreset) | 6 | 78 / 68 |
| 10 Riser and Down Impact | transition accents | [layer10-transition-fx.mid](MIDI/layer10-transition-fx.mid) | [Serum 2](Presets/layer10-transition-fx.SerumPreset) | 2 | 66 / 64 |
| Kick | percussion | [drum-kick.mid](MIDI/drum-kick.mid) | Cubase Sampler — sample Anda | 16 | 107 / 64 |
| Snare | percussion | [drum-snare.mid](MIDI/drum-snare.mid) | Cubase Sampler — sample Anda | 8 | 91 / 64 |
| Clap | percussion | [drum-clap.mid](MIDI/drum-clap.mid) | Cubase Sampler — sample Anda | 8 | 75 / 64 |
| Closed Hat | percussion | [drum-closed-hat.mid](MIDI/drum-closed-hat.mid) | Cubase Sampler — sample Anda | 48 | 77 / 58 |
| Open Hat | percussion | [drum-open-hat.mid](MIDI/drum-open-hat.mid) | Cubase Sampler — sample Anda | 16 | 68 / 71 |
| Shaker | percussion | [drum-shaker.mid](MIDI/drum-shaker.mid) | Cubase Sampler — sample Anda | 64 | 56 / 82 |
| Crash | percussion | [drum-crash.mid](MIDI/drum-crash.mid) | Cubase Sampler — sample Anda | 1 | 57 / 60 |

## Bentuk 4 bar dan ruang frase

| Bar | Chord / bass | Perkembangan |
| --- | --- | --- |
| 1 | Cm / C0 | Downbeat kick, crash, brass, impact; bass/arp mulai; hook memperkenalkan motif. Riser mulai pelan. |
| 2 | Fm / F0 | Hook beralih F–Ab lalu berhenti; whistle menjawab di setengah bar terakhir. |
| 3 | Ab / Ab0 | Hook mencapai C4; pad mempertahankan C dan Ab dari bar sebelumnya; riser makin membuka. |
| 4 | Bb / Bb0 | Hook turun; whistle mengantisipasi C pada akhir loop. Riser mencapai terang tepat di batas bar5. |

Pad mempertahankan harmoni per bar, bukan satu chord statis sepanjang empat bar. Riser empat bar cocok sebagai build menuju pengulangan berikutnya; bila loop diulang terus, mute riser pada pengulangan yang tidak memerlukan transisi. Pan/volume MIDI adalah titik awal balance, bukan hasil mix audio terukur.

## Konvensi parameter dan notasi

- **Nama nada selalu Cubase: C3=MIDI60.** Angka MIDI di kurung adalah acuan utama. Penamaan standar C4=MIDI60 menyebut semua nada satu oktaf lebih tinggi.
- **Posisi `bar.beat.16th`**: `2.3.3` = bar2, beat3, subdivision ketiga, yaitu beat3-and. Step bar 1–16 ditampilkan juga. Satu step = 0,25 beat ≈123,967 ms =120 tick. Durasi beat dan durasi step adalah gate MIDI, bukan tail reverb.
- Envelope ditulis **A/D/S/R**: attack, decay, release dalam ms; sustain dalam persen. Hold=0; curve attack=50%, decay/release=66,6% mengikuti schema.
- Oscillator detune dan level memakai nilai native/tool **0–1**; octave relatif ke nada MIDI, fine dalam cent. Pan0=tengah. Table position adalah nilai tersimpan `kParamTablePos` 0–256. Default Shapes frame0=saw, sekitar128=square; Basic Shapes frame0=sine, Basic Mini frame0=rounded saw. Identitas frame diperiksa offline dari WAV factory, bukan melalui listening plugin.
- Cutoff filter adalah nilai tersimpan normalized **0–1**, **bukan Hz**. Resonance/drive/wet memakai persen; `level_out=0.5`, stereo50 netral menurut schema. File native memuat nilai ini langsung. Nilai cutoff Hz pada EQ/Utility dan instruksi host ditulis terpisah.
- Label UI ENV1/ENV2 = schema env0/env1; LFO1/LFO2 = lfo0/lfo1. Depth matrix dalam persen normalized, **bukan langsung semitone/cent/Hz**. Bipolar berarti gerak dua arah; depth satu arah jika tidak ditandai.
- LFO `beat_sync=true, rate=0` menggunakan default **1/4** tersimpan tanpa key rate. Untuk `beat_sync=false`, rate eksplisit adalah Hz. Semua kurva LFO ordinary di paket ini triangle 0→1→0; Sub memakai kurva duck khusus.
- FX berikut ditulis dalam urutan rack Main. `kParamTimeL/R` delay dalam detik, chorus depth/delay kira-kira ms, compressor attack/release ms, makeup gain multiplier. FX yang tidak terdaftar **OFF**.
- Compression internal mengatur dinamika sound sendiri. **Sidechain kick audio adalah insert host**, tidak otomatis tersimpan di preset Serum. Semua angka gain-reduction host adalah target awal untuk disetel saat audition.

## Parameter Serum dan MIDI lengkap per layer

### 01 Sub Bass

Root panjang satu bar; Sub triangle mono ke Direct. Fundamental 32,70 / 43,65 / 51,91 / 58,27 Hz. Terapkan LP 80 Hz sesudah Serum agar harmonik triangle ikut dibatasi.

[MIDI](MIDI/layer01-sub-bass.mid) · [Preset native](Presets/layer01-sub-bass.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | OFF | 0 / 0 | 1 / 0 | 0 | none |
| B | OFF | 0 / 0 | 1 / 0 | 0 | none |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | ON: triangle | 0 / 0 cent; semitone 0 | 1 / 0 | 0.72 | direct; F1 balance 0 |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | OFF; lowpass_24; cutoff 0.28; resonance 0%; drive 0%; key track False; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 5 / 1000 / 100% / 45 |
| ENV2 A/D/S/R | 1 / 120 / 0% / 30 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.55; mono True; poly 8; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 1/4, default rate0; Free, mono/shared True; delay 0 ms; rise 0 ms; duck: (0,1), (0.075,1), (0.45,0.1), (0.75,0), (1,0) | oscillator4.volume -65%; aux macro0 |
| LFO2 | 1/4, default rate0; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | OFF: tidak dirutekan |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| Macro2 (LEVEL) | oscillator4.volume | -20% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| Distortion | OFF | Tidak digunakan |
| Chorus | OFF | Tidak digunakan |
| Delay | OFF | Tidak digunakan |
| Reverb | OFF | Tidak digunakan |
| Compression | OFF | Tidak digunakan |

Macro defaults: 1 PUMP=100%, 2 LEVEL=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Native LFO1 pump 1/4, kedalaman via PUMP=100. Untuk sidechain audio kick: PUMP=0; host compressor ratio 6:1, attack 1 ms, release 150 ms, threshold sampai reduction ≈8–10 dB. LP 24 dB/oct 80 Hz dan HP 24 Hz setelah Serum.

<details>
<summary>MIDI DATA lengkap — 4 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C0 (24) | 100 | 4 | 16 |
| 2.1.1 | 1 | F0 (29) | 100 | 4 | 16 |
| 3.1.1 | 1 | Ab0 (32) | 100 | 4 | 16 |
| 4.1.1 | 1 | Bb0 (34) | 100 | 4 | 16 |

</details>

### 02 Moroder Octave Bass

Saw punchy, tiap 16th berganti oktav. Gate 72% dari satu step; filter decay 72 ms, saturasi dan HP 95 Hz menjaga pemisahan dari sub.

[MIDI](MIDI/layer02-octave-bass.mid) · [Preset native](Presets/layer02-octave-bass.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: Analog/Basic Mini.wav; WT pos 0 | 0 / 0 cent; semitone 0 | 1 / 0 | 0.55 | filter; F1 balance 0 |
| B | ON: S2 Tables/Default Shapes.wav; WT pos 0 | 0 / 3 cent; semitone 0 | 1 / 0 | 0.2 | filter; F1 balance 0 |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; moog_lowpass_24; cutoff 0.37; resonance 19%; drive 16%; key track False; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 2 / 130 / 6% / 25 |
| ENV2 A/D/S/R | 1 / 72 / 0% / 22 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.48; mono True; poly 8; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 1/4, default rate0; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | OFF: tidak dirutekan |
| LFO2 | 1/4, default rate0; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | OFF: tidak dirutekan |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | filter0.cutoff | +33% unipolar |
| velocity | filter0.cutoff | +7% unipolar |
| velocity | global.voice_amp | +12% unipolar |
| Macro1 (TONE) | filter0.cutoff | +13% unipolar |
| Macro2 (GRIT) | filter0.drive | +12% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Distortion | 38% | kParamMode=kSoftClip; kParamDrive=25 |
| 2. Compression | 100% | kParamThresh=0.65; kParamRatio=2.5; kParamAttack=15; kParamRelease=90; kParamMakeup=1.7 |
| 3. Utility / band-limit | 100% | kParamHPF=95; kParamLPF=6500; kParamWidth=0 |
| Chorus | OFF | Tidak digunakan |
| Delay | OFF | Tidak digunakan |
| Reverb | OFF | Tidak digunakan |

Macro defaults: 1 TONE=0%, 2 GRIT=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host sidechain dari kick: ratio 4:1, attack 1 ms, release 85 ms, reduction awal 3–5 dB; atur threshold menurut sample kick.

<details>
<summary>MIDI DATA lengkap — 64 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C1 (36) | 108 | 0.18 | 0.72 |
| 1.1.2 | 2 | C2 (48) | 84 | 0.18 | 0.72 |
| 1.1.3 | 3 | C1 (36) | 94 | 0.18 | 0.72 |
| 1.1.4 | 4 | C2 (48) | 82 | 0.18 | 0.72 |
| 1.2.1 | 5 | C1 (36) | 108 | 0.18 | 0.72 |
| 1.2.2 | 6 | C2 (48) | 84 | 0.18 | 0.72 |
| 1.2.3 | 7 | C1 (36) | 94 | 0.18 | 0.72 |
| 1.2.4 | 8 | C2 (48) | 82 | 0.18 | 0.72 |
| 1.3.1 | 9 | C1 (36) | 108 | 0.18 | 0.72 |
| 1.3.2 | 10 | C2 (48) | 84 | 0.18 | 0.72 |
| 1.3.3 | 11 | C1 (36) | 94 | 0.18 | 0.72 |
| 1.3.4 | 12 | C2 (48) | 82 | 0.18 | 0.72 |
| 1.4.1 | 13 | C1 (36) | 108 | 0.18 | 0.72 |
| 1.4.2 | 14 | C2 (48) | 84 | 0.18 | 0.72 |
| 1.4.3 | 15 | C1 (36) | 94 | 0.18 | 0.72 |
| 1.4.4 | 16 | C2 (48) | 82 | 0.18 | 0.72 |
| 2.1.1 | 1 | F0 (29) | 108 | 0.18 | 0.72 |
| 2.1.2 | 2 | F1 (41) | 84 | 0.18 | 0.72 |
| 2.1.3 | 3 | F0 (29) | 94 | 0.18 | 0.72 |
| 2.1.4 | 4 | F1 (41) | 82 | 0.18 | 0.72 |
| 2.2.1 | 5 | F0 (29) | 108 | 0.18 | 0.72 |
| 2.2.2 | 6 | F1 (41) | 84 | 0.18 | 0.72 |
| 2.2.3 | 7 | F0 (29) | 94 | 0.18 | 0.72 |
| 2.2.4 | 8 | F1 (41) | 82 | 0.18 | 0.72 |
| 2.3.1 | 9 | F0 (29) | 108 | 0.18 | 0.72 |
| 2.3.2 | 10 | F1 (41) | 84 | 0.18 | 0.72 |
| 2.3.3 | 11 | F0 (29) | 94 | 0.18 | 0.72 |
| 2.3.4 | 12 | F1 (41) | 82 | 0.18 | 0.72 |
| 2.4.1 | 13 | F0 (29) | 108 | 0.18 | 0.72 |
| 2.4.2 | 14 | F1 (41) | 84 | 0.18 | 0.72 |
| 2.4.3 | 15 | F0 (29) | 94 | 0.18 | 0.72 |
| 2.4.4 | 16 | F1 (41) | 82 | 0.18 | 0.72 |
| 3.1.1 | 1 | Ab0 (32) | 108 | 0.18 | 0.72 |
| 3.1.2 | 2 | Ab1 (44) | 84 | 0.18 | 0.72 |
| 3.1.3 | 3 | Ab0 (32) | 94 | 0.18 | 0.72 |
| 3.1.4 | 4 | Ab1 (44) | 82 | 0.18 | 0.72 |
| 3.2.1 | 5 | Ab0 (32) | 108 | 0.18 | 0.72 |
| 3.2.2 | 6 | Ab1 (44) | 84 | 0.18 | 0.72 |
| 3.2.3 | 7 | Ab0 (32) | 94 | 0.18 | 0.72 |
| 3.2.4 | 8 | Ab1 (44) | 82 | 0.18 | 0.72 |
| 3.3.1 | 9 | Ab0 (32) | 108 | 0.18 | 0.72 |
| 3.3.2 | 10 | Ab1 (44) | 84 | 0.18 | 0.72 |
| 3.3.3 | 11 | Ab0 (32) | 94 | 0.18 | 0.72 |
| 3.3.4 | 12 | Ab1 (44) | 82 | 0.18 | 0.72 |
| 3.4.1 | 13 | Ab0 (32) | 108 | 0.18 | 0.72 |
| 3.4.2 | 14 | Ab1 (44) | 84 | 0.18 | 0.72 |
| 3.4.3 | 15 | Ab0 (32) | 94 | 0.18 | 0.72 |
| 3.4.4 | 16 | Ab1 (44) | 82 | 0.18 | 0.72 |
| 4.1.1 | 1 | Bb0 (34) | 108 | 0.18 | 0.72 |
| 4.1.2 | 2 | Bb1 (46) | 84 | 0.18 | 0.72 |
| 4.1.3 | 3 | Bb0 (34) | 94 | 0.18 | 0.72 |
| 4.1.4 | 4 | Bb1 (46) | 82 | 0.18 | 0.72 |
| 4.2.1 | 5 | Bb0 (34) | 108 | 0.18 | 0.72 |
| 4.2.2 | 6 | Bb1 (46) | 84 | 0.18 | 0.72 |
| 4.2.3 | 7 | Bb0 (34) | 94 | 0.18 | 0.72 |
| 4.2.4 | 8 | Bb1 (46) | 82 | 0.18 | 0.72 |
| 4.3.1 | 9 | Bb0 (34) | 108 | 0.18 | 0.72 |
| 4.3.2 | 10 | Bb1 (46) | 84 | 0.18 | 0.72 |
| 4.3.3 | 11 | Bb0 (34) | 94 | 0.18 | 0.72 |
| 4.3.4 | 12 | Bb1 (46) | 82 | 0.18 | 0.72 |
| 4.4.1 | 13 | Bb0 (34) | 108 | 0.18 | 0.72 |
| 4.4.2 | 14 | Bb1 (46) | 84 | 0.18 | 0.72 |
| 4.4.3 | 15 | Bb0 (34) | 94 | 0.18 | 0.72 |
| 4.4.4 | 16 | Bb1 (46) | 82 | 0.18 | 0.72 |

</details>

### 03 Analog Chord Stabs

Dual saw dengan 3+2 unison, chorus vintage, stab pada step 3/7/10/15. Voicing bar 1 Cm7, bar 2 Fm7, bar 3 Abmaj7; bar 4 upper voicing Bb/G: G–Bb–D–F. Dengan sub Bb, harmoni gabungan berbunyi Bb6.

[MIDI](MIDI/layer03-chord-stabs.mid) · [Preset native](Presets/layer03-chord-stabs.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: S2 Tables/Default Shapes.wav; WT pos 0 | 0 / 0 cent; semitone 0 | 3 / 0.075 | 0.36 | filter; F1 balance 0 |
| B | ON: Analog/Basic Mini.wav; WT pos 0 | 0 / -4 cent; semitone 0 | 2 / 0.045 | 0.32 | filter; F1 balance 0 |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; moog_lowpass_24; cutoff 0.48; resonance 16%; drive 10%; key track False; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 3 / 240 / 0% / 95 |
| ENV2 A/D/S/R | 2 / 160 / 0% / 55 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.4; mono False; poly 16; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 0.27 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator1.fine +1.2% bipolar |
| LFO2 | 1/4, default rate0; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | OFF: tidak dirutekan |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | filter0.cutoff | +28% unipolar |
| velocity | filter0.cutoff | +8% unipolar |
| Macro1 (TONE) | filter0.cutoff | +12% unipolar |
| Macro2 (SPACE) | fx3.wet | +15% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Distortion | 16% | kParamMode=kTapeSat; kParamDrive=12 |
| 2. Compression | 100% | kParamThresh=0.65; kParamRatio=2; kParamAttack=15; kParamRelease=90; kParamMakeup=1.45 |
| 3. Chorus | 32% | kParamRate=0.22; kParamDepth=6; kParamDelay=7; kParamFeedback=8; kParamFilt=3000 |
| 4. Reverb | 10% | kParamType=kVintage; kParamSize=35; kParamDelay=22; kParamWidth=100 |
| 5. Utility / band-limit | 100% | kParamHPF=160; kParamLPF=10500; kParamWidth=100 |
| Delay | OFF | Tidak digunakan |

Macro defaults: 1 TONE=0%, 2 SPACE=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host duck ringan 2–3 dB, attack 2 ms, release 110 ms bila stab terasa menutup kick.

<details>
<summary>MIDI DATA lengkap — 64 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.3 | 3 | C2 (48) + G2 (55) + Bb2 (58) + Eb3 (63) | 97/95/93/91 | 0.2875 | 1.15 |
| 1.2.3 | 7 | C2 (48) + G2 (55) + Bb2 (58) + Eb3 (63) | 87/85/83/81 | 0.2875 | 1.15 |
| 1.3.2 | 10 | C2 (48) + G2 (55) + Bb2 (58) + Eb3 (63) | 92/90/88/86 | 0.2875 | 1.15 |
| 1.4.3 | 15 | C2 (48) + G2 (55) + Bb2 (58) + Eb3 (63) | 104/102/100/98 | 0.2875 | 1.15 |
| 2.1.3 | 3 | C2 (48) + F2 (53) + Ab2 (56) + Eb3 (63) | 97/95/93/91 | 0.2875 | 1.15 |
| 2.2.3 | 7 | C2 (48) + F2 (53) + Ab2 (56) + Eb3 (63) | 87/85/83/81 | 0.2875 | 1.15 |
| 2.3.2 | 10 | C2 (48) + F2 (53) + Ab2 (56) + Eb3 (63) | 92/90/88/86 | 0.2875 | 1.15 |
| 2.4.3 | 15 | C2 (48) + F2 (53) + Ab2 (56) + Eb3 (63) | 104/102/100/98 | 0.2875 | 1.15 |
| 3.1.3 | 3 | C2 (48) + G2 (55) + Ab2 (56) + Eb3 (63) | 97/95/93/91 | 0.2875 | 1.15 |
| 3.2.3 | 7 | C2 (48) + G2 (55) + Ab2 (56) + Eb3 (63) | 87/85/83/81 | 0.2875 | 1.15 |
| 3.3.2 | 10 | C2 (48) + G2 (55) + Ab2 (56) + Eb3 (63) | 92/90/88/86 | 0.2875 | 1.15 |
| 3.4.3 | 15 | C2 (48) + G2 (55) + Ab2 (56) + Eb3 (63) | 104/102/100/98 | 0.2875 | 1.15 |
| 4.1.3 | 3 | G2 (55) + Bb2 (58) + D3 (62) + F3 (65) | 97/95/93/91 | 0.2875 | 1.15 |
| 4.2.3 | 7 | G2 (55) + Bb2 (58) + D3 (62) + F3 (65) | 87/85/83/81 | 0.2875 | 1.15 |
| 4.3.2 | 10 | G2 (55) + Bb2 (58) + D3 (62) + F3 (65) | 92/90/88/86 | 0.2875 | 1.15 |
| 4.4.3 | 15 | G2 (55) + Bb2 (58) + D3 (62) + F3 (65) | 104/102/100/98 | 0.2875 | 1.15 |

</details>

### 04 Synth Brass Accents

Saw 5 voices + square 3 voices, swell filter 35 ms. Chord di downbeat tiap bar, ditahan dua beat, dengan hall besar untuk lift.

[MIDI](MIDI/layer04-synth-brass.mid) · [Preset native](Presets/layer04-synth-brass.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: S2 Tables/Default Shapes.wav; WT pos 0 | 0 / 0 cent; semitone 0 | 5 / 0.09 | 0.38 | filter; F1 balance 0 |
| B | ON: S2 Tables/Default Shapes.wav; WT pos 128 | 0 / -3 cent; semitone 0 | 3 / 0.055 | 0.23 | filter; F1 balance 0 |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; moog_lowpass_24; cutoff 0.46; resonance 13%; drive 17%; key track False; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 24 / 700 / 66% / 180 |
| ENV2 A/D/S/R | 35 / 480 / 42% / 140 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.38; mono False; poly 16; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 4.7 Hz; Free, mono/shared True; delay 120 ms; rise 200 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator0.fine +1.5% bipolar |
| LFO2 | 1/4, default rate0; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | OFF: tidak dirutekan |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | filter0.cutoff | +38% unipolar |
| velocity | filter0.cutoff | +8% unipolar |
| Macro1 (TONE) | filter0.cutoff | +10% unipolar |
| Macro2 (SPACE) | fx3.wet | +12% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Distortion | 22% | kParamMode=kTapeSat; kParamDrive=17 |
| 2. Compression | 100% | kParamThresh=0.65; kParamRatio=2.2; kParamAttack=15; kParamRelease=90; kParamMakeup=1.6 |
| 3. Chorus | 15% | kParamRate=0.18; kParamDepth=4; kParamDelay=7; kParamFeedback=8; kParamFilt=3000 |
| 4. Reverb | 31% | kParamType=kHall; kParamSize=75; kParamDelay=22; kParamWidth=100 |
| 5. Utility / band-limit | 100% | kParamHPF=150; kParamLPF=12000; kParamWidth=100 |
| Delay | OFF | Tidak digunakan |

Macro defaults: 1 TONE=0%, 2 SPACE=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host duck 3–4 dB, attack 2 ms, release 130 ms; jaga transient brass.

<details>
<summary>MIDI DATA lengkap — 12 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C2 (48) + Eb2 (51) + G2 (55) | 104/102/100 | 2 | 8 |
| 2.1.1 | 1 | C2 (48) + F2 (53) + Ab2 (56) | 104/102/100 | 2 | 8 |
| 3.1.1 | 1 | C2 (48) + Eb2 (51) + Ab2 (56) | 104/102/100 | 2 | 8 |
| 4.1.1 | 1 | D2 (50) + F2 (53) + Bb2 (58) | 104/102/100 | 2 | 8 |

</details>

### 05 Bright Up Down Arp

Up/down triad 16th, gate 66%. Filter pluck membuka singkat; LFO1 menggerakkan cutoff lembut, LFO2 menggerakkan posisi PWM. Volume lebih rendah dari hook.

[MIDI](MIDI/layer05-bright-arp.mid) · [Preset native](Presets/layer05-bright-arp.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: S2 Tables/Default Shapes.wav; WT pos 0 | 0 / 0 cent; semitone 0 | 3 / 0.055 | 0.4 | filter; F1 balance 0 |
| B | ON: Analog/PWM Juno.wav; WT pos 120 | 0 / 0 cent; semitone 0 | 2 / 0.035 | 0.17 | filter; F1 balance 0 |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; moog_lowpass_24; cutoff 0.52; resonance 9%; drive 7%; key track False; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 1 / 180 / 0% / 35 |
| ENV2 A/D/S/R | 1 / 85 / 0% / 35 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.43; mono False; poly 16; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 1/4, default rate0; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | filter0.cutoff +5% bipolar |
| LFO2 | 0.33 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator1.table_position +4% bipolar |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | filter0.cutoff | +30% unipolar |
| velocity | global.voice_amp | +14% unipolar |
| Macro1 (TONE) | filter0.cutoff | +9% unipolar |
| Macro2 (SPACE) | fx2.wet | +14% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Compression | 100% | kParamThresh=0.65; kParamRatio=2; kParamAttack=15; kParamRelease=90; kParamMakeup=1.45 |
| 2. Chorus | 12% | kParamRate=0.3; kParamDepth=3; kParamDelay=7; kParamFeedback=8; kParamFilt=3000 |
| 3. Delay | 13% | kParamTimeL=0.247934; kParamTimeR=0.123967; kParamBeatSync=0; kParamMode=1; kParamFeedback=23; kParamFreq=4800 |
| 4. Reverb | 9% | kParamType=kHall; kParamSize=35; kParamDelay=22; kParamWidth=100 |
| 5. Utility / band-limit | 100% | kParamHPF=240; kParamLPF=13000; kParamWidth=100 |
| Distortion | OFF | Tidak digunakan |

Macro defaults: 1 TONE=0%, 2 SPACE=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host duck 2 dB, attack 2 ms, release 85 ms; prioritas jelasnya hook dan hi-hat.

<details>
<summary>MIDI DATA lengkap — 64 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C3 (60) | 84 | 0.165 | 0.66 |
| 1.1.2 | 2 | Eb3 (63) | 65 | 0.165 | 0.66 |
| 1.1.3 | 3 | G3 (67) | 73 | 0.165 | 0.66 |
| 1.1.4 | 4 | C4 (72) | 67 | 0.165 | 0.66 |
| 1.2.1 | 5 | G3 (67) | 84 | 0.165 | 0.66 |
| 1.2.2 | 6 | Eb3 (63) | 65 | 0.165 | 0.66 |
| 1.2.3 | 7 | C3 (60) | 73 | 0.165 | 0.66 |
| 1.2.4 | 8 | Eb3 (63) | 67 | 0.165 | 0.66 |
| 1.3.1 | 9 | G3 (67) | 84 | 0.165 | 0.66 |
| 1.3.2 | 10 | C4 (72) | 65 | 0.165 | 0.66 |
| 1.3.3 | 11 | G3 (67) | 73 | 0.165 | 0.66 |
| 1.3.4 | 12 | Eb3 (63) | 67 | 0.165 | 0.66 |
| 1.4.1 | 13 | C3 (60) | 84 | 0.165 | 0.66 |
| 1.4.2 | 14 | Eb3 (63) | 65 | 0.165 | 0.66 |
| 1.4.3 | 15 | G3 (67) | 73 | 0.165 | 0.66 |
| 1.4.4 | 16 | Eb3 (63) | 67 | 0.165 | 0.66 |
| 2.1.1 | 1 | F3 (65) | 84 | 0.165 | 0.66 |
| 2.1.2 | 2 | Ab3 (68) | 65 | 0.165 | 0.66 |
| 2.1.3 | 3 | C4 (72) | 73 | 0.165 | 0.66 |
| 2.1.4 | 4 | F4 (77) | 67 | 0.165 | 0.66 |
| 2.2.1 | 5 | C4 (72) | 84 | 0.165 | 0.66 |
| 2.2.2 | 6 | Ab3 (68) | 65 | 0.165 | 0.66 |
| 2.2.3 | 7 | F3 (65) | 73 | 0.165 | 0.66 |
| 2.2.4 | 8 | Ab3 (68) | 67 | 0.165 | 0.66 |
| 2.3.1 | 9 | C4 (72) | 84 | 0.165 | 0.66 |
| 2.3.2 | 10 | F4 (77) | 65 | 0.165 | 0.66 |
| 2.3.3 | 11 | C4 (72) | 73 | 0.165 | 0.66 |
| 2.3.4 | 12 | Ab3 (68) | 67 | 0.165 | 0.66 |
| 2.4.1 | 13 | F3 (65) | 84 | 0.165 | 0.66 |
| 2.4.2 | 14 | Ab3 (68) | 65 | 0.165 | 0.66 |
| 2.4.3 | 15 | C4 (72) | 73 | 0.165 | 0.66 |
| 2.4.4 | 16 | Ab3 (68) | 67 | 0.165 | 0.66 |
| 3.1.1 | 1 | Ab3 (68) | 84 | 0.165 | 0.66 |
| 3.1.2 | 2 | C4 (72) | 65 | 0.165 | 0.66 |
| 3.1.3 | 3 | Eb4 (75) | 73 | 0.165 | 0.66 |
| 3.1.4 | 4 | Ab4 (80) | 67 | 0.165 | 0.66 |
| 3.2.1 | 5 | Eb4 (75) | 84 | 0.165 | 0.66 |
| 3.2.2 | 6 | C4 (72) | 65 | 0.165 | 0.66 |
| 3.2.3 | 7 | Ab3 (68) | 73 | 0.165 | 0.66 |
| 3.2.4 | 8 | C4 (72) | 67 | 0.165 | 0.66 |
| 3.3.1 | 9 | Eb4 (75) | 84 | 0.165 | 0.66 |
| 3.3.2 | 10 | Ab4 (80) | 65 | 0.165 | 0.66 |
| 3.3.3 | 11 | Eb4 (75) | 73 | 0.165 | 0.66 |
| 3.3.4 | 12 | C4 (72) | 67 | 0.165 | 0.66 |
| 3.4.1 | 13 | Ab3 (68) | 84 | 0.165 | 0.66 |
| 3.4.2 | 14 | C4 (72) | 65 | 0.165 | 0.66 |
| 3.4.3 | 15 | Eb4 (75) | 73 | 0.165 | 0.66 |
| 3.4.4 | 16 | C4 (72) | 67 | 0.165 | 0.66 |
| 4.1.1 | 1 | Bb3 (70) | 84 | 0.165 | 0.66 |
| 4.1.2 | 2 | D4 (74) | 65 | 0.165 | 0.66 |
| 4.1.3 | 3 | F4 (77) | 73 | 0.165 | 0.66 |
| 4.1.4 | 4 | Bb4 (82) | 67 | 0.165 | 0.66 |
| 4.2.1 | 5 | F4 (77) | 84 | 0.165 | 0.66 |
| 4.2.2 | 6 | D4 (74) | 65 | 0.165 | 0.66 |
| 4.2.3 | 7 | Bb3 (70) | 73 | 0.165 | 0.66 |
| 4.2.4 | 8 | D4 (74) | 67 | 0.165 | 0.66 |
| 4.3.1 | 9 | F4 (77) | 84 | 0.165 | 0.66 |
| 4.3.2 | 10 | Bb4 (82) | 65 | 0.165 | 0.66 |
| 4.3.3 | 11 | F4 (77) | 73 | 0.165 | 0.66 |
| 4.3.4 | 12 | D4 (74) | 67 | 0.165 | 0.66 |
| 4.4.1 | 13 | Bb3 (70) | 84 | 0.165 | 0.66 |
| 4.4.2 | 14 | D4 (74) | 65 | 0.165 | 0.66 |
| 4.4.3 | 15 | F4 (77) | 73 | 0.165 | 0.66 |
| 4.4.4 | 16 | D4 (74) | 67 | 0.165 | 0.66 |

</details>

### 06 Glass Bell Counter Arp

Glassy bell: carrier sine A, B sine +7 semitone aktif dengan volume 0 sebagai sumber FM. C5–C6 Cubase/MIDI84–96. Pola eighth-grid dengan jeda; Space reverb menghasilkan atmosfer tanpa pitch-shift shimmer.

[MIDI](MIDI/layer06-glass-bells.mid) · [Preset native](Presets/layer06-glass-bells.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: Analog/Basic Shapes.wav; WT pos 0; warp fm 13% | 0 / 0 cent; semitone 0 | 1 / 0 | 0.42 | filter; F1 balance 0 |
| B | ON: Analog/Basic Shapes.wav; WT pos 0 | 0 / 0 cent; semitone 7 | 1 / 0 | 0 | filter; F1 balance 0 |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; lowpass_12; cutoff 0.73; resonance 6%; drive 0%; key track True; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 4 / 1250 / 0% / 380 |
| ENV2 A/D/S/R | 1 / 280 / 0% / 240 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.36; mono False; poly 16; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 0.18 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator0.pan +9% bipolar |
| LFO2 | 0.37 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator0.fine +0.6% bipolar |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | oscillator0.warp_amount | +12% unipolar |
| velocity | oscillator0.warp_amount | +7% unipolar |
| Macro1 (TONE) | oscillator0.warp_amount | +8% unipolar |
| Macro2 (SPACE) | fx1.wet | +15% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Delay | 27% | kParamTimeL=0.247934; kParamTimeR=0.123967; kParamBeatSync=0; kParamMode=1; kParamFeedback=38; kParamFreq=4800 |
| 2. Reverb | 32% | kParamType=kSpace; kParamSize=69; kParamDelay=22; kParamWidth=100 |
| 3. Utility / band-limit | 100% | kParamHPF=400; kParamLPF=12000; kParamWidth=100 |
| Distortion | OFF | Tidak digunakan |
| Chorus | OFF | Tidak digunakan |
| Compression | OFF | Tidak digunakan |

Macro defaults: 1 TONE=0%, 2 SPACE=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host sidechain OFF sebagai awal; volume rendah dan HP membatasi interferensi.

<details>
<summary>MIDI DATA lengkap — 24 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.2 | 2 | G5 (91) | 62 | 0.3375 | 1.35 |
| 1.1.4 | 4 | Eb5 (87) | 53 | 0.3375 | 1.35 |
| 1.2.4 | 8 | C5 (84) | 58 | 0.3375 | 1.35 |
| 1.3.2 | 10 | Eb5 (87) | 57 | 0.3375 | 1.35 |
| 1.3.4 | 12 | G5 (91) | 64 | 0.3375 | 1.35 |
| 1.4.4 | 16 | C6 (96) | 49 | 0.25 | 1 |
| 2.1.2 | 2 | F5 (89) | 62 | 0.3375 | 1.35 |
| 2.1.4 | 4 | Ab5 (92) | 53 | 0.3375 | 1.35 |
| 2.2.4 | 8 | C6 (96) | 58 | 0.3375 | 1.35 |
| 2.3.2 | 10 | Ab5 (92) | 57 | 0.3375 | 1.35 |
| 2.3.4 | 12 | F5 (89) | 64 | 0.3375 | 1.35 |
| 2.4.4 | 16 | C5 (84) | 49 | 0.25 | 1 |
| 3.1.2 | 2 | Ab5 (92) | 62 | 0.3375 | 1.35 |
| 3.1.4 | 4 | C6 (96) | 53 | 0.3375 | 1.35 |
| 3.2.4 | 8 | Eb5 (87) | 58 | 0.3375 | 1.35 |
| 3.3.2 | 10 | C5 (84) | 57 | 0.3375 | 1.35 |
| 3.3.4 | 12 | Eb5 (87) | 64 | 0.3375 | 1.35 |
| 3.4.4 | 16 | Ab5 (92) | 49 | 0.25 | 1 |
| 4.1.2 | 2 | Bb5 (94) | 62 | 0.3375 | 1.35 |
| 4.1.4 | 4 | F5 (89) | 53 | 0.3375 | 1.35 |
| 4.2.4 | 8 | D5 (86) | 58 | 0.3375 | 1.35 |
| 4.3.2 | 10 | F5 (89) | 57 | 0.3375 | 1.35 |
| 4.3.4 | 12 | Bb5 (94) | 64 | 0.3375 | 1.35 |
| 4.4.4 | 16 | C5 (84) | 49 | 0.25 | 1 |

</details>

### 07 Warm Ambient Pad

Voicing penuh satu bar per chord. Nada yang sama pada chord berurutan diikat: C3/MIDI60 berlangsung bar 1–3, Ab2/MIDI56 bar 2–3. Attack 620 ms dan release 650 ms sesuai pergantian chord sekitar 1,98 detik.

[MIDI](MIDI/layer07-warm-pad.mid) · [Preset native](Presets/layer07-warm-pad.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: Analog/Basic Mini.wav; WT pos 0 | 0 / 0 cent; semitone 0 | 5 / 0.065 | 0.24 | filter; F1 balance 0 |
| B | ON: Analog/PWM Juno.wav; WT pos 150 | 0 / -3 cent; semitone 0 | 3 / 0.045 | 0.2 | filter; F1 balance 0 |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; moog_lowpass_12; cutoff 0.54; resonance 7%; drive 5%; key track False; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 620 / 1400 / 85% / 650 |
| ENV2 A/D/S/R | 850 / 1800 / 62% / 600 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.38; mono False; poly 16; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 0.125 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | filter0.cutoff +4% bipolar |
| LFO2 | 0.08 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator1.table_position +5% bipolar; oscillator0.pan +5% bipolar |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | filter0.cutoff | +12% unipolar |
| Macro1 (TONE) | filter0.cutoff | +9% unipolar |
| Macro2 (SPACE) | fx1.wet | +14% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Chorus | 37% | kParamRate=0.19; kParamDepth=7; kParamDelay=7; kParamFeedback=8; kParamFilt=3000 |
| 2. Reverb | 22% | kParamType=kVintage; kParamSize=55; kParamDelay=22; kParamWidth=100 |
| 3. Utility / band-limit | 100% | kParamHPF=230; kParamLPF=7500; kParamWidth=115 |
| Distortion | OFF | Tidak digunakan |
| Delay | OFF | Tidak digunakan |
| Compression | OFF | Tidak digunakan |

Macro defaults: 1 TONE=0%, 2 SPACE=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host duck 3–4 dB, attack 3 ms, release 160 ms bila perlu gerak disco; native compressor OFF.

<details>
<summary>MIDI DATA lengkap — 9 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | Eb2 (51) + G2 (55) | 70/70 | 4 | 16 |
| 1.1.1 | 1 | C3 (60) | 70 | 12 | 48 |
| 2.1.1 | 1 | F2 (53) | 70 | 4 | 16 |
| 2.1.1 | 1 | Ab2 (56) | 70 | 8 | 32 |
| 3.1.1 | 1 | Eb2 (51) | 70 | 4 | 16 |
| 4.1.1 | 1 | F2 (53) + Bb2 (58) + D3 (62) | 70/70/70 | 4 | 16 |

</details>

### 08 Main Retro Hook

Hook baru dalam C natural minor. Mono/legato, portamento 50 ms; overlap antar nada dalam frase 0,07 beat (≈34,7 ms). Bar 2/4 berhenti tepat pada beat 3-and agar respons whistle punya ruang.

[MIDI](MIDI/layer08-main-lead.mid) · [Preset native](Presets/layer08-main-lead.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: S2 Tables/Default Shapes.wav; WT pos 0 | 0 / 0 cent; semitone 0 | 5 / 0.085 | 0.43 | filter; F1 balance 0 |
| B | ON: S2 Tables/Default Shapes.wav; WT pos 128 | 0 / 0 cent; semitone 0 | 2 / 0.035 | 0.22 | filter; F1 balance 0 |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; moog_lowpass_12; cutoff 0.67; resonance 12%; drive 12%; key track True; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 8 / 380 / 76% / 120 |
| ENV2 A/D/S/R | 4 / 250 / 30% / 90 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.46; mono True; poly 8; legato True; glide 50 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 5.2 Hz; Free, mono/shared True; delay 150 ms; rise 180 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator0.fine +3% bipolar; aux mod_wheel; oscillator1.fine +3% bipolar; aux mod_wheel |
| LFO2 | 0.22 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator1.warp_amount +2% bipolar |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | filter0.cutoff | +18% unipolar |
| velocity | filter0.cutoff | +5% unipolar |
| Macro1 (TONE) | filter0.cutoff | +10% unipolar |
| Macro2 (SPACE) | fx4.wet | +14% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Distortion | 32% | kParamMode=kTapeSat; kParamDrive=24 |
| 2. Compression | 100% | kParamThresh=0.65; kParamRatio=2.4; kParamAttack=15; kParamRelease=90; kParamMakeup=1.7 |
| 3. Chorus | 12% | kParamRate=0.2; kParamDepth=3; kParamDelay=7; kParamFeedback=8; kParamFilt=3000 |
| 4. Delay | 16% | kParamTimeL=0.247934; kParamTimeR=0.123967; kParamBeatSync=0; kParamMode=1; kParamFeedback=23; kParamFreq=4800 |
| 5. Reverb | 18% | kParamType=kHall; kParamSize=60; kParamDelay=22; kParamWidth=100 |
| 6. Utility / band-limit | 100% | kParamHPF=190; kParamLPF=12500; kParamWidth=100 |

Macro defaults: 1 TONE=0%, 2 SPACE=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host sidechain OFF sebagai awal; bila diperlukan duck 1–2 dB, attack 3 ms, release 100 ms.

<details>
<summary>MIDI DATA lengkap — 26 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C3 (60) | 105 | 0.57 | 2.28 |
| 1.1.3 | 3 | Eb3 (63) | 93 | 0.32 | 1.28 |
| 1.1.4 | 4 | G3 (67) | 100 | 0.82 | 3.28 |
| 1.2.3 | 7 | Bb3 (70) | 95 | 0.57 | 2.28 |
| 1.3.1 | 9 | G3 (67) | 105 | 0.82 | 3.28 |
| 1.3.4 | 12 | F3 (65) | 93 | 0.32 | 1.28 |
| 1.4.1 | 13 | Eb3 (63) | 100 | 0.57 | 2.28 |
| 1.4.3 | 15 | D3 (62) | 95 | 0.5 | 2 |
| 2.1.1 | 1 | C3 (60) | 105 | 0.57 | 2.28 |
| 2.1.3 | 3 | F3 (65) | 93 | 0.57 | 2.28 |
| 2.2.1 | 5 | Ab3 (68) | 100 | 0.82 | 3.28 |
| 2.2.4 | 8 | G3 (67) | 95 | 0.32 | 1.28 |
| 2.3.1 | 9 | F3 (65) | 105 | 0.5 | 2 |
| 3.1.1 | 1 | Eb3 (63) | 105 | 0.57 | 2.28 |
| 3.1.3 | 3 | G3 (67) | 93 | 0.57 | 2.28 |
| 3.2.1 | 5 | C4 (72) | 100 | 0.82 | 3.28 |
| 3.2.4 | 8 | Bb3 (70) | 95 | 0.32 | 1.28 |
| 3.3.1 | 9 | Ab3 (68) | 105 | 0.82 | 3.28 |
| 3.3.4 | 12 | G3 (67) | 93 | 0.32 | 1.28 |
| 3.4.1 | 13 | Eb3 (63) | 100 | 0.57 | 2.28 |
| 3.4.3 | 15 | G3 (67) | 95 | 0.5 | 2 |
| 4.1.1 | 1 | D3 (62) | 105 | 0.57 | 2.28 |
| 4.1.3 | 3 | F3 (65) | 93 | 0.57 | 2.28 |
| 4.2.1 | 5 | Bb3 (70) | 100 | 0.82 | 3.28 |
| 4.2.4 | 8 | Ab3 (68) | 95 | 0.32 | 1.28 |
| 4.3.1 | 9 | G3 (67) | 105 | 0.5 | 2 |

</details>

### 09 Whistle Response

Sine lead dengan lapisan square pelan dan vibrato tertunda. Menjawab pada beat 3-and, 4, 4-and di bar 2/4; keheningan bar 1/3 tetap dalam file.

[MIDI](MIDI/layer09-synth-whistle.mid) · [Preset native](Presets/layer09-synth-whistle.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: Analog/Basic Shapes.wav; WT pos 0 | 0 / 0 cent; semitone 0 | 1 / 0 | 0.49 | filter; F1 balance 0 |
| B | ON: S2 Tables/Default Shapes.wav; WT pos 128 | 0 / 0 cent; semitone 0 | 1 / 0 | 0.11 | filter; F1 balance 0 |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; lowpass_12; cutoff 0.66; resonance 12%; drive 0%; key track True; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 15 / 340 / 67% / 90 |
| ENV2 A/D/S/R | 18 / 240 / 28% / 90 |
| ENV3 A/D/S/R | 1 / 300 / 0% / 120 |
| Global | master 0.46; mono True; poly 8; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 5.6 Hz; Free, mono/shared True; delay 110 ms; rise 140 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator0.fine +3% bipolar; oscillator1.fine +3% bipolar |
| LFO2 | 0.24 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator0.pan +3% bipolar |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | filter0.cutoff | +12% unipolar |
| Macro1 (TONE) | filter0.cutoff | +8% unipolar |
| Macro2 (SPACE) | fx2.wet | +13% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Chorus | 12% | kParamRate=0.3; kParamDepth=3; kParamDelay=7; kParamFeedback=8; kParamFilt=3000 |
| 2. Delay | 14% | kParamTimeL=0.247934; kParamTimeR=0.123967; kParamBeatSync=0; kParamMode=1; kParamFeedback=20; kParamFreq=4800 |
| 3. Reverb | 19% | kParamType=kHall; kParamSize=52; kParamDelay=22; kParamWidth=100 |
| 4. Utility / band-limit | 100% | kParamHPF=380; kParamLPF=9500; kParamWidth=100 |
| Distortion | OFF | Tidak digunakan |
| Compression | OFF | Tidak digunakan |

Macro defaults: 1 TONE=0%, 2 SPACE=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host sidechain OFF sebagai awal; biarkan jawaban tetap terbaca.

<details>
<summary>MIDI DATA lengkap — 6 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 2.3.3 | 11 | F4 (77) | 92 | 0.425 | 1.7 |
| 2.4.1 | 13 | Ab4 (80) | 86 | 0.425 | 1.7 |
| 2.4.3 | 15 | G4 (79) | 99 | 0.425 | 1.7 |
| 4.3.3 | 11 | D4 (74) | 92 | 0.425 | 1.7 |
| 4.4.1 | 13 | F4 (77) | 86 | 0.425 | 1.7 |
| 4.4.3 | 15 | C4 (72) | 99 | 0.425 | 1.7 |

</details>

### 10 Riser and Down Impact

Satu preset poly dengan dua gesture. C3/MIDI60 velocity1 ditahan 16 beat untuk noise riser; C2/MIDI48 velocity127 di 1.1.1 ditahan satu beat untuk impact sine pitch-down. Jangan menormalisasi velocity layer ini.

[MIDI](MIDI/layer10-transition-fx.mid) · [Preset native](Presets/layer10-transition-fx.SerumPreset)

**Oscillator dan routing**

| Sumber | Status / waveform | Octave / fine | Unison / detune | Level | Routing |
| --- | --- | --- | --- | --- | --- |
| A | ON: Analog/Basic Shapes.wav; WT pos 0 | -1 / 0 cent; semitone 0 | 1 / 0 | 0 | master; F1 balance 0 |
| B | OFF | 0 / 0 | 1 / 0 | 0 | none |
| C | OFF | 0 / 0 | 1 / 0 | 0 | none |
| Noise | ON: White | 0 / 0 cent; semitone 0 | 1 / 0 | 0 | filter; F1 balance 0 |
| Sub | OFF | 0 / 0 | 1 / 0 | 0 | none |

**Filter dan envelope**

| Modul | Nilai eksplisit |
| --- | --- |
| Filter1 | ON; lowpass_24; cutoff 0.24; resonance 30%; drive 3%; key track False; wet 100%; output parallel |
| Filter2 | OFF; moog_lowpass_24; cutoff 0.5; resonance 10%; drive 0%; key track False; wet 100%; output parallel |
| ENV1 A/D/S/R | 1 / 1000 / 100% / 220 |
| ENV2 A/D/S/R | 7933.884298 / 10 / 100% / 200 |
| ENV3 A/D/S/R | 1 / 380 / 0% / 220 |
| Global | master 0.42; mono False; poly 16; legato False; glide 0 ms; Porta Always OFF; swing0; internal arp OFF |

**LFO1, LFO2, dan matrix**

| LFO | Clock / trigger / shape | Assignment |
| --- | --- | --- |
| LFO1 | 0.25 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator3.pan +8% bipolar; aux velocity inverted |
| LFO2 | 3 Hz; Free, mono/shared True; delay 0 ms; rise 0 ms; triangle (0,0)→(0.5,1)→(1,0) | oscillator3.noise_color +5% bipolar; aux velocity inverted |

| Sumber matrix lain | Tujuan | Depth / polarity / aux |
| --- | --- | --- |
| ENV2 | oscillator3.volume | +70% unipolar; aux velocity inverted |
| ENV2 | filter0.cutoff | +66% unipolar; aux velocity inverted |
| ENV3 | oscillator0.volume | +65% unipolar; aux velocity |
| ENV3 | oscillator0.pitch | +50% unipolar; aux velocity |
| Macro1 (RISE BRIGHT) | filter0.cutoff | +5% unipolar |
| Macro2 (SPACE) | fx2.wet | +10% unipolar |

**FX rack**

| Urutan / modul | Wet | Parameter |
| --- | --- | --- |
| 1. Distortion | 18% | kParamMode=kTapeSat; kParamDrive=12 |
| 2. Delay | 28% | kParamTimeL=0.247934; kParamTimeR=0.123967; kParamBeatSync=0; kParamMode=1; kParamFeedback=37; kParamFreq=4800 |
| 3. Reverb | 38% | kParamType=kSpace; kParamSize=78; kParamDelay=22; kParamWidth=100 |
| 4. Utility / band-limit | 100% | kParamHPF=45; kParamLPF=15000; kParamWidth=100 |
| Chorus | OFF | Tidak digunakan |
| Compression | OFF | Tidak digunakan |

Macro defaults: 1 RISE BRIGHT=0%, 2 SPACE=0%. Semua macro range 0–100%; tujuan/depth di tabel matrix. Posisi0 memakai nilai dasar, posisi100 menambahkan depth penuh; PUMP adalah depth pumping. SPACE memperbesar wet yang dirutekan, bukan mengubah durasi semua FX.

**Sidechain / insert DAW:** Host duck 3–5 dB dari kick, attack 1 ms, release 110 ms; jaga impact tidak menutupi pukulan pertama.

<details>
<summary>MIDI DATA lengkap — 2 nada, 4 bar</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C2 (48) | 127 | 1 | 4 |
| 1.1.1 | 1 | C3 (60) | 1 | 16 | 64 |

</details>

## Drum per layer / per file

Sample konkret belum dipilih atau disalin. Berikut karakter awal yang cocok untuk brief dan mapping Sampler Track; pitch **MIDI60 = C3 Cubase** berlaku untuk seluruh note di masing-masing file. CC7/CC10 pada tabel track merupakan level/pan independen per instrumen.

| File | Karakter sample yang dipilih di DAW | Performa / mapping |
| --- | --- | --- |
| [Kick](MIDI/drum-kick.mid) | Kick disco padat, fundamental sekitar 45–65 Hz, attack jelas, tail sekitar 100–160 ms; hindari tail bass panjang yang menutup sub. | C3/MIDI60, channel10; beats1/2/3/4 setiap bar. |
| [Snare](MIDI/drum-snare.mid) | Snare elektronik 80s: body terkontrol dan snap terang; tail sekitar 120–200 ms. | C3/MIDI60; beats2 dan4. |
| [Clap](MIDI/drum-clap.mid) | Clap disco agak lebar, HP sekitar200 Hz; layer lebih pelan daripada snare. | C3/MIDI60; tepat serempak snare, tanpa offset flam. |
| [Closed hat](MIDI/drum-closed-hat.mid) | Hat terang pendek, tail sekitar30–60 ms. | C3/MIDI60; pola16th, ruang pada step3/7/11/15 untuk open hat. |
| [Open hat](MIDI/drum-open-hat.mid) | Open hat airy offbeat; atur tail sekitar100–150 ms. | C3/MIDI60; step3/7/11/15. Bila dua sampler dapat memakai choke bersama, closed hat memotong open hat berikutnya; jika tidak, pendekkan tail sample. |
| [Shaker](MIDI/drum-shaker.mid) | Shaker lembut pendek, aksen offbeat, pan kanan ringan. | C3/MIDI60; straight16th dengan variasi velocity, tanpa swing. |
| [Crash](MIDI/drum-crash.mid) | Crash tipis berfilter, tail sekitar0,8–1,5 detik; tidak menutup attack kick. | C3/MIDI60; hanya downbeat bar1. |

<details>
<summary>Kick: MIDI lengkap — 16 hit</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C3 (60) | 117 | 0.175 | 0.7 |
| 1.2.1 | 5 | C3 (60) | 109 | 0.175 | 0.7 |
| 1.3.1 | 9 | C3 (60) | 113 | 0.175 | 0.7 |
| 1.4.1 | 13 | C3 (60) | 108 | 0.175 | 0.7 |
| 2.1.1 | 1 | C3 (60) | 117 | 0.175 | 0.7 |
| 2.2.1 | 5 | C3 (60) | 109 | 0.175 | 0.7 |
| 2.3.1 | 9 | C3 (60) | 113 | 0.175 | 0.7 |
| 2.4.1 | 13 | C3 (60) | 108 | 0.175 | 0.7 |
| 3.1.1 | 1 | C3 (60) | 117 | 0.175 | 0.7 |
| 3.2.1 | 5 | C3 (60) | 109 | 0.175 | 0.7 |
| 3.3.1 | 9 | C3 (60) | 113 | 0.175 | 0.7 |
| 3.4.1 | 13 | C3 (60) | 108 | 0.175 | 0.7 |
| 4.1.1 | 1 | C3 (60) | 117 | 0.175 | 0.7 |
| 4.2.1 | 5 | C3 (60) | 109 | 0.175 | 0.7 |
| 4.3.1 | 9 | C3 (60) | 113 | 0.175 | 0.7 |
| 4.4.1 | 13 | C3 (60) | 108 | 0.175 | 0.7 |

</details>

<details>
<summary>Snare: MIDI lengkap — 8 hit</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.2.1 | 5 | C3 (60) | 105 | 0.1375 | 0.55 |
| 1.4.1 | 13 | C3 (60) | 111 | 0.1375 | 0.55 |
| 2.2.1 | 5 | C3 (60) | 105 | 0.1375 | 0.55 |
| 2.4.1 | 13 | C3 (60) | 111 | 0.1375 | 0.55 |
| 3.2.1 | 5 | C3 (60) | 105 | 0.1375 | 0.55 |
| 3.4.1 | 13 | C3 (60) | 111 | 0.1375 | 0.55 |
| 4.2.1 | 5 | C3 (60) | 105 | 0.1375 | 0.55 |
| 4.4.1 | 13 | C3 (60) | 111 | 0.1375 | 0.55 |

</details>

<details>
<summary>Clap: MIDI lengkap — 8 hit</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.2.1 | 5 | C3 (60) | 85 | 0.1375 | 0.55 |
| 1.4.1 | 13 | C3 (60) | 92 | 0.1375 | 0.55 |
| 2.2.1 | 5 | C3 (60) | 85 | 0.1375 | 0.55 |
| 2.4.1 | 13 | C3 (60) | 92 | 0.1375 | 0.55 |
| 3.2.1 | 5 | C3 (60) | 85 | 0.1375 | 0.55 |
| 3.4.1 | 13 | C3 (60) | 92 | 0.1375 | 0.55 |
| 4.2.1 | 5 | C3 (60) | 85 | 0.1375 | 0.55 |
| 4.4.1 | 13 | C3 (60) | 92 | 0.1375 | 0.55 |

</details>

<details>
<summary>Closed Hat: MIDI lengkap — 48 hit</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C3 (60) | 72 | 0.08 | 0.32 |
| 1.1.2 | 2 | C3 (60) | 49 | 0.08 | 0.32 |
| 1.1.4 | 4 | C3 (60) | 56 | 0.08 | 0.32 |
| 1.2.1 | 5 | C3 (60) | 72 | 0.08 | 0.32 |
| 1.2.2 | 6 | C3 (60) | 49 | 0.08 | 0.32 |
| 1.2.4 | 8 | C3 (60) | 56 | 0.08 | 0.32 |
| 1.3.1 | 9 | C3 (60) | 72 | 0.08 | 0.32 |
| 1.3.2 | 10 | C3 (60) | 49 | 0.08 | 0.32 |
| 1.3.4 | 12 | C3 (60) | 56 | 0.08 | 0.32 |
| 1.4.1 | 13 | C3 (60) | 72 | 0.08 | 0.32 |
| 1.4.2 | 14 | C3 (60) | 49 | 0.08 | 0.32 |
| 1.4.4 | 16 | C3 (60) | 56 | 0.08 | 0.32 |
| 2.1.1 | 1 | C3 (60) | 72 | 0.08 | 0.32 |
| 2.1.2 | 2 | C3 (60) | 49 | 0.08 | 0.32 |
| 2.1.4 | 4 | C3 (60) | 56 | 0.08 | 0.32 |
| 2.2.1 | 5 | C3 (60) | 72 | 0.08 | 0.32 |
| 2.2.2 | 6 | C3 (60) | 49 | 0.08 | 0.32 |
| 2.2.4 | 8 | C3 (60) | 56 | 0.08 | 0.32 |
| 2.3.1 | 9 | C3 (60) | 72 | 0.08 | 0.32 |
| 2.3.2 | 10 | C3 (60) | 49 | 0.08 | 0.32 |
| 2.3.4 | 12 | C3 (60) | 56 | 0.08 | 0.32 |
| 2.4.1 | 13 | C3 (60) | 72 | 0.08 | 0.32 |
| 2.4.2 | 14 | C3 (60) | 49 | 0.08 | 0.32 |
| 2.4.4 | 16 | C3 (60) | 56 | 0.08 | 0.32 |
| 3.1.1 | 1 | C3 (60) | 72 | 0.08 | 0.32 |
| 3.1.2 | 2 | C3 (60) | 49 | 0.08 | 0.32 |
| 3.1.4 | 4 | C3 (60) | 56 | 0.08 | 0.32 |
| 3.2.1 | 5 | C3 (60) | 72 | 0.08 | 0.32 |
| 3.2.2 | 6 | C3 (60) | 49 | 0.08 | 0.32 |
| 3.2.4 | 8 | C3 (60) | 56 | 0.08 | 0.32 |
| 3.3.1 | 9 | C3 (60) | 72 | 0.08 | 0.32 |
| 3.3.2 | 10 | C3 (60) | 49 | 0.08 | 0.32 |
| 3.3.4 | 12 | C3 (60) | 56 | 0.08 | 0.32 |
| 3.4.1 | 13 | C3 (60) | 72 | 0.08 | 0.32 |
| 3.4.2 | 14 | C3 (60) | 49 | 0.08 | 0.32 |
| 3.4.4 | 16 | C3 (60) | 56 | 0.08 | 0.32 |
| 4.1.1 | 1 | C3 (60) | 72 | 0.08 | 0.32 |
| 4.1.2 | 2 | C3 (60) | 49 | 0.08 | 0.32 |
| 4.1.4 | 4 | C3 (60) | 56 | 0.08 | 0.32 |
| 4.2.1 | 5 | C3 (60) | 72 | 0.08 | 0.32 |
| 4.2.2 | 6 | C3 (60) | 49 | 0.08 | 0.32 |
| 4.2.4 | 8 | C3 (60) | 56 | 0.08 | 0.32 |
| 4.3.1 | 9 | C3 (60) | 72 | 0.08 | 0.32 |
| 4.3.2 | 10 | C3 (60) | 49 | 0.08 | 0.32 |
| 4.3.4 | 12 | C3 (60) | 56 | 0.08 | 0.32 |
| 4.4.1 | 13 | C3 (60) | 72 | 0.08 | 0.32 |
| 4.4.2 | 14 | C3 (60) | 49 | 0.08 | 0.32 |
| 4.4.4 | 16 | C3 (60) | 56 | 0.08 | 0.32 |

</details>

<details>
<summary>Open Hat: MIDI lengkap — 16 hit</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.3 | 3 | C3 (60) | 69 | 0.175 | 0.7 |
| 1.2.3 | 7 | C3 (60) | 77 | 0.175 | 0.7 |
| 1.3.3 | 11 | C3 (60) | 69 | 0.175 | 0.7 |
| 1.4.3 | 15 | C3 (60) | 77 | 0.175 | 0.7 |
| 2.1.3 | 3 | C3 (60) | 69 | 0.175 | 0.7 |
| 2.2.3 | 7 | C3 (60) | 77 | 0.175 | 0.7 |
| 2.3.3 | 11 | C3 (60) | 69 | 0.175 | 0.7 |
| 2.4.3 | 15 | C3 (60) | 77 | 0.175 | 0.7 |
| 3.1.3 | 3 | C3 (60) | 69 | 0.175 | 0.7 |
| 3.2.3 | 7 | C3 (60) | 77 | 0.175 | 0.7 |
| 3.3.3 | 11 | C3 (60) | 69 | 0.175 | 0.7 |
| 3.4.3 | 15 | C3 (60) | 77 | 0.175 | 0.7 |
| 4.1.3 | 3 | C3 (60) | 69 | 0.175 | 0.7 |
| 4.2.3 | 7 | C3 (60) | 77 | 0.175 | 0.7 |
| 4.3.3 | 11 | C3 (60) | 69 | 0.175 | 0.7 |
| 4.4.3 | 15 | C3 (60) | 77 | 0.175 | 0.7 |

</details>

<details>
<summary>Shaker: MIDI lengkap — 64 hit</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C3 (60) | 43 | 0.07 | 0.28 |
| 1.1.2 | 2 | C3 (60) | 34 | 0.07 | 0.28 |
| 1.1.3 | 3 | C3 (60) | 61 | 0.07 | 0.28 |
| 1.1.4 | 4 | C3 (60) | 39 | 0.07 | 0.28 |
| 1.2.1 | 5 | C3 (60) | 43 | 0.07 | 0.28 |
| 1.2.2 | 6 | C3 (60) | 34 | 0.07 | 0.28 |
| 1.2.3 | 7 | C3 (60) | 61 | 0.07 | 0.28 |
| 1.2.4 | 8 | C3 (60) | 39 | 0.07 | 0.28 |
| 1.3.1 | 9 | C3 (60) | 43 | 0.07 | 0.28 |
| 1.3.2 | 10 | C3 (60) | 34 | 0.07 | 0.28 |
| 1.3.3 | 11 | C3 (60) | 61 | 0.07 | 0.28 |
| 1.3.4 | 12 | C3 (60) | 39 | 0.07 | 0.28 |
| 1.4.1 | 13 | C3 (60) | 43 | 0.07 | 0.28 |
| 1.4.2 | 14 | C3 (60) | 34 | 0.07 | 0.28 |
| 1.4.3 | 15 | C3 (60) | 61 | 0.07 | 0.28 |
| 1.4.4 | 16 | C3 (60) | 39 | 0.07 | 0.28 |
| 2.1.1 | 1 | C3 (60) | 43 | 0.07 | 0.28 |
| 2.1.2 | 2 | C3 (60) | 34 | 0.07 | 0.28 |
| 2.1.3 | 3 | C3 (60) | 61 | 0.07 | 0.28 |
| 2.1.4 | 4 | C3 (60) | 39 | 0.07 | 0.28 |
| 2.2.1 | 5 | C3 (60) | 43 | 0.07 | 0.28 |
| 2.2.2 | 6 | C3 (60) | 34 | 0.07 | 0.28 |
| 2.2.3 | 7 | C3 (60) | 61 | 0.07 | 0.28 |
| 2.2.4 | 8 | C3 (60) | 39 | 0.07 | 0.28 |
| 2.3.1 | 9 | C3 (60) | 43 | 0.07 | 0.28 |
| 2.3.2 | 10 | C3 (60) | 34 | 0.07 | 0.28 |
| 2.3.3 | 11 | C3 (60) | 61 | 0.07 | 0.28 |
| 2.3.4 | 12 | C3 (60) | 39 | 0.07 | 0.28 |
| 2.4.1 | 13 | C3 (60) | 43 | 0.07 | 0.28 |
| 2.4.2 | 14 | C3 (60) | 34 | 0.07 | 0.28 |
| 2.4.3 | 15 | C3 (60) | 61 | 0.07 | 0.28 |
| 2.4.4 | 16 | C3 (60) | 39 | 0.07 | 0.28 |
| 3.1.1 | 1 | C3 (60) | 43 | 0.07 | 0.28 |
| 3.1.2 | 2 | C3 (60) | 34 | 0.07 | 0.28 |
| 3.1.3 | 3 | C3 (60) | 61 | 0.07 | 0.28 |
| 3.1.4 | 4 | C3 (60) | 39 | 0.07 | 0.28 |
| 3.2.1 | 5 | C3 (60) | 43 | 0.07 | 0.28 |
| 3.2.2 | 6 | C3 (60) | 34 | 0.07 | 0.28 |
| 3.2.3 | 7 | C3 (60) | 61 | 0.07 | 0.28 |
| 3.2.4 | 8 | C3 (60) | 39 | 0.07 | 0.28 |
| 3.3.1 | 9 | C3 (60) | 43 | 0.07 | 0.28 |
| 3.3.2 | 10 | C3 (60) | 34 | 0.07 | 0.28 |
| 3.3.3 | 11 | C3 (60) | 61 | 0.07 | 0.28 |
| 3.3.4 | 12 | C3 (60) | 39 | 0.07 | 0.28 |
| 3.4.1 | 13 | C3 (60) | 43 | 0.07 | 0.28 |
| 3.4.2 | 14 | C3 (60) | 34 | 0.07 | 0.28 |
| 3.4.3 | 15 | C3 (60) | 61 | 0.07 | 0.28 |
| 3.4.4 | 16 | C3 (60) | 39 | 0.07 | 0.28 |
| 4.1.1 | 1 | C3 (60) | 43 | 0.07 | 0.28 |
| 4.1.2 | 2 | C3 (60) | 34 | 0.07 | 0.28 |
| 4.1.3 | 3 | C3 (60) | 61 | 0.07 | 0.28 |
| 4.1.4 | 4 | C3 (60) | 39 | 0.07 | 0.28 |
| 4.2.1 | 5 | C3 (60) | 43 | 0.07 | 0.28 |
| 4.2.2 | 6 | C3 (60) | 34 | 0.07 | 0.28 |
| 4.2.3 | 7 | C3 (60) | 61 | 0.07 | 0.28 |
| 4.2.4 | 8 | C3 (60) | 39 | 0.07 | 0.28 |
| 4.3.1 | 9 | C3 (60) | 43 | 0.07 | 0.28 |
| 4.3.2 | 10 | C3 (60) | 34 | 0.07 | 0.28 |
| 4.3.3 | 11 | C3 (60) | 61 | 0.07 | 0.28 |
| 4.3.4 | 12 | C3 (60) | 39 | 0.07 | 0.28 |
| 4.4.1 | 13 | C3 (60) | 43 | 0.07 | 0.28 |
| 4.4.2 | 14 | C3 (60) | 34 | 0.07 | 0.28 |
| 4.4.3 | 15 | C3 (60) | 61 | 0.07 | 0.28 |
| 4.4.4 | 16 | C3 (60) | 39 | 0.07 | 0.28 |

</details>

<details>
<summary>Crash: MIDI lengkap — 1 hit</summary>

| Posisi bar.beat.16th | Step bar (1–16) | Pitch Cubase (MIDI) | Velocity | Durasi beat | Durasi step 16th |
| --- | ---: | --- | --- | ---: | ---: |
| 1.1.1 | 1 | C3 (60) | 94 | 0.25 | 1 |

</details>

## Batas implementasi yang perlu diperhatikan

- **Sub Direct vs low-pass:** Direct sengaja melewati filter/FX Serum. Filter LP24 disimpan OFF sebagai acuan, sehingga low-pass80 Hz yang diminta berada pada insert DAW. Pilihan triangle memenuhi opsi waveform brief; kandungan harmonik sebelum insert LP tetap ada. PUMP internal merupakan LFO beat-sync dan belum diuji phase terhadap transport; compressor sidechain host mengikuti kick sebenarnya.
- **Delay stereo/ping-pong:** file menyimpan L=0,247934 s (1/8), R=0,123967 s (1/16), beat syncOFF dan `kParamMode=1`, nilai yang ditemukan dalam preset Factory ARP–Aardvark. Arti UI mode1 belum diverifikasi; untuk ping-pong persis, pilih **Ping-Pong** di UI Serum dan konfirmasi interval saat playback. Waktu delay native ditetapkan untuk121 BPM, sehingga harus disetel ulang bila tempo diubah.
- **Bell shimmer:** file menggunakan FM + Space reverb + stereo delay. Tidak ada pitch-shift shimmer yang tersimpan. Ini memenuhi pilihan atmosfer Space; bila memerlukan shimmer beroktaf, tambah pitch-shift reverb/return di DAW.
- **Layer10:** selector velocity berupa scaling aux matrix, bukan hard split. Pada velocity1 carrier impact masih menerima sekitar1/127 scaling dan bisa bocor sangat pelan; pada velocity127 noise inverted-velocity menjadi0. Riser ENV2 attack=7,933884 s, impact ENV3 decay380 ms. Route ENV3→pitch depth+50% memberi pitch turun saat envelope turun; besaran semitone efektif belum diuji di plugin. Tetap gunakan velocity1/127 yang sudah ditulis.
- **EQ, macro dan balance:** titik awal sound sudah tersimpan; belum ada pengukuran level, peak, mono compatibility, envelope Direct, atau hasil macro ekstrem melalui audio. Mulai playback dengan fader rendah, lalu balance sesuai sample drum dan register tiap sound.

## Instrumen eksternal dan dependency

Semua instrumen synth memakai **Serum 2**. Instrumen eksternal hanya drum: **Cubase Sampler Track** atau sampler one-shot pilihan Anda. Set root C3/MIDI60, channel10, satu sample per track, one-shot untuk drum; gunakan note-gated jika ingin durasi MIDI mengontrol tail. Tidak ada keyswitch atau Program Change.
Preset memakai wavetable factory **Default Shapes**, **Basic Mini**, **Basic Shapes**, dan **PWM Juno**. Semua path dependency ditemukan di instalasi lokal. Tidak ada custom wavetable/sample/IR yang perlu disalin. Saat berpindah komputer, instal factory content Serum 2 yang sama. File native sudah berada di `Presets/`; registry/resource manifest, hash dan readback tersimpan di `_internal/serum/`.

## Verifikasi, asumsi, dan referensi

- **MIDI — PASS:** validate/generate/verify exit0 dan `ok:true`; 17 file SMF1 dengan tepat satu track/instrumen, 480 PPQN, tempo495868 µs/quarter, meter4/4, end tick7680. Total436 note-on, pasangan note-off lengkap, tidak ada overlap pitch sama atau offset onset. Lead memiliki overlap pitch berbeda untuk legato.
- **Preset native — PASS struktural:** 10 `.SerumPreset` benar-benar dibangun melalui server serum-mcp; container XferJson/Zstd/CBOR dapat didecode; source/filter/envelope/LFO/macro/FX/global/matrix cocok dengan spec; arp disabled diperiksa melalui raw switch. Nol unsafe wire type. Hash salinan sama dengan file yang dipasang; dependency ditemukan.
- **Audit musikal offline — selesai:** scale C natural minor, voice-leading, root/progresi, posisi drum, artikulasi 16th, chord polyphony dan jeda call/response diperiksa. Ini penilaian berdasarkan MIDI/spec, belum penilaian mix audio.
- **Pemuatan native dalam plugin — BELUM DIUJI.** Impor/drag-and-drop Cubase — BELUM DIUJI. Render/analisis audio — BELUM DILAKUKAN. Listening aktual — BELUM DILAKUKAN. Tidak ada klaim `.cpr` atau preview audio.
- **Asumsi berdampak:** register Sub disetujui C0/F0/Ab0/Bb0; 4-bar loop sesuai panjang eksplisit; warna chord7 dan Bb6 di bar4; common-tone pad ties; 7 drum dipilih sebagai bagian performa, sample tetap pilihan pengguna.
- Referensi karakter produksi: [Synth Ctrl — Take My Breath Breakdown](https://synthctrl.com/blogs/blog/the-weeknd-take-my-breath-breakdown), terutama envelope filter, velocity dan ruang synth; [Resident Advisor — ulasan Take My Breath](https://ra.co/reviews/34172) untuk konteks arp Moroder/disco. Artikel merupakan referensi pendekatan, bukan bukti patch asli rekaman.
- Referensi parameter lokal: Factory **BA–Eighty** (filter envelope cepat/drive), **PD–Analog Butter** (independent pad movement/space). Hanya struktur yang diperiksa; preset referensi tidak diaudisi pada run ini.

Untuk audit teknis: [_internal/source/composition.json](_internal/source/composition.json), [_internal/source/preset-specs.json](_internal/source/preset-specs.json), [receipt preset](_internal/serum/manifest.json), dan [receipt final](_internal/final-receipt.json).
