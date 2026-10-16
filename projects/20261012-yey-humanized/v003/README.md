# Yey — Piano Center / Left / Right · v003

**120 BPM · 4/4 · 76 bar · 2:32 · 480 PPQN · F# Dorian, dengan D natural pada D6.**

Hanya piano v002 yang ditulis ulang menjadi **tiga part piano independen**. Center membawa fondasi dan garis atas; left mengalirkan broken chord; right memberi jawaban tinggi. Permainan samping saling mengisi untuk membentangkan stereo. **Keenam layer BBC tetap identik dengan v002**, termasuk nada, timing, velocity, CC, volume, pan, dan byte MIDI.

Progresi chord, slash bass, posisi pergantian, struktur bagian, empat bar pembuka kosong, dan chord akhir **B/D#** tetap sama. Impor semua file dari **bar 1**; bunyi piano pertama tetap di **bar 5 / 0:08**. [v002](../v002/README.md) dan [referensi asli](../_internal/references/yey.mid) tetap tersimpan.

## Mengganti piano di Cubase

1. Pada sesi v002, mute/nonaktifkan piano lama. Buat tiga instrument track: **Piano Center, Piano Left, Piano Right**, masing-masing dengan instance piano akustik pilihan Anda. Keenam track BBC yang sudah ada tetap dapat dipakai; tidak perlu mengimpor duplikatnya.
2. Atur **120 BPM, 4/4**, Musical Time Base, left locator **1.1.1.0**. Impor ketiga MIDI dengan **Import to Left Locator**. Untuk drag-and-drop gunakan **Import Dropped File as Single Part**, lalu tempatkan part di bar 1. Pada project tempo tetap, **Ignore Master Track Events on Merge** mempertahankan tempo project.
3. Posisi awal: **center di tengah; left sekitar 70% kiri; right sekitar 70% kanan**. MIDI membawa **CC10 = 64 / 20 / 108**, tetapi plugin dapat mengabaikannya. Periksa posisi aktual dan gunakan panner Cubase/plugin bila perlu. Periksa juga agar dua kontrol pan tidak memperkuat pergeseran yang sama tanpa disengaja.
4. Mulai dengan patch piano yang sama pada ketiga instance. Center menjadi acuan volume; naikkan side sampai figur saling menjawab jelas, dengan cello tetap menjadi tema utama saat masuk. CC7 awal **94 / 82 / 84** adalah titik awal MIDI, bukan balance audio yang sudah diuji.
5. Untuk sampel piano stereo lebar, gunakan **Stereo Combined Panner** atau kontrol posisi/width plugin untuk menggeser keseluruhan citra. Sempitkan width piano samping bila masih menutupi tengah. Gunakan satu ruang reverb bersama dengan decay konsisten; pertahankan attack dan periksa dalam mono.
6. Pertahankan keheningan awal dan part penuh 76 bar. Tidak ada CC64 sustain pedal; koneksi ditulis melalui gate dan shared tone. Jika menambahkan pedal manual, bersihkan tiap pergantian chord. Biarkan tail plugin/reverb berbunyi saat ekspor audio.

Untuk sesi baru, impor kesembilan file berikut dari bar 1. Semua adalah **SMF format 1, tepat satu track instrumen, channel 1**, dengan akhir global **145920 ticks**. File tidak memilih patch otomatis dan tidak mengirim Program Change, Bank Select, SysEx, key atau section marker.

## Tiga permainan piano

Concert pitch **C4=60**; ikuti angka MIDI bila penamaan oktaf Cubase berbeda. Tanpa transposisi oktaf.

| Track / MIDI | Permainan dan ruang | Rentang / jumlah nada | Pan CC10 |
| --- | --- | --- | --- |
| [Piano Center](MIDI/piano-center.mid) | Bass/inversi asli, chord tersambung dan upper voice utama; reartikulasi lembut pada bagian lift | F#1–F#5 / **30–78** / **302** | **64**, center |
| [Piano Left](MIDI/piano-left.mid) | Broken chord menengah, naik-berbalik-kembali; lebih jarang di bawah tema, tanpa bass dalam di sisi kiri | F#3–F#4 / **54–66** / **213** | **20**, sekitar L69 |
| [Piano Right](MIDI/piano-right.mid) | Frasa tinggi turun/berbalik, mengisi sela left; diam pada bar woodwind dan awal masuk cello | F#5–E6 / **78–88** / **111** | **108**, sekitar R70 |

Gunakan **piano akustik velocity-sensitive pilihan Anda**, melanjutkan pengecualian instrumen v001/v002. Ketiganya dapat memakai patch yang sama pada instance terpisah; perbedaan part ada pada register, pola, gate, touch dan posisi. Tidak ada sound/preset baru atau layer Serum, sehingga tidak ada file `.SerumPreset` yang diperlukan. Muat patch secara manual.

Upper anchor center mempertahankan contour tersambung dari v002: span maksimal **9 semitone**, perpindahan tiap suara antarchord maksimal **4 semitone**. Common upper tone diartikulasikan ulang paling lambat setiap dua bar untuk memperhitungkan decay piano. Voicing left bergerak maksimal **3 semitone per suara**. Right selalu minimal dua semitone di atas upper anchor center pada bar permainannya.

Ini trio bebas dengan accompaniment dan jawaban melodis, memakai prinsip komplementaritas dari counterpoint. Seluruh nada piano adalah chord tone yang sesuai sepanjang gate. Timing **on-grid, tanpa swing atau onset jitter**; stereo berasal dari part berbeda. Tidak ada perubahan progresi.

