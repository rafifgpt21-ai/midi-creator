# Neon Breath — Lagu Penuh v002

**121 BPM · C minor · 4/4 · 168 bar · 5:33.22 (333.223296 detik).**

Revisi ini mengembangkan loop empat bar menjadi lagu instrumental penuh dengan 12 bagian. **10 layer synth Serum 2 + 7 drum terpisah**. Semua 17 MIDI mulai di bar1 dan berakhir di bar169, dengan tepat satu track/instrumen per file. Versi v001 tetap disimpan.

## Import versi lagu penuh di Cubase

1. Gunakan file dari **`v002/MIDI/`** pada tabel di bawah. Ganti part loop lama dengan file lagu penuh pada track yang sama; jangan menumpuk kedua versi pada track yang sama.
2. Set tempo121 BPM, meter4/4, Musical Time Base. Left locator **1.1.1.0**, right locator **169.1.1.0**. Setelah impor, zoom seluruh part untuk melihat168 bar; panjang tiap file termasuk keheningan awal dan akhir.
3. Gunakan **Import to Left Locator** untuk memasukkan dari bar1; **Import Dropped File as Single Part** bila drag-and-drop. Pada project bertempo tetap, **Ignore Master Track Events on Merge** menjaga tempo project.
4. Sepuluh preset pada `Presets/` identik dengan v001. Jika preset v001 sudah dimuat, gunakan sound yang sama; untuk memuat dari paket pilih **Load Preset** di Serum2 dan file native yang sesuai. Browser instalasi v001 tetap berada di User/MIDI Creator/20261012-neon-breath-121/v001.
5. Drum tetap satu sample per Sampler Track: root **C3 Cubase/MIDI60**, channel10. Semua MIDI drum memakai pitch60, sehingga perlu tujuh sampler terpisah. Sample tetap pilihan Anda.
6. Sub Direct membutuhkan insert **LP80 Hz/24 dB per oktav** serta sidechain audio dari kick. Bila memakai sidechain host, set macro PUMP=0 agar pumping LFO tidak ikut mendobel. Internal arp Serum tetapOFF karena semua event arp sudah ada dalam MIDI.

## Bentuk lagu dan cue waktu

| Bagian | Bar | Waktu awal–akhir | Perkembangan |
| --- | --- | --- | --- |
| Intro | 1–16 | 0:00.00–0:31.74 | Pad/bell dahulu; sub dan kick masuk bar5, stabs/arp bar9, cuplikan hook bar13. Riser13–16 menuju verse. |
| Verse 1 | 17–32 | 0:31.74–1:03.47 | Bass berjalan, stabs lebih jarang, arp berjarak; hook dipotong menjadi call pendek dan jawaban whistle. |
| Pre-Chorus 1 | 33–40 | 1:03.47–1:19.34 | Arp eighth menjadi16th, hat/shaker lebih rapat, lead memakai chord tones naik. Riser37–40. |
| Chorus 1 | 41–56 | 1:19.34–1:51.07 | Hook utama, brass tiap downbeat, groove penuh. Setiap siklus memakai variasi arp dan ending hook. |
| Post-Chorus | 57–64 | 1:51.07–2:06.94 | Lead utama beristirahat; arp/bell/whistle meneruskan motif di atas bass dan drum. |
| Verse 2 | 65–80 | 2:06.94–2:38.68 | Bass eighth pada delapan bar pertama lalu16th; countertexture dan fragment lead lebih aktif. |
| Pre-Chorus 2 | 81–88 | 2:38.68–2:54.55 | Build harmoni lebih kuat, brass akhir frase, riser85–88 dan snare/clap fill. |
| Chorus 2 | 89–104 | 2:54.55–3:26.28 | Full groove, tambahan brass accent setiap delapan bar; riser101–104 melepas energi ke breakdown. |
| Breakdown | 105–120 | 3:26.28–3:58.02 | Kick berhenti selama12 bar, bass rhythm diam; pad/FM bells/lead panjang. Sub kembali bar113, kick bar117. |
| Build | 121–128 | 3:58.02–4:13.88 | Bass eighth→16th, arp bertambah rapat, snare makin aktif. Riser125–128; beat4 bar128 dibiarkan kosong pada kick. |
| Final Chorus | 129–152 | 4:13.88–5:01.49 | 24 bar klimaks: motif asli, ending alternatif dan lift oktaf pilihan, brass/fill drum berulang dengan variasi. |
| Outro | 153–168 | 5:01.49–5:33.22 | Layer dilepas bertahap; cadence Cm bar165. Note-off terakhir di166.1.1; bar166–168 memberi ruang tail. |

