# Composition revision brief

- Project: Afterimage Garden
- Revision: v002, drum-only supplement
- Source revision: v001
- Date: 2026-10-12

## Original request

"re generete only the drum midi use this as new guide (and make the .md file for default drum)". The full new user mapping is recorded in docs/default-drum-map.md and the revision's drum-map.json.

## Musical decisions

- Keep 108 BPM, D minor arrangement context, 4/4, 104 bars / approximately 3:51, 480 PPQN.
- Preserve v001 form, drum note count, onset, duration, velocity and initial CC7/CC10.
- Export only disco-kit.mid. Six melodic MIDIs and six native Serum presets stay in v001 unchanged.
- Strict straight 1/16 grid; no swing. Same disco-funk rhythm and dynamics.
- New pitch mapping by articulation, rather than transposition by octave.

| Layer | Instrument | Function | Channel |
| --- | --- | --- | --- |
| disco-kit | User-selected external mapped drum kit | Disco-funk beat and fills | 10 |

## Assumptions and substitutions

The new map omits sidestick/cross-stick and cowbell. Use snare rim 41 for old sidestick 37, and stick 88 for old cowbell 56, preserving the respective rhythmic and dynamic roles. These are timbral substitutions. Open hat uses 57, the first of the user's three open-hat choices. High/low rack tom and floor tom are mapped by role. No sample selection, copying, synth preset generation, or audio render requested.

## Changes and preserved material

Only drum pitches change. Prior v001 remains intact. Source-checksums.json records all prior MIDI/preset hashes for final comparison. remap_drums.py regenerates the specification without random decisions.

## Acceptance criteria

- One format-1 MIDI with one drum instrument track on channel 10.
- Same tempo, meter, start, global length, note count, timing, velocities, gates, CC7 and CC10 as v001 drums.
- All pitches in new guide; mapping choices/substitutions documented.
- Validate/generate/verify pass. Prior MIDI and preset bytes unchanged.
- Default drum guide saved and linked from AGENTS.md for future drum work.
- README includes import at bar 1, form, mapping, sound recommendations and accurate verification/listening status.
- No playback or Cubase import performed.