## Orchestra yang dipertahankan

Load **BBC Symphony Orchestra → Discover**, lalu instrumen/artikulasi berikut, channel **1 / All**, tanpa transposisi. String adalah section patch; woodwind adalah **a3**, bukan solo. Pilih dan kunci **Long** bila perlu. Tidak ada keyswitch atau pergantian teknik tertulis.

| MIDI | Patch / artikulasi | Fungsi | Rentang MIDI / jumlah nada |
| --- | --- | --- | --- |
| [BBC Basses](MIDI/bbc-basses.mid) | Strings → Basses → Long / Long (vib) | Bowed root dan slash bass, masuk bar 9 | F#1–A2 / **30–45** / 68 |
| [BBC Celli](MIDI/bbc-celli.mid) | Strings → Celli → Long / Long (vib) | Tema liris, masuk bar 33 beat 3 | C#3–A4 / **49–69** / 71 |
| [BBC Violas](MIDI/bbc-violas.mid) | Strings → Violas → Long / Long (vib) | Inner common-tone, masuk bar 13 | E4–F#4 / **64–66** / 26 |
| [BBC 1st Violins](MIDI/bbc-violins-1.mid) | Strings → 1st Violins → Long / Long (vib) | Harmoni atas, masuk bar 17; jeda bar 53–54 | B4–C#5 / **71–73** / 52 |
| [BBC Flutes](MIDI/bbc-flutes.mid) | Woodwinds → Flutes a3 → Long | Enam jawaban pada ruang cello | D#5–A5 / **75–81** / 12 |
| [BBC Clarinets](MIDI/bbc-clarinets.mid) | Woodwinds → Clarinets a3 → Long | Enam jawaban hangat pada bagian B | D#4–C#5 / **63–73** / 12 |

Pengecualian instrumen BBC dilanjutkan untuk mempertahankan orchestra Anda. Semua memakai satu garis monofonik per patch, **CC1 tetap 100** dan **CC11 membentuk expression**. Pertahankan Dynamics=CC1 dan Expression=CC11. Discover mempunyai satu recorded dynamic layer; expression tidak berarti timbral crossfade atau true legato. Tidak membundel konten library/preset pihak ketiga. Detail pilihan asal tetap ada di [README v002](../v002/README.md).

## Bentuk dan progresi yang dikunci

Setiap chord satu bar di posisi aslinya; D6 = D–F#–A–B.

| Bar | Chord | Perkembangan piano v003 |
| --- | --- | --- |
| 1–4 | Hening | Keheningan pembuka tetap |
| 5–12 | F#m–B/D# ×4 | Center membuka; side menyusul dalam bar, figur left berkembang setelah empat bar pertama |
| 13–16 | F#m–B/D# ×2 | Figur kiri menipis menjadi dua nada panjang, right melembut |
| 17–20 | F#m–B/D# ×2 | Gerak kiri kembali, center tetap tersambung |
| 21–24 | D6–E–F#m–E/G# | Center direartikulasi lembut; jawaban kanan menjadi tiga nada |
| 25–32 | A–E–B–F#m ×2 | Stereo terbuka, right memberi ruang bar clarinet |
| 33–48 | F#m–B/D# ×8 | Left dua nada per bar, right melewatkan awal tema dan bar flute |
| 49–52 | D6–E–F#m–E/G# | Lift luas, touch sedikit lebih kuat dan balasan lengkap |
| 53–60 | A–E–B–F#m ×2 | Ruang clarinet; paruh kedua mengubah akhir figur kiri dan memperpanjang jawaban kanan |
| 61–76 | F#m–B/D# ×8 | Tema kembali dengan figur ringan; bar 73–76 makin jarang/lembut, B/D# tetap terbuka |

Tidak ada drum MIDI atau sample, mengikuti aransemen piano/orchestra v002. Pilihan kit dan mapping drum tidak berlaku.

## Verifikasi dan batas pemeriksaan

- **Validate, generate, verify lulus**, exit code 0 dan `ok: true`. **9 file / 867 note-on**, semua on-grid, tanpa same-pitch overlap, dengan tempo, meter, PPQN dan akhir global sama. Timing policy **strict 1/32**; piano baru memakai subdivisi straight 1/8.
- Audit 72 bar memastikan chord pitch-class lengkap serta lowest piano pitch sesuai root/inversi. Tidak ada gate piano ke chord yang tidak mendukung. Onset left/right tidak serempak; right diam di bar woodwind; tidak ada overlap semitone bersebelahan antara piano dan cello.
- **Enam spesifikasi layer BBC dan keenam file MIDI BBC identik dengan v002**, diperiksa lewat perbandingan isi dan SHA-256. Revisi terdahulu tetap utuh.
- Skill **music-composition-skills**: mc-workflow, mc-harmony, mc-counterpoint, mc-orchestration beserta referensi piano, mc-texture-layering, mc-mix-intent, mc-development, mc-symbolic-score dan mc-ai-tell-audit. Keputusan dan self-audit tersimpan bersama sumber.
- **Pemuatan plugin/preset, impor live Cubase, render audio, dan listening aktual belum dilakukan.** Penilaian musik bersifat simbolik; balance stereo, respons velocity, decay, reverb dan mono perlu didengar melalui patch Anda. Pan MIDI bukan bukti posisi audio plugin sudah diterapkan.

Sumber reproduksi, snapshot, binding, ARR-SPEC, brief dan receipt berada di `_internal/`. Produser cukup memakai README ini dan folder MIDI.
