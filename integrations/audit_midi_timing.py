"""Independent timing repro against actual exported MIDI, without renderer code.

--strict exits 1 when note-ons are off a straight 1/32-note grid. That verdict
is a diagnostic expectation, not a claim that explicitly requested swing is bad.
Tempo/alignment failures always exit 1. MIDI tick positions, not playback seconds,
define the grid. Original files are read only.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import mido

def inspect_bundle(folder):
    manifest_path=folder/'_internal'/'manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    reports=[]
    errors=[]
    for layer in manifest['layers']:
        path=folder/layer['file']
        midi=mido.MidiFile(path)
        tempo=[]; meter=[]; ends=[]; starts=[]; off=[]
        for track in midi.tracks:
            tick=0
            for msg in track:
                tick+=msg.time
                if msg.type=='set_tempo': tempo.append([tick,msg.tempo])
                if msg.type=='time_signature': meter.append([tick,msg.numerator,msg.denominator])
                if msg.type=='note_on' and msg.velocity>0:
                    starts.append(tick)
                    # Nearest 1/32 note: 1/8 quarter beat; allow half-tick rounding.
                    nearest=round(tick*8/midi.ticks_per_beat)*midi.ticks_per_beat/8
                    error=tick-nearest
                    if abs(error)>.500001: off.append((tick,error,msg.note))
            ends.append(tick)
        expected_tempo=mido.bpm2tempo(manifest['tempo_bpm'])
        if tempo!=[[0,expected_tempo]]: errors.append(f'{path.name}: tempo {tempo}')
        if meter!=[[0,*manifest['time_signature']]]: errors.append(f'{path.name}: meter {meter}')
        if ends!=[manifest['end_tick']]: errors.append(f'{path.name}: track ends {ends}')
        if midi.ticks_per_beat!=manifest['ticks_per_beat']: errors.append(f'{path.name}: PPQN mismatch')
        reports.append(dict(layer=layer['id'],file=str(path),format=midi.type,ppqn=midi.ticks_per_beat,
            tempo=tempo,track_ends=ends,note_ons=len(starts),off_grid_note_ons=len(off),
            max_grid_error_beats=max([abs(e)/midi.ticks_per_beat for t,e,p in off] or [0]),
            frequent_error_ticks=Counter(round(e,3) for t,e,p in off).most_common(6),
            examples=[{'tick':t,'beat':t/midi.ticks_per_beat,'offset_ticks':e,'pitch':p} for t,e,p in off[:5]]))
    return dict(project=folder.parent.name,revision=folder.name,tempo_bpm=manifest['tempo_bpm'],
                bars=manifest['bars'],alignment_errors=errors,
                off_grid_note_ons=sum(r['off_grid_note_ons'] for r in reports),files=reports)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folders',nargs='*',type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--strict',action='store_true')
    args=parser.parse_args()
    folders=args.folders
    if not folders:
        for project in sorted(Path('projects').iterdir()):
            revisions=sorted(p for p in project.glob('v[0-9]*') if (p/'_internal'/'manifest.json').is_file())
            if revisions: folders.append(revisions[-1])
    results=[inspect_bundle(folder) for folder in folders]
    report=dict(grid='straight 1/32 note-on grid, half-tick rounding tolerance',projects=results)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for result in results:
        print(f"{result['project']}/{result['revision']}: tempo/alignment errors={len(result['alignment_errors'])}; off-grid note-ons={result['off_grid_note_ons']}")
        for file in result['files']:
            if file['off_grid_note_ons']:
                print(f"  {file['layer']}: {file['off_grid_note_ons']}/{file['note_ons']}, max offset {file['max_grid_error_beats']:.6f} beats, tick offsets {file['frequent_error_ticks']}")
    failed=any(r['alignment_errors'] or (args.strict and r['off_grid_note_ons']) for r in results)
    print('FAIL' if failed else 'PASS')
    raise SystemExit(int(failed))

if __name__=='__main__': main()
