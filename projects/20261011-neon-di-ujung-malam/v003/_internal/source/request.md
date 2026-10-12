# Brief komposisi

- Proyek: Neon di Ujung Malam
- Revisi: v003
- Revisi asal: v002 (koreksi timing)
- Tanggal: 2026-10-11

## Permintaan asli

> tulis ulang midi projek ini 20261011-neon-di-ujung-malam dengan menggunakan progresi yang lebih dark dan sedih ala the weeknd, tetap dengan instrumen yang sama

## Keputusan musik

- Mood: dark synth-pop melankolis, harmoni lebih tegang dan hook turun dengan ruang frase.
- Tempo: 118 quarter-note BPM; meter 4/4; F# minor dengan modal mixture dan harmonic minor.
- Panjang: 112 bar / 227.7968 detik; bentuk sama dengan v002, bar 109–112 kosong untuk release.
- Chorus/intro: F#m9 – E(add9) – Dmaj7 – C#7(b9), dua bar per chord. Bass F#–E–D–C#.
- Verse/interlude: F#m9 – F#m(maj9)/E# – F#m7/E – Dmaj7; bass kromatis F#–E#–E–D.
- Pre: Bm9 – Dmaj7 – Gmaj7(#11) – C#7(b9). Gmaj7 adalah borrowed bII.
- Breakdown: Bm9 – F#m(add9)/A – Gmaj7(#11) – C#7(b9).
- Final cadence bar 101–104: Bm9 – Gmaj7(#11) – C#7(b9) – F#m9, satu bar per chord.
- Groove: straight, seluruh onset 1/16; velocity/gate ekspresif tanpa jitter. Drum v002 tetap, chorus pulse bass offbeat dan arp eighth-note renggang di dekat serangan lead.
- DAW: Cubase; tujuh instrumen Serum 2 dengan preset asli, satu sampler/kit pilihan pengguna.

| Layer ID | Sound yang dipertahankan | Fungsi / program GM atau mapping |
| --- | --- | --- |
| pulse-bass | Pulse Bass | Bass mono / 38 |
| midnight-pad | Midnight Pad | Harmoni PWM / 89 |
| neon-chords | Neon Chords | Stab analog / 62 |
| glass-arp | Glass Arp | Pluck / 81 |
| night-hook | Night Hook | Lead mono / 80 |
| rain-keys | Rain Keys | Bell electric keys / 4 |
| radio-haze | Radio Haze | Tekstur tonal/noise / 95 |
| retro-drums | Retro Drum Kit | 36 kick, 38 snare, 39 clap, 42/46 hat, 49 crash, 82 shaker |

## Asumsi dan referensi

Tempo/key/panjang/bentuk dipertahankan untuk membandingkan perubahan harmoni dengan v002. Instrumen berarti layer, program hint, mixer, binding dan preset yang sama. Referensi adalah atmosfer synth gelap dan melankolis; motif baru ditulis tanpa mengambil melodi lagu tertentu. Seed velocity 2026101103; script build_song.py dan harmonic-plan.json dapat direproduksi. Kit/sample belum ditentukan, tidak disalin. Bass turun hingga C#1 (MIDI 25) memakai sound mono yang sama.

## Perubahan revisi

Ketujuh layer tonal ditulis ulang, termasuk voicing, jalur bass, motif hook, urutan arp, keys dan nada/gate haze. Drum MIDI, semua preset native, parameter instrument/mixer, tempo/meter/PPQN, bagian dan panjang dipertahankan. v001 dan v002 tetap utuh.

## Kriteria penerimaan dan hasil

- Delapan file MIDI format 1 dengan tepat satu track instrumen; 3785 nada total.
- Semua tempo/meter/PPQN sama dan end-of-track global 430080 tick.
- Onset 1/16 strict; tanpa offset arp atau jitter; validate/generate/verify lulus.
- Nada ditinjau terhadap harmonic plan, register, resolusi E#–F#, phrase gaps, serta hubungan bass/drum/chord.
- Tujuh preset .SerumPreset byte-identik dengan versi asal, dicek decode/readback dan wire types melalui repo serum-mcp.
- Output: projects/20261011-neon-di-ujung-malam/v003.
- Pemuatan preset dan impor/listening live tidak dilakukan; penilaian musik dari spesifikasi/event.
