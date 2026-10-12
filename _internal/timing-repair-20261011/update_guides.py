from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'src/midi_creator/spec.py').is_file())

def replace(file, old, new):
    path = ROOT / file
    text = path.read_text(encoding='utf-8')
    if old not in text:
        raise ValueError(f'{file}: expected text missing')
    path.write_text(text.replace(old, new), encoding='utf-8')

grid = '''
## Pemeriksaan grid onset

`validate` dan ekspor baru memeriksa onset absolut pada grid straight 1/32 secara default. Pilih grid secara eksplisit dengan `"timing": {"mode": "strict", "grid_division": 16}` untuk 1/16. Division 12/24/48/96 mendukung triplet; pilihan lengkap ada dalam schema. Posisi grid dibulatkan ke tick dengan half-up. Durasi/gate tidak wajib pada grid; pemeriksaan berlaku pada note-on, termasuk offset dan pengulangan clip. Validator menolak offset dan tidak mengkuantisasi diam-diam.

Untuk swing atau humanization timing yang disengaja, gunakan `"timing": {"mode": "free", "grid_division": 16}` dan catat rasio, anchor antarlayer, serta toleransinya dalam brief/README. Mode ini mempertahankan offset; bukan bukti groove konsisten. Default humanization melalui velocity dan gate. Sinkopasi pada grid tetap sah. Audit pola bersama tetap diperlukan karena offset yang tepat pada subgrid pun dapat terasa tidak cocok dengan pulsa layer lain.

`verify` tetap menerima snapshot arsip tanpa kebijakan timing dan menambahkan laporan `timing` terpisah: `mode`, `grid_division`, `on_grid`, jumlah dan contoh offset per layer. `ok: true` membuktikan integritas/struktur MIDI, bukan bahwa seluruh onset lurus. Snapshot dengan mode strict tetap wajib memenuhi grid; mode free yang disengaja perlu pemeriksaan groove tersendiri.

'''
replace('docs/composition-guide.md', '## Dokumen minimum', grid + '## Dokumen minimum')
replace('docs/composition-guide.md', '`ticks_per_beat`, `key_signature`, `sections`', '`ticks_per_beat`, `timing`, `key_signature`, `sections`')
replace('docs/agent-workflow.md', 'Clip berulang berguna untuk pola dasar.', 'Tetapkan satu grid onset dan anchor groove bersama sebelum menulis layer; ikuti kebijakan `timing` dalam [kontrak komposisi](composition-guide.md#pemeriksaan-grid-onset). Default onset strict, humanization melalui velocity/gate. Untuk swing yang disengaja, catat rasio dan gunakan transform timing yang sama pada layer yang berbagi pulsa. Nilai lead/arp terhadap bass, drum dan chord bersama; lolos grid saja tidak menjamin ritme cocok.\n\nClip berulang berguna untuk pola dasar.')
replace('AGENTS.md', '- Semua layer dalam satu komposisi menggunakan tempo, meter, resolusi, titik awal, dan panjang total yang sama.', '- Onset default memakai satu grid strict yang dinyatakan dalam `timing`; humanization default melalui velocity/gate. Untuk swing yang disengaja, nyatakan mode free, rasio dan anchor bersama sesuai `docs/composition-guide.md`. Nilai ritme lead/arp bersama core bass/drum/chord sebelum menyerahkan hasil.\n- Semua layer dalam satu komposisi menggunakan tempo, meter, resolusi, titik awal, dan panjang total yang sama.')

