# Neon Orbits — v003, revisi koherensi

**124 BPM · E harmonic minor · 4/4 · 164 bar · 5:17.419 · 13 layer · 7 preset native Serum 2.**

Revisi ini menanggapi laporan bahwa instrumen terdengar kacau saat pola silang ditumpuk. Lead, pluck 7/8, pulse 3:2 dan brass sekarang mengambil giliran. Bass dan pad menjelaskan harmoni yang sama, dengan voicing tiga nada dan motif lead yang lebih sederhana. Tempo, panjang lagu, batas bagian, kick, snare/clap dan crash dipertahankan dari v002. [v002](../v002/README.md) tetap tersimpan.

**Status:** MIDI dan struktur preset telah diverifikasi. Pemuatan native dalam Serum, impor langsung Cubase, rendering dan pendengaran aktual belum dilakukan. Revisi ini merupakan perbaikan susunan nada dan artikulasi yang dapat diperiksa; keberhasilan bunyinya belum dikonfirmasi lewat listening.

## Mulai di Cubase

1. Gunakan project atau salinan project baru pada **124 BPM, 4/4**, Musical Time Base, left locator **1.1.1.0**. Impor dengan **Import to Left Locator**. Untuk drag-and-drop aktifkan **Import Dropped File as Single Part**. Pada tempo tetap sesuai lagu, **Ignore Master Track Events on Merge** mempertahankan tempo project.
2. Muat tujuh preset **v003** pada tujuh instrument track Serum 2, lalu impor pasangan MIDI dari tabel pada bar 1. Pertahankan keheningan awal. Setiap file SMF 1 berisi tepat satu track dan total 629760 tick. Gunakan satu versi aransemen lengkap saat membandingkan; pastikan part v002 tidak ikut berbunyi bersama v003.
3. Buka `.SerumPreset` melalui menu **Load Preset** Serum. File juga terpasang di library User komputer ini pada `MIDI Creator/20261016-neon-orbits/v003/`. Untuk komputer lain, salin file dari `Presets/` ke library User dan rescan. Diperlukan **Serum 2 dan factory wavetables**; tidak ada sample/wavetable custom.
4. Buat enam Sampler Track terpisah untuk drum, pilih sample Anda sendiri dan set root **C3 di Cubase = MIDI 60**, channel 10. Jangan arahkan keenam file ke satu kit tanpa merancang ulang mapping. Tidak ada sample yang dipilih/disalin oleh revisi ini.
5. Pertahankan CC1 untuk gerak cutoff. CC7/CC10 memberi volume/pan awal; bila host tidak menerapkannya, gunakan nilai tabel sebagai acuan mixer lalu dengarkan dan atur gain. Note velocity dan preset output juga memengaruhi loudness; nilai ini bukan gain yang sudah diseimbangkan melalui audio.

## Track synth dan preset

Rentang di bawah adalah angka MIDI numerik. Semua instrumen bernada memakai Serum 2; arpeggiator internal dimatikan karena MIDI sudah memuat seluruh nada. Tidak ada Program Change dalam ekspor.

