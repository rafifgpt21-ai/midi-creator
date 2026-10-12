# Kontrak komposisi v1

Schema di `src/midi_creator/composition.schema.json` adalah sumber otoritatif untuk tipe, field, dan rentang. CLI `schema` mencetaknya. Field yang tidak dikenal ditolak agar salah ketik terlihat.

## Waktu dan nada

`start` dan `duration` memakai **quarter-note beats**, dimulai dari 0. `tempo_bpm` juga dihitung per quarter note, termasuk dalam meter seperti 6/8. Satu bar memiliki `numerator × 4 / denominator` beat: 4/4 = 4; 3/4 = 3; 6/8 = 3. Total beat = `bars × beat_per_bar`.

Default resolusi adalah 480 tick per quarter note. Nilai beat diubah ke tick dengan pembulatan half-up; onset dan akhir nada dibulatkan terpisah. Naikkan `ticks_per_beat` untuk pola sangat rapat. Durasi yang membulat menjadi nol ditolak. Nada dan marker harus berada dalam panjang komposisi.

Pitch berupa angka MIDI 0–127 atau nama seperti `C4`, `F#3`, `Bb2`, `C-1`. **C4 = 60**, A4 = 69. DAW tertentu menamai angka 60 sebagai C3/C5; angka MIDI tetap sama. `velocity` 1–127, default 90. Nada berbeda boleh simultan untuk chord; pitch sama boleh retrigger tepat ketika nada sebelumnya berakhir, namun overlap pitch yang sama ditolak.


## Pemeriksaan grid onset

`validate` dan ekspor baru memeriksa onset absolut pada grid straight 1/32 secara default. Pilih grid secara eksplisit dengan `"timing": {"mode": "strict", "grid_division": 16}` untuk 1/16. Division 12/24/48/96 mendukung triplet; pilihan lengkap ada dalam schema. Posisi grid dibulatkan ke tick dengan half-up. Durasi/gate tidak wajib pada grid; pemeriksaan berlaku pada note-on, termasuk offset dan pengulangan clip. Validator menolak offset dan tidak mengkuantisasi diam-diam.

Kebijakan musikal default dan pengecualian pengguna mengikuti [panduan timing MIDI](midi-timing-guide.md): on-grid tanpa swing, dengan dotted note dan meter selain 4/4 tetap diizinkan. Jika pengguna meminta swing atau humanization timing, gunakan `"timing": {"mode": "free", "grid_division": 16}` dan catat rasio bila memakai swing, anchor antarlayer, serta toleransinya dalam brief/README. Mode ini mempertahankan offset; bukan bukti groove konsisten. Audit pola bersama tetap diperlukan karena offset yang tepat pada subgrid pun dapat terasa tidak cocok dengan pulsa layer lain.

`verify` tetap menerima snapshot arsip tanpa kebijakan timing dan menambahkan laporan `timing` terpisah: `mode`, `grid_division`, `on_grid`, jumlah dan contoh offset per layer. `ok: true` membuktikan integritas/struktur MIDI, bukan bahwa seluruh onset lurus. Snapshot dengan mode strict tetap wajib memenuhi grid; mode free yang disengaja perlu pemeriksaan groove tersendiri.

## Dokumen minimum

```json
{
  "version": 1,
  "title": "Piano pendek",
  "tempo_bpm": 100,
  "time_signature": [4, 4],
  "bars": 1,
  "key_signature": "C",
  "layers": [{
    "id": "piano",
    "name": "Piano",
    "kind": "melodic",
    "program": 0,
    "notes": [
      {"pitch": "C4", "start": 0, "duration": 1, "velocity": 90},
      {"pitch": "E4", "start": 1, "duration": 1, "velocity": 85},
      {"pitch": "G4", "start": 2, "duration": 1.5, "velocity": 95}
    ]
  }]
}
```

Field opsional tingkat komposisi: `description`, `prompt`, `assumptions` (array string), `ticks_per_beat`, `timing`, `key_signature`, `sections` (`name`, `start`), dan `$schema` untuk bantuan editor. Key signature adalah metadata; generator mempertahankan pitch yang ditulis, sehingga nada kromatik tetap bisa dipakai. Key minor memakai format seperti `Am`, `F#m`.

## Instrumen dan layer

`id` unik menggunakan huruf kecil, angka, dan tanda hubung, dimulai dengan huruf. ID dipakai sebagai filename; nama khusus Windows seperti `con` dan `aux` ditolak. `name` adalah nama track di DAW, dan `role` opsional.

