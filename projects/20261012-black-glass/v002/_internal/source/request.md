# Black Glass — preset revision v002

- Date: 2026-10-12. Origin: v001.
- User request: **“update preset nya dan buat lebih bagus lagi”**.
- Interpretation: redesign and refine all five Serum layers for the existing dark trap R&B arrangement. Preserve all notes, timing, velocity, mixer settings, piano expression and seven separate drum performances exactly.
- Musical context: 136 BPM / 68 half-time, F minor with harmonic-minor dominant, 4/4, 112 bars / 3:17.65, 13 layers. Main chorus drops: bars 33, 77 and 101.
- Piano still uses the user's chosen sound; no piano preset. Drum samples remain user-selected. No combined file, rendered audio or new musical arrangement requested.

## Changes and reasons

| Sound | v002 design change | Intended benefit |
| --- | --- | --- |
| sub-bass | Pure sine, no distortion, high sustain, short attack-lift envelope, BODY/PUNCH gestures | Separate clean low foundation from driven octave; maintain verse/chorus velocity contrast |
| bass-grit | Verified saw/square content, serial HP/LP, transient filter envelope, tape saturation and post EQ | Articulated bite with a darker body and controlled low-frequency overlap |
| shadow-pad | Saw/triangle contrast, slight brown-noise air, serial HP/LP, slower attack, macro-controlled slow stereo/color motion | Darker atmosphere around the piano with less static texture |
| ghost-bell | Sine body plus short 4.49x inharmonic upper partial, softer attack, zero sustain and darker short echoes | A more coherent struck response without relying on ambiguous FM-source selection |
| tension-rise | Pink noise, high-pass/low-pass sweep, late resonance lift, 20 ms release and no FX | Build from dark to bright through the seven-beat rise while leaving the pre-drop gap clear |

## Workflow and assumptions

- Applied workspace skills: serum-sound-design, serum-synthesis, serum-modulation, serum-effects, serum-preset-build and serum-preset-qa.
- Current list_parameters and semantic PresetSpec inspected. Raw source waveform FFT confirms Basic Shapes frame 0 sine, 1 saw, 2 triangle, 3 square; OSCAR frame 0 is saw-like. This source analysis is not plugin audio rendering or listening.
- New native files built through serum-mcp in a new User bank. No v001 preset edited or overwritten. Exact MIDI byte comparisons prove preservation.
- Phase/randomness control and full live sonic macro behavior are not tested. The semantic tool has no general source-phase setter; use its existing/default phase state without claiming fixed phase.
- Native playback unavailable through current studio tools; the installed Serum version is 2.0.23. Native load, audio render/analysis and actual listening remain untested. No claim of audible improvement is made from structural evidence alone.

## Acceptance

- All five native files decode, requested settings read back, wire-type scans pass, arp explicitly disabled, dependencies resolve and delivered hashes match.
- Every MIDI in v002 is identical to v001; validate/generate/verify pass and all 13 one-track files remain aligned.
- Specs, analysis, capability notes, resource manifest, checks, logs and receipts are in `_internal/`; producer guide links every MIDI/preset with macro defaults and loading instructions.
