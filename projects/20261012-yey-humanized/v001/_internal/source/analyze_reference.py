import collections
import hashlib
import json
import shutil
from pathlib import Path

import mido

HERE = Path(__file__).resolve().parent
ATTACHMENT = Path(r'C:\Users\rafif\.t3\userdata\attachments\af7ac073-5999-4c56-93c1-9e008849f1c1-cd1b66fa-5db6-4a55-848d-00875d38d3c5-mid.mid')
PROJECT = next(p for p in HERE.parents if p.name == '20261012-yey-humanized')
REF = PROJECT / '_internal' / 'references' / 'yey.mid'
REF.parent.mkdir(parents=True, exist_ok=True)
if not REF.exists():
    shutil.copy2(ATTACHMENT, REF)
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def name(p):
    return NAMES[p % 12] + str(p // 12 - 1)

def read_notes(track):
    tick, active, notes = 0, {}, []
    for msg in track:
        tick += msg.time
        if msg.type == 'note_on' and msg.velocity:
            assert (msg.channel, msg.note) not in active, (msg, tick)
            active[msg.channel, msg.note] = (tick, msg.velocity)
        elif msg.type == 'note_off' or (msg.type == 'note_on' and not msg.velocity):
            start, velocity = active.pop((msg.channel, msg.note))
            notes.append(dict(pitch=msg.note, start_tick=start, end_tick=tick, velocity=velocity))
    assert not active
    return sorted(notes, key=lambda n: (n['start_tick'], n['pitch'])), tick

def main():
    m = mido.MidiFile(REF)
    tracks = []
    lines = []
    for i, track in enumerate(m.tracks):
        notes, end = read_notes(track)
        tracks.append(dict(index=i, name=track.name, notes=notes, end_tick=end))
        lines.append(f'Track {i}: {track.name}, {len(notes)} notes, end {end}, onset residues /60: {dict(collections.Counter(n["start_tick"] % 60 for n in notes))}')
    piano, flute = tracks[2]['notes'], tracks[3]['notes']
    for bar in range(76):
        s, e = bar * 1920, (bar + 1) * 1920
        pn = [n for n in piano if s <= n['start_tick'] < e]
        fn = [n for n in flute if s <= n['start_tick'] < e]
        lines.append(f'\nBAR {bar+1:02d}: piano={len(pn)} flute={len(fn)}')
        groups = collections.defaultdict(list)
        for n in pn:
            groups[n['start_tick']].append(n)
        for tick, ns in groups.items():
            lines.append(f'  {(tick-s)/480:6.3f}: ' + ', '.join(f'{name(n["pitch"])}({(n["end_tick"]-tick)/480:.3f},v{n["velocity"]})' for n in ns))
        if fn:
            lines.append('  FLUTE: ' + ', '.join(f'{(n["start_tick"]-s)/480:.3f}:{name(n["pitch"])}({(n["end_tick"]-n["start_tick"])/480:.3f})' for n in fn))
    result = dict(source_sha256=hashlib.sha256(REF.read_bytes()).hexdigest(), ppqn=m.ticks_per_beat, tracks=tracks)
    (HERE / 'reference-analysis.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    (HERE / 'reference-notes.txt').write_text('\n'.join(lines), encoding='utf-8')
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