Cm–Fm–Ab–Bb tetap satu chord per bar; siklus dimulai dari Cm pada setiap bagian. Stab memakai warna Cm7/Fm7/Abmaj7; voicing G–Bb–D–F di atas bass Bb menghasilkan Bb6. Pada bar165 lagu kembali ke Cm untuk penutup. Intro/outro dan breakdown mempunyai keheningan yang sengaja ditulis; chorus memakai four-on-the-floor penuh.

## Track, MIDI, preset dan pemakaian

| Track | MIDI lagu168 bar | Native preset / instrumen | Jumlah nada | CC7 / CC10 |
| --- | --- | --- | ---: | --- |
| 01 Sub Bass | [layer01-sub-bass.mid](MIDI/layer01-sub-bass.mid) | [Preset](Presets/layer01-sub-bass.SerumPreset) | 153 | 99 / 64 |
| 02 Moroder Octave Bass | [layer02-octave-bass.mid](MIDI/layer02-octave-bass.mid) | [Preset](Presets/layer02-octave-bass.SerumPreset) | 2112 | 95 / 64 |
| 03 Analog Chord Stabs | [layer03-chord-stabs.mid](MIDI/layer03-chord-stabs.mid) | [Preset](Presets/layer03-chord-stabs.SerumPreset) | 1860 | 87 / 61 |
| 04 Synth Brass Accents | [layer04-synth-brass.mid](MIDI/layer04-synth-brass.mid) | [Preset](Presets/layer04-synth-brass.SerumPreset) | 204 | 79 / 64 |
| 05 Bright Up Down Arp | [layer05-bright-arp.mid](MIDI/layer05-bright-arp.mid) | [Preset](Presets/layer05-bright-arp.SerumPreset) | 1632 | 72 / 72 |
| 06 Glass Bell Counter Arp | [layer06-glass-bells.mid](MIDI/layer06-glass-bells.mid) | [Preset](Presets/layer06-glass-bells.SerumPreset) | 284 | 60 / 52 |
| 07 Warm Ambient Pad | [layer07-warm-pad.mid](MIDI/layer07-warm-pad.mid) | [Preset](Presets/layer07-warm-pad.SerumPreset) | 389 | 67 / 64 |
| 08 Main Retro Hook | [layer08-main-lead.mid](MIDI/layer08-main-lead.mid) | [Preset](Presets/layer08-main-lead.SerumPreset) | 493 | 94 / 64 |
| 09 Whistle Response | [layer09-synth-whistle.mid](MIDI/layer09-synth-whistle.mid) | [Preset](Presets/layer09-synth-whistle.SerumPreset) | 162 | 78 / 68 |
| 10 Riser and Down Impact | [layer10-transition-fx.mid](MIDI/layer10-transition-fx.mid) | [Preset](Presets/layer10-transition-fx.SerumPreset) | 15 | 66 / 64 |
| Kick | [drum-kick.mid](MIDI/drum-kick.mid) | Sampler Track / sample Anda | 592 | 107 / 64 |
| Snare | [drum-snare.mid](MIDI/drum-snare.mid) | Sampler Track / sample Anda | 330 | 91 / 64 |
| Clap | [drum-clap.mid](MIDI/drum-clap.mid) | Sampler Track / sample Anda | 268 | 75 / 64 |
| Closed Hat | [drum-closed-hat.mid](MIDI/drum-closed-hat.mid) | Sampler Track / sample Anda | 1360 | 77 / 58 |
| Open Hat | [drum-open-hat.mid](MIDI/drum-open-hat.mid) | Sampler Track / sample Anda | 528 | 68 / 71 |
| Shaker | [drum-shaker.mid](MIDI/drum-shaker.mid) | Sampler Track / sample Anda | 1536 | 56 / 82 |
| Crash | [drum-crash.mid](MIDI/drum-crash.mid) | Sampler Track / sample Anda | 9 | 57 / 60 |

