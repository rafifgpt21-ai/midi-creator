# Neon di Ujung Malam — v003

**118 BPM · F# minor · 4/4 · 112 bar · 3:47.797 · 960 PPQN**

Revisi harmoni dan motif dari [v002](../v002/README.md), dengan delapan instrumen yang sama. Tujuh preset Serum 2 dan drum dipertahankan persis. Harmoni lebih melankolis: garis bass turun, warna minor-major dan dominant b9. Hook, arp, bass, pad, stabs, keys dan haze ditulis ulang. Referensi atmosfer dark synth-pop; melodi dan aransemen asli, instrumental tanpa vokal.

## Mulai di Cubase

1. Atur **118 BPM, 4/4**, Musical Time Base (ikon not), dan left locator **1.1.1.0**.
2. Buat tujuh instrument track Serum 2 dan satu sampler/kit drum. Muat preset pasangan pada tabel.
3. Preset sama dengan versi awal: browser Serum `User > MIDI Creator > 20261011-neon-di-ujung-malam > v001`. Salinan identik tersedia di `Presets/`; untuk komputer lain salin ke folder User Serum lalu rescan. Factory wavetables Serum 2 diperlukan, tanpa sample/wavetable tambahan.
4. Untuk File > Import > MIDI File aktifkan **Import to Left Locator**. Pada project bertempo tetap 118 BPM, **Ignore Master Track Events on Merge** mempertahankan tempo project. Untuk drag/drop aktifkan **Import Dropped File as Single Part** dan letakkan setiap part di bar 1.
5. Semua file mencakup timeline penuh. Pertahankan keheningan awal; jangan menggeser nada pertama layer yang masuk belakangan ke bar 1. Key Editor Bars+Beats, grid **1/16**; Snap posisi part tidak mengkuantisasi isi nada.
6. Gunakan kit/sample drum pilihan Anda, pitch numerik pada tabel drum. Arp sudah ditulis dalam MIDI; jangan menambah arpeggiator kedua.

[Panduan impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html?contentId=u1NHlJBAfqTrfj0eW_QNMQ). Impor live revisi ini belum diuji.

## Track dan sound

Rentang di bawah adalah nomor MIDI; C4 = 60. Semua onset pada grid straight 1/16. Semua layer synth memakai channel 1; drum channel 10. Program Change, Bank Select dan SysEx tidak dikirim.

| Track / fungsi | Rentang MIDI | MIDI | Preset native / macro |
| --- | --- | --- | --- |
| Pulse Bass — Bass mono; F#–E#–E–D di verse dan F#–E–D–C# di chorus | 25–47 | [pulse-bass.mid](MIDI/pulse-bass.mid) | [pulse-bass.SerumPreset](Presets/pulse-bass.SerumPreset); OPEN, SNAP, WARMTH, SUB |
| Midnight Pad — Voicing minor9/minor-major9, harmoni gelap dengan perpindahan dekat | 54–68 | [midnight-pad.mid](MIDI/midnight-pad.mid) | [midnight-pad.SerumPreset](Presets/midnight-pad.SerumPreset); OPEN, DRIFT, SPACE, GLOW |
| Neon Chords — Stab sinkopasi; menegaskan warna minor dan dominant b9 | 61–74 | [neon-chords.mid](MIDI/neon-chords.mid) | [neon-chords.SerumPreset](Presets/neon-chords.SerumPreset); BITE, BODY, WIDTH, ROOM |
| Glass Arp — Pluck descending; pulsa eighth-note dengan celah di chorus | 73–86 | [glass-arp.mid](MIDI/glass-arp.mid) | [glass-arp.SerumPreset](Presets/glass-arp.SerumPreset); GLASS, DECAY, ECHO, HALO |
| Night Hook — Hook baru turun, nada tertahan dan resolusi E#–F# | 61–73 | [night-hook.mid](MIDI/night-hook.mid) | [night-hook.SerumPreset](Presets/night-hook.SerumPreset); OPEN, BODY, ECHO, SPACE |
| Rain Keys — Jawaban pendek dalam celah frase | 61–71 | [rain-keys.mid](MIDI/rain-keys.mid) | [rain-keys.SerumPreset](Presets/rain-keys.SerumPreset); TINE, LENGTH, CHORUS, ROOM |
| Radio Haze — Tekstur tonal C# / D pada borrowed bII | 73–74 | [radio-haze.mid](MIDI/radio-haze.mid) | [radio-haze.SerumPreset](Presets/radio-haze.SerumPreset); TUNE, DUST, DRIFT, SPACE |
| Retro Drum Kit — Beat retro v002 yang sama, channel 10 | 36–82 | [retro-drums.mid](MIDI/retro-drums.mid) | Sampler/kit pilihan Anda |

Mulai dengan macro default 0%. Sound tidak diubah: macro membuka warna, panjang envelope dan FX sebagaimana versi sebelumnya. Delay Glass Arp/Night Hook tetap **254.237 ms**, setara eighth-note pada 118 BPM; sesuaikan jika tempo diubah. Tidak ada automation macro dalam MIDI.

## Harmoni dan bentuk lagu

Setiap chord di loop berlangsung dua bar, kecuali cadence akhir satu bar per chord. **Verse: F#m9 → F#m(maj9)/E# → F#m7/E → Dmaj7**. Gerakan bass F#–E#–E–D memberi rasa menurun. **Chorus: F#m9 → E(add9) → Dmaj7 → C#7(b9)**, dengan dominant yang kembali ke tonic minor. C#7 memakai E# sebagai major third dan D sebagai b9. Warna ini lebih tegang daripada progresi v002 yang melewati Aadd9.

