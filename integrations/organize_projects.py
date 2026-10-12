"""Prepare producer-friendly v002 packages while retaining original v001 revisions.

Run from the workspace with `uv run python integrations/organize_projects.py`.
Archiving is a separate checked PowerShell move after package verification.
"""

import json
from pathlib import Path
import shutil

import mido

from midi_creator.cli import main as midi_cli
from midi_creator.export import digest, generate_export, json_bytes, verify_export
from midi_creator.studio.session import verify_session

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / 'projects'

DRUMS = {
    '20261009-afterglow-circuit-progressive-house':
        'Kick elektronik tebal dengan transient jelas dan tail pendek/sedang untuk four-on-the-floor 126 BPM. '
        'Clap lebar untuk backbeat; snare tajam yang tetap bersih saat roll makin rapat. '
        'Closed hat pendek untuk sixteenth, open hat lebih terang di offbeat, ride tipis di final drop, '
        'serta shaker ringan. Hindari kick yang tail-nya menutup bass offbeat. Sample/kit masih dipilih Anda.',
    '20261009-neon-step-new-jack-swing':
        'Kick drum-machine yang padat dan pendek, snare elektronik dengan gated tail untuk backbeat, '
        'clap sebagai lapisan chorus, closed hat kering dan open hat pendek agar swing sixteenth 108 BPM '
        'tetap jelas. Shaker ringan, tambourine terang di chorus, serta tom elektronik bernada untuk fill. '
        'Gunakan velocity ghost snare yang lebih lembut, bukan sample besar pada setiap pukulan. '
        'Sample/kit masih dipilih Anda.',
    '20261010-synthwave-studio-starter':
        'Kick drum-machine dengan low-end padat dan tail pendek, snare elektronik dengan body sedang '
        'yang dapat diberi gated reverb, closed hat kering, dan open hat terang dengan decay terkendali '
        'untuk eighth-note groove 110 BPM. Kit lama ikut disalin sebagai pilihan yang sudah ada; '
        'Anda boleh mengganti sample pada pitch yang sama. Kit lama menggunakan 36 kick, 38 snare, '
        '42 closed hat, dan 46 open hat.'
}


def bounded(path):
    resolved = path.resolve()
    if not resolved.is_relative_to(PROJECTS.resolve()):
        raise ValueError(f'Outside projects: {resolved}')
    return resolved


def fingerprint(folder):
    return {path.relative_to(folder).as_posix(): digest(path.read_bytes())
            for path in sorted(folder.rglob('*')) if path.is_file()}


def performance(path):
    midi = mido.MidiFile(path, charset='utf-8')
    tick, events = 0, []
    for message in midi.tracks[0]:
        tick += message.time
        if message.type in ('note_on', 'note_off', 'control_change'):
            events.append((tick, message.copy(time=0).bytes()))
    return midi.ticks_per_beat, tick, events


