# The Lantern Gate

Aransemen orkestra fantasy menuju final epic, dibuat untuk **BBC Symphony Orchestra Discover (gratis)**. **35 MIDI terpisah**, satu instrumen dan satu artikulasi tetap per track. Buat satu instance BBCSO untuk setiap baris tabel di bawah.

**Tempo:** 108 BPM quarter note · **Meter:** 6/8 (rasa dua pulsa, dotted-quarter = 72) · **Mode:** D Dorian — D E F G A B C · **Panjang:** 96 bar / 2:40 · **Resolusi:** 960 PPQN.

## Mulai di Cubase

1. Buat project dengan tempo **108 BPM**, meter **6/8**, dan instrument track pada **Musical Time Base**. Semua MIDI harus mulai pada **1.1.1.0**, meskipun not pertama baru muncul belakangan.
2. Muat **BBC Symphony Orchestra**, pilih mode **Discover**, lalu pilih instrumen dan artikulasi dari tabel. Nama browser mungkin memakai prefiks “Discover -”. Pilih hanya satu artikulasi; jangan Shift-select beberapa teknik sekaligus. Kunci Technique Selector bila diperlukan.
3. Buat satu instance/track khusus per artikulasi, termasuk instrument yang sama: Violins 2 Long, Spiccato dan Pizzicato adalah tiga track terpisah. Tidak ada keyswitch atau pergantian program dalam MIDI.
4. Gunakan **File > Import > MIDI File**, left locator **1.1.1.0**, **Import to Left Locator**. Dengan tempo project sudah benar, **Ignore Master Track Events on Merge** mempertahankan tempo project. Untuk drag-and-drop, **Import Dropped File as Single Part**, lalu tempatkan setiap part pada bar 1. Pertahankan keheningan awal.
5. MIDI melodic menggunakan channel **1**; Untuned Percussion menggunakan channel **10**. Set MIDI channel BBCSO ke **All** atau channel yang sesuai. Instance percussion juga terpisah per baris agar dinamika dan pan independen.
6. Pertahankan **CC1 Dynamics** dan **CC11 Expression** saat impor. Dengan mapping default BBCSO, kurva ini membentuk swell dan frase. Pada preset Long gunakan respons velocity normal; hindari velocity-to-dynamics yang menimpa kurva CC1. Periksa lane CC1/CC11 di Key Editor.
7. File juga membawa level awal **CC7** dan pan **CC10** yang moderat. BBCSO memiliki posisi panggung dalam sampel; pan MIDI di sini hanya tambahan kecil. Jika Anda memakai pan/gain mixer sendiri, filter CC7/CC10 sesuai kebutuhan, sambil mempertahankan CC1/CC11.

## Track, patch, dan MIDI

Rentang memakai **C4 = MIDI 60**. Cubase biasanya menamai MIDI 60 sebagai C3; angka MIDI pada tabel tetap otoritatif. Semua pitch sudah berupa concert/sounding pitch: jangan transposisi tambahan untuk clarinet, horns, piccolo, atau double bass.

