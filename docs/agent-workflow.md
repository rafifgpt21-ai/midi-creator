# Dari brief menjadi komposisi

## Menetapkan brief

Catat permintaan asli di `_internal/request.md`. Ambil genre/mood, instrumen, tempo, meter, key/scale, panjang, struktur bagian, densitas, dan tujuan DAW bila diberikan. Permintaan musik baru adalah izin untuk membuat spesifikasi dan file MIDI dalam workspace ini. Terapkan default Serum 2, multi-instrumen sepanjang lagu, serta drum pilihan pengguna dari AGENTS.md; baca `project-layout.md` untuk lokasi bahan kerja dan hasil.

Jika detail belum ada, pilih nilai yang sesuai dengan gaya dan jelaskan asumsi. Misalnya, brief ambient dapat memakai progresi lambat dengan pad dan melodi renggang; brief funk memerlukan sinkopasi serta kerja sama bass dan kick. Genre tidak diputuskan oleh contoh bawaan. Informasi wajib ditanyakan bila hasil bergantung pada bahan yang belum tersedia, misalnya meniru MIDI referensi yang belum ada atau mapping drum khusus yang tidak diketahui.

## Menyusun layer

Tentukan fungsi setiap instrumen: harmony, bass, melody, countermelody, texture, atau percussion. Gunakan satu program dan satu instrumen per layer. Dua piano dengan fungsi berbeda boleh menjadi dua layer instrumen piano. Nama layer menerangkan instrumennya; `role` menerangkan fungsinya.

Drum mengikuti permintaan: satu track kit dengan beberapa pitch percussion, atau track terpisah per bagian (kick, snare, closed hi-hat, shaker, dll.). Pilih mapping sesuai layout dalam [mapping drum default](default-drum-map.md), termasuk root Cubase Sampler untuk drum per layer dan mapping terpisah bila gabungan diminta. Semua drum tetap channel 10. Program drum tidak disetel, karena pemetaan kit dipilih di DAW. Volume dan pan tiap file boleh independen. Jika pengguna juga meminta gabungan, percussion yang berbagi channel 10 harus memakai volume/pan sama dan pitch yang tidak tumpang tindih.

Program GM adalah petunjuk praktis untuk sound awal. Untuk instrumen VST di luar GM, pilih program representatif, jelaskan target sound/plugin di brief, lalu gunakan pitch, velocity, dan register yang sesuai. Nama plugin dan preset tidak tersimpan otomatis sebagai sound MIDI.

Untuk bundle Cubase dengan Serum dan sample drum, ikuti [panduan studio](cubase-studio.md). Binding plugin disimpan terpisah dari spesifikasi performa; bundle menambahkan preset VST3 dan sample tanpa mengubah kontrak satu MIDI per layer. Verifikasi file, reload preset, dan koneksi live Cubase adalah pemeriksaan berbeda.

## Komposisi dan bentuk lagu

Mulai dengan progresi harmoni atau pusat tonal, kemudian bangun ritme, bass, dan motif. Susunan itu boleh berubah untuk gaya yang memulai dari beat atau melodi. Gunakan voicing dengan perpindahan masuk akal, register yang sesuai instrumen, dan variasi yang mempunyai tujuan. Chord dalam satu instrumen adalah beberapa nada simultan dalam layer yang sama.

Pakai `sections` untuk marker intro/verse/chorus/bridge/outro atau bentuk lain. Layer yang masuk belakangan memakai onset absolut yang sesuai; hindari menggeser setiap layer ke nada pertamanya. Panjang komposisi tetap mencakup seluruh bagian dan tail yang dibutuhkan.

Sebelum menulis layer, baca [panduan timing MIDI](midi-timing-guide.md) dan tetapkan satu grid onset serta anchor groove bersama. Ikuti field `timing` dalam [kontrak komposisi](composition-guide.md#pemeriksaan-grid-onset). Nilai lead/arp terhadap bass, drum dan chord bersama; lolos grid saja tidak menjamin ritme cocok.

Clip berulang berguna untuk pola dasar. Tambah variasi antarbagian, fill, aksen, atau jeda sesuai brief. Hitung onset, gate, dan velocity secara eksplisit; script dengan random seed tetap dapat membantu. Jika pengguna meminta swing atau offset timing lain, terapkan pengecualian sesuai panduan timing. Humanization harus mempertahankan batas komposisi dan menghindari overlap pitch yang sama.

## Referensi dan revisi

Simpan bahan pengguna di `references/<slug>/` dan catat lokasi serta perannya dalam `request.md`. Untuk MIDI, `midi-creator inspect <file>` memberi ringkasan struktur; gunakan Mido untuk membaca nada/tempo bila perlu analisis rinci. Untuk audio, gunakan kemampuan analisis atau playback yang tersedia dan nyatakan keterbatasannya jika belum dapat didengar.

Revisi memakai folder versi berikutnya dalam proyek yang sama. Salin spesifikasi sumber, ubah bagian yang diminta, dan catat revisi asal serta perubahan. Jika mempertahankan layer tertentu, bandingkan nada, timing, velocity, program, dan mixer layer tersebut dengan revisi asal sebelum ekspor. Perubahan tempo global berlaku pada durasi semua layer dan perlu sesuai brief.

## Kriteria hasil siap

- Setiap instrumen yang diminta mempunyai layer dan file sendiri; format per-layer memiliki tepat satu track.
- Semua file sejajar pada timeline global dan tetap mempunyai panjang total yang sama.
- `validate`, `generate`, dan `verify` berhasil; setiap note-on mempunyai note-off dan tidak ada overlap pitch yang sama dalam layer.
- Penilaian musik mencakup brief, harmoni, register, rhythm/groove, dinamika, dan perkembangan bagian. Catat jika suatu asumsi mengubah ekspektasi pengguna.
- README revisi lengkap dan menautkan file MIDI/preset yang ada. Saran drum khusus
  lagu, mapping pitch, dan panduan instrumen di luar Serum bila diperlukan sudah
  tersedia. `manifest.json`, `validation.json`, `summary.md`, serta snapshot
  spesifikasi dikelompokkan dalam `_internal/`.

Verifikasi struktural tidak membuktikan sound plugin tertentu atau musikalitas. Klaim bahwa hasil sudah didengarkan hanya digunakan setelah playback benar-benar dilakukan.
