# Brief komposisi

- Proyek: Neon Breath — Nu-Disco / Synthwave study
- Revisi: v001
- Revisi asal: tidak ada; proyek baru
- Mulai: 2026-10-12 Asia/Jakarta. Selesai: 2026-10-13.

## Permintaan pengguna

Membuat spesifikasi preset Xfer Serum dan susunan file MIDI lengkap untuk 10 layer synth dalam gaya Nu-Disco / Synthwave four-on-the-floor seperti “Take My Breath” The Weeknd. BPM121, C minor, 4/4, progresi empat bar Cm–Fm–Ab–Bb. Setiap layer mempunyai parameter OscA/B, unison/detune/octave, Sub, Noise, filter cutoff/resonance/drive, ENV1/2 ADSR, assignment LFO1/2 dan FX Distortion/Chorus/Delay/Reverb/Compression/Sidechain; semua event MIDI pitch/posisi16th/velocity/durasi empat bar disediakan. Drum diminta **per layer, per file**.

1. Sub mono murni 30–80 Hz, Sub sine/triangle Direct, low-pass ketat, fast attack, sidechain kuat. Sustained C0/F0/Ab−1/Bb−1 awalnya diminta.
2. Moroder octave bass 16th punchy, saw dengan filter decay cepat dan saturasi mid; pola C1↔C2, F0↔F1, Ab0↔Ab1, Bb0↔Bb1.
3. Juno/Jupiter dual saw stab chorus vintage, decay pendek; voicing Cm7/Fm7/Abmaj7/Bb/G, sinkopasi offbeat.
4. Brass80s saw/square unison, slight filter attack swell, heavy hall; chord accent sustained hit pertama setiap bar.
5. Bright pluck up/down16th Cm/Fm/Ab/Bb, fast decay, stereo/ping-pong delay dan cutoff LFO.
6. FM glass bell counterarp lebih lambat/eighth atau dotted-eighth, C5–C6, decay panjang dan shimmer/Space.
7. Warm analog pad dengan LP rendah, attack/release lambat, dimension/chorus; sustained inversions mengikat empat bar.
8. Thick retro saw/pulse main lead, tape/compression/hall, glide sekitar50 ms; catchy C natural minor hook empat bar dengan legato.
9. Square/pulse atau sweet sine whistle dengan vibrato, call/response hanya bar2 dan4 saat lead istirahat.
10. White-noise filter sweep riser dan pitch-down synth impact dengan reverb/delay; sustained trigger empat bar dan hit beat1 bar1.

## Klarifikasi yang disetujui

Pengguna memilih: **“Gunakan register 30–80 Hz: C0–F0–Ab0–Bb0 (disarankan)”** dengan penamaan **Cubase C3=MIDI60**. Jadi sub numerical MIDI24/29/32/34. Ab/Bb dinaikkan satu oktaf dari permintaan awal.

## Keputusan musik

- 121 BPM quarter note, meter4/4, C natural minor; empat bar/16 beat/7680 tick/7,933888 s setelah pembulatan tempo MIDI.
- Satu chord per bar; 10 synth Serum2, 7 drum one-shot Sampler tracks: kick/snare/clap/closed hat/open hat/shaker/crash.
- Straight1/16 strict, tanpa swing, tanpa randomisasi. Gate dan velocity bervariasi; onset tetap grid. Script deterministik tidak memakai seed karena tidak memakai generator acak.
- Pad tie common tones; lead overlap pitch berbeda35 ms, jeda sebelum respons bar2/4; bell high-register pelan agar hook/arp tidak bertabrakan.
- Stab Bb/G memakai upper G–Bb–D–F, sub tetapBb: aggregate Bb6; bass progression tidak diganti menjadiG.
- Layer10 satu preset poly: velocity1 riser, velocity127 impact dengan aux velocity inverted. Continuous crossfade, bukan hard switch. Ini menjaga 10 instrumen synth, satu MIDI per instrumen.
- Semua drum integer pitch60/channel10, C3 Cubase, separate Sampler Track. Sample belum dipilih/ditransfer. Tidak ada gabungan MIDI atau audio diminta.
- Sub triangleDirect disimpan native; LP80 dan real kick sidechain berada di DAW sebab Direct bypasses internal filter/FX. Native PUMP adalah LFO1 quarter-note level duck, bukan audio detection.
- Delay native eighth L + sixteenth R; ping-pong UI belum diverifikasi. Bell memakai Space reverb; tidak ada pitched shimmer. Batas implementasi dicatat di README.

## Referensi dan implementasi

- Penamaan artist/genre adalah arah karakter produksi; tidak ada audio pengguna. Hook dan MIDI disusun baru.
- Web: https://synthctrl.com/blogs/blog/the-weeknd-take-my-breath-breakdown ; https://ra.co/reviews/34172
- Factory native: BA–Eighty, PD–Analog Butter sebagai referensi struktural; ARP–Aardvark sebagai observed delay mode1. Tidak diaudisi pada run ini.
- WAV factory diperiksa offline via FFT untuk identitas sine/saw/square: Basic Shapes frame0 sine, Default Shapes frame0 saw/frame4 square, Basic Mini frame0 saw.
- Build native melalui MCP stdio upstream serum-mcp, schema runtime/readback, commit7299f2eea1acd2ae5a863965f5bd4beedf107ee8. Spec/bindings/receipt terpisah dari composition.

## Kriteria penerimaan dan hasil

- [x] 10 synth MIDI, 10 file native .SerumPreset, 7 drum MIDI per bagian.
- [x] Semua file MIDI satu track/instrumen, tempo/meter/PPQN/start/length sejajar, EOT7680.
- [x] validate/generate/verify exit0, ok:true, strict1/16, tanpa onset offset.
- [x] Native format/readback/wire-type/hash/dependency pemeriksaan offline lulus.
- [x] README per-layer lengkap dengan parameter dan semua event MIDI; cara import, mapping, macro dan batas implementasi tersedia.
- [x] Harmoni/register/pola/kepadatan/ruang frase dinilai offline.
- [ ] Pemuatan native Serum2, impor live Cubase, audio render/analisis dan listening aktual belum diuji.

## Perubahan selama build

- Pada pemeriksaan awal, introspection mengembalikan arp=None untuk switchOFF; receipt membandingkan raw Arp0.kParamEnabled=0 agar statusOFF diverifikasi secara benar.
- HP Utility bell dikoreksi650→400 Hz sebelum preset bell dibuat karena schema FXUtils maksimum400 Hz.
- File native yang sudah dibuat dipertahankan; build hanya dilanjutkan dengan exact spec dan hash yang sama.

Output siap produser: `projects/20261012-neon-breath-121/v001/README.md`, `MIDI/`, `Presets/`. Bahan sumber final di `v001/_internal/source/`.
