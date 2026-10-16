"""Deterministic piano-only revision. Run: uv run python <this file>."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = next(p for p in HERE.parents if p.name == '20261012-yey-humanized')
BASE = PROJECT / 'v002'
OLD = json.loads((BASE / '_internal/composition.json').read_text(encoding='utf-8'))
DESIGN = json.loads((BASE / '_internal/source/performance-design.json').read_text(encoding='utf-8'))
HARMONY = DESIGN['harmony']
ANCHORS = DESIGN['piano_rh_anchors']
CHORDS = {
    'F#m': ({6, 9, 1}, 6), 'B/D#': ({11, 3, 6}, 3),
    'D6': ({2, 6, 9, 11}, 2), 'E': ({4, 8, 11}, 4),
    'E/G#': ({4, 8, 11}, 8), 'A': ({9, 1, 4}, 9),
    'B': ({11, 3, 6}, 11),
}
LAYERS = {l['id']: l for l in OLD['layers']}
END = OLD['bars'] * 4
EVENTS = []


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def section(b):
    return next(s['name'] for s in reversed(OLD['sections']) if s['start'] <= b * 4)


def overlaps(n, start, end):
    return n['start'] < end - 1e-7 and n['start'] + n['duration'] > start + 1e-7


def pcs(b):
    return CHORDS[HARMONY[b]][0]


def dynamic(b):
    nominal = {'a1': 0, 'held': -9, 'a2': 2, 't1': 5, 'b1': 4,
               'lead': -4, 't2': 8, 'b2': 5, 'final': -3}[section(b)]
    # Deterministic four-bar breath; no random variation or onset offset.
    arc = [0, 2, 1, -2][(b - 4) % 4]
    if b >= 72:
        nominal = -7 - (b - 72) * 3
    return nominal + arc


def add(layer, pitch, start, duration, velocity, role):
    duration = min(duration, END - start)
    assert duration > 0
    note = {'pitch': int(pitch), 'start': start, 'duration': round(duration * 480) / 480,
            'velocity': int(max(1, min(127, velocity)))}
    layer['notes'].append(note)
    EVENTS.append({'layer': layer['id'], 'bar': int(start // 4) + 1, 'role': role, **note})


def path(rows, targets, max_move, center=None):
    """Voice-leading DP; modest span, stable voice order, gentle contrary motion."""
    costs = {v: sum(abs(p-t) * .2 for p, t in zip(v, targets[0])) for v in rows[0]}
    parents = []
    for idx, (options, target) in enumerate(zip(rows[1:], targets[1:]), 1):
        new, parent = {}, {}
        for v in options:
            candidates = []
            for prev, cost in costs.items():
                moves = [abs(a-b) for a, b in zip(v, prev)]
                if max(moves) > max_move:
                    continue
                penalty = sum(m + 1.1 * max(0, m-2)**2 for m in moves)
                penalty += sum(.18 * abs(p-t) for p, t in zip(v, target))
                if center:
                    upper_change = center[idx] - center[idx-1]
                    change = v[-1] - prev[-1]
                    if change * upper_change > 0:
                        penalty += 2.0
                    if change == upper_change and abs(v[-1]-center[idx]) % 12 in (0, 7):
                        penalty += 4.0
                candidates.append((cost+penalty, prev))
            if candidates:
                new[v], parent[v] = min(candidates)
        assert new, ('No voice-leading path', idx)
        parents.append(parent)
        costs = new
    v = min(costs, key=lambda v: (costs[v], v))
    result = [v]
    for parent in reversed(parents):
        v = parent[v]
        result.append(v)
    return list(reversed(result))


def piano(layer_id, name, role, volume, pan):
    return {'id': layer_id, 'name': name, 'kind': 'melodic', 'program': 0,
            'role': role, 'channel': 1, 'volume': volume, 'pan': pan, 'notes': []}


# Commit ARR-SPEC before emitting any notes. Inherit only the fixed form/harmony
# and unchanged orchestral decisions; replace all former single-piano intent.
arr = json.loads((BASE / '_internal/source/ARR-SPEC.json').read_text(encoding='utf-8'))
arr['meta']['title'] = 'Yey — Three Stereo Pianos and BBC Discover'
arr['meta']['upstream']['brief'] = 'request.md; v002; original yey.mid'
arr['intent'] = {
    'one_thing': 'Expand only the piano into a complementary stereo trio, keeping every original chord and song position.',
    'reference_pair': [
        {'track': 'Original yey.mid', 'borrow': 'Exact 72-bar progression, slash basses, harmonic rhythm, silence and open B/D# ending.'},
        {'track': 'Yey v002 piano and BBC arrangement', 'borrow': 'Connected upper contour, all six BBC performances, and space for cello/woodwind phrases.'}],
    'listener_situation': 'Stereo listening with a stable center and interlocking acoustic piano gestures at the sides.',
    'emotional_arc': arr['intent']['emotional_arc'],
}
arr['material'] = {
    'motif': 'Two bars: a held center chord/top voice, a mid-register broken-chord rise and return on the left, answered by a high descending two/three-note phrase on the right.',
    'character': 'Spacious, lyrical, and quietly grand', 'stated_in': ['a1'],
    'development_mode': '加工处理',
}
for f in arr['form']:
    f['note'] = 'Source form and chords locked; stereo piano density and touch vary, BBC parts unchanged.'
    if f['id'] == 'held':
        f['development'] = 'augment'
    elif f['id'] == 'lead':
        f['development'] = 'vary'
    elif f['id'] == 'final':
        f['note'] += ' Varied recap, liquidated to sparse two-note side gestures over bars 73–76.'
arr['arrangement']['roster'] = [
    {'id': 'piano-center', 'instrument': 'User-selected acoustic piano', 'role': 'harmony', 'band': 'low and mid-high',
     'midi': {'program': 0, 'bank': 0, 'channel': 1}, 'entry': 'a1', 'exit': 'end',
     'note': 'Bass and three close upper anchors; connected gates, strongest top-voice touch.'},
    {'id': 'piano-left', 'instrument': 'Separate user-selected acoustic piano instance', 'role': 'texture', 'band': 'mid',
     'midi': {'program': 0, 'bank': 0, 'channel': 1}, 'entry': 'a1 beat 1-and', 'exit': 'end',
     'note': 'Legato-light broken-chord figure; no deep bass, fewer notes under cello.'},
    {'id': 'piano-right', 'instrument': 'Separate user-selected acoustic piano instance', 'role': 'countermelody', 'band': 'high',
     'midi': {'program': 0, 'bank': 0, 'channel': 1}, 'entry': 'a1 beat 2-and', 'exit': 'end',
     'note': 'High descending replies; silence in wind bars and at cello entrances, no copied delay part.'},
] + arr['arrangement']['roster'][1:]
arr['arrangement']['depth_map'] = {l['id']: ('foreground' if l['id'].startswith('piano') else
    ('midground' if l['id'] in ('bbc-celli', 'bbc-flutes', 'bbc-clarinets') else 'background'))
    for l in arr['arrangement']['roster']}
arr['arrangement']['spectrum_budget'] = [
    {'band': 'low', 'owner': 'bbc-basses', 'competitors': ['piano-center'], 'resolution': 'Keep single piano bass in center and use v002 octave lift from bar 9.'},
    {'band': 'mid', 'owner': 'bbc-celli', 'competitors': ['piano-left'], 'resolution': 'Reduce left to two restrained notes per bar under theme; one line, no chord stack.'},
    {'band': 'mid-high', 'owner': 'piano-center', 'competitors': ['piano-left'], 'resolution': 'Center holds anchors while left attacks between center gestures; side touch is subordinate.'},
    {'band': 'high', 'owner': 'bbc-flutes and bbc-clarinets during replies', 'competitors': ['piano-right'], 'resolution': 'Right leaves every wind-containing bar silent.'},
]
arr['arrangement']['subtraction_events'] = [
    {'at': {'section': 'held', 'bar_offset': 0}, 'what': 'Lengthen and reduce both side figures', 'why': 'Retain original held-section breath.'},
    {'at': {'section': 'lead', 'bar_offset': 0}, 'what': 'Remove right on cello entry and thin left', 'why': 'Keep source theme in focus.'},
    {'at': {'section': 'final', 'bar_offset': 12}, 'what': 'Reduce all piano gestures, soften progressively', 'why': 'Retain original open ending.'},
]
arr['arrangement']['hooks']['arrangement_hook'] = {
    'what': 'Left broken-chord gesture answered by high right piano over a stable center chord.',
    'first_at': 'a1', 'recurs_at': ['a2', 'b1', 'b2', 'final'],
}
arr['arrangement']['groove']['fill_policy'] = {'bars': [20, 24, 52, 60, 71], 'rationale': 'One extra soft left chord tone at selected seams, no new chord.'}
arr['mix_intent'] = {
    'mood': 'A broad piano trio in one coherent acoustic space, with the original intimate orchestra behind it.',
    'sound_stage': [{'id': l['id'], 'pan': {'piano-center': 0, 'piano-left': -69, 'piano-right': 70}.get(l['id'],
                     round((LAYERS.get(l['id'], {}).get('pan', 64)-64)/63*100)),
                     'depth': 'near' if l['id'].startswith('piano') else 'mid' if l['id'] in ('bbc-celli', 'bbc-flutes', 'bbc-clarinets') else 'far'}
                    for l in arr['arrangement']['roster']],
    'focus_by_section': [{'section': f['id'], 'focus': 'bbc-celli with center piano support' if f['id'] in ('lead', 'final') else 'piano-center with alternating side gestures'} for f in arr['form']],
    'ducking_map': [], 'deliberate_imbalance': [],
    'width_map': {'a1': 'Side notes unfold after center', 'held': 'Fewer stereo transients', 'b1': 'Open interlock',
                  'lead': 'Subdued around cello and wind rests', 't2': 'Fullest stereo register',
                  'b2': 'Longer replies in second half', 'final': 'Recap then sparse sides in final four bars'},
    'dynamics': {'target_DR_dB': 0, 'notes': ['MIDI delivery; no audio loudness target. Preserve left/right balance by ear after patch loading.']},
    'reference_tracks': [{'track': 'v002 symbolic arrangement', 'aspect': 'Foreground theme and retained orchestra; no reference audio available for mix matching.'}],
}
arr['render'] = {'midi': {'instrument_map': {l['id']: {'name': l['instrument'], 'program': l['midi']['program'], 'bank': 0, 'channel': 1} for l in arr['arrangement']['roster']}}}
arr['checks'] = {
    'self_audit': [
        '1: Four intent fields and two specific source references complete.',
        '2: Existing sections contiguous over bars 1–76.', '3: Four-bar held and transition sections retained.',
        '4: Energy keys inherited unchanged for the locked form.', '5: Held section, theme entrance and ending recede.',
        '6: Three explicit subtraction events.', '7: All entries set; existing winds exit early.',
        '8: Stereo call/answer hook defined.', '9: D6 retains borrowed D natural.',
        '10: Seam fill bars 20,24,52,60,71 are non-periodic.', '11: Strict timing exception, zero onset jitter.',
        '12: Stereo activity changes through sections while track pans stay fixed.', '13: Exempt non-Suno output.',
        '14: 76*4/120*60=152 seconds.', '15: No vocals.', '16: No vocals; B2 piano reply varies.',
        '17: No style fusion.', '18: Motif develops by repeat, augmentation, variation and varied recap.',
        '19: Inherited ASCII chord spellings.', '20: Inherited tonal meta/section names and structured subtraction positions.',
    ],
    'exemptions': [
        'One chord per bar, exact form and last B/D# are user-locked; no reharmonization or added tonic cadence.',
        'Workspace strict timing policy takes precedence over generic push/pull recommendations.',
        'Piano and BBC factory patches continue the project instrument exceptions; no new sound design or Serum patch.',
        'No audio reference, render, listening, vocal, score, Suno/YuE, combined MIDI or CPR requested.',
        'Left is accompaniment figuration; use counterpoint complementarity principles, not a strict species-counterpoint claim.',
    ],
}
save('ARR-SPEC.json', arr)

center = piano('piano-center', 'Piano Center', 'harmony', 94, 64)
left = piano('piano-left', 'Piano Left', 'texture', 82, 20)
right = piano('piano-right', 'Piano Right', 'countermelody', 84, 108)

# Left voices cover the chord within one octave. D6's D is in center bass.
left_rows = []
for b in range(4, 76):
    upper = {6, 9, 11} if HARMONY[b] == 'D6' else pcs(b)
    left_rows.append([v for v in itertools.combinations(range(53, 69), 3)
                      if v[-1]-v[0] <= 12 and {p % 12 for p in v} == upper])
left_voicings = [None]*4 + path(left_rows, [(55, 60, 64)]*72, 5)

# Right reply anchor is an independent smooth high line, not the center line at octave.
right_rows = [[(p,) for p in range(80, 90) if p % 12 in pcs(b)
               and any(q % 12 in pcs(b) for q in range(max(77, ANCHORS[b][-1]+2), p))]
              for b in range(4, 76)]
right_targets = [(87 if section(b) in ('t2', 'b2') else 84,) for b in range(4, 76)]
right_anchor = [None]*4 + [v[0] for v in path(right_rows, right_targets, 5, [v[-1] for v in ANCHORS[4:]])]

for b in range(4, 76):
    t, sid, d = b*4, section(b), dynamic(b)
    v = ANCHORS[b]
    bass = min(n['pitch'] for n in LAYERS['piano']['notes'] if t <= n['start'] < t+4)
    add(center, bass, t, 3.94 if b < 75 else 3.68, 53+d, 'bass/inversion')
    for i, p in enumerate(v):
        # Tie common upper voice only; keeps an audible held line over moving sides.
        previous = next((n for n in reversed(center['notes']) if n['pitch'] == p and n['start'] < t), None)
        # A piano decays: refresh the common top at least once every two bars.
        if i == 2 and b % 2 == 1 and previous and abs(previous['start']+previous['duration']-t) < .07:
            previous['duration'] = round((t+3.96-previous['start'])*480)/480
            if b == 75:
                previous['duration'] -= .28
        else:
            add(center, p, t, (3.96 if b < 75 else 3.68), (73 if i == 2 else 51+i*3)+d, 'upper' if i == 2 else 'inner-anchor')
    # Center stays metrically simple; selected lift bars rearticulate only the two inner keys.
    if sid in ('t1', 't2') or (sid in ('b1', 'b2') and b % 4 == 2):
        for i, p in enumerate(v[:2]):
            add(center, p, t+2, 1.91, 49+i*2+d, 'inner-pulse')

    lv = left_voicings[b]
    # A repeated turn identifies the left; returning B2 uses an altered ending.
    if sid == 'held':
        lp = [(0.5, lv[0], 1.35), (2.5, lv[2], 1.35)]
    elif b >= 72:
        lp = [(0.5, lv[0], 1.35), (2.5 if b < 75 else 1.0, lv[1], 1.2 if b < 75 else 2.5)]
    elif sid in ('lead', 'final'):
        lp = [(0.5, lv[0], 1.4), (2.5, lv[1 if b % 2 else 2], 1.35)]
    elif sid == 'a1' and b < 8:
        lp = [(0.5, lv[0], .95), (2, lv[1], .9), (3, lv[2], .8)]
    elif sid == 'b2' and b >= 56:
        lp = [(0.5, lv[0], .8), (1, lv[1], .8), (2, lv[2], .8), (3, lv[1], .8)]
    else:
        lp = [(0.5, lv[0], .85), (1, lv[1], .85), (2, lv[2], .85), (3, lv[1 if b % 2 else 0], .8)]
    if b+1 in (20, 24, 52, 60, 71):
        lp.append((3.0, lv[2], .72))
        # Replace that onset's normal note rather than double the seam accent.
        lp = [x for k, x in enumerate(lp) if x[0] != 3.0 or k == len(lp)-1]
    for j, (off, p, dur) in enumerate(lp):
        add(left, p, t+off, dur, 48+d+(2 if j == 1 else 0)-(3 if j == len(lp)-1 else 0), 'broken-chord')

    wind_bar = any(overlaps(n, t, t+4) for name in ('bbc-flutes', 'bbc-clarinets') for n in LAYERS[name]['notes'])
    if wind_bar or b in (32, 60):
        continue
    high = right_anchor[b]
    # Diatonic/chord-tone answer descending below anchor, strictly above center.
    minimum = max(77, v[-1]+2)
    lower = [p for p in range(max(minimum, high-5), high) if p % 12 in pcs(b)]
    answer = max(lower) if lower else high
    return_pitch = min((p for p in range(max(minimum, answer-5), answer) if p % 12 in pcs(b)), default=high,
                       key=lambda p: abs(p-(answer-3)))
    if sid == 'held':
        rp = [(1.5, high, .85), (3.5, answer, .43)]
    elif b >= 72:
        rp = [(1.5, high, 1.0), (3.5, answer, .32)] if b < 75 else [(1.5, answer, 2.15)]
    elif sid in ('lead', 'final'):
        # One bar out of every four rests; let cello phrase points stay clear.
        rp = [] if b % 4 == 0 else [(1.5, high, .85), (3.5, answer, .42)]
    elif sid in ('t1', 't2') or (sid == 'b2' and b >= 56):
        rp = [(1.5, high, .8), (2.5, answer, .8), (3.5, return_pitch, .42)]
    else:
        rp = [(1.5, high, .85), (3.5, answer, .42)]
    for j, (off, p, dur) in enumerate(rp):
        add(right, p, t+off, dur, 54+d-(3*j), 'high-answer')

# Release each repeated key before its own next attack. This also clips center
# inner anchors before the half-bar rearticulation without modifying any onset.
for layer in (center, left, right):
    layer['notes'].sort(key=lambda n: (n['start'], n['pitch']))
    for p in {n['pitch'] for n in layer['notes']}:
        notes = [n for n in layer['notes'] if n['pitch'] == p]
        for a, z in zip(notes, notes[1:]):
            assert a['start'] < z['start'], (layer['id'], a, z)
            a['duration'] = min(a['duration'], round((z['start']-a['start']-.025)*480)/480)

new = copy.deepcopy(OLD)
new.update(title='Yey — Three Stereo Pianos and BBC Discover',
           description='v003: piano-only rewrite into independent center/left/right parts; all BBC layers and harmonic/form timeline unchanged.',
           prompt='Rewrite only piano as three complementary stereo piano performances, preserving chord progression and song structure.',
           assumptions=[
               'Continue the user-selected acoustic piano and BBCSO Discover exceptions from v002; no new sound or Serum layers.',
               'Three independent acoustic piano instances; CC10 center64, left20, right108; manual DAW panning if plugin ignores MIDI pan.',
               'F# Dorian with D natural on D6; retain exact chords, inversions, sections, four silent bars, 120 BPM, 4/4 and 76 bars.',
               'All six BBC layers are unchanged including notes, timing, velocity, mixer and CC1/CC11.',
               'Strict 1/32 policy inherited; new piano onsets are straight eighth-note subdivisions, with deterministic velocity/gate phrasing.',
               'No MIDI sustain pedal, randomness, combined file, new patches, audio or CPR.',
               'Actual plugin loading, Cubase import, audible balance, reverb/mono compatibility and listening not tested.',
           ])
new['layers'] = [center, left, right] + [copy.deepcopy(l) for l in OLD['layers'] if l['id'] != 'piano']
save('composition.json', new)

bindings = json.loads((BASE / '_internal/source/bindings.json').read_text(encoding='utf-8'))
original_binding = bindings['mapping'][0]
bindings['mapping'] = [{**copy.deepcopy(original_binding), 'layer': l['id'], 'cc10_pan': l['pan'],
                       'status': 'Manual loading; separate acoustic piano instance. MIDI pan requires plugin support.'}
                      for l in (center, left, right)] + bindings['mapping'][1:]
save('bindings.json', bindings)
save('performance-design.json', {'source': 'v002', 'randomness': 'none', 'harmony': HARMONY,
    'center_anchors': ANCHORS, 'left_voicings': left_voicings, 'right_anchors': right_anchor,
    'event_roles_before_gate_cleanup': EVENTS})

# Musical acceptance is distinct from MIDI integrity verification.
for k in ('tempo_bpm', 'time_signature', 'bars', 'ticks_per_beat', 'key_signature', 'timing', 'sections'):
    assert new[k] == OLD[k], k
unchanged = []
for l in new['layers'][3:]:
    assert l == LAYERS[l['id']], l['id']
    unchanged.append(l['id'])
bar_checks = []
for b in range(4, 76):
    sounding = [n for l in (center, left, right) for n in l['notes'] if overlaps(n, b*4, (b+1)*4)]
    assert {n['pitch'] % 12 for n in sounding} == pcs(b), (b+1, HARMONY[b], sounding)
    assert min(n['pitch'] for n in sounding) % 12 == CHORDS[HARMONY[b]][1], b+1
    bar_checks.append({'bar': b+1, 'chord': HARMONY[b], 'pitch_classes': sorted(pcs(b)),
                       'lowest_pitch': min(n['pitch'] for n in sounding)})
for l in (center, left, right):
    assert min(n['start'] for n in l['notes']) >= 16
    for n in l['notes']:
        assert abs(n['start']*2-round(n['start']*2)) < 1e-7
        for b in range(int(n['start']//4), min(76, math.ceil((n['start']+n['duration'])/4))):
            if overlaps(n, b*4, (b+1)*4):
                assert n['pitch'] % 12 in pcs(b), (l['id'], n, b)
left_onsets = {n['start'] for n in left['notes']}
right_onsets = {n['start'] for n in right['notes']}
assert not (left_onsets & right_onsets), left_onsets & right_onsets
assert all(not overlaps(w, n['start']//4*4, n['start']//4*4+4)
           for n in right['notes'] for k in ('bbc-flutes', 'bbc-clarinets') for w in LAYERS[k]['notes'])

stats = {}
for l in (center, left, right):
    stats[l['id']] = {'notes': len(l['notes']), 'pitch_range': [min(n['pitch'] for n in l['notes']), max(n['pitch'] for n in l['notes'])],
        'velocity_range': [min(n['velocity'] for n in l['notes']), max(n['velocity'] for n in l['notes'])],
        'pan_cc10': l['pan'], 'volume_cc7': l['volume'], 'first_beat': min(n['start'] for n in l['notes']),
        'sections': {s['name']: sum(1 for n in l['notes'] if section(int(n['start']//4)) == s['name']) for s in OLD['sections']}}
save('musical-audit.json', {'ok': True, 'base': 'v002', 'preserved_non_piano_specs': unchanged,
    'global_properties_identical': True, 'chord_bars': bar_checks, 'all_piano_gates_chord_supported': True,
    'strict_eighth_note_onsets': True, 'simultaneous_left_right_attack_times': 0,
    'right_piano_silent_in_wind_bars': True, 'piano_stats': stats,
    'center_anchor_max_span': max(v[-1]-v[0] for v in ANCHORS[4:]),
    'center_anchor_max_voice_travel': max(abs(a-z) for v, w in zip(ANCHORS[4:], ANCHORS[5:]) for a, z in zip(v, w)),
    'left_voicing_max_voice_travel': max(abs(a-z) for v, w in zip(left_voicings[4:], left_voicings[5:]) for a, z in zip(v, w)),
    'right_anchor_max_travel': max(abs(a-z) for a, z in zip(right_anchor[4:], right_anchor[5:])),
    'source_spec_sha256': hashlib.sha256((BASE/'_internal/composition.json').read_bytes()).hexdigest(),
    'audio_render': False, 'actual_listening': False, 'live_import_tested': False})
print(json.dumps({'ok': True, 'piano_stats': stats, 'preserved_non_piano_specs': unchanged}, indent=2))
