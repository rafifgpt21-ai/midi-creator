# Brief komposisi

- Proyek: Neon di Ujung Malam
- Revisi: v001, komposisi baru
- Revisi asal: tidak ada
- Tanggal: 11 Oktober 2026, Asia/Jakarta

## Permintaan asli

“coba buatkan lagu seperti lagunya the weeknd pada album dawn FM dan after hour (dark synth music),”

## Keputusan musik

- Gaya / mood: instrumental dark synth-pop, nuansa malam, retro analog, melancholic dance groove.
- Tempo: 118 quarter-note BPM; meter 4/4; F# minor dengan E# pada C#7.
- Panjang: 112 bar, 227.7968 detik menurut tempo MIDI; empat bar terakhir tanpa note baru untuk release.
- Bentuk: intro 8 / verse 1 16 / pre 1 8 / chorus 1 16 / interlude 8 / verse 2 16 / pre 2 8 / breakdown 8 / final chorus 16 / outro 8.
- Harmoni utama: F#m9–Dmaj7–Aadd9–E6, masing-masing dua bar. Pre: Bm7–Dmaj7–E6–C#7. Breakdown: Bm7–F#m9–Dmaj7–C#7. Penutup chorus: Bm7–C#7–F#m–F#m, satu bar per chord.
- Groove: verse kick sinkopasi dan snare 2/4; chorus kick empat ketukan, bass offbeat, hat eighth-note dan clap. Tambah shaker pada verse 2 dan final chorus.
- Motif baru delapan bar, register C#5–F#5 dengan ruang jawaban keys; pre-chorus lebih sederhana dan breakdown lebih rendah.
- DAW: import seluruh MIDI di bar 1 Cubase. Semua non-drum Serum 2. Satu kit drum channel 10, mapping eksplisit di README.

| Layer ID | Sound target | Fungsi | GM hint / pitch drum |
| --- | --- | --- | --- |
| pulse-bass | Mono analog pulse | Bass | 38 |
| midnight-pad | Pad PWM dan oscillator hangat | Harmoni | 89 |
| neon-chords | Polyphonic brass-like stabs | Harmoni ritmis | 62 |
| glass-arp | Glassy decaying pluck | Arpeggio | 81 |
| night-hook | Mono saw/pulse singing lead | Melodi | 80 |
| rain-keys | Electric bell-like keys | Jawaban frase | 4 |
| radio-haze | Tonal haze dan filtered brown noise | Tekstur | 95 |
| retro-drums | Kit elektronik retro pilihan pengguna | Percussion | 36,38,39,42,46,49,82 |

## Asumsi dan referensi

Instrumental tanpa vokal/lirik dipilih karena pengguna meminta lagu dan suasana tanpa brief vokal. Tidak ada audio/MIDI referensi yang diberikan atau disalin. Album yang disebut menjadi acuan atmosfer, sementara motif, progresi dalam konteks aransemen, bentuk dan performa ditulis baru. Tidak ada sample konkret dipilih; bank drum pengguna dipertahankan.

Random seed 20261011. Script `build_song.py` menulis spesifikasi sumber. Script `build_sound_specs.py` menulis tujuh spesifikasi sound. `make_native_presets.py` menggunakan koneksi MCP stdio sungguhan ke repo serum-mcp; bukan JSON yang hanya diberi ekstensi preset.

Riset: [wawancara Daniel Lopatin di Synth History](https://www.synthhistory.com/post/three-questions-with-oneohtrix-point-never) menyebut penggunaan Juno-60 dalam penulisan untuk The Weeknd dan arp di Until I Bleed Out. Ini mendasari pilihan PWM pad dan arp sebagai interpretasi sound design; tidak menyatakan emulasi perangkat atau reproduksi lagu. [Wawancara GQ](https://www.gq.com/story/oneohtrix-point-never-magic-oneohtrix-point-never-album-the-weeknd-interview) memberikan konteks kolaborasi synthesizer pada After Hours. Referensi preset lokal Neon Wave diperiksa dengan `find_reference_presets` dan `describe_preset`; file bank itu tidak disalin, diedit, atau dijadikan base preset. Sound baru dibangun dari init factory oleh serum-mcp.

## Perubahan revisi

v001 merupakan komposisi baru. Tidak ada revisi lama yang diubah.

## Kriteria penerimaan dan hasil

- Delapan MIDI, satu track/instrumen per file, SMF format 1.
- Tempo, meter, PPQN, bar 1, dan end-of-track global sama: 118 BPM, 4/4, 960 PPQN, 430080 tick.
- validate / generate / verify: PASS, `ok: true`, 3849 note.
- Tujuh native `.SerumPreset`, nama sesuai layer; oscillator/filter/envelope/LFO/macro/FX/global/mod-route dan metadata nama cocok dengan readback.
- Audit musikal memeriksa fungsi layer, register, harmoni, perkembangan bagian, frase lead, note overlap, groove dan ending. Audit berbasis spesifikasi; belum merupakan listening.
- Hasil: `../../README.md` dari folder sumber akhir, dengan MIDI dan preset pada revisi yang sama.
- Pemuatan preset di plugin: belum diuji. Impor live Cubase: belum diuji. Rendering/listening: belum dilakukan. Tidak ada `.cpr` dibuat.
