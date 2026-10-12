# Struktur proyek untuk produser

Area siap pakai setiap revisi:

```text
projects/YYYYMMDD-nama-lagu/
  README.md                 tautan revisi siap pakai terbaru
  v002/
    README.md               mulai di sini
    MIDI/                   satu instrumen, satu track, satu file
    Presets/                preset Serum 2 dan sound lain yang diminta
    Audio/                  hanya bila stem/preview diminta
    Drums/                  hanya bila kit/sample sudah dipilih pengguna
    _internal/              seluruh bahan teknis dan arsip
```

Simpan brief, spesifikasi performa, script generator, binding, spesifikasi preset,
schema, checksum, receipt, dan output antara dalam `_internal/`. Source komposisi
baru adalah `_internal/composition.json`; ketika hasil dipublikasikan, file di
lokasi itu menjadi snapshot yang diverifikasi generator. Bahan kerja tambahan
dapat ditempatkan di `_internal/source/`.

Generator menerbitkan folder baru berisi `README.md`, `MIDI/`, dan `_internal/`.
Untuk revisi baru, simpan source/brief di folder persiapan `_internal` milik proyek,
generate ke folder revisi yang belum ada, lalu pindahkan bahan kerja itu ke
`vNNN/_internal/source/`. Alternatif: generate ke staging `_internal/export/`,
verifikasi, kemudian publikasikan isi hasil ke revisi tanpa menimpa file.
Agent melengkapi README bawaan dengan keputusan sound dan drum khusus brief.
Contoh: source `projects/NEW/_internal/source/composition.json`, ekspor baru
`projects/NEW/v001`, kemudian salin brief/script/binding ke
`projects/NEW/v001/_internal/source/`. Buat index `projects/NEW/README.md` yang
menautkan `v001/README.md`. `_internal` tingkat proyek boleh menjadi tempat staging
dan arsip, sedangkan `_internal` revisi menyimpan snapshot dan receipt hasil itu.

Preset native `.SerumPreset` berada di `Presets/`; catat track tujuan dan macro yang
berguna. File wavetable/sample tambahan yang benar-benar diperlukan ikut paket,
dengan petunjuk lokasi instalasi. `.vstpreset` tetap diberi nama format aslinya dan
dijelaskan cara membukanya. Preset native tidak dianggap berhasil dimuat hanya
karena dapat didecode.

Setiap README revisi mengikuti `templates/project-readme.md`. README tingkat proyek
menautkan revisi terbaru dan menjelaskan lokasi arsip. Untuk merapikan proyek lama,
buat revisi baru dari spesifikasi lama tanpa mengubah nada atau timing. Simpan
revisi lama utuh di `_internal/previous-revisions/` tingkat proyek dan catat lokasi
asalnya. Periksa checksum file arsip dan perbaiki tautan dokumentasi yang berubah.

Nama `_internal` mengelompokkan bahan teknis di satu tempat; folder tidak diberi
atribut hidden Windows agar agent, backup, dan pengguna tetap dapat membukanya.
Kode framework (`src`, `tests`, dependency, integrasi) tetap di root workspace;
produser cukup membuka `projects/` lewat README utama.

## MIDI dan Cubase

Ekspor baru memakai format 1 dengan satu track instrumen per file. Nama track,
tempo, meter, CC7/CC10, nada, dan panjang global dipertahankan. Teks judul, key
signature, marker bagian, serta Program Change GM tidak dikirim pada per-layer;
keterangan musik tetap tersedia di README dan snapshot. Gabungan opsional tetap
mempunyai conductor track. File lama dan manifest v1 tetap bisa diverifikasi.

Audit file lama di workspace menemukan nol pesan SysEx. Track bernama “SysEx Data”
di screenshot belum dapat direproduksi otomatis dalam Cubase, sehingga penyebab
pastinya belum terkonfirmasi. Format 1 dan metadata minimal menghindari jalur
pemisahan format 0; ini mitigasi yang dapat diperiksa pada file.

Untuk drag-and-drop, di Preferences > MIDI > MIDI File aktifkan **Import Dropped
File as Single Part**. Untuk MIDI format 0 lama, nonaktifkan **Auto Dissolve Format
0**. Pengaturan ini dijelaskan dalam [panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html).
Untuk posisi dan time base, ikuti [panduan timing impor](cubase-studio.md#timing-saat-impor-cubase). Single Part tidak mengkuantisasi nada.
Pilih preset pada instrument track Serum sebelum memasukkan MIDI dan letakkan
semua file di bar 1. Jangan memotong keheningan awal.