| Track | Patch BBCSO Discover | Artikulasi tetap | MIDI | Rentang aktual | Masuk bar | Fungsi |
| --- | --- | --- | --- | --- | --- | --- |
| 01 Violins 1 - Long | Strings: Violins 1 | Long | [s01-violins1-long.mid](MIDI/s01-violins1-long.mid) | D5–B6 (74–95) | 29 | tema utama; nada panjang pada klimaks |
| 02 Violins 1 - Tremolo | Strings: Violins 1 | Tremolo | [s02-violins1-tremolo.mid](MIDI/s02-violins1-tremolo.mid) | G5–G5 (79–79) | 67 | ketegangan menjelang gerbang |
| 03 Violins 2 - Long | Strings: Violins 2 | Long | [s03-violins2-long.mid](MIDI/s03-violins2-long.mid) | G4–A5 (67–81) | 5 | garis harmoni dan jawaban |
| 04 Violins 2 - Spiccato | Strings: Violins 2 | Spiccato | [s04-violins2-spiccato.mid](MIDI/s04-violins2-spiccato.mid) | D4–G5 (62–79) | 29 | ostinato eighth-note 3+3 |
| 05 Violins 2 - Pizzicato | Strings: Violins 2 | Pizzicato | [s05-violins2-pizzicato.mid](MIDI/s05-violins2-pizzicato.mid) | F4–D5 (65–74) | 13 | langkah ringan di pembukaan |
| 06 Violas - Long | Strings: Violas | Long | [s06-violas-long.mid](MIDI/s06-violas-long.mid) | D3–F4 (50–65) | 1 | suara tengah yang bergerak halus |
| 07 Violas - Spiccato | Strings: Violas | Spiccato | [s07-violas-spiccato.mid](MIDI/s07-violas-spiccato.mid) | F3–D4 (53–62) | 33 | jawaban ritmis pada ostinato |
| 08 Cellos - Long | Strings: Cellos | Long | [s08-cellos-long.mid](MIDI/s08-cellos-long.mid) | C3–A3 (48–57) | 29 | akar harmoni; countermelody tenor |
| 09 Cellos - Spiccato | Strings: Cellos | Spiccato | [s09-cellos-spiccato.mid](MIDI/s09-cellos-spiccato.mid) | B2–D4 (47–62) | 37 | dorongan low strings |
| 10 Cellos - Pizzicato | Strings: Cellos | Pizzicato | [s10-cellos-pizzicato.mid](MIDI/s10-cellos-pizzicato.mid) | C3–A3 (48–57) | 3 | bass ringan pada bagian fantasy |
| 11 Double Basses - Long | Strings: Basses | Long | [s11-basses-long.mid](MIDI/s11-basses-long.mid) | D1–D2 (26–38) | 13 | fondasi low bass tanpa voicing rapat |
| 12 Flutes a3 - Long | Woodwinds: Flutes a3 | Long | [w01-flutes-long.mid](MIDI/w01-flutes-long.mid) | D5–B6 (74–95) | 5 | tema fantasy dan puncak frase |
| 13 Flutes a3 - Staccatissimo | Woodwinds: Flutes a3 | Staccatissimo | [w02-flutes-staccatissimo.mid](MIDI/w02-flutes-staccatissimo.mid) | D5–A6 (74–93) | 67 | kilau pendek; run transisi |
| 14 Oboes a3 - Long | Woodwinds: Oboes a3 | Long | [w03-oboes-long.mid](MIDI/w03-oboes-long.mid) | D4–F5 (62–77) | 9 | jawaban hangat pada tema |
| 15 Clarinets a3 - Long | Woodwinds: Clarinets a3 | Long | [w04-clarinets-long.mid](MIDI/w04-clarinets-long.mid) | D4–B4 (62–71) | 16 | tema intim pada jeda tengah |
| 16 Bassoons a3 - Long | Woodwinds: Bassoons a3 | Long | [w05-bassoons-long.mid](MIDI/w05-bassoons-long.mid) | C3–D4 (48–62) | 29 | gerak tenor dan pengikat bass |
| 17 Piccolo - Long | Woodwinds: Piccolo | Long | [w06-piccolo-long.mid](MIDI/w06-piccolo-long.mid) | D6–B6 (86–95) | 73 | kilau puncak; baru hadir saat akhir |
| 18 Horns a4 - Long | Brass: Horns a4 | Long | [b01-horns-long.mid](MIDI/b01-horns-long.mid) | C4–B4 (60–71) | 39 | tema heroik dalam register tengah |
| 19 Horns a4 - Staccatissimo | Brass: Horns a4 | Staccatissimo | [b02-horns-staccatissimo.mid](MIDI/b02-horns-staccatissimo.mid) | C4–A4 (60–69) | 67 | aksen fanfare sebelum klimaks |
| 20 Trumpets a3 - Long | Brass: Trumpets a3 | Long | [b03-trumpets-long.mid](MIDI/b03-trumpets-long.mid) | D4–B5 (62–83) | 79 | mahkota tema saat akhir |
| 21 Trumpets a3 - Staccatissimo | Brass: Trumpets a3 | Staccatissimo | [b04-trumpets-staccatissimo.mid](MIDI/b04-trumpets-staccatissimo.mid) | A4–D5 (69–74) | 74 | fanfare pendek di sela tema |
| 22 Tenor Trombones a3 - Long | Brass: Tenor Trombones a3 | Long | [b05-tenor-trombones-long.mid](MIDI/b05-tenor-trombones-long.mid) | G3–F4 (55–65) | 71 | isi harmoni brass |
| 23 Bass Trombones a2 - Long | Brass: Bass Trombones a2 | Long | [b06-bass-trombones-long.mid](MIDI/b06-bass-trombones-long.mid) | G2–F3 (43–53) | 71 | fifth/root rendah saat tutti |
| 24 Tuba - Long | Brass: Tuba | Long | [b07-tuba-long.mid](MIDI/b07-tuba-long.mid) | F1–D2 (29–38) | 71 | fondasi brass pada frase penting |
| 25 Harp - Plucks | Percussion: Harp | Plucks / default | [k01-harp.mid](MIDI/k01-harp.mid) | D3–C6 (50–84) | 1 | arpeggio Dorian sebagai cahaya fantasy |
| 26 Celeste - Hits | Percussion: Celeste | Hits / default | [k02-celeste.mid](MIDI/k02-celeste.mid) | A5–E6 (81–88) | 2 | gema motif kecil dan bintang di awal |
| 27 Glockenspiel - Hits | Percussion: Glockenspiel | Hits / default | [k03-glockenspiel.mid](MIDI/k03-glockenspiel.mid) | B5–B6 (83–95) | 15 | titik cahaya pada nada puncak |
| 28 Tubular Bells - Hits | Percussion: Tubular Bells | Hits / default | [k04-tubular-bells.mid](MIDI/k04-tubular-bells.mid) | D4–D4 (62–62) | 71 | tanda gerbang dan resolusi |
| 29 Timpani - Hits | Percussion: Timpani | Hits | [p01-timpani-hits.mid](MIDI/p01-timpani-hits.mid) | D2–A2 (38–45) | 37 | pulsa bertonal D/A; roll dimainkan ulang dengan Hits |
| 30 Bass Drum - Hits | Percussion: Untuned Percussion | Hits | [p02-bass-drum.mid](MIDI/p02-bass-drum.mid) | C2–C2 (36–36) | 71 | aksen structural; bukan kick pop |
| 31 Snare Drum - Hits | Percussion: Untuned Percussion | Hits | [p03-snare.mid](MIDI/p03-snare.mid) | E2–E2 (40–40) | 68 | aksen march 6/8 dan roll dari repeated Hits |
| 32 Suspended Cymbal - Hits | Percussion: Untuned Percussion | Hits | [p04-suspended-cymbal.mid](MIDI/p04-suspended-cymbal.mid) | F2–F2 (41–41) | 44 | aksen transisi lembut |
| 33 Suspended Cymbal - Roll | Percussion: Untuned Percussion | Roll trigger | [p05-suspended-cymbal-roll.mid](MIDI/p05-suspended-cymbal-roll.mid) | G2–G2 (43–43) | 69 | swell ke bagian epic |
| 34 Piatti - Hits | Percussion: Untuned Percussion | Hits | [p06-piatti.mid](MIDI/p06-piatti.mid) | B3–B3 (59–59) | 71 | crash orkestral pada klimaks |
| 35 Triangle - Hits | Percussion: Untuned Percussion | Hits | [p07-triangle.mid](MIDI/p07-triangle.mid) | E3–E3 (52–52) | 4 | kilau jarang pada pembukaan |