| Track | Peran | Rentang MIDI | MIDI | Native Serum 2 | Sound / mixer awal |
| --- | --- | --- | --- | --- | --- |
| Mono Bass | Root offbeat tetap; mengunci kick tanpa pickup atau octave run | 28–36 | [mono-bass.mid](MIDI/mono-bass.mid) | [mono-bass.SerumPreset](Presets/mono-bass.SerumPreset) | Mono saw/triangle, Mini-family VCO approximation; release 65 ms; CC7 101, CC10 64 |
| Juno Pad | Tiga suara Em–C–Am–B dengan voice leading pendek; jangkar harmoni | 54–64 | [juno-pad.mid](MIDI/juno-pad.mid) | [juno-pad.SerumPreset](Presets/juno-pad.SerumPreset) | DCO-family PWM source + chorus, tanpa pitch drift; attack 350 ms, release 220 ms, reverb 6%; CC7 66, CC10 64 |
| Phase Seven Pluck | Foreground jawaban 7/8; lima serangan dan dua jeda per siklus | 63–72 | [phase-seven-pluck.mid](MIDI/phase-seven-pluck.mid) | [phase-seven-pluck.SerumPreset](Presets/phase-seven-pluck.SerumPreset) | Saw pendek; release 60 ms, delay dihapus, reverb 4%; CC7 78, CC10 56 |
| Three Two Pulse | Jawaban 3:2 selama empat bar; satu pitch stabil per chord | 76–78 | [three-two-pulse.mid](MIDI/three-two-pulse.mid) | [three-two-pulse.SerumPreset](Presets/three-two-pulse.SerumPreset) | Square/triangle pendek; release 55 ms, reverb 4%; CC7 68, CC10 76 |
| Analog Lead | Motif E–G–B / G–E, mengikuti chord dan menyisakan backbeat | 71–84 | [analog-lead.mid](MIDI/analog-lead.mid) | [analog-lead.SerumPreset](Presets/analog-lead.SerumPreset) | Dual VCO-family saw/pulse -2/+2 cents; mono retrigger, release 100 ms; tanpa delay, reverb 6%; CC7 95, CC10 64 |
| Poly Brass | Aksen chord pada ruang kosong antarkalimat | 66–76 | [poly-brass.mid](MIDI/poly-brass.mid) | [poly-brass.SerumPreset](Presets/poly-brass.SerumPreset) | Dua saw -3/+3 cents, swell; arsitektur dan FX dipertahankan; CC7 70, CC10 60 |
| Glass Keys | Satu foreground di breakdown; motif lebih panjang | 66–76 | [glass-keys.mid](MIDI/glass-keys.mid) | [glass-keys.SerumPreset](Presets/glass-keys.SerumPreset) | Digital glass OPL/Dying Sine, bukan piano; release 250 ms, tanpa delay, reverb 12%; CC7 80, CC10 72 |

Macro **Tone** default 15/100 membuka cutoff dan **Contour** default 20/100 memperpanjang envelope timbre. CC1 juga membuka cutoff; kurva CC1 dibuat lebih jarang dan maksimum lebih rendah dari v002. Semua kontrol pitch, oscillator, filter, detune, LFO dan routing sebelumnya dipertahankan. Macro endpoints dan gabungan modulasi belum diaudisi. Delay lead/pluck/keys dihapus; tidak ada lagi echo yang menghasilkan salinan ritmis tambahan pada patch tersebut.

Pendekatan retro memakai keluarga instrumen: bass mono VCO, pad DCO stabil, lead dual VCO dan poly brass. Ini approximation dengan factory wavetable, bukan emulasi perangkat keras yang sudah dibandingkan melalui audio. Tidak ditambahkan drift, wow/flutter atau noise secara otomatis.

## Bentuk lagu

| Bar | Bagian | Perkembangan v003 |
| --- | --- | --- |
| 1–16 | Intro | Pad memberi pusat tonal; kilatan keys. Hat masuk bar 5, kick/bass bar 9. |
| 17–32 | Groove | Pluck 7/8 menjadi satu foreground. Bass root tetap dan kick 4/4 memperjelas pijakan. |
| 33–48 | Build | Lead call pada 33/35; brass 36, pluck 37–44. Bass keluar 45–48; aksen brass 48, beat terakhir hening. |
| 49–80 | Drop 1 | Lead 49–56; pluck 57–63; brass 64; lead singkat 65–68; pulse 3:2 69–72; pluck 73–79; lead dominant 80. |
| 81–96 | Breakdown | Drum/bass diam. Glass keys satu foreground, pad mengikuti chord yang sama. Tidak ada arp/lead/pulse. |
| 97–112 | Rebuild | Lead call 97/99; brass 100, pluck 101–108; kick kembali 105; bass keluar 109–112; brass 112 sebelum jeda. |
| 113–144 | Drop 2 | Lead 113–120; pluck 121–127; brass 128; lead dengan satu variasi 129–132; 3:2 133–136; pluck 137–143; lead dominant 144. |
| 145–160 | Outro | Pluck 145–151, lalu keluar. Hat berhenti setelah 156; bass dan kick tetap sebagai jangkar; brass terakhir 160. |
| 161–164 | Coda | Em dan E terakhir 161; bar 162–164 tanpa serangan baru untuk release. |