`kind: "melodic"` mewajibkan `program` GM **0-based** (0–127). Jika referensi menulis nomor 1–128, kurangi satu. Program tetap untuk seluruh layer. `kind: "drums"` memakai channel 10 dan pitch percussion; field `program` tidak digunakan dan ditolak. Tidak ada batas genre atau pilihan sound DAW: instrumen plugin ditentukan saat playback, sementara MIDI mengirim data performa.

`channel` ditulis 1–16 dalam spesifikasi, dikonversi menjadi 0–15 oleh renderer. Channel 10 dicadangkan untuk drum. Ekspor per-layer memberi channel 1 untuk instrumen melodi secara default; file yang independen boleh berbagi nomor channel. Bila memakai `--combined`, channel melodi dialokasikan berbeda dan slot eksplisit diperhitungkan terlebih dahulu. Maksimal 15 layer melodi dapat digabungkan dalam kontrak satu port MIDI ini; jumlah layer ekspor terpisah dapat lebih banyak.

`volume` default 100 (CC7) dan `pan` default 64/tengah (CC10), keduanya 0–127. Untuk kit khusus, pilih mapping pitch sesuai instrumen di DAW dan catat di `request.md`. Contoh yang disertakan menggunakan program piano 0, electric piano 4, finger bass 33, serta percussion kick 36, snare 38, dan closed hi-hat 42.

## Notes dan clips

Layer membutuhkan minimal satu nada melalui `notes`, `clips`, atau keduanya. `notes` memakai onset absolut dari awal komposisi. `clips` memakai onset nada relatif terhadap awal clip:

```json
{
  "id": "kick",
  "name": "Kick",
  "kind": "drums",
  "clips": [{
    "start": 0,
    "repeat": 4,
    "every": 4,
    "notes": [
      {"pitch": 36, "start": 0, "duration": 0.2, "velocity": 105},
      {"pitch": 36, "start": 2, "duration": 0.2, "velocity": 95}
    ]
  }]
}
```

Onset hasil = `clip.start + indeks_pengulangan × every + note.start`. `repeat` default 1; jika lebih dari 1, `every` wajib. Pola contoh membutuhkan empat bar 4/4. Nada dari clips dan notes digabungkan lalu diperiksa terhadap batas dan overlap. Untuk variasi, gunakan clip berbeda atau tambahkan notes pada bagian tertentu.

Ekspor per-layer baru adalah SMF type 1 dengan tepat satu track instrumen, tempo,
meter, nama track, CC7/CC10, dan end-of-track pada panjang global. Key/marker bagian
tetap berada dalam spesifikasi dan README; teks/key/marker tambahan, SysEx,
Bank Select, serta Program Change tidak dikirim pada per-layer. `program` GM dalam
spesifikasi tetap merupakan hint sound dan dikirim hanya dalam gabungan opsional.
Gabungan adalah type 1 dengan conductor track serta track tiap instrumen.
Manifest ekspor v2 dan snapshot/validation/summary berada di `_internal/`, file
produser di `MIDI/` dan `README.md`. Ekspor lama v1/type 0 tetap bisa diverifikasi.

## Validasi dan batas v1

Validator menolak schema salah, JSON duplicate key/non-finite numbers, ID duplikat, pitch di luar MIDI, velocity nol, durasi nol, nada melewati akhir, dan overlap pitch sama setelah pembulatan tick. Generasi dilakukan dalam staging lalu folder dipublikasikan setelah verifikasi lulus. Output yang sudah ada dipertahankan; buat revisi/folder baru.

`verify` membuka MIDI, memeriksa tempo/meter/PPQN, panjang semua track, channel/program, jumlah nada, pasangan note-on/off, inventory, checksum, dan kecocokan byte dengan komposisi snapshot. Hasil yang sengaja diedit di DAW bisa berbeda dari snapshot; ekspor ulang dari spesifikasi untuk membuat hasil framework yang tervalidasi.

Tempo dan meter konstan dalam v1. Pitch bend, automation CC selain pengaturan awal volume/pan, sustain pedal, sysex, microtonality, dan keyswitch belum mempunyai field. Jika brief memerlukan fitur ini, perluas schema, renderer, dan validator bersama pemeriksaan yang sesuai. Timing, velocity, dan panjang nada dapat mengungkapkan banyak variasi performa tanpa fitur tersebut.

Semantik teknis mengikuti [Mido: MIDI files](https://mido.readthedocs.io/en/stable/files/midi.html), [message ranges](https://mido.readthedocs.io/en/stable/message_types.html), dan [meta messages](https://mido.readthedocs.io/en/stable/meta_message_types.html).
