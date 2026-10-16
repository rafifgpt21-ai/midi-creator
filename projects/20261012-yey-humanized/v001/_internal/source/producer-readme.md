# Yey — Humanized Reference Arrangement

**120 BPM · 4/4 · 76 bar · 2:32 · 480 PPQN**

Pusat tonal mengikuti nada sumber: **F# Dorian**, dengan D natural pada bagian D6. Seluruh progresi, letak perubahan chord, urutan bagian dan panjang `yey.mid` dipertahankan. **Empat bar pertama tetap kosong**, seperti file asli; musik mulai bar 5 / detik 8.

Hasil berupa lima MIDI. **Semua sound kamu yang pilih**, termasuk VST Fender Precision Bass. Tidak ada preset, audio, drum atau file gabungan yang dibuat.

## Mulai di Cubase

1. Set project ke **120 BPM, 4/4**. Buat lima instrument track dengan **Musical Time Base**.
2. Pilih piano, ensemble strings, solo strings, Fender Precision Bass dan flute milikmu. Muat sound/artikulasi sebelum impor MIDI.
3. Impor **semua file dari bar 1**, bukan dari nada pertama. Set left locator **1.1.1.0**, lalu gunakan **File > Import > MIDI File > Import to Left Locator**. Untuk drag-and-drop, aktifkan **Import Dropped File as Single Part**.
4. Pada project dengan tempo tetap, gunakan **Ignore Master Track Events on Merge** agar tempo project tetap 120 BPM. Pertahankan keheningan awal dan part sepanjang 76 bar; jangan mengkuantisasi ulang piano bila ingin menjaga rolled timing asli.
5. Atur gain/pan di mixer sesuai sound pilihanmu. MIDI memakai CC7=100 dan CC10=64 untuk semua layer; jika plugin merespons kedua CC itu, filter setelah impor bila ingin memakai nilai mixer berbeda.

Setiap `.mid` berformat SMF 1, tepat satu track dan satu channel instrumen, dengan panjang global 145920 tick. Tidak ada SysEx, Bank Select, Program Change, key/marker atau track conductor tambahan. File MIDI tidak memilih sound otomatis.

## Track dan MIDI

Rentang nada menggunakan **C4=60**; label oktaf Cubase/plugin bisa berbeda, sehingga angka MIDI adalah acuan.

| Track | MIDI | Fungsi dan perubahan | Sound/artikulasi yang kamu muat | Rentang / jumlah nada |
| --- | --- | --- | --- | --- |
| Piano | [piano.mid](MIDI/piano.mid) | Semua 445 pitch dan onset asli tetap; dinamika/gate diperhalus, ditambah 30 nada chord-tone penghubung di ujung frasa | Piano pilihanmu; respons velocity alami | E2–E6 / 40–88 / 475 |
| Strings chord | [strings-chord.mid](MIDI/strings-chord.mid) | Masuk bar 13; empat suara, common tone ditahan dan voice leading halus | Ensemble strings pilihanmu, sustain/legato | D#3–A4 / 51–69 / 162 |
| Strings solo | [strings-solo.mid](MIDI/strings-solo.mid) | Tema berasal dari 71 nada track Flute sumber, satu oktaf lebih rendah; ada napas di ujung frasa | Solo strings pilihanmu, sustained lyrical | C#4–F#5 / 61–78 / 71 |
| Precision Bass — Fender | [precision-bass.mid](MIDI/precision-bass.mid) | Root dan slash-bass sumber; pola fingerstyle ringan dengan pendekatan chord-tone | VST Fender Precision Bass milikmu, fingerstyle/sustain | E1–B2 / 28–47 / 148 |
| Flute counter melody | [flute-counter.mid](MIDI/flute-counter.mid) | **Diarrange ulang**: dua entrance motif serta sembilan jawaban pendek, dengan contour yang melengkapi solo | Flute pilihanmu, soft sustain/legato; tongue ringan untuk nada pendek | C#5–B5 / 73–83 / 28 |

Tidak ada native Serum preset karena kamu meminta memilih sound sendiri. Angka program GM di spesifikasi internal hanya hint schema dan tidak dikirim pada MIDI.

## Bentuk dan progresi sumber

Nama bagian berikut bersifat deskriptif; tidak membuat struktur baru. Setiap chord berumur satu bar, persis harmoni sumber. `B/D#` dan `E/G#` mempertahankan bass inversi asli; D6 memiliki pitch class D–F#–A–B.