## Drum, sample dan mapping

Ketujuh MIDI drum memakai **pitch60 (C3 Cubase), channel10**. CC7/CC10 independen berlaku pada masing-masing sampler. Snare/clap berada pada beats2/4, dengan fill straight16th di akhir frase; open hat mengisi offbeat. Closed hat lebih rapat pada chorus/pre/build, shaker bervariasi velocity. Kick menjaga empat ketukan di setiap bar chorus, dengan jeda yang disengaja pada intro/breakdown/build.

Pilih kick disco padat dengan tail sekitar100–160 ms; snare elektronik80s dengan body terkontrol dan snap; clap lebar dengan low-end dikurangi; closed hat pendek30–60 ms; open hat airy100–150 ms; shaker lembut; crash tipis sekitar0,8–1,5 detik. Sample belum dipilih/disalin. Untuk choke hat antar sampler, gunakan routing choke yang didukung atau pendekkan open-hat tail. One-shot playback tidak selalu mengikuti note-off MIDI.

Instrumen eksternal hanya sampler drum (**Cubase Sampler Track** atau sampler one-shot pilihan Anda); root60/channel10, tanpa keyswitch/program change. Tidak ada synth di luar Serum2.

## Perubahan musikal dan sound

Seluruh preset native dipertahankan byte-for-byte. Perubahan v002 ada pada aransemen: density bass/arp, fragmen hook, ending alternatif, lift register, rhythm fills, transition trigger dan outro. Macro default, envelope, LFO dan FX tidak diganti. Jumlah/posisi note berubah; 121 BPM, key, meter, channel, CC7/CC10 dan IDs tetap.

Label nada mengikuti Cubase **C3=MIDI60**. Sub tetap MIDI24/29/32/34 = C0/F0/Ab0/Bb0. Lead pilihan mencapai MIDI79/G4 Cubase; respons whistle berada MIDI72–80, bell MIDI84–96. Onset strict straight1/16, tanpa swing atau random timing; durasi gate tidak harus tepat sepanjang grid.

Semua event lengkap ada dalam MIDI dan [composition source](_internal/source/composition.json). Untuk inspeksi piano-roll, [CSV event per layer](_internal/midi-events/) memuat pitch numerik, bar.beat.16th, velocity dan durasi. Native resource memakai empat factory wavetables Serum2 yang sama; dependency diverifikasi, tanpa custom sample/table/IR.

### Batas implementasi yang tetap berlaku

- Direct Sub melewati filter/FX Serum: LP80 Hz dan real sidechain dari kick berada di DAW. Native PUMP adalah quarter-note LFO, belum diuji phase transport.
- Delay menyimpan eighth L dan sixteenth R pada121 BPM, `kParamMode=1` dari observed factory state. Arti UI ping-pong belum diuji; bila diperlukan pilih Ping-Pong di UI dan periksa timing saat playback.
- FM bell memakai Space reverb; pitch-shift shimmer tidak tersimpan. FX layer10 menggunakan velocity1 riser/127 impact sebagai aux scaling, bukan hard split. Jangan normalize velocity FX; small carrier leakage pada velocity1 tetap mungkin.
- Lima riser berdurasi4 bar memakai envelope asli sekitar7,934 s. Tiga bar tail di akhir merupakan ruang MIDI; panjang decay audio sebenarnya belum diukur. Outro mengurangi layer dan memberi cadence, tanpa CC/fader fade otomatis.

## Verifikasi dan asumsi

