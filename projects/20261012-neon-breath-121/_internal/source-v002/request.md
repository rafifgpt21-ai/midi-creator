# Brief revisi lagu penuh

- Proyek: Neon Breath
- Revisi: v002
- Revisi asal: v001 (loop empat bar)
- Tanggal: 2026-10-13

## Permintaan asli

Pengguna: **“saya lihat ini hanya 4 bar … buat jadi lagu dengan durasi 5-6 menit”**. Screenshot Cubase menunjukkan part versi empat bar; screenshot disimpan di `../reference/cubase-four-bars.png` pada paket revisi.

Permintaan sebelumnya tetap menjadi dasar: 121 BPM, C minor,4/4, Cm–Fm–Ab–Bb, gaya Nu-Disco/Synthwave, 10 synth Serum2 dan drum per layer/per file. Register Sub yang disetujui C0–F0–Ab0–Bb0 memakai label Cubase C3=MIDI60.

## Keputusan musik

- 168 bar, 672 quarter-note beats, 480PPQN, endtick322560; durasi MIDI **333,223296 detik / 5:33,223** termasuk tiga bar tail terakhir.
- Struktur: Intro1–16, Verse1 17–32, Pre1 33–40, Chorus1 41–56, Post57–64, Verse2 65–80, Pre2 81–88, Chorus2 89–104, Breakdown105–120, Build121–128, FinalChorus129–152, Outro153–168.
- Chord cycle empat bar dipertahankan; final cadence Cm pada bar165, note-off terakhir di bar166, ruang tail bar166–168.
- Semua onset strict straight1/16; gate/velocity bervariasi, tanpa swing/jitter. Script deterministik tanpa RNG/seed.
- Perkembangan melalui masuk/keluar layer, bass eighth→sixteenth, pola arp ascending/descending/reordered, hook fragments/answer variants/selected octave lifts, drum fills dan breakdown tanpa kick.
- Hook asli tetap dikenali pada chorus; whistle memakai ruang akhir bar2/4 dalam siklus, tidak menimpa lead. Lead lift mencapai MIDI79; sonic behavior register tambahan belum diaudisi.
- Native riser tetap 4bar, dipicu di bar13/37/85/101/125. Impact dipicu pada boundary yang dipilih. Riser tidak dipanjang-gate menjadi168bar.
- Outro menanggalkan layer, bukan memakai CC fade yang belum didukung schema. Bar165 memberi resolution Cm; panjang file tetap168bar.

## Yang dipertahankan

- Semua **10 preset native v001 identik byte-for-byte**, termasuk macro/routing/FX; source preset-spec dan readback disertakan di v002.
- IDs/nama layer, channel, program hint, CC7/CC10, drum pitch60/channel10 tetap sama. Satu track/instrumen per file.
- Sample drum tetap pilihan pengguna; tidak ada sample dipilih atau disalin, tidak ada instrumen synth eksternal.
- Sub Direct membutuhkan insert LP80 Hz dan actual kick sidechain host. Native pumping LFO, arti UI delay mode1/ping-pong, Space tanpa pitched shimmer dan velocity-crossfade FX mempunyai batas sama seperti v001.
- Versi v001 tetap utuh. File gabungan, audio/stems, perubahan proyek live `.cpr` tidak diminta.

## Daftar layer

| ID | Instrumen | Fungsi |
| --- | --- | --- |
| layer01-sub-bass | Serum2 triangle Sub Direct | Root30–80 Hz |
| layer02-octave-bass | Serum2 saw bass | Groove eighth/16th octave |
| layer03-chord-stabs | Serum2 dual saw | Syncopated harmony |
| layer04-synth-brass | Serum2 brass | Chorus accents/lift |
| layer05-bright-arp | Serum2 pluck | Motif arpeggiated |
| layer06-glass-bells | Serum2 FM bell | Countertexture/air |
| layer07-warm-pad | Serum2 pad | Harmonic glue/ties |
| layer08-main-lead | Serum2 mono/glide | Main instrumental hook |
| layer09-synth-whistle | Serum2 sine/square whistle | Call/response |
| layer10-transition-fx | Serum2 dual gesture FX | Four-bar rises/impact |
| drum-kick/snare/clap/closed-hat/open-hat/shaker/crash | Separate Sampler Tracks | Drum pitch60/channel10 |

## Kriteria penerimaan

1. Durasi5–6 menit dan bentuk lagu lengkap; jangan hanya mengulang identik loop4bar.
2. 17 file MIDI sejajar, 10 preset native tersedia, semua tautan README valid.
3. validate/generate/verify berhasil, format1/satu track, EOT322560, onset strict1/16, no same-pitch overlap.
4. Scale/progresi/phrase development, main lead versus whistle, fill dan ruang ending diperiksa offline.
5. Preset decode/readback/wire types/dependency/hash lulus dan match v001.
6. Pemuatan native/plugin, Cubase import, render/audio analysis/listening tetap dilaporkan terpisah; jangan klaim live operation.

Hasil pemeriksaan tercatat di `../final-receipt.json`, `../musical-audit.json`, `../serum/manifest.json`, dan `../final-midi-verification.json`.