| Bar | Bagian | Harmoni / perkembangan |
| --- | --- | --- |
| 1–8 | Intro | Loop chorus; pad/haze, bass/arp masuk bar 5, teaser dominant bar 7 |
| 9–24 | Verse 1 | Dua loop verse dengan bass kromatis; stabs jarang dan keys menjawab |
| 25–32 | Pre-chorus 1 | Bm9 → Dmaj7 → Gmaj7(#11) → C#7(b9); borrowed bII menaikkan ketegangan |
| 33–48 | Chorus 1 | Dua loop chorus; hook delapan bar menurun, beat dansa dan bass offbeat |
| 49–56 | Interlude | Loop verse, densitas turun; keys dan teaser hook |
| 57–72 | Verse 2 | Dua loop verse; velocity keys lebih kuat, shaker core masuk bar 65 |
| 73–80 | Pre-chorus 2 | Loop pre yang sama; ketegangan dominant menuju breakdown |
| 81–88 | Breakdown | Bm9 → F#m(add9)/A → Gmaj7(#11) → C#7(b9); lead jarang dan arp/drum kembali bar 85 |
| 89–100 | Final chorus | Loop chorus dan separuh loop berikutnya; hook lebih kuat |
| 101–104 | Cadence | Bm9 → Gmaj7(#11) → C#7(b9) → F#m9; resolusi hook E#–F# |
| 105–108 | Outro | F#m(add9) dua bar, F#m9 dua bar; bass tonic, pad/haze dan satu jawaban hook |
| 109–112 | Release | Empat bar tanpa nada baru/ditahan, sekitar 8.14 detik untuk FX |

Gmaj7(#11) memakai G natural sebagai borrowed bII dari warna Phrygian; key utama tetap F# minor. Tidak ada perpindahan tempo atau swing tersembunyi. Gate dan velocity bervariasi untuk artikulasi. Pad minor-major9 memakai voicing yang menyertakan F#, agar inversion E# tetap mempertahankan identitas tonic minor.

## Drum yang cocok

Performa drum **byte-identik dengan v002**. Gunakan kit elektronik retro dengan transient jelas: kick bulat dengan tail sekitar 100–180 ms, snare singkat dengan gated room, clap tipis di chorus, hat gelap pendek. Low-end harus memberi ruang pada bass C#1–F#1; atur gain/sub berdasarkan kit yang dipilih. Snare backbeat dan clap tepat pada pulsa; ghost note dipertahankan.

| Pitch MIDI | Bagian | Karakter / mapping |
| --- | --- | --- |
| 36 | Kick | Punchy, low-end terkontrol; chorus empat ketukan |
| 38 | Snare | Gated 80-an, ghost/fill lebih lembut |
| 39 | Clap | Lebar dan tipis, bersama snare di chorus |
| 42 | Closed hat | Pendek, warna gelap; velocity berselang-seling |
| 46 | Open hat | Ringkas di offbeat; choke terhadap closed hat |
| 49 | Crash | Lembut di awal blok chorus |
| 82 | Shaker | Halus di verse 2/final chorus; map manual pada sampler |

Sample belum dipilih atau disertakan. Gunakan mode one-shot dan choke hat sesuai kit. CC7=106 dan CC10=64 berlaku pada seluruh kit; atur gain/pan per pad. Note-off drum pendek tidak mengharuskan pemotongan sample.

## Instrumen di luar Serum

Hanya drum memakai sampler/kit pilihan Anda, misalnya Groove Agent SE. Petakan pitch 36–82 sesuai tabel, channel 10, mode one-shot, tanpa keyswitch. Ketujuh instrumen tonal memakai Serum 2 dengan preset asli; tidak ada library baru.

## Verifikasi dan asumsi

| Pemeriksaan | Status |
| --- | --- |
| Validate / generate / verify | PASS; delapan MIDI, 3785 nada, tepat satu track per file |
| Tempo / meter / PPQN / panjang | PASS; 118 BPM, 4/4, 960 PPQN, end-of-track 430080 tick |
| Onset aktual | PASS; seluruh note-on pada grid 1/16; tanpa offset arp/jitter |
| Harmoni / register / frase | Ditinjau melalui spesifikasi dan event; seluruh nada tonal sesuai pitch-class chord sepanjang gate, termasuk saat chord berubah |
| Instrumen / drum / preset | Layer, program hint, mixer, binding sama; drum dan tujuh preset byte-identik dengan v002 |
| Preset native | PASS decode/readback parameter dan CBOR wire-type scan melalui repo serum-mcp |
| Impor Cubase / pemuatan preset / listening | Belum dilakukan untuk revisi ini; tidak ada CPR atau audio render dibuat |

Tempo, panjang, bentuk, sound dan drum dipertahankan sesuai permintaan instrumen yang sama. Bass lebih rendah di jalur turun; sound/gain akhir perlu dinilai saat playback. Instrumen tetap sama meskipun seluruh part tonal ditulis ulang. Seed velocity 2026101103; onset tanpa random timing.

[v001](../v001/README.md) dan [v002](../v002/README.md) tetap utuh. Source, harmonic plan, binding, spesifikasi preset, checksum dan receipt berada di `_internal/`.
