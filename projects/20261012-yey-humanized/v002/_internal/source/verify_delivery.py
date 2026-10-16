"""Musical acceptance checks, independent of the framework's byte verification."""
import hashlib
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
REV = HERE.parent.parent if HERE.name == 'source' else HERE.parent.parent / 'v002'
PROJECT = REV.parent
spec = json.loads((HERE / 'composition.json').read_text(encoding='utf-8'))
design = json.loads((HERE / 'performance-design.json').read_text(encoding='utf-8'))
analysis = json.loads((HERE / 'reference-analysis.json').read_text(encoding='utf-8'))
layers = {l['id']: l for l in spec['layers']}
chords = {'F#m': ({6, 9, 1}, 6), 'B/D#': ({11, 3, 6}, 3), 'D6': ({2, 6, 9, 11}, 2),
          'E': ({4, 8, 11}, 4), 'E/G#': ({4, 8, 11}, 8), 'A': ({9, 1, 4}, 9), 'B': ({11, 3, 6}, 11)}
harmony = design['harmony']
assert spec['tempo_bpm'] == 120 and spec['time_signature'] == [4, 4] and spec['bars'] == 76
assert spec['timing'] == {'mode': 'strict', 'grid_division': 32}
assert len(layers) == 7 and 'precision-bass' not in layers
reference = PROJECT / '_internal/references/yey.mid'
assert hashlib.sha256(reference.read_bytes()).hexdigest() == analysis['source_sha256']
assert all(n['start'] >= 16 for l in layers.values() for n in l['notes'])

bar_checks = []
for b in range(4, 76):
    expected, root = chords[harmony[b]]
    source_pcs = {n['pitch'] % 12 for n in analysis['tracks'][2]['notes'] if b*1920 <= n['start_tick'] < (b+1)*1920}
    assert source_pcs == expected, (b + 1, source_pcs, expected)
    piano = [n for n in layers['piano']['notes'] if n['start'] < (b+1)*4 and n['start'] + n['duration'] > b*4]
    piano_pcs = {n['pitch'] % 12 for n in piano}
    assert piano_pcs == expected, (b+1, piano_pcs, expected)
    # Left root present at every change; preserve exact inversion class.
    roots = [n for n in piano if n['start'] == b*4 and n['pitch'] < 60]
    assert roots and min(n['pitch'] for n in roots) % 12 == root
    if b >= 8:
        bass = [n for n in layers['bbc-basses']['notes'] if n['start'] <= b*4 < n['start']+n['duration']]
        assert len(bass) == 1 and bass[0]['pitch'] % 12 == root
    bar_checks.append({'bar': b+1, 'chord': harmony[b], 'piano_pitch_classes': sorted(piano_pcs), 'bass_pc': root, 'ok': True})

# All sustained supporting lines must agree throughout their full note lengths.
for ident in ('bbc-basses', 'bbc-violas', 'bbc-violins-1', 'bbc-flutes', 'bbc-clarinets'):
    for n in layers[ident]['notes']:
        for b in range(int(n['start']//4), min(75, int((n['start']+n['duration']-0.001)//4))+1):
            assert n['pitch'] % 12 in chords[harmony[b]][0], (ident, n, b+1)

official = {'piano': (21,108), 'bbc-basses': (24,54), 'bbc-celli': (36,82), 'bbc-violas': (48,90),
            'bbc-violins-1': (55,97), 'bbc-flutes': (59,96), 'bbc-clarinets': (50,88)}
ranges = {}
for ident, layer in layers.items():
    notes = layer['notes']
    low, high = min(n['pitch'] for n in notes), max(n['pitch'] for n in notes)
    assert official[ident][0] <= low <= high <= official[ident][1]
    assert all(abs(n['start']*8 - round(n['start']*8)) < 1e-6 for n in notes)
    if ident != 'piano':
        assert all(a['start']+a['duration'] <= b['start']+0.001 for a,b in zip(notes,notes[1:])), ident
        controls = layer['control_changes']
        assert {c['control'] for c in controls} == {1,11}
        assert all(c['value'] == 100 for c in controls if c['control'] == 1)
    ranges[ident] = {'midi_min': low, 'midi_max': high, 'notes': len(notes),
                     'first_bar': round(notes[0]['start']/4+1,3),
                     'last_note_end_bar': round(max(n['start']+n['duration'] for n in notes)/4+1,3)}
for n in layers['bbc-flutes']['notes']:
    assert not any(c['start'] < n['start']+n['duration'] and c['start']+c['duration'] > n['start'] for c in layers['bbc-celli']['notes'])

anchors = design['piano_rh_anchors'][4:]
travel = [abs(a-b) for v,w in zip(anchors,anchors[1:]) for a,b in zip(v,w)]
assert all(v[0] < v[1] < v[2] and v[2]-v[0] <= 12 for v in anchors)
assert max(travel) <= 5
source_tops = [max(n['pitch'] for n in analysis['tracks'][2]['notes'] if b*1920 <= n['start_tick'] < (b+1)*1920) for b in range(4,76)]
old_top_travel = [abs(a-b) for a,b in zip(source_tops,source_tops[1:])]
new_top_travel = [abs(v[2]-w[2]) for v,w in zip(anchors,anchors[1:])]
roles = design['piano_role_events']
left = [n for n in layers['piano']['notes'] if n['pitch'] < 60]
assert all(a['start']+a['duration'] <= b['start']+0.001 or abs(a['pitch']-b['pitch']) <= 12 for i,a in enumerate(left) for b in left[i+1:] if a['start'] <= b['start'] < a['start']+a['duration'])
receipt = {
    'ok': True, 'reference_sha256': analysis['source_sha256'], 'preserved_progression_bars': 72,
    'preserved_initial_silence_bars': 4, 'bar_checks': bar_checks, 'layers': ranges,
    'piano_rh_anchor_travel': {'max_semitones': max(travel), 'mean_semitones': round(statistics.mean(travel),3),
                              'common_voice_transitions': travel.count(0), 'total_voice_transitions': len(travel),
                              'max_hand_span_semitones': max(v[2]-v[0] for v in anchors)},
    'piano_upper_anchor_comparison': {'source_max_travel': max(old_top_travel), 'source_mean_travel': round(statistics.mean(old_top_travel),3),
                                      'v002_max_travel': max(new_top_travel), 'v002_mean_travel': round(statistics.mean(new_top_travel),3),
                                      'scope': 'Bar upper anchors; not an audio-quality score or every melodic note.'},
    'cello_melody_pitch_class_preservation': [n['pitch']%12 for n in layers['bbc-celli']['notes']] == [n['pitch']%12 for n in analysis['tracks'][3]['notes']],
    'flute_overlaps_cello': False,
    'verification_scope': 'Symbolic musical and MIDI design; no playback/listening inference.',
}
write = HERE / 'musical-audit.json'
write.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k not in ('bar_checks','layers')}, indent=2))
