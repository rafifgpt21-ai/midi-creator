# Composition brief

- Project: Black Glass; revision v001, new composition; 2026-10-12.

## Original requests

> make a dark trap rnb with piano (piano dont need a preset, ill pick the sound myself), the inspiration is the hills by the weeknd, withs seperate midi file for each drum sound, with a huge bass drop at the chorus

> make the piano like played by human make sound so dynamic

## Musical decisions

- Dark, spacious, half-time trap R&B; original music using the reference for mood and contrast. No reference audio/MIDI was supplied or transcribed.
- 136 quarter-note BPM / 68 BPM half-time feel; 4/4; F minor; 112 bars / 3:17.65; 480 PPQN.
- Form: intro 8 / verse 16 / pre 8 / chorus 16 / aftershock 4 / verse 16 / pre 8 / chorus 16 / bridge 8 / final chorus 8 / outro 4.
- Harmony: Fm9, Dbmaj7(add9), Bbm9, Csus4(b9) to C7(b9); E resolves to F. Outro returns to F minor.
- Expressive piano: different hand weights, soft inner notes, melody accents, phrase arcs, rests, varied gates, and intentional broken chords. Straight 1/32 onset grid without swing or random timing jitter.
- Deep chorus bass; quieter verse bass one octave higher; separate chorus-only distorted octave. Seven-beat rise and one-beat MIDI silence before drops at bars 33, 77 and 101.
- Piano selected by user; five native Serum 2 presets; seven separate drum files with user default pitches.

| Layer | Instrument / purpose | GM hint / pitch |
| --- | --- | --- |
| piano | User-selected acoustic piano, harmony and hook | 0 |
| sub-bass | Serum 2 low foundation | 38 |
| bass-grit | Serum 2 distorted chorus octave | 38 |
| shadow-pad | Serum 2 upper atmosphere | 89 |
| ghost-bell | Serum 2 response melody | 98 |
| tension-rise | Serum 2 noise swell | 97 |
| kick | Short kick | 36 |
| snare | Half-time backbeat | 38 |
| rim | Ghost accents | 41 |
| closed-hat | Straight hats / rolls | 54 |
| open-hat | Offbeat lift | 57 |
| crash | Chorus punctuation | 64 |
| floor-tom | Transition fills | 47 |

## Assumptions, reproduction and acceptance

- Seed 20261012; reproduce composition with `build_composition.py`.
- Piano expression depends on a velocity-sensitive sound. Pedal CC is unavailable in the current schema; overlapping different notes provide connected phrasing.
- Drum samples remain user-selected. No combined MIDI, audio, or piano preset requested.
- New native presets generated through serum-mcp at the recorded commit. Factory Dark Space and 808 Drill descriptions informed synthesis choices, without reusing their preset state.
- Thirteen independent single-track, globally aligned MIDI files; five paired native presets; validate/generate/verify and structural preset readback pass.
- Acceptance audit checks drum pitches, drop entries/rests, chorus-only grit and expressive piano velocities/gates. Musical review uses note data; plugin loading, live Cubase import and listening were not performed.
- Output: `projects/20261012-black-glass/v001/`. Producer README links all deliverables and explains import, mapping, sound selection and test status.
