"""Point producer indexes at the verified v003; preserve previous revisions."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'src/midi_creator/spec.py').is_file())
project=ROOT/'projects/20261011-neon-di-ujung-malam'
folder=project/'v003'
read=lambda path:json.loads(path.read_text(encoding='utf-8'))
midi=read(folder/'_internal/verify-receipt.json')
presets=read(folder/'_internal/preset-check/receipt.json')
music=read(folder/'_internal/musical-check.json')
origin=read(folder/'_internal/origin-preservation.json')
assert midi['ok'] and midi['timing']['on_grid'] and presets['ok'] and music['ok']
assert all(hashlib.sha256((project/'v002'/file).read_bytes()).hexdigest()==digest
           for file,digest in origin['sha256'].items())
assert {p.name for p in folder.iterdir()}=={'README.md','MIDI','Presets','_internal'}
assert len(list((folder/'MIDI').glob('*.mid')))==8
assert len(list((folder/'Presets').glob('*.SerumPreset')))==7
(project/'README.md').write_text(
    '# Neon di Ujung Malam\n\n'
    '[Revisi terbaru v003 — harmoni lebih gelap dan sedih](v003/README.md).\n\n'
    '118 BPM · F# minor · 4/4 · 112 bar · delapan instrumen yang sama, tujuh preset native Serum 2. '
    'Chorus F#m9–E(add9)–Dmaj7–C#7(b9); verse dengan bass kromatis turun. Semua onset pada grid 1/16.\n\n'
    '[v002 — koreksi timing](v002/README.md) dan [v001 — aransemen awal](v001/README.md) tetap utuh. '
    'Bahan teknis berada di `_internal/` setiap revisi.\n',encoding='utf-8')
for path in [ROOT/'README.md',ROOT/'projects/README.md']:
    text=path.read_text(encoding='utf-8')
    text=text.replace('20261011-neon-di-ujung-malam/v002/README.md','20261011-neon-di-ujung-malam/v003/README.md')
    text=text.replace('| Neon di Ujung Malam — dark synth-pop | [v002]', '| Neon di Ujung Malam — dark synth-pop | [v003]')
    path.write_text(text,encoding='utf-8')
receipt={'ok':True,'revision':'v003','origin':'v002','midi_files':8,'native_presets':7,
         'notes':sum(l['note_count'] for l in music['layers']),
         'all_onsets_grid':'straight 1/16','origin_preserved':True,
         'drum_byte_identical':True,'preset_readback':True,
         'tempo_bpm':118,'key':'F#m','meter':[4,4],'bars':112,'ppqn':960,
         'duration_seconds':227.7968,'end_tick':430080,
         'live_import_tested':False,'plugin_loaded':False,'listening':False,
         'files':{p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                  for parent in [folder/'MIDI',folder/'Presets'] for p in parent.iterdir() if p.is_file()}}
(folder/'_internal/completion-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print('Published v003 indexes: MIDI/grid/harmony, native preset readback and original preservation PASS.')
