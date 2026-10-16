# Black Glass — piano revision v003

- Origin: v002. Date: 2026-10-12.
- User request: “make e new version of piano that played more chord focus and not arpegio, and make it natural (and some tastefull improvisation)”.

## Decisions

- Replace only the piano performance with simultaneous, chord-led playing, connected extended voicings, longer holds and occasional rhythmic chord repeats.
- Preserve the existing Fm9/Fm7 → Dbmaj9 → Bbm9 → Csus4(b9)/C7(b9) harmony, song structure, 136 BPM, F minor, 4/4, 112 bars / 3:17.65 and chorus entries at bars 33/77/101.
- Natural expression comes from soft inner voices, restrained bass-hand weight, stronger top notes, section/phrase dynamics, unequal release lengths and rests. Strict straight onset grid; no swing, rolled chord attacks or timing jitter requested.
- Sparse authored two/three-note melodic answers at selected phrase endings. Most attacks are full chords; no continuous arpeggio accompaniment or continuous lead line.
- All twelve non-piano layers are preserved exactly, including notes, program hints, channel and mixer settings. All five native Serum presets are copied unchanged from v002. Piano has no preset; user still chooses a velocity-sensitive acoustic piano.
- New piano seed: 2026101203. Reproduce using `revise_piano.py`; original non-piano seed remains 20261012. No samples, combined file or audio requested.

## Acceptance

- Composition validate/generate/verify pass; 13 individual format-1 single-track MIDI files retain equal global duration.
- Piano full-chord attacks account for at least 90% of note-ons; planned improvisations remain confined to selected phrase ends. Dynamic velocity range and varied gates preserved.
- No same-pitch overlaps; suspended F releases before C7 E enters; complete one-beat MIDI silence remains before all three big drops.
- Non-piano layer specifications and exported bytes match v002. All five delivered presets hash-match their previously verified v002 counterparts; current wire scans pass.
- Producer guide links all MIDI/presets, explains replacing the piano at bar 1, sound selection, section form, timing and drum mapping, and reports actual evidence.
- Musical review uses note data. Playback through the user's piano, live Cubase import, render analysis and listening have not been performed.