import_guide = '''
## Timing saat impor Cubase

Atur tempo/meter project sesuai README dan instrument track pada **Musical Time Base** (ikon not). Untuk posisi deterministik gunakan **File > Import > MIDI File**, left locator **1.1.1.0**, dan **Import to Left Locator**. Pada project bertempo tetap yang sudah disetel sesuai lagu, **Ignore Master Track Events on Merge** mempertahankan tempo project. Untuk drop, **Import Dropped File as Single Part** menjaga file sebagai satu part; tempatkan semua part pada bar 1 dan pertahankan keheningan awal. Periksa start part melalui Info Line dan onset dalam Key Editor Bars+Beats. Snap menentukan posisi part, bukan mengkuantisasi isi nada. Hindari menggeser nada pertama dari layer yang masuk belakangan ke bar 1.

Grid straight dan swing harus mengikuti kebijakan README lagu. Mengkuantisasi seluruh New Jack Swing ke grid straight mengubah groove yang disengaja. Jika file asli sudah pada grid tetapi hasil impor berbeda, diperlukan posisi part/nada yang tersimpan di Cubase untuk membedakan offset impor dari ritme komposisi; pemeriksaan offline tidak membuktikan hasil drop live.

[Opsi impor resmi](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html?contentId=u1NHlJBAfqTrfj0eW_QNMQ) menjelaskan locator, single part dan master events. [Time base track](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/track_handling/track_handling_defining_the_track_time_base_t.html) menjelaskan musical/linear.

'''
replace('docs/cubase-studio.md', '## Enable live Cubase control once', import_guide + '## Enable live Cubase control once')
replace('docs/cubase-studio.md', 'The local MIDI schema and generator are unchanged.', 'The MIDI schema now includes an optional timing policy; new validation/export checks onset grids, while legacy verification reports timing separately. See [composition timing](composition-guide.md#pemeriksaan-grid-onset).')
replace('docs/project-layout.md', 'Pilih preset pada instrument track Serum sebelum memasukkan MIDI dan letakkan', 'Untuk posisi dan time base, ikuti [panduan timing impor](cubase-studio.md#timing-saat-impor-cubase). Single Part tidak mengkuantisasi nada.\nPilih preset pada instrument track Serum sebelum memasukkan MIDI dan letakkan')
replace('templates/project-readme.md', '1. Atur tempo/meter project dan mulai import dari bar 1.', '1. Atur tempo/meter project, Musical Time Base, dan left locator 1.1.1.0. Gunakan Import to Left Locator untuk impor dari bar 1; Single Part untuk drop.\n   Untuk project bertempo tetap sesuai lagu, Ignore Master Track Events on Merge mempertahankan tempo project.')
replace('templates/project-readme.md', 'Catat asumsi musikal, hasil validate/generate/verify,', 'Catat grid onset atau rasio swing/anchor bersama, asumsi musikal, hasil validate/generate/verify,')

replace('projects/README.md', '20261009-neon-step-new-jack-swing/v002/README.md', '20261009-neon-step-new-jack-swing/v004/README.md')
replace('projects/README.md', '| Neon Step | [v002]', '| Neon Step | [v004]')
replace('projects/README.md', '20261011-neon-di-ujung-malam/v001/README.md', '20261011-neon-di-ujung-malam/v002/README.md')
replace('projects/README.md', '| Neon di Ujung Malam — dark synth-pop | [v001]', '| Neon di Ujung Malam — dark synth-pop | [v002]')
replace('README.md', '20261009-neon-step-new-jack-swing/v002/README.md', '20261009-neon-step-new-jack-swing/v004/README.md')
replace('README.md', '| Warm Motion — uji preset Serum MCP', '| Neon di Ujung Malam — dark synth-pop | 118 BPM · F# minor · 112 bar · 8 track | [README](projects/20261011-neon-di-ujung-malam/v002/README.md) |\n| Warm Motion — uji preset Serum MCP')
replace('README.md', 'Versi sebelumnya tetap utuh', 'Revisi timing terbaru: Neon Step v004 mempertahankan 11 layer core dan menyelaraskan empat pelengkap ke groove 60:40; Neon di Ujung Malam v002 menghapus jitter dan offset arp. Pemeriksaan ekspor baru menolak onset off-grid yang tidak dinyatakan disengaja. [Laporan diagnosis](docs/timing-repair-20261011.md).\n\nVersi sebelumnya tetap utuh')
replace('README.md', 'Di **Preferences > MIDI > MIDI File**,', 'Untuk locator, time base dan tempo, ikuti [panduan timing impor](docs/cubase-studio.md#timing-saat-impor-cubase).\n\nDi **Preferences > MIDI > MIDI File**,')
replace('README.md', 'Verifikasi ekspor lama tetap didukung.', 'Verifikasi ekspor lama tetap didukung. Kebijakan grid/swing ada di [kontrak timing](docs/composition-guide.md#pemeriksaan-grid-onset).')

for name in ['integrations/repair_project_timing.py', 'projects/20261009-neon-step-new-jack-swing/v003/_internal/source/repair_project_timing.py', 'projects/20261011-neon-di-ujung-malam/v002/_internal/source/repair_project_timing.py']:
    replace(name, 'ROOT=Path(__file__).resolve().parents[1]', "ROOT=next(p for p in Path(__file__).resolve().parents if (p/'src'/'midi_creator'/'spec.py').is_file())")
for name in ['projects/20261011-neon-di-ujung-malam/README.md']:
    replace(name, ']( ', '](')
replace('projects/20261009-neon-step-new-jack-swing/v004/README.md', 'Swing pasangan not 1/16 sebesar 60:40; variasi velocity memakai seed 108960 tanpa jitter onset tambahan.', 'Swing pasangan not 1/16 sebesar 60:40; seed velocity asal 108960. Offset core asli, termasuk clap flam, dipertahankan; strum delay pada muted guitar dihapus.')
replace('projects/20261009-neon-step-new-jack-swing/v004/README.md', 'Revisi ini memperbarui struktur folder dan file impor; nada/velocity/timing/mixer tetap sama seperti v001.', 'Revisi v004 mempertahankan core v002 dan memperbaiki onset empat layer pelengkap seperti dijelaskan di atas. Pitch/velocity/durasi/mixer tetap sama.')
print('Guides and latest revision links updated.')