| Bar | Bagian sumber | Progresi | Perkembangan aransemen |
| --- | --- | --- | --- |
| 1–4 | Keheningan awal | — | Semua layer diam |
| 5–12 | Tema piano A1 | F#m–B/D# ×4 | Figur piano asli dengan bass ringan |
| 13–16 | Tema ditahan | F#m–B/D# ×2 | Piano panjang; ensemble strings masuk lembut, bass ditahan |
| 17–20 | Tema piano A2 | F#m–B/D# ×2 | Gerak piano kembali, dinamika meningkat |
| 21–24 | Transisi 1 | D6–E–F#m–E/G# | Voice leading strings menghubungkan harmoni sumber |
| 25–32 | Tema B1 | A–E–B–F#m ×2 | Bass sedikit lebih bergerak; piano tetap memimpin |
| 33–48 | Tema A dengan lead | F#m–B/D# ×8 | Strings solo membawa motif sumber; flute memberi motif masuk dan jawaban akhir frasa |
| 49–52 | Transisi 2 | D6–E–F#m–E/G# | Chord piano yang lebih lebar dipertahankan; warna ensemble menguat |
| 53–60 | Tema B2 | A–E–B–F#m ×2 | Figur B sumber kembali; tail solo dari bar 52 dibiarkan pada posisi aslinya |
| 61–76 | Tema A akhir | F#m–B/D# ×8 | Solo kembali, flute memberi jawaban bervariasi; dinamika mereda dekat akhir |

Chord terakhir **tetap B/D#**. Tidak ditambah cadence F#m, bar baru atau tail ekstensi.

## Humanisasi dan transisi

Piano mempertahankan posisi setiap nada sumber, termasuk rolled chords dan pickup yang sudah ada. Velocity kini mengikuti fungsi suara: melodi atas lebih jelas, bass piano lebih ringan, dan inner voices menopang harmoni. Gate dibentuk agar nada yang tidak cocok dengan chord berikutnya melepas sebelum perubahan chord. Improvisasi dibatasi pada 30 chord tones pendek di ujung frasa, sekitar 7% dari jumlah nada asli.

Strings chord mempertahankan nada bersama tanpa retrigger setiap bar. Perpindahan setiap suara maksimum **3 semitone**, rata-rata sekitar **1,05 semitone**, sehingga perubahan chord lebih mengalir. Bass tidak mengganti root atau inversi sumber.

Strings solo mempertahankan urutan pitch class tema asli, dengan penurunan satu oktaf. Onset lead sumber diselaraskan paling jauh **1 tick ≈1,04 ms**. Sembilan akhir frasa dilepas sedikit lebih cepat untuk membuka ruang jawaban flute. Flute disusun ulang sesuai follow-up kamu; semua aksennya berada di ruang diam solo, sehingga tidak menumpuk dengan frase lead.

**Timing:** mode `free` dipakai hanya untuk menjaga **46 onset piano off-grid yang sudah ada di sumber**. Tidak menambah jitter atau swing. Improvisasi piano dan empat layer baru memakai pulsa straight pada grid 1/32; durasi note-off tetap mengikuti artikulasi.

## Plugin dan artikulasi

Pilihan VST/library piano, strings dan flute sepenuhnya milikmu; tidak ada plugin tertentu yang dikonfigurasikan atau dibuktikan telah dimuat. Pakai rentang pada tabel untuk memeriksa patch yang kamu pilih. Strings chord menggunakan sustain, solo strings dan flute menggunakan sustained/legato dengan napas. MIDI menyediakan pitch, velocity dan note length; jika library memakai CC1/CC11 untuk dinamika, sesuaikan expression di DAW sesuai suara pilihanmu.

Bass ditulis untuk **Fender Precision Bass VST** yang kamu pilih, sebagai permintaan instrumen eksternal khusus. Pilih patch fingerstyle normal dan pastikan rentang **MIDI 28–47** merupakan nada bunyi. Tidak ada slide, hammer-on atau keyswitch spesifik vendor; mapping articulation perlu mengikuti VST yang kamu pakai. Semua layer memakai channel 1 pada file independen. Sustain pedal, expression automation dan keyswitch belum ditulis.

## Drum

Tidak ada drum yang diminta, sehingga tidak ditambahkan. Tidak ada kit/sample atau mapping drum dalam hasil ini.

## Verifikasi dan asumsi

- **Validate, generate, verify: lulus**, exit code 0, `ok: true`.
- Kelima MIDI memiliki tepat satu track dan panjang global yang sama, tempo/meter/PPQN yang sama, note-on/off lengkap dan tanpa overlap pitch yang sama dalam satu layer.
- Perbandingan dengan sumber memeriksa seluruh **445 pitch/onset piano asli**, semua **71 pitch class motif lead**, root/inversi bass dan pitch class chord pada setiap bar.
- Empat bar kosong, batas bagian dan durasi 152 detik sumber dipertahankan. File sumber tidak diubah.
- Status pemuatan VST/preset: **belum diuji**; tidak membuat preset.
- Impor/drag-and-drop live Cubase: **belum diuji**.
- Render audio dan listening aktual: **belum dilakukan**, karena sound kamu yang pilih. Penilaian dilakukan dari nada, harmoni, register, rhythm, voice leading dan dinamika MIDI.

[MIDI sumber asli](../_internal/references/yey.mid) tersimpan utuh. Snapshot, script reproduksi, audit musikal dan receipt pemeriksaan berada di `_internal/`; file yang dipakai produser ada di `MIDI/`.