def prepare(project):
    old = bounded(project / 'v001')
    new = bounded(project / 'v002')
    before = fingerprint(old)
    source = old / 'composition.json'
    if source.is_file():
        if midi_cli(['validate', str(source)]):
            raise ValueError('Source validation failed')
        generated = generate_export(source, new)
        for layer in generated['manifest']['layers']:
            previous = old / 'output/midi/layers' / f"{layer['id']}.mid"
            assert performance(previous) == performance(new / layer['file']), layer['id']
        text = (new / 'README.md').read_text(encoding='utf-8')
        start = text.index('Pilih kit yang sesuai warna lagu:')
        end = text.index('\n\n| Track drum', start)
        text = text[:start] + DRUMS[project.name] + text[end:]
        if (old / 'studio').is_dir():
            assert verify_session(old / 'studio')['ok']
            for previous, current in [('presets', 'Presets'), ('audio', 'Audio'), ('samples', 'Drums')]:
                shutil.copytree(old / 'studio' / previous, new / current)
            (new / '_internal/drum-kit.json').write_bytes((old / 'studio/drum-kit.json').read_bytes())
            text += '\n## Preset dan audio yang ikut paket\n\n'
            text += ('Preset VST3 dan stem dari starter v001 dipertahankan tanpa perubahan sound. '
                     'Di MediaBay Cubase, browse `Presets/` lalu buat instrument track dari `.vstpreset`. '
                     'Import MIDI yang namanya sama di bar 1. Untuk native Serum MCP lihat proyek demo terpisah.\n\n'
                     '| Track | Preset | Audio |\n| --- | --- | --- |\n')
            for track in generated['manifest']['layers']:
                name = track['id']
                preset = f'[VST3](Presets/{name}.vstpreset)' if (new / f'Presets/{name}.vstpreset').is_file() else 'Drums/'
                text += f'| {name} | {preset} | [stem](Audio/{name}.wav) |\n'
            text += ('\nGunakan audio ATAU MIDI untuk setiap part agar tidak terdengar ganda. '
                     'Stem lama sudah diverifikasi sejajar dan tidak dirender ulang dalam revisi ini. '
                     'Drums/kit.sfz dapat dibuka di sampler SFZ; untuk Groove Agent SE muat WAV ke pad '
                     '36/38/42/46. Audio belum didengarkan.\n')
        else:
            text += ('\n## Sound untuk revisi ini\n\n'
                     'Revisi ini memperbarui struktur folder dan file impor; nada/velocity/timing/mixer '
                     'tetap sama seperti v001. Preset Serum baru belum dibuat untuk lagu arsip ini. '
                     'Gunakan Serum 2 dengan karakter sesuai nama/fungsi track, atau sound sebelumnya.\n')
        if 'new-jack-swing' in project.name:
            text += ('\nUntuk electric piano dan muted guitar, gunakan engine multisample Serum 2 '
                     '(epiano_suitcase / guitar_ac) sebagai titik awal, envelope pendek untuk guitar scratches. '
                     'Untuk slap bass realistis, bila suara Serum tidak mencukupi gunakan library bass yang Anda '
                     'sudah miliki: buat instrument track terpisah, muat patch slap, import `slap-bass.mid` '
                     'di bar 1, cek rentang pitch pada `_internal/validation.json`, lalu sesuaikan keyswitch '
                     'menurut manual library. MIDI ini belum mengandung keyswitch. '
                     'Sound eksternal ini opsional dan belum dipasang atau diuji.\n')
        (new / 'README.md').write_text(text, encoding='utf-8')
        assert verify_export(new)['ok']
    else:
        if new.exists():
            raise FileExistsError(new)
        (new / 'Presets').mkdir(parents=True)
        (new / '_internal').mkdir()
        original = old / 'native-verified/PD - Warm Motion MCP.SerumPreset'
        copied = new / 'Presets' / original.name
        shutil.copy2(original, copied)
        assert digest(original.read_bytes()) == digest(copied.read_bytes())
        text = ('# Serum MCP: Warm Motion\n\n'
                '[Preset native PD - Warm Motion MCP](Presets/PD%20-%20Warm%20Motion%20MCP.SerumPreset).\n\n'
                'Pad analog hangat dengan chorus, hall reverb, dan 4 macro: BRIGHT, MOTION, SPACE, COLOR. '
                'Attack 650 ms, release 1.7 detik; mainkan chord register tengah C3-C5. '
                'Sudah dipasang di browser Serum: User > MIDI Creator > 20261011-serum-mcp-demo > v001.\n\n'
                'Ini proyek uji preset, sehingga tidak mempunyai lagu, MIDI, atau drum. '
                'Jika dipakai untuk synthwave, kick pendek dan snare gated dapat melengkapinya; '
                'drum tetap pilihan Anda. Tidak ada instrumen melodi di luar Serum.\n\n'
                'Koneksi MCP serta struktur preset/macro/14 modulasi lulus verifikasi. '
                'Preset belum dimuat di plugin atau didengarkan. '
                'Catatan teknis dan percobaan terdahulu berada di arsip `_internal/previous-revisions/v001` tingkat proyek.\n')
        (new / 'README.md').write_text(text, encoding='utf-8')
        shutil.copy2(old / 'preset-spec.json', new / '_internal/preset-spec.json')
        shutil.copy2(old / 'native-verified/receipt.json', new / '_internal/original-preset-receipt.json')
    request = ('# Revisi struktur proyek\n\nTanggal: 2026-10-11. Revisi: v002. '
               'Asal: v001 (dipertahankan utuh dalam _internal/previous-revisions).\n\n'
               'Permintaan: default instrumen Serum 2 selain drum pilihan pengguna; per-layer MIDI '
               'sepanjang lagu, README khusus proyek, dan bahan teknis di satu folder.\n\n'
               'Perubahan: layout hasil, README, serta profil MIDI format 1 dengan metadata minimal '
               'dan tanpa Program Change. Nada, timing, velocity, CC7/10, serta panjang total '
               'dibandingkan terhadap v001 dan dipertahankan. Sound/preset yang ada tidak diubah. '
               'MIDI/preset-only dibedakan; tidak ada lagu baru yang dikomposisikan.\n\n'
               'Uji impor live Cubase dan listening belum dilakukan. Nol pesan SysEx ditemukan '
               'pada MIDI lama; perubahan format merupakan mitigasi impor, bukan klaim '
               'bahwa penyebab track SysEx Data telah dibuktikan.\n')
    (new / '_internal/request.md').write_text(request, encoding='utf-8')
    assert fingerprint(old) == before, 'Original revision changed'
    receipt = {'ok': True, 'from': str(old), 'to': str(new), 'original_files': before,
               'new_files': fingerprint(new), 'cubase_import_tested': False, 'auditioned': False}
    (new / '_internal/migration.json').write_bytes(json_bytes(receipt))
    (project / 'README.md').write_text(
        f"# {project.name}\n\n[Mulai di sini — revisi v002](v002/README.md).\n\n"
        'Semua file siap import ada di v002. Bahan teknis dan revisi lama disimpan di '
        '`_internal/previous-revisions/`; v001 tetap dipertahankan.\n', encoding='utf-8')
    print(f'Prepared and verified: {new.relative_to(ROOT)}')


if __name__ == '__main__':
    for folder in sorted(PROJECTS.iterdir()):
        if folder.is_dir() and (folder / 'v001').is_dir():
            prepare(folder)
