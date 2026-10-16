# MIDI Creator

Minta lagu ke agent, lalu buka README proyek dan drag MIDI ke Cubase. Default: aransemen lengkap dari awal sampai akhir, semua instrumen melodi memakai **Serum 2**, dan drum memakai kit/sample pilihan Anda. Setiap instrumen mempunyai **satu file MIDI dengan tepat satu track**, sejajar dari bar 1 hingga akhir lagu.

## Proyek siap dibuka

| Proyek | Tempo / key / panjang | Mulai di sini |
| --- | --- | --- |
| Afterglow Circuit — Progressive House | 126 BPM · F minor · 160 bar · 12 track | [README](projects/20261009-afterglow-circuit-progressive-house/v002/README.md) |
| Neon Step — New Jack Swing | 108 BPM · F# minor · 96 bar · 15 track | [README](projects/20261009-neon-step-new-jack-swing/v004/README.md) |
| Serum Synthwave Starter | 110 BPM · A minor · 16 bar · 10 track | [README](projects/20261010-synthwave-studio-starter/v002/README.md) |
| Neon di Ujung Malam — dark synth-pop | 118 BPM · F# minor · 112 bar · 8 track | [README](projects/20261011-neon-di-ujung-malam/v003/README.md) |
| Warm Motion — uji preset Serum MCP | Pad native dengan chorus/reverb dan 4 macro | [README](projects/20261011-serum-mcp-demo/v002/README.md) |

Revisi timing terbaru: Neon Step v004 mempertahankan 11 layer core dan menyelaraskan empat pelengkap ke groove 60:40; Neon di Ujung Malam v002 menghapus jitter dan offset arp. Pemeriksaan ekspor baru menolak onset off-grid yang tidak dinyatakan disengaja. [Laporan diagnosis](docs/timing-repair-20261011.md).

Versi sebelumnya tetap utuh dalam `_internal/previous-revisions/` di masing-masing proyek. Tiga komposisi telah diekspor ulang tanpa mengubah nada, timing, velocity, volume/pan, atau panjang lagu. Starter menyertakan enam preset VST3 dan stem yang sudah ada; demo Serum MCP menyertakan preset native `.SerumPreset`.

## Meminta lagu

> Buat lagu synthwave 3 menit, mood malam yang hangat, 110 BPM. Bass tebal, chord lebar, arp ringan, dan lead yang mudah diingat.

Anda dapat menentukan genre, mood, tempo, key, panjang, atau sound tertentu. Detail yang belum ditentukan dipilih agent dan dijelaskan dalam README. Permintaan eksplisit satu melodi, cuplikan, atau instrumen di luar Serum tetap diikuti. File gabungan hanya dibuat jika diminta.

Setiap proyek mempunyai panduan import, tabel MIDI/preset, bentuk lagu, saran karakter drum dan mapping pitch, serta petunjuk instrumen eksternal jika diperlukan. Preset Serum native dibuat melalui [serum-mcp](https://github.com/Celian-mrc/serum-mcp).

## Folder yang digunakan produser

```text
projects/nama-proyek/
  README.md          tautan revisi terbaru
  v002/
    README.md        keterangan lagu dan cara memakai hasil
    MIDI/            drag file ini ke Cubase dari bar 1
    Presets/         bila tersedia
    Audio/           bila diminta/disertakan
    Drums/           bila kit/sample telah dipilih
    _internal/       data teknis; tidak diperlukan untuk import
  _internal/         arsip revisi sebelumnya
```

## Import Cubase

MIDI baru memakai **SMF format 1 dengan satu track**, tanpa SysEx, Program Change, atau metadata teks/key/marker tambahan. Tempo, meter, nada, velocity, volume/pan, dan panjang global tetap tersimpan. Key dan bagian lagu ada dalam README.

Untuk locator, time base dan tempo, ikuti [panduan timing impor](docs/cubase-studio.md#timing-saat-impor-cubase).

Di **Preferences > MIDI > MIDI File**, aktifkan **Import Dropped File as Single Part**. Untuk MIDI format 0 lama, nonaktifkan **Auto Dissolve Format 0**. [Panduan resmi Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html) menjelaskan kedua opsi ini. Pilih preset di Serum sebelum memasukkan MIDI.

File lama tidak mengandung pesan SysEx. Track “SysEx Data” pada screenshot belum direproduksi otomatis dalam Cubase; format baru merupakan mitigasi impor, dan hasil drag-and-drop live masih perlu diperiksa di Cubase Anda.

## Agent dan pengembangan

[Panduan sound design Serum 2 dan tujuh skill agent](docs/serum-sound-design/README.md) mencakup teori, lima engine, modulasi, FX, keluarga sound, rekonstruksi referensi, preset native, dan verifikasi. Mulai dengan `$serum-sound-design` untuk permintaan sound lengkap.

[Panduan detail analog dan retro Serum 2](skills/serum-sound-design/references/analog-retro.md) menjadi default untuk sound analog/vintage/retro analog serta pendekatan gear analog nyata. Panduan membedakan VCO/DCO, variasi voice dan drift, lima teknik karakter analog, resep instrumen, serta verifikasi.

[AGENTS.md](AGENTS.md) menetapkan default dan kriteria hasil. [Struktur proyek](docs/project-layout.md), [kontrak komposisi](docs/composition-guide.md), [Serum MCP](docs/serum-mcp.md), serta [Cubase/live studio](docs/cubase-studio.md) menjelaskan pengerjaan teknis. Kode/dependency/integrasi di root adalah framework; produser cukup memakai `projects/`.

```powershell
uv sync --locked
uv run midi-creator --help
uv run midi-creator validate examples/multi-layer/composition.json
uv run midi-creator generate examples/multi-layer/composition.json --out projects/demo-output
uv run midi-creator verify projects/demo-output
uv run python -m unittest discover -s tests -v
```

Ekspor memakai folder baru: `MIDI/*.mid`, `README.md`, dan seluruh snapshot/manifest/validation di `_internal/`. `--combined` menambahkan `MIDI/arrangement.mid` jika diminta. Verifikasi ekspor lama tetap didukung. Kebijakan grid/swing ada di [kontrak timing](docs/composition-guide.md#pemeriksaan-grid-onset). Restart koneksi Codex/T3 Code setelah perubahan framework agar server MCP memuat implementasi terbaru.
