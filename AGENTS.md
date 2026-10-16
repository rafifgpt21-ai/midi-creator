# Membuat musik MIDI di workspace ini

## Sound design Serum 2

- Saat membuat sound baru atau menentukan sound setiap layer komposisi, gunakan [serum-sound-design](skills/serum-sound-design/SKILL.md). [Panduan utama](docs/serum-sound-design/README.md) dan [indeks referensi](skills/serum-sound-design/references/index.md) menyediakan teori, engine, keluarga sound, resep, dan template; baca hanya cabang yang relevan.
- Permintaan satu sound/preset menghasilkan sound/preset itu. Default aransemen lengkap di bawah berlaku untuk permintaan komposisi musik; permintaan penjelasan atau dokumentasi mengikuti hasil yang diminta pengguna.
- Untuk sound analog/vintage/retro analog atau emulasi gear analog nyata, wajib gunakan [panduan analog dan retro Serum 2](skills/serum-sound-design/references/analog-retro.md) sebagai default, termasuk saat menentukan sound tiap layer. Mulai dari arsitektur gear dan kondisi terawat; bedakan VCO/DCO, variasi antar voice, drift kontinu, serta warna rekaman. Terapkan lima teknik sesuai kebutuhan, bukan semuanya otomatis. Pilihan eksplisit pengguna diutamakan; catat asumsi, batas implementasi, dan bukti verifikasi. Istilah retro saja tidak otomatis berarti analog.
- Pilih skill khusus berdasarkan pekerjaan berikut. Skill tersedia dalam `skills/` workspace dan salinan terpasang di skill home; salinan workspace menjadi sumber pemeliharaan.

| Pekerjaan | Skill |
|---|---|
| Merancang sound lengkap dari brief | [serum-sound-design](skills/serum-sound-design/SKILL.md) |
| Mencocokkan audio atau preset referensi | [serum-reference-match](skills/serum-reference-match/SKILL.md) |
| Memilih oscillator/engine, wavetable, FM/AM, filter, dan routing | [serum-synthesis](skills/serum-synthesis/SKILL.md) |
| Membentuk envelope, LFO, macro, expression, glide, arp, dan clip | [serum-modulation](skills/serum-modulation/SKILL.md) |
| Merancang FX, dinamika, stereo, ruang, dan bus | [serum-effects](skills/serum-effects/SKILL.md) |
| Membuat atau merevisi preset native dan dependency | [serum-preset-build](skills/serum-preset-build/SKILL.md) |
| Memeriksa, mendengarkan, atau memperbaiki hasil sound | [serum-preset-qa](skills/serum-preset-qa/SKILL.md) |

- Dasarkan pilihan musikal pada brief dan teori; gunakan manual Serum untuk perilaku UI serta schema/runtime tool terkini untuk parameter implementasi. [Indeks sumber](skills/serum-sound-design/references/sources.md) membedakan isi PDF yang tersedia, bagian demo teori yang tidak disertakan, dan panduan tambahan. Resep adalah titik awal yang perlu dinilai terhadap brief.
- Sebelum build native, baca [Serum MCP](docs/serum-mcp.md) dan panggil `list_parameters()`. Untuk kontrol yang belum didukung tool, baca [batas kemampuan](skills/serum-sound-design/references/tool-capabilities.md), gunakan template/UI yang terverifikasi bila tersedia, atau catat kebutuhan yang belum terpenuhi. Simpan spec, resource manifest, readback, dan receipt di `_internal/`; dependency custom ikut paket preset dengan petunjuk instalasi.
- Nilai sound terhadap register, artikulasi, spektrum, gerakan, stereo, dan gesture yang diminta memakai [panduan verifikasi](skills/serum-sound-design/references/verification.md). Laporkan verifikasi struktur, pemuatan plugin, render/analisis audio, dan listening aktual secara terpisah. Jika akses live/audio belum tersedia, selesaikan pemeriksaan offline dan tandai pemeriksaan musikal terkait sebagai belum diuji.

## Kontrak hasil

