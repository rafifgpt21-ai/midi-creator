# Preset native Serum dengan serum-mcp

Preset native Serum 2 dibuat memakai [Celian-mrc/serum-mcp](https://github.com/Celian-mrc/serum-mcp).
Checkout lokal ada di `integrations/serum-mcp`; commit yang dipakai dicatat di
[`serum-mcp-source.json`](../integrations/serum-mcp-source.json). Environment upstream
terpisah dari environment MIDI Creator. Dependensi diinstal dari `uv.lock` upstream
menggunakan Python 3.13.3 yang sudah tersedia di komputer ini.

Server `serum-mcp` terdaftar di konfigurasi global Codex. Restart koneksi Codex/T3 Code
agar tools baru tersedia di sesi berikutnya. Konfigurasi mengarah ke folder asli
`Documents/Xfer/Serum 2 Presets` di OneDrive: `SERUM_PRESETS_PATH` menunjuk `Presets/User`,
`SERUM_TABLES_PATH` menunjuk `Tables`, dan `SERUM_SAMPLES_PATH` menunjuk `Samples`.
`SAMPLE_BANK_PATH` menunjuk bank sample pengguna. Salinan konfigurasi untuk client MCP
lain ada di `integrations/mcp.local.json`.

## Alur preset

1. Panggil `list_parameters()` sebelum merancang preset untuk memastikan nama field,
   enum, rentang, satuan, dan tingkat keyakinan parameter.
2. Gunakan `find_reference_presets(query)` dan `describe_preset(path)` jika ada referensi
   genre, karakter, atau preset tertentu. Pencarian memakai nama/folder; hasil pencarian
   belum membuktikan kualitas sound.
3. Simpan brief dan `preset-spec.json` dalam `_internal/` revisi baru. Tulis oscillator,
   filter, envelope, LFO, `fx_chain`, macro, serta `mod_routes` sesuai fungsi sound.
   Gunakan macro dan modulasi yang berguna secara musikal.
4. Panggil `generate_preset(spec, subfolder)` dalam subfolder baru di `Presets/User`.
   Tool upstream bisa menimpa nama yang sama; cek tujuan lebih dahulu. Revisi memakai
   nama/folder baru dan mempertahankan preset sebelumnya. Untuk `edit_preset`, buat
   salinan revisi terlebih dahulu.
5. Panggil `describe_preset` pada hasil; decode dan cocokkan parameter yang diminta.
   Simpan preset siap pakai dalam `Presets/`, lalu spesifikasi, commit upstream,
   checksum, dan receipt dalam `_internal/`. Lengkapi README revisi dengan mapping
   track/preset, macro, cara membuka sound, serta status pengujian yang benar.
6. Buka hasil melalui browser preset Serum 2 untuk memeriksa kompatibilitas dan suara.
   Verifikasi struktur tidak sama dengan plugin berhasil memuat preset atau audio
   benar-benar didengarkan; catat setiap status secara terpisah.

`serum-mcp` menulis `.SerumPreset` langsung dan tidak memuat plugin, merender audio,
atau mengontrol Cubase. Alur MIDI/live Cubase yang sudah ada tetap menggunakan
`midi-studio`. Offline host MIDI Creator saat ini menerima `.vstpreset`; untuk
merender hasil native melalui host itu, buka di Serum/Cubase lalu simpan sebagai
VST preset. Jangan mengganti ekstensi file untuk konversi.

Wavetable/sample tambahan yang dibuat upstream harus ikut disimpan ketika membagikan
preset. Wavetable factory tetap bergantung pada library Serum yang terpasang.
Bank sample asli pengguna tetap digunakan sebagai sumber baca.

## Pemeriksaan yang dapat diulang

Script [`check_serum_mcp.py`](../integrations/check_serum_mcp.py) membuka koneksi MCP
stdio sungguhan, mengambil schema dan referensi, lalu opsional membuat preset dan
mencocokkan readback struktural. Tujuan output dan preset harus baru.

```powershell
& integrations/serum-mcp/.venv/Scripts/python.exe integrations/check_serum_mcp.py --out integrations/serum-mcp-check-new
& integrations/serum-mcp/.venv/Scripts/python.exe integrations/check_serum_mcp.py --spec projects/20261011-serum-mcp-demo/v002/_internal/preset-spec.json --subfolder 'MIDI Creator/20261011-serum-mcp-demo/v003' --out projects/20261011-serum-mcp-demo/_internal/check-v003
```

Untuk memasang ulang, clone URL pada source receipt ke `integrations/serum-mcp`, checkout
commit tercatat, dan jalankan `uv sync --locked --no-dev --python C:/Python313/python.exe` di
folder repo tersebut. Checkout upstream diabaikan oleh `.gitignore`; preset hasil,
spesifikasi, panduan, dan receipt tetap merupakan artefak workspace.