- **MIDI PASS:** validate/generate/verify exit0, ok:true. 17 file SMF1, satu track,480 PPQN, tempo495868 µs/quarter, endtick322560, total11,927 note-on; seluruh onset grid1/16 dan panjang sama. Note-on/off lengkap; no same-pitch overlap.
- **Preset PASS struktural:** 10 native `.SerumPreset` tersedia, hash identik dengan v001, decode/readback diperiksa ulang, zero unsafe wire type, semua dependency factory ditemukan. Native files awal dibangun melalui serum-mcp; revisi ini memakai salinan yang sama.
- **Audit musikal offline:** scale/root/pad voice-leading lulus, lead/whistle tidak beririsan secara MIDI, kick chorus four-on-the-floor; 41 blok4 bar berbeda dari41 blok aktif menunjukkan perkembangan aransemen. Cadence Cm bar165 dan tiga bar tail tersedia.
- **Native plugin load, import live Cubase, render/analisis audio dan listening aktual BELUM DIUJI** pada revisi ini. Screenshot pengguna menunjukkan penggunaan Cubase, tetapi tidak membuktikan setiap file/preset v002 sudah dimuat. Tidak ada `.cpr` atau audio preview dibuat.
- Durasi dipilih5:33 dalam rentang5–6 menit; bentuk instrumental tanpa vokal. Progresi/tempo/register sub disetujui tetap dipakai. Sample drum masih pilihan pengguna.

[Receipt final](_internal/final-receipt.json) · [MIDI verification](_internal/final-midi-verification.json) · [Musical audit](_internal/musical-audit.json) · [Preset readback](_internal/serum/manifest.json) · [Revisi asal v001](../v001/README.md)

## Parameter Serum yang dipertahankan

Tabel berikut berasal dari preset yang sama dengan v001. Assignment/modulation dan nilai FX berlaku untuk MIDI lagu penuh v002. Bagian MIDI empat bar pada dokumentasi lama tidak disalin; file pada tabel track di atas berisi aransemen168 bar.

- **Nama nada selalu Cubase: C3=MIDI60.** Angka MIDI di kurung adalah acuan utama. Penamaan standar C4=MIDI60 menyebut semua nada satu oktaf lebih tinggi.
- **Posisi `bar.beat.16th`**: `2.3.3` = bar2, beat3, subdivision ketiga, yaitu beat3-and. Step bar 1–16 ditampilkan juga. Satu step = 0,25 beat ≈123,967 ms =120 tick. Durasi beat dan durasi step adalah gate MIDI, bukan tail reverb.
- Envelope ditulis **A/D/S/R**: attack, decay, release dalam ms; sustain dalam persen. Hold=0; curve attack=50%, decay/release=66,6% mengikuti schema.
- Oscillator detune dan level memakai nilai native/tool **0–1**; octave relatif ke nada MIDI, fine dalam cent. Pan0=tengah. Table position adalah nilai tersimpan `kParamTablePos` 0–256. Default Shapes frame0=saw, sekitar128=square; Basic Shapes frame0=sine, Basic Mini frame0=rounded saw. Identitas frame diperiksa offline dari WAV factory, bukan melalui listening plugin.
- Cutoff filter adalah nilai tersimpan normalized **0–1**, **bukan Hz**. Resonance/drive/wet memakai persen; `level_out=0.5`, stereo50 netral menurut schema. File native memuat nilai ini langsung. Nilai cutoff Hz pada EQ/Utility dan instruksi host ditulis terpisah.
- Label UI ENV1/ENV2 = schema env0/env1; LFO1/LFO2 = lfo0/lfo1. Depth matrix dalam persen normalized, **bukan langsung semitone/cent/Hz**. Bipolar berarti gerak dua arah; depth satu arah jika tidak ditandai.
- LFO `beat_sync=true, rate=0` menggunakan default **1/4** tersimpan tanpa key rate. Untuk `beat_sync=false`, rate eksplisit adalah Hz. Semua kurva LFO ordinary di paket ini triangle 0→1→0; Sub memakai kurva duck khusus.
- FX berikut ditulis dalam urutan rack Main. `kParamTimeL/R` delay dalam detik, chorus depth/delay kira-kira ms, compressor attack/release ms, makeup gain multiplier. FX yang tidak terdaftar **OFF**.
- Compression internal mengatur dinamika sound sendiri. **Sidechain kick audio adalah insert host**, tidak otomatis tersimpan di preset Serum. Semua angka gain-reduction host adalah target awal untuk disetel saat audition.

### 01 Sub Bass

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

### 02 Moroder Octave Bass

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

### 03 Analog Chord Stabs

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

### 04 Synth Brass Accents

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

### 05 Bright Up Down Arp

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

### 06 Glass Bell Counter Arp

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

### 07 Warm Ambient Pad

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

### 08 Main Retro Hook

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

### 09 Whistle Response

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

### 10 Riser and Down Impact

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
