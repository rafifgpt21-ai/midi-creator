# Brief komposisi

- Proyek: Yey — Humanized Reference Arrangement
- Revisi: v001
- Revisi asal: MIDI pengguna `yey.mid`; bukan aransemen proyek lain.
- Tanggal mulai: 2026-10-12, Asia/Jakarta.

## Permintaan asli

> (120bpm) ini adalah piano midi buatan saya, saya ingin kamu buat ini lebih humanize, dengan tastefull improfisasi, tanpa mengganti chord progression, tapi saya ingin transisi antar chordnya lebih natural, jangan ganti progression dan struktur, semua berdasarkan file midi ini
>
> generate file ini (sound nya saya yang pilih)
>
> untuk midi piano; midi strings chord; midi strings solo; bass (precision bass fender (vst)); dan aksen flute untuk counter melody dari solo

Follow-up pengguna 2026-10-13:

> untuk flute nya, di arrange ulang saja sesuai dengan apa yang menurutmu bagus

## Keputusan musik

- Gaya/mood: aransemen chamber-pop instrumental lembut mengikuti figur piano dan motif melodi sumber; tidak menambahkan drum atau bagian baru.
- Tempo: 120 quarter-note BPM, persis sumber.
- Meter: 4/4, persis sumber.
- Pusat tonal: F# Dorian pada vamp F#m–B/D#, dengan D natural pada D6. Label conductor sumber `D Dorian - 120 BPM` tidak sesuai pitch aktual, sehingga tidak digunakan untuk mengubah nada.
- Panjang: 76 bar / 304 quarter beats / 152 detik, 480 PPQN, end tick 145920. Empat bar awal kosong dipertahankan.
- Bentuk: batas 1, 5, 13, 17, 21, 25, 33, 49, 53, 61; label bagian deskriptif diturunkan dari perubahan figur sumber, bukan restrukturisasi.
- Harmoni: 5–20 [F#m, B/D#] x8; 21–24 D6, E, F#m, E/G#; 25–32 [A, E, B, F#m] x2; 33–48 [F#m, B/D#] x8; 49–52 D6, E, F#m, E/G#; 53–60 [A, E, B, F#m] x2; 61–76 [F#m, B/D#] x8.
- Piano: 445 pitch/onset asli tetap persis; 30 chord-tone ornaments pada ujung frasa. Velocity diatur menurut fungsi suara, aksen dan perkembangan sumber; gate dibentuk untuk perpindahan harmoni. Tidak mengubah urutan maupun letak chord.
- Timing: `free` untuk menjaga 46 onset piano off-grid yang sudah ada, termasuk rolled chords. Tidak menambahkan swing atau jitter. Layer baru straight 1/32; melodi sumber diselaraskan paling jauh 1 tick.
- Strings chord: masuk bar 13; 4 suara, common tone ditahan, voice leading optimal (maksimal 3 semitone per suara), re-bow pada batas frasa sumber.
- Strings solo: mempertahankan 71 pitch/motif dari track Flute sumber, satu oktaf lebih rendah; napas pendek di sembilan ujung frasa.
- Bass: mengikuti nada bass terendah sumber, termasuk D# pada B/D# dan G# pada E/G#; E1–B2, tanpa keyswitch.
- Flute: diaransemen ulang secara bebas sesuai follow-up. Dua entrance motif pada bar 33/61 dan sembilan jawaban 2–3 nada setelah solo melepas nada; contour bergantian/berlawanan dengan solo, semua chord tone harmoni saat itu.
- CC7=100, CC10=64 netral untuk seluruh layer. Mix dan sound dipilih pengguna.

| Layer ID | Instrumen target | Fungsi | Program GM internal / rentang MIDI |
| --- | --- | --- | --- |
| piano | Piano pilihan pengguna | Harmoni/motif asli + ornaments | 0 / 40–88 |
| strings-chord | Strings ensemble pilihan pengguna | Chord legato | 48 / 51–69 |
| strings-solo | Solo strings pilihan pengguna | Motif lead dari sumber | 40 / 61–78 |
| precision-bass | Fender Precision Bass VST pilihan pengguna | Root/inversi sumber | 33 / 28–47 |
| flute-counter | Flute pilihan pengguna | Entrance/countermelody akhir frasa solo | 73 / rentang akhir dalam musical-audit.json |

Program GM hanya field schema, tidak dikirim dalam file MIDI. Tidak membuat preset/sound karena pengguna secara eksplisit memilih sound sendiri; ini mengalahkan default Serum/native preset.

## Asumsi dan referensi

- Sumber asli tersimpan utuh di `projects/20261012-yey-humanized/_internal/references/yey.mid`; attachment asli tidak diubah.
- Track `LABS 01` diperlakukan sebagai piano; track `Flute` yang sudah berisi 71 nada diperlakukan sebagai sumber tema solo. Track `Piano 1` dan `Bass` kosong.
- Strings solo menggunakan motif flute asli agar seluruh aransemen berdasarkan sumber. Transposisi oktaf tidak mengubah pitch class.
- Final chord tetap B/D#; tidak membuat resolusi F#m baru maupun memperpanjang tail.
- Seed tetap 20261012. `analyze_reference.py` dan `build_arrangement.py` mereproduksi analisis dan spesifikasi.
- Tidak menulis sustain/expression automation karena kontrak generator tidak memiliki field ini; pengguna mengatur articulation di plugin.

## Perubahan revisi

Performa piano diperhalus, empat layer dimasukkan sesuai fungsi yang diminta. Progresi, urutan chord, posisi perubahan chord, keheningan awal dan panjang sumber dijaga. Melodi track flute sumber dialihkan menjadi strings solo, sementara flute baru berupa counter accents.

## Kriteria penerimaan dan hasil

- Tepat lima `.mid`, masing-masing SMF format 1 dengan tepat satu track instrumen.
- Tempo/meter/PPQN dan global end tick sama untuk semua file.
- Seluruh 445 pitch dan onset piano sumber dipertahankan; 71 pitch class melodi sumber dipertahankan pada solo.
- Chord-tone inventory pada setiap downbeat diperiksa terhadap nada sumber, bass root/inversi tidak diubah.
- Tidak ada pitch overlap pada satu layer, nada macet, Sysex, Bank Select atau Program Change.
- Validate/generate/verify wajib exit 0 dan `ok: true`; bukti akhir tersimpan dalam receipt teknis.
- Output: `projects/20261012-yey-humanized/v001/`.
- Status playback: belum dirender/didengarkan; sound/plugin dan impor live Cubase belum diuji.