Long dipakai untuk garis menyambung dengan gate hampir penuh dan swell, bukan patch Legato yang tidak tersedia di Discover. Spiccato adalah nama teknik short strings di Discover; woodwind/brass pendek memakai Staccatissimo. Timpani dan snare roll cepat di part Hits ditulis sebagai pukulan ulang, bukan sebagai pergantian ke mode Rolls. Suspended Cymbal Roll mendapat track khusus dan trigger khusus.

Saat Long dan short strings dari seksi yang sama berjalan bersamaan, perlakukan sebagai pembagian fungsi/divisi secara musikal. Sampel Discover tetap merupakan seksi penuh: turunkan level short/harmony pendukung bila keseimbangan terdengar terlalu besar.

## Bentuk lagu

| Bar | Waktu mulai | Bagian | Perkembangan |
| --- | --- | --- | --- |
| 1–12 | 0:00 | Whispering Lanterns | Harp dan viola membuka ruang; flute masuk bar 5, oboe menjawab bar 9. |
| 13–28 | 0:20 | The Hidden Path | Tema lengkap pada flute, lalu oboe; pizzicato memberi langkah ringan. |
| 29–44 | 0:46 | The Quest | Tema pindah ke Violins 1; ostinato masuk bertahap, horn muncul bar 39. |
| 45–54 | 1:13 | Sanctuary | Brass, percussion, dan short strings keluar; clarinet, harp, viola, cello mengisi ruang. |
| 55–70 | 1:30 | The Gate Awakens | Tema kembali pada strings lalu horn; tremolo, flute pendek dan roll membangun antisipasi. |
| 71–86 | 1:56 | Banner of Dawn | Tema heroik pada violin/horn; trumpet mengambil alih paruh kedua, low brass dan drum bergabung. |
| 87–94 | 2:23 | The Lantern Gate | Tema diperlebar; puncak B6 lalu final D minor tutti pada bar 93. |
| 95–96 | 2:36 | Hall Release | Tidak ada serangan nada baru; ruang release sekitar 3,3 detik. |


