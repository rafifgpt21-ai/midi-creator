"""Reference-preserving performance arrangement; no synthesis or sound selection."""
import collections
import itertools
import json
import math
import random
from pathlib import Path

from analyze_reference import NAMES, PROJECT, REF, name

HERE = Path(__file__).resolve().parent
PPQ = 480
BAR = 1920
END = 76 * BAR
SEED = 20261012
RNG = random.Random(SEED)
ANALYSIS = json.loads((HERE / 'reference-analysis.json').read_text(encoding='utf-8'))
SOURCE_PIANO = ANALYSIS['tracks'][2]['notes']
SOURCE_MELODY = ANALYSIS['tracks'][3]['notes']

# Harmony comes from the original piano. Labels are explanatory, never reharmonization.
CHORDS = {
    'F#m': {'pcs': {6, 9, 1}, 'bass': 42},
    'B/D#': {'pcs': {11, 3, 6}, 'bass': 39},
    'D6': {'pcs': {2, 6, 9, 11}, 'bass': 38},
    'E': {'pcs': {4, 8, 11}, 'bass': 40},
    'E/G#': {'pcs': {4, 8, 11}, 'bass': 44},
    'A': {'pcs': {9, 1, 4}, 'bass': 33},
    'E-low': {'pcs': {4, 8, 11}, 'bass': 28},
    'B': {'pcs': {11, 3, 6}, 'bass': 35},
    'F#m-low': {'pcs': {6, 9, 1}, 'bass': 30},
}
HARMONY = [None] * 4
HARMONY += ['F#m', 'B/D#'] * 8
HARMONY += ['D6', 'E', 'F#m', 'E/G#']
HARMONY += ['A', 'E-low', 'B', 'F#m-low'] * 2
HARMONY += ['F#m', 'B/D#'] * 8
HARMONY += ['D6', 'E', 'F#m', 'E/G#']
HARMONY += ['A', 'E-low', 'B', 'F#m-low'] * 2
HARMONY += ['F#m', 'B/D#'] * 8
assert len(HARMONY) == 76

SECTIONS = [
    ('Keheningan sumber', 1, 4),
    ('Tema piano A1', 5, 12),
    ('Tema piano ditahan', 13, 16),
    ('Tema piano A2', 17, 20),
    ('Transisi sumber 1', 21, 24),
    ('Tema B1', 25, 32),
    ('Tema A dengan melodi sumber', 33, 48),
    ('Transisi sumber 2', 49, 52),
    ('Tema B2', 53, 60),
    ('Tema A akhir', 61, 76),
]

def intensity(bar):
    if bar < 12:
        return 0.25 + (bar - 4) * 0.028
    if bar < 16:
        return 0.20
    if bar < 20:
        return 0.42 + (bar - 16) * 0.04
    if bar < 24:
        return 0.58
    if bar < 32:
        return 0.68 + 0.06 * math.sin((bar - 24) * math.pi / 7)
    if bar < 48:
        return 0.48 + 0.12 * math.sin((bar - 32) * math.pi / 15)
    if bar < 52:
        return 0.80
    if bar < 60:
        return 0.78
    return 0.65 + 0.13 * math.sin((bar - 60) * math.pi / 15) - max(0, bar - 72) * 0.07

def note(pitch, start, end, velocity, **extra):
    assert 0 <= start < end <= END, (pitch, start, end)
    return dict(pitch=pitch, s=int(start), e=int(end), velocity=max(1, min(127, round(velocity))), **extra)

def clean(notes):
    notes.sort(key=lambda n: (n['s'], n['pitch']))
    by_pitch = collections.defaultdict(list)
    for n in notes:
        by_pitch[n['pitch']].append(n)
    for ns in by_pitch.values():
        for a, b in zip(ns, ns[1:]):
            assert a['s'] < b['s'], ('duplicate onset', a, b)
            a['e'] = min(a['e'], b['s'])
    assert all(n['e'] > n['s'] for n in notes)
    return notes