- Default setiap permintaan musik adalah aransemen multi-instrumen lengkap dari awal sampai akhir. Semua instrumen selain drum menggunakan **Serum 2**. Jumlah layer mengikuti kebutuhan musikal; permintaan eksplisit seperti satu melodi, cuplikan, atau plugin lain mengalahkan default ini.
- Default setiap permintaan musik juga mencakup pembuatan file preset native **`.SerumPreset`** untuk setiap sound/layer Serum 2, tanpa perlu diminta terpisah. Buat melalui repo `serum-mcp`; baca `docs/serum-mcp.md` sebelum membuat atau mengedit preset. Simpan file siap pakai di `Presets/`, dengan nama yang cocok dengan layer MIDI, dan spesifikasi/binding/receipt di `_internal/`. README wajib menautkan setiap pasangan MIDI–preset dan menjelaskan cara memuatnya. Pengecualian mengikuti permintaan eksplisit pengguna; drum tetap memakai kit/sample pilihan pengguna.
- Setiap layer adalah satu instrumen dan diekspor ke satu `.mid` dengan tepat satu track instrumen. Buat layer terpisah untuk instrumen berbeda. Drum bisa satu kit, atau satu bagian percussion per layer sesuai brief.
- Default MIDI on-grid dengan `timing.mode: "strict"` dan tanpa swing; swing hanya jika diminta pengguna. Dotted note dan meter selain 4/4 tetap diizinkan sesuai kebutuhan musik. Baca [panduan timing MIDI](docs/midi-timing-guide.md) saat membuat musik, memakai referensi, atau merevisi ritme.
- Semua layer dalam satu komposisi menggunakan tempo, meter, resolusi, titik awal, dan panjang total yang sama. Keheningan tetap berada pada posisi aslinya agar file sejajar saat diimpor ke DAW.
- Drum memakai kit/sample yang dipilih pengguna. Buat performa MIDI drum bila aransemen membutuhkannya, lalu jelaskan karakter drum yang cocok dan mapping pitch di README. Pemilihan atau penyalinan sample konkret dilakukan setelah pengguna menentukan pilihan atau meminta agent memilihkan.
- Saat membuat atau merevisi drum MIDI, baca [mapping drum default](docs/default-drum-map.md) dan pilih cabang drum per layer atau satu kit. Drum per layer mengikuti default root Cubase Sampler di panduan itu, kecuali pengguna memberikan mapping lain; pilihan kit/sample tetap mengikuti pengguna.
- Gaya musik, instrumen, jumlah layer, dan aransemen mengikuti pengguna. File gabungan hanya dibuat jika diminta, dengan `--combined`.
- Setiap revisi mempunyai `README.md` untuk produser: tempo/key/meter/panjang, bentuk lagu, tabel track/MIDI/preset, cara import Cubase dari bar 1, saran drum khusus lagu, mapping, asumsi, dan status verifikasi/listening. Jika instrumen di luar Serum diperlukan atau diminta, cantumkan alasan, plugin/library, cara memuatnya, rentang nada, artikulasi, dan mapping di README itu.
- Area hasil yang dibuka produser hanya berisi `README.md`, `MIDI/`, `Presets/`, serta `Audio/` atau `Drums/` bila diminta. Semua bahan kerja agent (brief, spesifikasi, script, binding, schema, manifest, receipt, log, output antara, dan arsip revisi lama) berada dalam satu folder `_internal/`. Baca `docs/project-layout.md` saat membuat, merevisi, atau merapikan proyek.

## Alur permintaan