Harmoni menggunakan Dm/add9/6, G, F, C, Am/Am7 dan Em7, dengan inversion dan pedal D. **B natural** pada G dan Dm6 mempertahankan warna Dorian; tidak ada Bb atau C# yang menggeser ke natural/harmonic minor. Kecepatan ganti harmoni berubah dari dua/empat bar menjadi per bar; tema juga berpindah register dan instrumen. Final kembali ke **D minor pada bar 93**, ditahan hampir dua bar, lalu bar 95–96 memberi ruang release. Penutup musikal tetap besar; ruang akhir bukan fade-out yang panjang.

## Percussion yang dipakai

Semua memakai patch bawaan pilihan Anda: **BBCSO Discover**, bukan kit GM atau Cubase Sampler. **Jangan remap semua pitch ke MIDI 60.** Load **Untuned Percussion** untuk baris drum/cymbal/triangle; load **Timpani** untuk track bertonal.

| Part | Pitch MIDI | Nama pada manual (C4 = 60) | Nama Cubase (C3 = 60) | Peran |
| --- | --- | --- | --- | --- |
| Bass Drum Hits | 36 | C2 | C1 | Pukulan konser dalam dan jarang; menegaskan kedatangan frase. |
| Snare Hits | 40 | E2 | E1 | March 6/8, ghost notes dan repeated-hit rolls. |
| Suspended Cymbal Hits | 41 | F2 | F1 | Satu tanda transisi lembut, bukan crash di setiap bar. |
| Suspended Cymbal Roll | 43 | G2 | G1 | Dua swell sebelum klimaks dan penutup. |
| Piatti Hits | 59 | B3 | B2 | Crash orkestral pada bar 71, 79, 87, 93. |
| Triangle Hits | 52 | E3 | E2 | Kilau kecil di pembukaan. |
| Timpani Hits | 38 / 45 | D2 / A2 | D1 / A1 | Nada D dan A; tidak memakai map Untuned Percussion. |