def piano():
    output = []
    for source in SOURCE_PIANO:
        s, e, p = source['start_tick'], source['end_tick'], source['pitch']
        # Preserve original onsets exactly, including its rolled chords and one pickup.
        bar = s // BAR
        beat = (s % BAR) / PPQ
        cell = min(75, (s + 24) // BAR)  # pre-existing 11-tick anticipation belongs to next chord
        boundary = (cell + 1) * BAR
        top = max(n['pitch'] for n in SOURCE_PIANO if n['start_tick'] // BAR == bar)
        melody_voice = p >= 64 and p >= top - 2
        bass_voice = p == min(n['pitch'] for n in SOURCE_PIANO if n['start_tick'] // BAR == bar)
        base = 62 + 15 * intensity(bar)
        base += 13 if melody_voice else (-6 if bass_voice else 0)
        base += 2 if beat < 0.25 else (-3 if beat >= 3 else 0)
        # Source velocities contribute modestly; avoid the source's arbitrary 46..122 jumps.
        velocity = base + 0.13 * (source['velocity'] - 85) + RNG.uniform(-2.5, 2.5)
        gate = (e - s) - (RNG.randint(7, 17) if melody_voice else RNG.randint(13, 29))
        end = s + max(36, gate)
        if cell < 75 and p % 12 not in CHORDS[HARMONY[cell + 1]]['pcs']:
            end = min(end, boundary - 9)
        output.append(note(p, s, max(s + 6, min(end, END)), velocity, origin='original'))

    # Short chord-tone connections, only at selected existing phrase ends.
    additions = []
    phrase_end_bars = [8, 12, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72]
    for human_bar in phrase_end_bars:
        bar = human_bar - 1
        start, boundary = bar * BAR + 1680, (bar + 1) * BAR
        occupied = {n['pitch'] for n in output if n['s'] < boundary and n['e'] > start}
        pcs = CHORDS[HARMONY[bar]]['pcs']
        choices = [p for p in range(61, 80) if p % 12 in pcs and p not in occupied]
        next_sources = [n for n in SOURCE_PIANO if boundary - 24 <= n['start_tick'] < boundary + 120 and n['pitch'] >= 60]
        target = min((n['pitch'] for n in next_sources), default=66)
        pairs = [(a, b) for a in choices for b in choices if 0 < abs(a-b) <= 5]
        if not pairs:
            continue
        a, b = min(pairs, key=lambda ab: (abs(ab[1]-target) + 0.25*abs(ab[0]-ab[1]) + 0.2*abs(ab[0]-69), ab))
        vel = 55 + 12 * intensity(bar)
        output.extend([note(a, start, start + 105, vel - 3, origin='ornament'),
                       note(b, start + 120, boundary - 14, vel, origin='ornament')])
        additions.append(dict(bar=human_bar, notes=[name(a), name(b)], beats=[3.5, 3.75]))
    return clean(output), additions

def voicing_candidates(pcs):
    pitches = [p for p in range(50, 72) if p % 12 in pcs]
    return [v for v in itertools.combinations(pitches, 4)
            if {p % 12 for p in v} == pcs and 12 <= v[-1] - v[0] <= 21
            and all(2 <= b-a <= 9 for a, b in zip(v, v[1:]))]

def strings_chord():
    # Dynamic programming minimizes voice travel through the unchanged chord sequence.
    candidates = [voicing_candidates(CHORDS[h]['pcs']) for h in HARMONY[12:]]
    states = {v: (sum(abs(p-t) for p, t in zip(v, (54, 57, 61, 66))), [v]) for v in candidates[0]}
    for options in candidates[1:]:
        next_states = {}
        for v in options:
            choices = []
            for old, (cost, path) in states.items():
                movement = sum(abs(a-b) for a, b in zip(old, v))
                large_leaps = sum(max(0, abs(a-b)-5)**2 for a, b in zip(old, v))
                retain = len(set(old) & set(v))
                choices.append((cost + movement + 2*large_leaps - retain*0.8 + abs(v[-1]-66)*0.06, path + [v]))
            next_states[v] = min(choices, key=lambda entry: entry[0])
        states = next_states
    _, path = min(states.values(), key=lambda entry: entry[0])
    output, active = [], {}
    for offset, voicing in enumerate(path):
        bar = offset + 12
        s, e = bar * BAR, (bar + 1) * BAR
        # Common tones continue without re-attacks; changed voices release just before boundary.
        for p in set(active) - set(voicing):
            active.pop(p)['e'] = s - 8
        for p in voicing:
            if p in active:
                active[p]['e'] = e
            else:
                n = note(p, s, e, 44 + 17*intensity(bar) + (3 if p == max(voicing) else 0) + RNG.uniform(-2, 2))
                output.append(n)
                active[p] = n
        # Re-bow common tones at source section boundaries only, with continuous timing.
        if bar + 1 in (16, 20, 24, 32, 48, 52, 60, 68, 72):
            active = {}
    return clean(output), [dict(bar=i + 13, pitches=list(v), names=[name(p) for p in v]) for i, v in enumerate(path)]

def strings_solo():
    output = []
    melody_log = []
    # The source already has a composed flute line. Re-orchestrate that exact pitch contour,
    # one octave lower, as the solo rather than inventing an unrelated lead.
    for source in SOURCE_MELODY:
        s = round(source['start_tick'] / 60) * 60
        p = source['pitch'] - 12
        bar, beat = divmod(s, BAR)
        # Two consecutive B5s in the source remain two articulated B4s.
        duration = source['end_tick'] - source['start_tick']
        e = min(END - 7, s + duration - 10)
        breath = bar + 1 in (36, 40, 44, 48, 52, 64, 68, 72, 76) and beat == 960
        if breath:
            e = min(e, s + 420)  # quarter-note phrase ending leaves room for flute answer
        velocity = 71 + 14*intensity(bar) + (2 if beat == 0 else 0) + RNG.uniform(-3, 3)
        output.append(note(p, s, e, velocity, origin='source-melody', breath=breath))
        melody_log.append(dict(source_start=source['start_tick'], start=s, original_pitch=source['pitch'], pitch=p, breath=breath))
    return clean(output), melody_log

def bass():
    output = []
    for bar in range(4, 76):
        h = HARMONY[bar]
        root = CHORDS[h]['bass']
        # Source lowest piano pitch fixes root/slash bass; no new inversions.
        original_lowest = min(n['pitch'] for n in SOURCE_PIANO if n['start_tick'] // BAR == bar)
        assert root % 12 == original_lowest % 12
        s = bar * BAR
        vel = 59 + 15*intensity(bar)
        if 12 <= bar < 16 or bar == 75:
            output.append(note(root, s, s + BAR - 12, vel))
            continue
        second_beat = 2.5 if bar % 2 else 2
        first_end = s + round(second_beat * PPQ) - 30
        output.append(note(root, s, first_end, vel + RNG.uniform(-2, 2)))
        final_phrase = bar + 1 in (12, 20, 24, 32, 48, 52, 60, 68, 72)
        last_start = s + 1680 if final_phrase else s + BAR
        second = root
        if 24 <= bar < 32 or 52 <= bar < 60:
            second = root + 12 if bar % 4 in (0, 2) else root
        output.append(note(second, s + round(second_beat*PPQ), last_start - 27, vel - 5 + RNG.uniform(-2, 2)))
        if final_phrase:
            target = CHORDS[HARMONY[bar + 1]]['bass']
            # A short existing-chord tone approaches the next exact source bass.
            candidates = [p for p in range(28, 49) if p % 12 in CHORDS[h]['pcs']]
            approach = min(candidates, key=lambda p: (abs(p-target) + 0.25*abs(p-root), p))
            output.append(note(approach, last_start, s + BAR - 16, vel - 10))
    return clean(output)

def flute_counter(solo):
    output, choices_log = [], []
    # New flute material, independently rearranged as requested in the follow-up.
    # Two light entrances occupy the source solo's natural initial two-beat rests.
    for human_bar in (33, 61):
        s = (human_bar - 1) * BAR
        entrance = [81, 78, 73] if human_bar == 33 else [73, 78, 81]
        for p, beat, duration, vel in zip(entrance, (0.5, 1, 1.5), (0.4, 0.4, 0.35), (55, 59, 56)):
            output.append(note(p, s + round(beat*PPQ), s + round((beat+duration)*PPQ), vel))
        choices_log.append(dict(bar=human_bar, pitches=entrance, function='new counter-motif entrance'))
    answer_bars = [36, 40, 44, 48, 52, 64, 68, 72, 76]
    for phrase_index, human_bar in enumerate(answer_bars):
        bar = human_bar - 1
        s, e = bar * BAR, (bar + 1) * BAR
        line = [n for n in solo if s <= n['s'] < e]
        last = max(line, key=lambda n: n['s'])
        pcs = CHORDS[HARMONY[bar]]['pcs']
        # Answer the contour above the strings, entirely within the current source harmony.
        candidates = [p for p in range(73, 87) if p % 12 in pcs]
        melodic_direction = last['pitch'] - line[0]['pitch']
        descending = melodic_direction > 0 if melodic_direction else phrase_index % 2 == 0
        ordered = sorted(candidates, reverse=descending)
        triples = [v for v in itertools.combinations(ordered, 3)
                   if all(0 < abs(b-a) <= 5 for a,b in zip(v,v[1:]))]
        phrase = min(triples, key=lambda v: (abs(v[0]-(last['pitch']+12))+0.3*abs(v[-1]-78), v))
        if human_bar < 76:
            upcoming = [n for n in solo if e <= n['s'] < e + BAR]
            target = upcoming[0]['pitch']+12 if upcoming else 78
            if phrase_index % 2:
                # Two-note answers balance the three-note turn figures.
                pairs = [(a,b) for a in candidates for b in candidates if 0 < abs(b-a) <= 5]
                phrase = min(pairs, key=lambda v: (abs(v[-1]-target)+0.5*abs(v[0]-phrase[0]), v))
        else:
            phrase = (78, 83)  # source final B/D#, not a newly added tonic cadence
        velocity = 54 + 11*intensity(bar)
        beats = (3, 3.5, 3.75) if len(phrase) == 3 else (3, 3.5)
        durations = (0.4, 0.18, 0.17) if len(phrase) == 3 else (0.4, 0.4)
        for index, (p, beat, duration) in enumerate(zip(phrase, beats, durations)):
            output.append(note(p, s + round(beat*PPQ), s + round((beat+duration)*PPQ),
                               velocity + (0 if index == 0 else -3)))
        choices_log.append(dict(bar=human_bar, pitches=list(phrase), after_solo_end=last['e'],
                                function='new contrary-motion phrase answer'))
    return clean(output), choices_log

def as_spec(notes):
    return [dict(pitch=n['pitch'], start=n['s']/PPQ, duration=(n['e']-n['s'])/PPQ, velocity=n['velocity']) for n in notes]

def main():
    piano_notes, ornaments = piano()
    chords, voicings = strings_chord()
    solo, melody_map = strings_solo()
    bass_notes = bass()
    flute, answers = flute_counter(solo)
    data = [('piano', 'Piano - Humanized', 'Harmoni dan motif piano asli', 0, piano_notes),
            ('strings-chord', 'Strings - Chord', 'Sustained harmony dengan common-tone voice leading', 48, chords),
            ('strings-solo', 'Strings - Solo', 'Melodi sumber dengan napas frasa', 40, solo),
            ('precision-bass', 'Precision Bass - Fender', 'Root dan slash bass sumber, fingerstyle', 33, bass_notes),
            ('flute-counter', 'Flute - Counter Melody Accents', 'Jawaban pendek terhadap strings solo', 73, flute)]
    spec = dict(version=1, title='Yey - Humanized Reference Arrangement', tempo_bpm=120,
                time_signature=[4, 4], bars=76, ticks_per_beat=480,
                timing=dict(mode='free', grid_division=32),
                description='Lima layer berdasarkan yey.mid; seluruh progression, posisi perubahan chord, struktur dan 4 bar kosong sumber dipertahankan.',
                assumptions=[
                    'MIDI saja; semua sound dipilih pengguna, termasuk VST Fender Precision Bass. Tidak membuat preset Serum.',
                    'Pusat tonal F# Dorian dengan D natural pada D6; label track sumber D Dorian tidak digunakan untuk transpose.',
                    'Timing free hanya untuk mempertahankan 46 onset piano off-grid yang sudah ada di sumber. Tidak menambah jitter atau swing.',
                    'Humanisasi baru melalui hierarchy velocity, gate dan phrasing; nada asli piano dan onsetnya dipertahankan.',
                    'Melodi flute asli menjadi strings solo satu oktaf lebih rendah. Sesuai follow-up, flute diaransemen ulang menjadi motif masuk dan jawaban akhir frasa yang baru.',
                    'Seluruh file 76 bar termasuk 4 bar kosong; tidak menambah intro, outro, drum atau cadence baru.',
                    'Tidak mengirim sustain pedal, expression CC, keyswitch atau program change; artikulasi plugin diatur pengguna.',
                ], sections=[dict(name=label, start=(start-1)*4) for label, start, end in SECTIONS],
                layers=[dict(id=id, name=label, role=role, kind='melodic', program=program,
                             channel=1, volume=100, pan=64, notes=as_spec(notes))
                        for id, label, role, program, notes in data])
    (HERE/'composition.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    # Direct source preservation checks, independent of musical chord labels.
    source_keys = collections.Counter((n['pitch'], n['start_tick']) for n in SOURCE_PIANO)
    preserved = collections.Counter((n['pitch'], n['s']) for n in piano_notes if n.get('origin') == 'original')
    assert source_keys == preserved
    chord_pcs_audit = []
    for bar in range(4, 76):
        # Include source onsets in the initial 0.21-beat chord-roll window.
        source_pcs = {n['pitch'] % 12 for n in SOURCE_PIANO if bar*BAR <= n['start_tick'] < bar*BAR+110}
        expected = CHORDS[HARMONY[bar]]['pcs']
        assert source_pcs == expected, (bar + 1, source_pcs, expected)
        chord_pcs_audit.append(dict(bar=bar+1, label=HARMONY[bar], source_pcs=sorted(source_pcs)))
    for id, _, _, _, ns in data:
        assert min(n['s'] for n in ns) >= 4*BAR
        for n in ns:
            if id in ('strings-chord', 'precision-bass', 'flute-counter'):
                assert n['pitch'] % 12 in CHORDS[HARMONY[n['s']//BAR]]['pcs'], (id,n)
    for f in flute:
        assert not any(n['s'] < f['e'] and n['e'] > f['s'] for n in solo), f
    voice_moves = [abs(b-a) for x,y in zip(voicings,voicings[1:]) for a,b in zip(x['pitches'], y['pitches'])]
    receipt = dict(seed=SEED, source_sha256=ANALYSIS['source_sha256'], tempo_bpm=120, bars=76,
                   original_piano_notes=len(SOURCE_PIANO), preserved_piano_pitch_onsets=sum(preserved.values()),
                   piano_added_notes=len(piano_notes)-len(SOURCE_PIANO), piano_original_offsets_unchanged=True,
                   original_melody_notes=len(SOURCE_MELODY), strings_solo_source_notes=len(solo),
                   source_melody_onset_max_adjustment_ticks=max(abs(x['start']-x['source_start']) for x in melody_map),
                   source_melody_octave_transposition=-12,
                   four_initial_silent_bars_preserved=True, chord_progression_audit=chord_pcs_audit,
                   ornaments=ornaments, strings_voicings=voicings, strings_max_voice_step=max(voice_moves),
                   strings_mean_voice_step=sum(voice_moves)/len(voice_moves),
                   melody_map=melody_map, flute_answers=answers, flute_answers_during_solo_rests=True,
                   layers={id:dict(notes=len(ns), pitch_min=min(n['pitch'] for n in ns),
                                   pitch_max=max(n['pitch'] for n in ns), velocity_min=min(n['velocity'] for n in ns),
                                   velocity_max=max(n['velocity'] for n in ns), first_tick=min(n['s'] for n in ns))
                           for id,_,_,_,ns in data},
                   listening_performed=False, plugin_loading_tested=False, live_cubase_import_tested=False)
    (HERE/'musical-audit.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:receipt[k] for k in ('original_piano_notes','preserved_piano_pitch_onsets','piano_added_notes','strings_max_voice_step','strings_mean_voice_step','layers')},indent=2))

if __name__ == '__main__':
    main()