Harmoni utama **Em – C – Am – B**, masing-masing dua bar. Build memakai **Am – C – B – B**, diikuti empat bar terakhir pada B. Breakdown memakai **C – Am – Em – B**, lalu **Em – C – Am – B**. Koleksi tetap **E F# G A B C D#**. D# hadir pada dominant B dan menyelesaikan ke E ketika tonik kembali. Extension add9, maj7/b9 dan diminished detour yang sebelumnya menambah ketegangan telah dilepas.

Pad: **G–B–E → G–C–E → A–C–E → F#–B–D#**. Semua berada di atas bass. Pada loop utama tiap suara bergerak paling jauh tiga semiton; tidak ada cluster semiton di voicing. Sustain gate dan release amp diperpendek untuk memberi jarak sebelum chord berikutnya; panjang reverb aktual belum diukur.

## Polymeter dan polyrhythm

**7/8:** siklus tujuh slot eighth, pengelompokan **2+2+3**, dengan nada pada slot 0, 1, 2, 4, 5 dan jeda pada 3, 6. Jadi lima note-on per siklus, bukan tujuh note-on terus-menerus. Fase tidak di-reset per bar 4/4 atau saat chord berganti; pitch tetap mengikuti chord yang berlangsung. Delapan siklus utuh memakan **28 quarter beats = tujuh bar 4/4**. Jendela jawaban 57–63, 73–79, 121–127, 137–143 dan 145–151 masing-masing membiarkan satu pertemuan penuh itu terdengar sebelum instrumen lain mengambil giliran. Groove/build memakai span lebih panjang dengan reset hanya pada batas jendelanya. Global MIDI tetap 4/4 agar seluruh file sejajar.

**3:2:** tiga serangan rata pada **0, 2/3, 4/3 quarter beat** melawan kick pada 0 dan 1; jarak pulse **640 tick** pada 960 PPQN. Hanya bar **69–72 dan 133–136**. Setiap chord mempertahankan satu pitch pulse, sehingga kompleksitas datang dari ritme, bukan perubahan nada cepat. Lead, 7/8 pluck dan brass diam selama respons ini.

Timing **strict, tanpa swing/jitter**. Grid 1/48 whole note = 1/12 quarter beat mengakomodasi subdivisi straight dan triplet. Variasi ada pada gate, aksen, velocity dan timbre. Pola silang tetap berfungsi terhadap kick yang sama, dengan satu pusat perhatian pada satu waktu.

## Drum dan instrumen eksternal

Sample/kit tetap pilihan pengguna. Semua pemicu drum **MIDI 60**, yang bernama C3 di Cubase dan C4 menurut generator; angka numerik adalah acuan. Tidak ada instrumen di luar Serum selain enam sampler drum ini.