Mapping nama nada mengikuti [daftar resmi Untuned Percussion Discover](https://support.spitfireaudio.com/en/articles/11815993-what-are-the-untuned-percussion-instruments-used-in-bbc-so-discover). Konversi numerik memakai middle C = 60 dan preferensi lokal BBCSO `defaultMiddleCIsC4=1`; pemicu plugin belum diuji live. Pada keyboard BBCSO, pastikan pitch 36 menampilkan Bass Drum dan 40 Snare sebelum playback lengkap. Perubahan label octave di DAW tidak memerlukan transposisi file.

Timpani mengunci pulsa 3+3, bass drum memberi bobot pada batas frase, snare mengisi perkembangan tanpa backbeat pop, dan cymbal hanya memberi tanda besar. Hindari tambahan kick/hat elektronik atau compression yang menghapus kontras sanctuary–epic. Sampel sudah dipilih melalui library Anda; tidak ada file sample yang disalin.

## Dinamika dan batas Discover

Velocity berbeda menurut aksen dan tujuan frase; gate dipendekkan untuk short notes dan hampir penuh untuk Long. CC1 membentuk perkembangan besar, sedangkan CC11 memberi swell ringan dalam frase. Kedua kurva tidak memakai atenuasi dalam yang identik. Semua note-on **on-grid 1/16, straight, tanpa swing atau random timing jitter**; perubahan panjang nada dan velocity menghasilkan variasi performa.

Discover hanya memiliki satu dynamic layer, tanpa true legato atau round robins. Karena itu CC1 di Discover bertindak sebagai pengatur level tambahan; kurvanya tidak menghasilkan perubahan timbre pp–ff seperti Core/Professional. Pembagian frase, register dan orkestrasi sudah disusun untuk batas tersebut. Lihat [manual Discover, bagian controls dan Appendix B/C](https://d1t3zg51rvnesz.cloudfront.net/p/files/product-manuals/4924/1688057212/BBC%20Symphony%20Orchestra%20Discover_User%20Manual.pdf) dan [perbandingan resmi edisi](https://support.spitfireaudio.com/en/articles/11815936-which-features-are-different-between-editions-of-bbc-so).

## Instrumen eksternal dan asumsi

Semua track menggunakan **BBC Symphony Orchestra Discover by Spitfire Audio**, sesuai permintaan Anda. Alasan: sampel orkestral Anda menentukan artikulasi dan karakter permainan. Cara muat, register dan mapping ada pada tabel. Tidak diperlukan Serum, plugin tambahan, file preset, instrument Core/Professional, atau file gabungan. Harp, Celeste, Glockenspiel dan Tubular Bells memakai patch Discover bawaan; tidak perlu keyswitch maupun pedal.

Durasi, D Dorian, tempo dan meter dipilih karena tidak ditentukan secara spesifik. Penyusunan memakai seed **20261014** yang tetap. Skill yang diterapkan: `mc-workflow`, `mc-development`, `mc-melody`, `mc-harmony`, `mc-orchestration`, `mc-arrangement-arch`, dan pemeriksaan `mc-ai-tell-audit` pada struktur/performa MIDI. Pemaksaan chord di luar Dorian serta timing offset dari contoh skill dikecualikan untuk mengikuti mode dan kontrak timing workspace.

## Status verifikasi

- **Validate / generate / verify: PASS (`ok: true`).** 35 file SMF format 1, tepat satu track per file; semua 960 PPQN, 6/8, tempo 108, akhir tick **276480**, durasi **160.000128 detik** akibat pembulatan tempo MIDI.
- **1.966 nada dan 7.024 event CC1/CC11**; readback posisi/channel/controller/value sesuai spesifikasi; tidak ada stuck note atau overlap pitch yang sama. Semua 1.966 note-on on-grid.
- Audit offline: seluruh nada bertonal berada di D Dorian; serangan final bertonal membentuk D minor; register diperiksa; sanctuary mengurangi jumlah layer; klimaks memperluas register dan instrumentasi; bar release tanpa note-on baru.
- Pengujian generator: **46 tes dijalankan, 45 lulus dan 1 integrasi Serum opt-in dilewati**; contoh single-layer dan multi-layer juga diperiksa.
- **Pemuatan patch BBCSO, pemicu percussion dan impor Cubase live: belum diuji. Audio tidak dirender dan belum didengarkan melalui VST Anda.** Verifikasi struktur MIDI tidak membuktikan hasil bunyi atau keseimbangan mixing.

Semua MIDI siap diimpor dari bar 1. Bahan sumber, binding, spesifikasi, seed, laporan verifikasi dan audit berada dalam `_internal/`; folder kerja produser berisi README dan MIDI.
