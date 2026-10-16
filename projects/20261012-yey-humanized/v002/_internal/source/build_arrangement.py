"""Reproducible Yey v002 rewrite. Run with uv run python <this file>."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 20261014
RNG = random.Random(SEED)
PPQ = 480
END = 304.0
ANALYSIS = json.loads((HERE / 'reference-analysis.json').read_text(encoding='utf-8'))
SOURCE_PIANO = ANALYSIS['tracks'][2]['notes']
SOURCE_MELODY = ANALYSIS['tracks'][3]['notes']
CHORDS = {
    'F#m': ({6, 9, 1}, 6), 'B/D#': ({11, 3, 6}, 3),
    'D6': ({2, 6, 9, 11}, 2), 'E': ({4, 8, 11}, 4),
    'E/G#': ({4, 8, 11}, 8), 'A': ({9, 1, 4}, 9),
    'B': ({11, 3, 6}, 11),
}
HARMONY = [None] * 4 + ['F#m', 'B/D#'] * 8
HARMONY += ['D6', 'E', 'F#m', 'E/G#'] + ['A', 'E', 'B', 'F#m'] * 2
HARMONY += ['F#m', 'B/D#'] * 8
HARMONY += ['D6', 'E', 'F#m', 'E/G#'] + ['A', 'E', 'B', 'F#m'] * 2
HARMONY += ['F#m', 'B/D#'] * 8
assert len(HARMONY) == 76
SECTIONS = [
    ('silence', 'Intro', 1, 4, 'repeat', 0.0),
    ('a1', 'Verse', 5, 8, 'repeat', 3.0),
    ('held', 'Breakdown', 13, 4, 'vary', 2.2),
    ('a2', 'Verse', 17, 4, 'vary', 3.7),
    ('t1', 'Pre-Chorus', 21, 4, 'fragment', 4.6),
    ('b1', 'Chorus', 25, 8, 'vary', 5.2),
    ('lead', 'Instrumental', 33, 16, 'vary', 4.8),
    ('t2', 'Pre-Chorus', 49, 4, 'recap', 6.0),
    ('b2', 'Chorus', 53, 8, 'recap', 5.5),
    ('final', 'Outro', 61, 16, 'recap', 4.0),
]


def write_json(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def section(bar):
    return next(s for s in SECTIONS if s[2] - 1 <= bar < s[2] - 1 + s[3])


def energy(bar):
    s = section(bar)
    phase = (bar - s[2] + 1) / max(1, s[3] - 1)
    value = s[5] + 0.45 * math.sin(phase * math.pi)
    if bar >= 70:
        value -= (bar - 69) * 0.40
    return max(1.0, value)


def pcs(bar):
    return CHORDS[HARMONY[bar]][0]


def optimize(candidate_rows, targets, weights=None, max_move=7):
    """Whole-phrase DP: stable voice indices, no voice crossing, low travel cost."""
    weights = weights or [1.0] * len(candidate_rows[0][0])
    costs = {v: sum(0.10 * abs(p - t) for p, t in zip(v, targets[0])) for v in candidate_rows[0]}
    parents = []
    for rows, target in zip(candidate_rows[1:], targets[1:]):
        new, parent = {}, {}
        for v in rows:
            options = []
            for old, old_cost in costs.items():
                movements = [abs(a - b) for a, b in zip(v, old)]
                if max(movements) > max_move:
                    continue
                cost = old_cost + sum(w * (m + 1.8 * max(0, m - 2) ** 2) for w, m in zip(weights, movements))
                cost += sum(0.08 * abs(p - t) for p, t in zip(v, target))
                options.append((cost, old))
            if options:
                new[v], parent[v] = min(options)
        assert new, ('No playable path', rows, target)
        parents.append(parent)
        costs = new
    last = min(costs, key=lambda v: (costs[v], v))
    result = [last]
    for parent in reversed(parents):
        last = parent[last]
        result.append(last)
    return list(reversed(result))


def add(notes, pitch, start, duration, velocity):
    start = round(start * PPQ) / PPQ
    duration = min(duration, END - start)
    assert duration > 0 and start >= 16, (pitch, start, duration)
    notes.append({'pitch': int(pitch), 'start': start, 'duration': round(duration * PPQ) / PPQ,
                  'velocity': int(max(1, min(127, round(velocity))))})


def clean(notes):
    """Release a key before its own next attack; never delete or displace onsets."""
    notes.sort(key=lambda n: (n['start'], n['pitch']))
    groups = {}
    for n in notes:
        groups.setdefault(n['pitch'], []).append(n)
    for group in groups.values():
        for a, b in zip(group, group[1:]):
            assert b['start'] > a['start'], (a, b)
            a['duration'] = min(a['duration'], round((b['start'] - a['start']) * PPQ) / PPQ)
    return notes


def long_line(pitch_by_bar, first, last, velocity, breaks=()):
    notes = []
    for b in range(first, last):
        pitch = pitch_by_bar[b]
        if pitch is None:
            continue
        start = b * 4
        # Tie only exact common pitches through uninterrupted, supported harmonies.
        if notes and b not in breaks and notes[-1]['pitch'] == pitch and abs(notes[-1]['start'] + notes[-1]['duration'] - start) < 0.02:
            notes[-1]['duration'] += 4
        else:
            if notes and notes[-1]['start'] + notes[-1]['duration'] >= start:
                notes[-1]['duration'] = start - notes[-1]['start'] - 0.025
            add(notes, pitch, start, 4, velocity + energy(b) * 2)
    if notes:
        notes[-1]['duration'] = min(notes[-1]['duration'], last * 4 - notes[-1]['start'] - 0.28)
    return notes


TARGETS = [
    ('piano', 'Piano', 0, 'harmony', 'User-selected acoustic piano', 'Velocity-sensitive piano', 100, 64),
    ('bbc-basses', 'BBC Basses', 43, 'bass', 'BBCSO Discover / Strings / Basses', 'Long (vib)', 88, 68),
    ('bbc-celli', 'BBC Celli theme', 42, 'melody', 'BBCSO Discover / Strings / Celli', 'Long (vib)', 94, 66),
    ('bbc-violas', 'BBC Violas inner voice', 41, 'harmony', 'BBCSO Discover / Strings / Violas', 'Long (vib)', 78, 64),
    ('bbc-violins-1', 'BBC 1st Violins upper voice', 40, 'harmony', 'BBCSO Discover / Strings / 1st Violins', 'Long (vib)', 76, 60),
    ('bbc-flutes', 'BBC Flutes answers', 73, 'countermelody', 'BBCSO Discover / Woodwinds / Flutes a3', 'Long', 80, 61),
    ('bbc-clarinets', 'BBC Clarinets warm responses', 71, 'countermelody', 'BBCSO Discover / Woodwinds / Clarinets a3', 'Long', 80, 67),
]

# Intent and thematic material are committed before note emission.
romans = {'F#m': 'i', 'B/D#': 'IV/6', 'D6': 'bVI6', 'E': 'bVII', 'E/G#': 'bVII/3', 'A': 'bIII', 'B': 'IV'}
arr = {
    'spec_version': '1.0',
    'meta': {'title': 'Yey — Piano and BBC Discover', 'style_layer': 'none', 'style_layers': [],
             'key': 'F# minor', 'mode': 'dorian', 'meter': '4/4', 'tempo': 120,
             'target_duration': '2:32', 'deliverable': ['midi'],
             'upstream': {'brief': 'request.md; v001 and original yey.mid', 'lyrics': {}, 'picture': {}}},
    'intent': {'one_thing': 'Let the original Yey progression unfold like a pianist telling a quiet story.',
               'reference_pair': [
                   {'track': 'Original yey.mid / piano', 'borrow': 'All chord pitch classes, slash basses, harmonic change bars and four-bar opening silence.'},
                   {'track': 'Original yey.mid / flute theme', 'borrow': 'Recognizable pitch-class contour, recast in cello register with phrase breathing.'}],
               'listener_situation': 'Close listening at home, piano foreground and orchestra behind it.',
               'emotional_arc': [{'section': s[0], 'mood': ('recede' if s[0] in ('held', 'final') else 'unfold'), 'value': s[5]} for s in SECTIONS]},
    'material': {'motif': 'Two-bar minor-to-major-IV response, held upper note over gently alternating eighth-note inner voices; the cello recalls the source long-note theme.',
                 'character': 'Reflective and unhurried', 'stated_in': ['a1', 'lead'], 'development_mode': '加工处理'},
    'form': [{'id': sid, 'name': name, 'start_bar': start, 'bars': length,
              'harmony': ' | '.join(romans[HARMONY[b]] if HARMONY[b] else '-' for b in range(start - 1, start - 1 + length)),
              'harmony_letters': ' | '.join(HARMONY[b] or '-' for b in range(start - 1, start - 1 + length)),
              'melody_register': 'mid-high' if sid in ('a1', 'b1', 'b2') else 'mid',
              'development': development, 'energy': level, 'events': [],
              'note': 'Original harmonic timeline locked; recap varies touch, density and phrasing without new chords.'}
             for sid, name, start, length, development, level in SECTIONS],
    'arrangement': {
        'roster': [{'id': t[0], 'instrument': t[4] + ' / ' + t[5], 'midi': {'program': t[2], 'bank': 0, 'channel': 1},
                    'role': t[3], 'band': 'low' if t[0] == 'bbc-basses' else 'mid-high',
                    'entry': {'piano': 'a1', 'bbc-basses': 'a1', 'bbc-celli': 'lead', 'bbc-violas': 'held',
                              'bbc-violins-1': 'a2', 'bbc-flutes': 'lead', 'bbc-clarinets': 'b1'}[t[0]],
                    'exit': {'bbc-flutes': 'final bar 72', 'bbc-clarinets': 'b2 bar 60'}.get(t[0], 'end'),
                    'note': 'Concert pitch, one independent section line; BBC uses CC1=100 and shaped CC11.'}
                   for t in TARGETS],
        'depth_map': {'piano': 'foreground', 'bbc-celli': 'midground', 'bbc-basses': 'background',
                      'bbc-violas': 'background', 'bbc-violins-1': 'background', 'bbc-flutes': 'midground', 'bbc-clarinets': 'midground'},
        'bass_kick_relation': {},
        'spectrum_budget': [
            {'band': 'low', 'owner': 'bbc-basses', 'competitors': ['piano'], 'resolution': 'Piano left hand moves up an octave when bowed bass enters.'},
            {'band': 'mid', 'owner': 'bbc-celli', 'competitors': ['piano', 'bbc-violas'], 'resolution': 'Piano density drops under theme; viola sits above the cello line.'},
            {'band': 'high', 'owner': 'piano', 'competitors': ['bbc-flutes'], 'resolution': 'Flute answers only in cello gaps and is restrained behind piano.'}],
        'energy_curve': {s[0]: s[5] for s in SECTIONS},
        'subtraction_events': [
            {'at': {'section': 'held', 'bar_offset': 0}, 'what': 'Remove moving piano inner pattern', 'why': 'Four-bar breath before rebuilding.'},
            {'at': {'section': 'lead', 'bar_offset': 0}, 'what': 'Reduce piano rhythm density', 'why': 'Let cello theme emerge.'},
            {'at': {'section': 'final', 'bar_offset': 12}, 'what': 'Woodwinds have already exited; thin piano and strings', 'why': 'Soft open-ended final B/D#.'}],
        'hooks': {'vocal_hook': {}, 'arrangement_hook': {'what': 'Connected piano inversions answered later by the original theme in cellos.', 'first_at': 'a1', 'recurs_at': ['a2', 'lead', 'final']}},
        'groove': {'feel': 'straight', 'push_pull': [{'part': 'all', 'offset_ms': 0, 'note': 'Workspace strict onset policy; touch/gate/CC provide phrase variation.'}],
                   'fill_policy': {'bars': [20, 24, 52, 60, 71], 'rationale': 'Short chord-tone links at structural seams, with one late-theme variation.'}}},
    'vocal': {},
    'mix_intent': {'mood': 'Close piano with a warm, lightly voiced orchestra behind it.',
                   'sound_stage': [{'id': t[0], 'pan': round((t[7] - 64) / 63 * 100), 'depth': 'foreground' if t[0] == 'piano' else 'background'} for t in TARGETS],
                   'ducking_map': [], 'dynamics': {'target_DR_dB': 0, 'notes': ['No mastering target: MIDI delivery. Preserve quieter held section and final retreat.']},
                   'width_map': {'a1': 'mostly piano', 'b1': 'strings and clarinet spread', 'final': 'gradually narrows as winds exit'}, 'loudness_target': ''},
    'render': {'midi': {'instrument_map': {t[0]: {'name': t[4], 'program': t[2], 'bank': 0, 'channel': 1} for t in TARGETS}}},
    'checks': {'self_audit': ['1: Intent complete, two separate source-track references.', '2: Sections contiguous 1–76.', '3: Four-bar sections preserve source.',
                             '4: Energy map matches all section ids.', '5: Drops at held, lead, b2 and final.', '6: Three subtraction events.',
                             '7: Winds exit early.', '8: Piano/cello hook specified.', '9: D6 retains borrowed natural D.',
                             '10: Five non-periodic fill bars.', '11: Exempt strict timing.', '12: Instrumental width changes.',
                             '13: Exempt non-Suno delivery.', '14: 76*4/120*60=152 seconds.', '15-16: Instrumental, no vocals.',
                             '17: No style fusion.', '18: Recognizable repeat/vary/recap; no new sections.', '19: ASCII chord names.',
                             '20: Dorian meta, closed section names, structured subtraction positions.'],
               'exemptions': ['Strict grid takes precedence over skill push/pull preference; no timing offset requested.',
                              'One chord per bar and last B/D# locked by source; no added tonic cadence.',
                              'No Suno/YuE prompt, vocal design, extra score or audio requested.',
                              'Piano is user-selected from v001; BBC orchestral instruments explicitly requested, so Serum default does not apply.']},
    'messages': [],
}
write_json('ARR-SPEC.json', arr)

# Three stable RH voices, narrow enough for one hand. D6 root is supplied by LH.
rows, targets = [], []
for b in range(4, 76):
    upper_pcs = {6, 9, 11} if HARMONY[b] == 'D6' else pcs(b)
    rows.append([v for v in itertools.combinations(range(60, 80), 3)
                 if v[-1] - v[0] <= 12 and {p % 12 for p in v} == upper_pcs])
    source_top = max(n['pitch'] for n in SOURCE_PIANO if b * 1920 <= n['start_tick'] < (b + 1) * 1920)
    while source_top > 78:
        source_top -= 12
    while source_top < 69:
        source_top += 12
    target_top = max(69, min(78, source_top))
    targets.append((target_top - 9, target_top - 4, target_top))
voicings = [None] * 4 + optimize(rows, targets, [1, 1, 1.25], max_move=5)

piano, role_events = [], []
for b in range(4, 76):
    start, e = b * 4, energy(b)
    sid = section(b)[0]
    v = voicings[b]
    next_v = voicings[b + 1] if b < 75 else None
    bass_pc = CHORDS[HARMONY[b]][1]
    low_choices = [p for p in range(40, 56) if p % 12 == bass_pc]
    low = min(low_choices, key=lambda p: abs(p - 48))
    # LH is an open line, not a dense low triad. Basses enter bar 9.
    if b < 8:
        low -= 12
    add(piano, low, start, 3.95, 46 + e * 2.8 + RNG.randint(-2, 2))
    role_events.append({'role': 'left-root', 'bar': b + 1, 'pitch': low, 'start': start})
    slow = sid in ('held', 'lead', 'final')
    quiet_end = b >= 72
    pulse = [] if sid == 'held' or quiet_end else ([1.5, 3.0] if slow else [1.0, 1.5, 2.5, 3.0])
    for i, pitch in enumerate(v):
        is_top = i == 2
        if is_top:
            # Held melody has priority over inner figures; tied common-tone at boundary.
            if piano and b > 4 and pitch == voicings[b - 1][2]:
                previous = next((n for n in reversed(piano) if n['pitch'] == pitch and n['start'] < start), None)
                if previous and abs(previous['start'] + previous['duration'] - start) < 0.02:
                    previous['duration'] += 4
                    role_events.append({'role': 'top-tie', 'bar': b + 1, 'pitch': pitch, 'start': start})
                    continue
            duration = 4 if next_v and next_v[2] == pitch else 3.95
            if quiet_end:
                duration = 3.72 if b == 75 else duration
            velocity = 66 + e * 3.3
        else:
            future = [x for j, x in enumerate(pulse) if j % 2 == i]
            duration = (future[0] + 0.03) if future else 3.95
            velocity = 42 + e * 2.3
        add(piano, pitch, start, duration, velocity + RNG.randint(-2, 2))
        role_events.append({'role': 'top' if is_top else 'inner', 'bar': b + 1, 'pitch': pitch, 'start': start})
    for j, offset in enumerate(pulse):
        pitch = v[j % 2]
        future = [x for k, x in enumerate(pulse) if k > j and k % 2 == j % 2]
        duration = ((future[0] - offset + 0.025) if future else (4 - offset - 0.025))
        add(piano, pitch, start + offset, duration, 39 + e * 2.0 + (2 if offset == 1.5 else 0) + RNG.randint(-2, 2))
        role_events.append({'role': 'inner', 'bar': b + 1, 'pitch': pitch, 'start': start + offset})
    if not slow and b % 2 == 0:
        choices = [p for p in range(low + 5, min(low + 13, 60)) if p % 12 in pcs(b)]
        lh = min(choices, key=lambda p: abs(p - 55))
        add(piano, lh, start + 2, 1.94, 42 + e * 2 + RNG.randint(-1, 1))
        role_events.append({'role': 'left-upper', 'bar': b + 1, 'pitch': lh, 'start': start + 2})
    # Short melodic links stay inside outgoing harmony, and stop before next bar.
    if b + 1 in (20, 24, 52, 60, 71) and next_v:
        top = v[2]
        target = next_v[2]
        choices = [p for p in range(max(v[0], top - 5), min(v[0] + 13, top + 6)) if p % 12 in pcs(b) and p != top and p not in v[:2]]
        if choices:
            bridge = min(choices, key=lambda p: (abs(p - target), abs(p - top), p))
            held = next(n for n in reversed(piano) if n['pitch'] == top and n['start'] <= start)
            held['duration'] = start + 3.5 - held['start'] - 0.015
            add(piano, bridge, start + 3.5, 0.46, 62 + e * 2.5)
            role_events.append({'role': 'connector', 'bar': b + 1, 'pitch': bridge, 'start': start + 3.5})
clean(piano)

bass_rows = [[(p,) for p in range(28, 48) if p % 12 == CHORDS[HARMONY[b]][1]] for b in range(4, 76)]
bass_pitch = [None] * 4 + [v[0] for v in optimize(bass_rows, [(35,)] * 72, max_move=9)]
# First four musical bars remain piano-only; orchestral bass then establishes weight.
basses = long_line(bass_pitch, 8, 76, 60, breaks=(12, 24, 32, 48, 60, 72))

# Sustained strings: one sounding voice per section, never a chord in one patch.
string_rows = [[(a, z) for a in range(57, 68) for z in range(69, 79)
                if a % 12 in pcs(b) and z % 12 in pcs(b) and a % 12 != z % 12 and z - a <= 19]
               for b in range(4, 76)]
strings = [None] * 4 + optimize(string_rows, [(62, 73)] * 72, max_move=5)
viola_pitch = [v[0] if v else None for v in strings]
violin_pitch = [v[1] if v else None for v in strings]
violas = long_line(viola_pitch, 12, 76, 54, breaks=tuple(range(16, 76, 4)))
violins = long_line(violin_pitch, 16, 76, 51, breaks=tuple(range(20, 76, 4)))
# Let the B2 piano/clarinet breathe: violin drops for its first two bars.
violins = [n for n in violins if not (208 <= n['start'] < 216)]
for n in violins:
    if n['start'] < 208 < n['start'] + n['duration']:
        n['duration'] = 208 - n['start'] - 0.10

# Revoice the original theme as a cello line; nearest octave decisions reduce jumps.
melody_rows = [[(p,) for p in range(49, 71) if p % 12 == n['pitch'] % 12] for n in SOURCE_MELODY]
melody_voiced = optimize(melody_rows, [(60,)] * len(melody_rows), max_move=9)
celli = []
phrase_ends = []
for i, (source, voiced) in enumerate(zip(SOURCE_MELODY, melody_voiced)):
    start = round(source['start_tick'] / 60) / 8
    bar = int(start // 4)
    next_start = round(SOURCE_MELODY[i + 1]['start_tick'] / 60) / 8 if i + 1 < len(SOURCE_MELODY) else END
    nominal_end = source['end_tick'] / PPQ
    phrase_end = i == len(SOURCE_MELODY) - 1 or next_start - start > 3.0 or int(next_start // 16) != int(start // 16)
    duration = min(nominal_end - start, next_start - start - 0.04)
    if phrase_end:
        duration = max(0.7, duration - 0.55)
        phrase_ends.append(round(start + duration, 4))
    # Source theme may include a passing pitch: never hang it into a new harmony.
    boundary = (bar + 1) * 4
    if bar < 75 and voiced[0] % 12 not in pcs(bar + 1):
        duration = min(duration, boundary - start - 0.03)
    add(celli, voiced[0], start, duration, 63 + energy(bar) * 2.1 + (3 if i % 4 == 1 else 0))
clean(celli)


def overlaps(notes, start, end):
    return any(n['start'] < end and n['start'] + n['duration'] > start for n in notes)


flutes, clarinets = [], []
# Answers in available theme breaths, no mechanically periodic fill schedule.
for b in (35, 39, 46, 63, 67, 70):
    start = b * 4 + 2.75
    # Explicit call-and-response breath: release the preceding cello gesture,
    # then postpone the next cello attack by 0.75 beat, shortening its gate.
    for n in celli:
        old_end = n['start'] + n['duration']
        if n['start'] < start and old_end > start:
            n['duration'] = start - n['start'] - 0.05
        elif start <= n['start'] < start + 2.0:
            n['start'] = b * 4 + 4.75
            n['duration'] = max(0.5, old_end - n['start'])
    assert not overlaps(celli, start, start + 2.0)
    next_pc = pcs(b + 1)
    shared = pcs(b) & next_pc
    if not shared:
        continue
    p = min((p for p in range(73, 84) if p % 12 in shared), key=lambda p: abs(p - 78))
    add(flutes, p, start, 1.05, 58 + energy(b) * 1.4)
    end_pitch = min((q for q in range(p - 3, p + 4) if q % 12 in next_pc and q != p), key=lambda q: (abs(q - p), q))
    add(flutes, end_pitch, start + 1.25, 0.73, 55 + energy(b) * 1.2)

# Longer independent replies in B passages; derived from the piano's upper descent.
for b in (25, 28, 30, 53, 56, 58):
    first = min((p for p in range(62, 74) if p % 12 in pcs(b)), key=lambda p: abs(p - 68))
    second = min((p for p in range(first - 4, first + 5) if p % 12 in pcs(b) and p != first), key=lambda p: (abs(p - first), p))
    add(clarinets, first, b * 4 + 1, 1.4, 59 + energy(b) * 1.5)
    add(clarinets, second, b * 4 + 2.5, 1.25, 55 + energy(b) * 1.3)
clean(flutes)
clean(clarinets)
assert flutes and clarinets


def expression(notes, layer_id):
    """Half-beat CC11 curves; slow arcs for strings, per-phrase breathing for winds."""
    cc = [{'start': 0, 'control': 1, 'value': 100}, {'start': 0, 'control': 11, 'value': 80}]
    last = 80
    for tick in range(32, 609):
        beat = tick / 2
        b = min(75, int(beat // 4))
        e = energy(b)
        active = [n for n in notes if n['start'] <= beat < n['start'] + n['duration']]
        if layer_id in ('bbc-flutes', 'bbc-clarinets', 'bbc-celli') and active:
            n = active[0]
            phase = (beat - n['start']) / n['duration']
            # Cello/wind phrase reaches its dynamic point before the release.
            shaped = math.sin(math.pi * min(1.0, phase))
            value = round(59 + e * 3.2 + shaped * 15)
        else:
            phrase_phase = (beat % 16) / 16
            value = round(62 + e * 3.1 + 7 * math.sin(math.pi * phrase_phase))
        if beat > 288:
            value -= round((beat - 288) * 1.1)
        value = max(36, min(105, value))
        if value != last:
            cc.append({'start': beat, 'control': 11, 'value': value})
            last = value
    return cc


note_map = {'piano': piano, 'bbc-basses': basses, 'bbc-celli': celli, 'bbc-violas': violas,
            'bbc-violins-1': violins, 'bbc-flutes': flutes, 'bbc-clarinets': clarinets}
layers = []
for ident, name, program, role, plugin, articulation, volume, pan in TARGETS:
    layer = {'id': ident, 'name': name, 'kind': 'melodic', 'program': program, 'role': role,
             'channel': 1, 'volume': volume, 'pan': pan, 'notes': clean(note_map[ident])}
    if ident != 'piano':
        layer['control_changes'] = expression(layer['notes'], ident)
    layers.append(layer)
comp = {'version': 1, 'title': 'Yey — Piano and BBC Discover', 'tempo_bpm': 120, 'time_signature': [4, 4],
        'bars': 76, 'ticks_per_beat': PPQ, 'key_signature': 'F#m', 'timing': {'mode': 'strict', 'grid_division': 32},
        'description': 'v002: original progression/timeline, newly voiced piano and restrained BBC Discover orchestra.',
        'prompt': 'Same piano chord progression; smoother natural playing; rewrite arrangement, replace P-bass with BBC basses.',
        'assumptions': [
            'User-selected acoustic piano from v001 remains an external instrument; all orchestral layers explicitly use BBCSO Discover. No Serum layers.',
            'F# Dorian with borrowed D natural on D6; SMF key hint F#m does not change written pitches.',
            '120 BPM, 4/4, 76 bars and four silent opening bars preserved; final B/D# unchanged.',
            'Fresh strict 1/32 onset performance, straight without swing; dynamics and gate provide phrasing, no timing jitter.',
            'All BBC sections use Long; no true recorded legato or solo string articulation assumed.',
            'BBC Discover CC1=100, CC11 shaped; single dynamic layer, no timbral-crossfade claim.',
            'No MIDI pedal, keyswitches, Program Change, audio, combined file or Cubase project requested.',
            f'Deterministic seed {SEED} for small piano velocity differences only.'],
        'sections': [{'name': sid, 'start': (start - 1) * 4} for sid, _, start, _, _, _ in SECTIONS],
        'layers': layers}
write_json('composition.json', comp)
write_json('bindings.json', {'version': 1, 'mapping': [
    {'layer': t[0], 'plugin': t[4], 'articulation': t[5], 'channel': 1,
     'transpose_semitones': 0, 'midi_pitch_convention': 'C4=60, sounding/concert pitch',
     'cc1': 100 if t[0] != 'piano' else None, 'cc11': 'written in MIDI' if t[0] != 'piano' else None,
     'keyswitches': [], 'status': 'manual patch loading required'} for t in TARGETS]})
write_json('performance-design.json', {'seed': SEED, 'harmony': HARMONY, 'piano_rh_anchors': voicings,
                                     'piano_role_events': role_events, 'bass_pitch_by_bar': bass_pitch,
                                     'string_anchors': strings, 'cello_phrase_ends': phrase_ends,
                                     'original_midi_sha256': ANALYSIS['source_sha256']})
print(json.dumps({'seed': SEED, 'layers': {l['id']: len(l['notes']) for l in layers},
                  'rh_max_voice_movement': max(abs(a-b) for x,y in zip(voicings[4:],voicings[5:]) for a,b in zip(x,y))}))