1. Baca `docs/agent-workflow.md` saat membuat musik baru, memakai referensi, atau merevisi komposisi. Baca `docs/composition-guide.md` sebelum menulis spesifikasi; schema otoritatif berada di `src/midi_creator/composition.schema.json`.
2. Ubah brief menjadi tempo, meter, key bila relevan, jumlah bar, bentuk lagu, dan daftar instrumen. Pilih detail yang belum ditentukan dengan pertimbangan musikal dan catat asumsi; tanyakan hanya informasi yang benar-benar menghalangi pekerjaan.
3. Siapkan komposisi baru di `projects/YYYYMMDD-slug/_internal/source-v001/`; folder hasil `v001/` dibuat generator. Simpan permintaan, keputusan, dan kriteria penerimaan dalam `request.md` di folder sumber memakai `templates/request.md`. Revisi berikutnya memakai `v002`, dst., dan menyebut revisi asal. README tingkat proyek menautkan revisi siap pakai terbaru.
4. Tulis `composition.json` di folder sumber internal. Gunakan generator Python lokal jika jumlah nada besar, lalu simpan script di folder sumber agar hasil dapat direproduksi. Seed acak harus tetap dan dicatat. Setelah publikasi, simpan bahan sumber dalam `vNNN/_internal/source/`. Contoh ada di `examples/`.
5. Jalankan `uv sync --locked` jika environment belum siap. Jalankan `uv run midi-creator validate <spec>` lalu `uv run midi-creator generate <spec> --out projects/YYYYMMDD-slug/vNNN` ke folder yang belum ada. Tambahkan `--combined` pada keduanya hanya bila diminta. Ekspor per-layer selalu tersedia.
6. Jalankan `uv run midi-creator verify <folder-output>`. Selesai teknis berarti exit code 0, `ok: true`, semua file yang diminta tersedia, dan setiap file layer memiliki satu track/instrumen serta panjang yang sama.
7. Periksa musikalitas terhadap brief: harmoni, register, fungsi setiap instrumen, ritme drum, perkembangan bagian, dinamika, dan ruang frase. Validator memeriksa struktur MIDI; keputusan musikal tetap perlu dinilai agent. Jika tersedia dan relevan, dengarkan lewat instrumen pengguna. Nyatakan secara akurat apakah audio benar-benar didengarkan.
8. Lengkapi README memakai `templates/project-readme.md`; selesai hanya jika semua file yang ditautkan ada, setiap layer Serum mempunyai file `.SerumPreset` yang lolos pemeriksaan struktur/readback, saran drum sesuai lagu, dan setiap instrumen eksternal mempunyai panduan. Preset belum dianggap selesai jika baru berupa JSON, nama/rekomendasi sound, atau `.vstpreset`. Berikan tautan README, semua MIDI, dan preset native yang dibuat, ringkasan tempo/key/meter/bar/layer, status verifikasi, serta asumsi yang berdampak pada hasil. Laporkan pemuatan plugin dan listening terpisah dari verifikasi struktur preset.

## Revisi dan pemeliharaan

- Untuk Cubase/Serum, baca `docs/cubase-studio.md`. Simpan binding plugin terpisah dari `composition.json`; gunakan konfigurasi lokal dan mapping drum eksplisit. Panggil status terlebih dahulu, verifikasi bundle, dan pisahkan hasil offline dari status live Cubase. Jangan mengklaim `.cpr`, preset native Serum, atau audio yang sudah didengarkan tanpa bukti.

- Jadikan `composition.json` sumber kebenaran. Koreksi spesifikasi dan ekspor ulang ke folder baru untuk memperbaiki MIDI; hasil ekspor menyimpan snapshot komposisinya sendiri.
- MIDI per-layer baru memakai SMF format 1 dengan tepat satu track, tanpa SysEx, metadata teks/key/marker tambahan, Bank Select, atau Program Change. Key dan bagian lagu tetap ada dalam spesifikasi/README. Tempo, meter, nada, velocity, CC7/CC10, serta end-of-track global dipertahankan. Verifikasi file terpisah dari uji drag-and-drop Cubase; laporkan secara akurat bila impor live belum diuji.
- Pertahankan revisi sebelumnya dan bahan referensi pengguna. Revisi musikal menjaga bagian yang diminta tetap sama; dokumentasikan bagian yang diubah dalam `request.md`.
- Satu layer melodi memiliki satu program tetap. Untuk dua instrumen, buat dua layer; artikulasi dan drum map khusus mengikuti plugin pengguna.
- Gunakan `uv run midi-creator --help` untuk opsi CLI. Kesalahan validasi harus diperbaiki sebelum hasil diserahkan.
- Bila mengubah generator/schema, jalankan `uv run python -m unittest discover -s tests -v` dan periksa contoh single serta multi-layer. Perbarui panduan bila kontrak berubah. Komposisi biasa cukup dengan validate/generate/verify dan penilaian musikal.
