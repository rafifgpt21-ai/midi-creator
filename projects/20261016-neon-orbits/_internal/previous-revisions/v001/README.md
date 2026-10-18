# Neon Orbits v001 ? arsip pra-audit

124 BPM ? E harmonic minor ? 4/4 ? 164 bar / 5:17.419 ? 13 layer.

Versi ini dipertahankan untuk jejak revisi. Gunakan [v002 final](../../../v002/README.md). v002 memperbaiki delapan gate bass yang overlap serta lompatan oktaf lead di bar 139/141; sebelas layer lain tidak berubah. v001 lolos struktur MIDI/preset, tetapi temuan musikal tersebut belum dirapikan di arsip ini.

## Loading dan sound

Atur Cubase 124 BPM, 4/4, Musical Time Base; left locator 1.1.1.0, Import to Left Locator atau drop Single Part ke bar 1. Muat satu Serum 2 per synth dan preset pasangannya. Pertahankan keheningan awal. Semua file satu track dan sejajar 164 bar. CC1 menggerakkan cutoff. Sample drum belum dipilih: buat enam sampler terpisah, tiap bagian root C3 Cubase / MIDI 60, channel 10. Semua instrumen non-drum memakai Serum 2. Library factory wajib; tidak ada custom resource.

| Synth | MIDI | Preset |
| --- | --- | --- |
| analog-lead | [analog-lead.mid](MIDI/analog-lead.mid) | [analog-lead.SerumPreset](Presets/analog-lead.SerumPreset) |
| glass-keys | [glass-keys.mid](MIDI/glass-keys.mid) | [glass-keys.SerumPreset](Presets/glass-keys.SerumPreset) |
| juno-pad | [juno-pad.mid](MIDI/juno-pad.mid) | [juno-pad.SerumPreset](Presets/juno-pad.SerumPreset) |
| mono-bass | [mono-bass.mid](MIDI/mono-bass.mid) | [mono-bass.SerumPreset](Presets/mono-bass.SerumPreset) |
| phase-seven-pluck | [phase-seven-pluck.mid](MIDI/phase-seven-pluck.mid) | [phase-seven-pluck.SerumPreset](Presets/phase-seven-pluck.SerumPreset) |
| poly-brass | [poly-brass.mid](MIDI/poly-brass.mid) | [poly-brass.SerumPreset](Presets/poly-brass.SerumPreset) |
| three-two-pulse | [three-two-pulse.mid](MIDI/three-two-pulse.mid) | [three-two-pulse.SerumPreset](Presets/three-two-pulse.SerumPreset) |

Tone default 15 membuka cutoff; Contour default 20 memperpanjang envelope timbre. Delay 241.935 ms sesuai 124 BPM; retime jika tempo diubah. Bass/lead mono, pad/brass poly. Model analog adalah pendekatan keluarga instrumen terawat; pad DCO memakai tabel PWM tunggal/chorus, lead/brass VCO memakai detune kecil, tanpa drift/noise FM/tape otomatis. Key E F# G A B C D#, on-grid tanpa swing, strict 1/48 dan 960 PPQN.

## Drum

- [kick.mid](MIDI/kick.mid): kick elektronik bulat, body 100-180 ms; trigger 60, channel 10.
- [snare-clap.mid](MIDI/snare-clap.mid): snare/clap gated 80-an, backbeat 2/4; trigger 60, channel 10.
- [closed-hat.mid](MIDI/closed-hat.mid): hat kering dan pendek; trigger 60, channel 10.
- [open-hat.mid](MIDI/open-hat.mid): hat offbeat, tail 100-200 ms; atur choke/envelope; trigger 60, channel 10.
- [synth-tom.mid](MIDI/synth-tom.mid): tom elektronik E/B bila dituning, untuk fill; trigger 60, channel 10.
- [crash.mid](MIDI/crash.mid): crash pendek untuk aksen bagian; trigger 60, channel 10.

## Bentuk dan verifikasi

Intro 1-16, groove 17-32, build 33-48, drop 49-80, breakdown 81-96, rebuild 97-112, drop kedua 113-144, outro 145-160, coda/release 161-164. Arp 7/8 menyilang 4/4 dan realign tiap 7 bar; 3:2 pada bar 57-72 dan 121-136. Harmoni utama Emadd9-Cmaj7-Amadd9-B7b9, breakdown memakai F#m7b5 dan D#dim7. Akhir Em, tiga bar tanpa serangan baru. Materi orisinal, referensi artis konseptual tanpa transkripsi.

Validate/generate/verify MIDI dan struktur native preset lulus. Pemuatan preset dalam plugin, render audio, live import Cubase, dan actual listening belum dilakukan. Bukti teknis berada di _internal/. Gunakan README v002 untuk audit musikal final.
