"""Producer-facing instructions; performance data stays in the composition schema."""

from .spec import Composition


def project_readme(composition: Composition) -> str:
    source = composition.source
    meter = source['time_signature']
    lines = [f"# {source['title']}", "",
             f"{source['tempo_bpm']} BPM | {meter[0]}/{meter[1]} | "
             f"{source.get('key_signature', 'pusat tonal mengikuti nada')} | {source['bars']} bar", "",
             "## Memakai MIDI di Cubase", "",
             "1. Atur tempo/meter project sesuai keterangan di atas dan gunakan Musical Time Base (ikon not).",
             "2. Buat satu instrument track Serum 2 untuk setiap instrumen melodi. Pilih preset sesuai fungsi pada tabel.",
             "3. Impor semua file dari bar 1; untuk File > Import > MIDI File gunakan left locator 1.1.1.0 dan Import to Left Locator. Pertahankan keheningan awal/akhir.",
             "4. Untuk drum, pilih sendiri kit/sample dan cocokkan pitch pada tabel drum di bawah.", "",
             "Setiap file berisi tepat satu track instrumen dan mencakup seluruh panjang lagu. "
             "File baru memakai SMF format 1, tanpa SysEx, teks/marker tambahan, atau Program Change. "
             "Preset dipilih di Serum, bukan oleh MIDI.", "",
             "## Instrumen", "", "| Track | Fungsi | Sound awal | MIDI |", "| --- | --- | --- | --- |"]
    for source_layer, layer in zip(source['layers'], composition.layers):
        name = layer.name.replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
        role = source_layer.get('role', 'mengikuti aransemen').replace('|', '\\|')
        sound = 'Serum 2; pilih preset sesuai fungsi' if layer.kind == 'melodic' else 'Kit/sample pilihan Anda'
        lines.append(f"| {name} | {role} | {sound} | [{layer.id}.mid](MIDI/{layer.id}.mid) |")
    lines.extend(["", "## Drum yang disarankan", "",
                  "Pilih kit yang sesuai warna lagu: kick dengan low-end yang menyisakan ruang bass; "
                  "snare/clap untuk backbeat; hi-hat pendek agar groove tetap jelas. "
                  "Sesuaikan karakter dan panjang tail terhadap tempo serta kepadatan aransemen. "
                  "Sample belum dipilih atau disertakan dalam ekspor MIDI ini.", "",
                  "| Track drum | Pitch MIDI |", "| --- | --- |"])
    drums = [layer for layer in composition.layers if layer.kind == 'drums']
    for layer in drums:
        pitches = ', '.join(str(pitch) for pitch in sorted({note.pitch for note in layer.notes}))
        lines.append(f"| {layer.name.replace('|', ' / ')} | {pitches} |")
    if not drums:
        lines.append("| Belum ada layer drum dalam aransemen ini | — |")
    lines.extend(["", "Jika beberapa bagian drum memakai channel 10 dan satu kit bersama, "
                  "filter CC7/CC10 saat impor lalu atur volume/pan per pad, atau gunakan track sampler terpisah.", "",
                  "## Instrumen di luar Serum", "",
                  "Default semua instrumen melodi menggunakan Serum 2; drum memakai sampler/kit pilihan Anda. "
                  "Belum ada plugin atau library melodi eksternal yang dikonfigurasikan dalam ekspor ini. "
                  "Ekspor MIDI saja belum membuktikan adanya preset atau plugin yang berhasil dimuat."])
    policy = source.get('timing', {})
    division = policy.get('grid_division', 32)
    lines.extend(["", "## Timing", "",
                  (f"Onset memakai grid straight 1/{division}. Durasi/gate dapat lebih pendek dari grid."
                   if policy.get('mode') != 'free' else
                   "Timing free: swing/offset disengaja dipertahankan. Catat rasio dan anchor groove antarlayer sebelum memakai hasil ini."),
                  "Snap posisi part tidak mengkuantisasi isi nada. Periksa part pada bar 1 dan nada dalam Key Editor Bars+Beats; jangan memindahkan nada pertama layer yang masuk belakangan ke bar 1."])
    if source.get('sections'):
        beats_per_bar = meter[0] * 4 / meter[1]
        lines.extend(["", "## Bagian lagu", "", "| Bagian | Mulai bar |", "| --- | --- |"])
        for section in source['sections']:
            name = section['name'].replace('|', '\\|')
            lines.append(f"| {name} | {section['start'] / beats_per_bar + 1:g} |")
    if source.get('assumptions'):
        lines.extend(["", "## Asumsi", ""] + [f"- {item}" for item in source['assumptions']])
    lines.extend(["", "## Keterangan hasil", "",
                  "Verifikasi struktur MIDI lulus. Status sound/preset dan listening perlu dicatat "
                  "sesuai pemeriksaan yang benar-benar dilakukan. Data teknis dan snapshot komposisi ada di `_internal/`.", "",
                  "Untuk impor Cubase, buka Preferences > MIDI > MIDI File: aktifkan "
                  "**Import Dropped File as Single Part** dan nonaktifkan **Auto Dissolve Format 0** "
                  "untuk file lama. Pada project bertempo tetap sesuai lagu, Ignore Master Track Events on Merge mempertahankan tempo project. Keberhasilan drag-and-drop perlu diperiksa di Cubase Anda.", "",
                  "[Panduan resmi impor Cubase](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html)"])
    return '\n'.join(lines) + '\n'
