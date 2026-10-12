# Contoh yang bisa dijalankan

- `single-layer`: piano, C major, 100 BPM, 4/4, empat bar. Satu file `piano.mid`.
- `multi-layer`: A minor, 92 BPM, 4/4, delapan bar. Enam file terpisah: electric piano, bass, lead, kick, snare, dan closed hi-hat.

Setiap contoh menyimpan `composition.json`. Folder `output/` berisi hasil yang sudah dibuat dan diverifikasi. Perintah generate menggunakan output yang baru; untuk membuat varian, salin contoh ke revisi baru di `projects/`, edit spesifikasinya, lalu jalankan generator di sana.

File MIDI per layer memiliki tepat satu track. Semua onset, keheningan, dan akhir komposisi tetap sejajar di DAW. Contoh ini menunjukkan format kerja; gaya musik untuk permintaan berikutnya mengikuti pengguna.