| Track | MIDI | Root / trigger | Channel | Performa dan karakter sample |
| --- | --- | --- | --- | --- |
| Kick | [kick.mid](MIDI/kick.mid) | **60 / Cubase C3** | 10 | Four-on-the-floor; performa dipertahankan. Elektronik bulat dan tegas, body sekitar 100–180 ms. Sisakan ruang untuk bass pada eighth offbeat; tuning E dapat dicoba setelah sample didengar. CC7 111, CC10 64. |
| Snare Clap | [snare-clap.mid](MIDI/snare-clap.mid) | **60 / Cubase C3** | 10 | Backbeat 2 dan 4; performa dipertahankan. Satu sample snare/clap gated era 80-an, tail 120–250 ms, tanpa flam tambahan. CC7 96, CC10 64. |
| Closed Hat | [closed-hat.mid](MIDI/closed-hat.mid) | **60 / Cubase C3** | 10 | Eighth lurus; 16th tambahan dihapus. Hat kering 30–70 ms. Dipakai juga untuk mengganti dua open-hat offbeat per bar agar tekstur lebih renggang. CC7 75, CC10 72. |
| Open Hat | [open-hat.mid](MIDI/open-hat.mid) | **60 / Cubase C3** | 10 | Hanya posisi beat 1.5 dan 3.5 pada bar aktif. Hat terbuka pendek 100–200 ms. Hindari tail panjang yang menyamarkan serangan 7/8. CC7 79, CC10 74. |
| Synth Tom | [synth-tom.mid](MIDI/synth-tom.mid) | **60 / Cubase C3** | 10 | Dua serangan per fill terpilih. Satu tom elektronik, decay sekitar 150–300 ms; bila bernada, coba E atau B. MIDI 60 adalah trigger root, bukan pitch bunyi C yang diwajibkan. CC7 86, CC10 52. |
| Crash | [crash.mid](MIDI/crash.mid) | **60 / Cubase C3** | 10 | Aksen bagian; performa dipertahankan. Crash/splash terkendali sekitar 0.8–1.8 s; tidak paling keras saat motif masuk. CC7 77, CC10 54. |

Fill tom pada bar **31, 46, 48, 63, 78, 103, 110, 112, 127, 142, 158**, masing-masing dua serangan. Closed dan open hat tidak menyerang bersamaan. Sampler Track terpisah tidak otomatis berbagi choke; batasi tail open hat lewat envelope sampler. Jika one-shot mengabaikan note-off, gate MIDI sendiri tidak memperpendek sample.

## Perbandingan dan verifikasi

Audit mencatat **92 pemeriksaan lulus**; `validate`, `generate`, dan `verify` sukses. 13 file MIDI satu track/SMF1, panjang sama dan seluruh onset on-grid. Tujuh native preset dibuat lewat serum-mcp, dibaca kembali, dibandingkan dengan spesifikasi, lolos wire-type scan, dependency factory diperiksa, dan hash salinan cocok. Bass/brass mempertahankan state semantik; lima preset lain hanya mengubah envelope amp dan FX terkait.

- Note synth turun **2261 → 1261** (sekitar 44%); pulse 3:2 turun 192 → 48 note.
- Tumpang tindih gate antar empat foreground turun **132.793 → 0 quarter beats**; budget release amp yang ditulis juga tidak tumpang tindih pada v003.
- Waktu gate yang memuat interval semiton antar nada synth turun **362.973 → 0 quarter beats**. Penghilangan ini adalah keputusan khusus perbaikan ini; interval semiton tidak otomatis salah dalam musik.
- Seluruh nada synth sekarang chord tones, dan gate tidak melewati chord yang tidak cocok. Ini memeriksa kompatibilitas harmoni tertulis, bukan hasil spektrum atau psychoacoustics.

**Batas bukti:** plugin Serum 2.0.23 terdeteksi terpasang, tetapi native preset v003 belum dimuat di plugin, belum dirender, belum diimpor langsung ke Cubase dan belum didengarkan oleh agent. Perhitungan gate/release tidak mencakup reverb atau sample yang sebenarnya. Tidak ada `.cpr`, audio, sample drum atau file MIDI gabungan yang dibuat.

Untuk mengevaluasi revisi, putar **bar 49–80** (sekitar 1:32.9–2:34.8): dengarkan perpindahan lead → 7/8 → lead → 3:2 → 7/8. Lalu bandingkan bar 113–144 dan transisi breakdown 81. Mulai dengan bass/kick/pad, kemudian nyalakan satu foreground sesuai timeline. Evaluasi ini belum dilakukan oleh agent; keseimbangan timbre dan sample perlu didengar pada instrumen pengguna.

Sumber, perubahan, build receipts dan audit disimpan di `_internal/`. Materi melodi orisinal; arahan artis dipahami sebagai perkembangan sequence/filter, tanpa menyalin rekaman tertentu.
