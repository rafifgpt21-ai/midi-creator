# Revisi timing

- Proyek: Neon Step - New Jack Swing
- Revisi: v003; asal v002
- Tanggal: 2026-10-11

## Permintaan asli

“hampir di semua projek, file midi ... temponya tidak rapih dan tidak konsisten antar layer ... tidak on grid ... telusuri kenapa dan perbaiki”

Steering: seluruh layer sudah di-drop di grid yang sama; lead/arp terasa tidak menyambung dengan piano/pad.

## Keputusan dan perubahan

Semua onset pada grid straight 1/16, tanpa jitter, swing baked-in, strum delay atau clap flam. Dark synth arp kehilangan offset tetap 1/32 sehingga pulsa eighth-note sejajar dengan groove. Nada, velocity, sound, mixer, tempo, meter, PPQN, bagian dan panjang tetap. Durasi/gate hanya dipendekkan bila onset baru menyebabkan overlap pitch yang sama; detail pada timing-change.json. Revisi lama tetap utuh. Versi New Jack Swing ini merupakan alternatif straight; versi swing tersedia pada revisi asal.

## Penerimaan

Validate/generate/verify dan audit MIDI independen lulus; zero off-grid onset pada 1/16. Preset yang sudah ada dipakai ulang byte-identik. Pemuatan plugin/listening serta impor live belum diuji. Ekspor ulang dari Cubase masih diperlukan untuk membandingkan posisi part/note sesudah drop.
