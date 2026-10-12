# Composition brief

- Project: Afterimage Garden
- Revision: v001; new composition
- Date: 2026-10-11

## Original request

Create an (tame impala inspired) atmospheric, synth-heavy psychedelic pop track inspired by 80s analog synthpop and modern neo-psychedelia. Features lush, sweeping analog synth pads (Juno-106 style), bright arpeggiated synth leads, and a thick, hypnotic bassline with phaser modulation. The drums should have a groovy, compressed 70s/80s disco-funk beat Overall vibe: nostalgic, introspective, groovy, warm, and euphoric.

User drum guide, numeric MIDI values authoritative: kick 36; snare sidestick 37, center 38, flam 39, rimshot 40; closed hat 42, pedal 44, open 46, tight 17, loose 21; low floor tom 41, high floor tom 43, low rack tom 45, high rack tom 47; crash left 49, left choke 57, crash right 55, right choke 59, ride bow 51, bell 53, edge 58, China 52; splash 54, cowbell 56. Preserve this supplied mapping rather than substituting GM instrument names for 17, 21, 55 or 56.

## Musical decisions

- Style/mood: original instrumental psychedelic synthpop with disco-funk pulse; nostalgic minor-key verses and brighter major-colored choruses.
- Tempo: 108 quarter-note BPM. Meter: 4/4. Key: D natural minor.
- Length: 104 bars / approximately 3:51, including four bars of release space.
- Form: intro 1-8; verse 1 9-24; lift 25-32; chorus 33-48; interlude 49-56; verse 2 57-64; lift 65-72; final chorus 73-88; outro 89-100; tail 101-104.
- Harmony: verse Dm9-Bbmaj7-Fmaj9-Cadd9, chorus Bbmaj7-F/A-Cadd9-Dm9, lifts Gm9-Bbmaj7-Dm9-Cadd9; two bars per chord. Outro resolves to Dm9.
- Timing: strict straight sixteenth grid, no swing or onset humanization; variation in velocity and gate, repeated phrases with deliberate rests.
- Sound: Serum 2 for all six pitched layers; external user-selected kit for one drum track.

| Layer | Target | Function | GM hint / map |
| --- | --- | --- | --- |
| juno-pad | detuned saw/PWM, slow filter sweep, chorus | sustained extended harmony | 89 |
| phase-bass | mono analog bass, phaser on upper tone, direct triangle support | kick-locked and syncopated foundation | 38 |
| prism-arp | bright short analog pluck with eighth-note echo | pulse and lift | 81 |
| afterimage-lead | warm melodic analog hook with gentle vibrato | chorus hook and sparse answers | 80 |
| velvet-keys | soft percussive analog keys with chorus | offbeat chord stabs | 4 |
| halo-texture | quiet high harmonic texture | atmosphere and transitions | 91 |
| disco-kit | supplied drum map, one kit | rhythm and fills | channel 10 |

## Assumptions and references

No reference recording supplied; artist mention guides broad instrumentation and mood. All notes and motifs are original. Agent selected key, tempo, duration, and instrumental form. Drum sample bank/kit was not selected by user, so only MIDI performance and sound/mixing guidance are delivered; no sample files are selected or copied. Native Serum patches are designed from scratch after upstream schema inspection and Juno-name reference inspection; that reference is not copied. Seed 108104; reproducible script build_composition.py.

## Revision changes

New v001; no prior version changed.

## Acceptance and results

- Seven synchronized format-1 MIDI files, exactly one track per instrument.
- All files at 108 BPM, 4/4, 480 PPQN, bar 1 origin, 104-bar EOT, with leading silence preserved.
- Six native .SerumPreset files with oscillator/filter/envelope/LFO/FX/macro routing, matching layer names, and structural readback receipts.
- Validate/generate/verify must pass. README must link each pair and explain Cubase import, supplied drum mapping, and selected musical assumptions.
- Musical review: harmony/register, interlocking bass/drums, chorus motif/space, density changes, and release space. Automated MIDI checks are separate from musical judgment.
- Output: ../.. (revision v001 after publication).
- Playback/render/plugin loading/live Cubase import: not performed; structural readback and MIDI integrity checks only.
