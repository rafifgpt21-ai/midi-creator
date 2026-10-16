# Design and audition criteria

This document describes intended sonic behavior. Structural evidence proves stored settings and resource identity; audible behavior remains untested.

## Architecture

| Layer | Actual MIDI register | Excitation, body, and path | Articulation, motion and space |
| --- | --- | --- | --- |
| sub-bass | 29–49, F1–Db3 | Basic Shapes sine A → Master → output; one oscillator, centered mono, no FX/filter | 5 ms attack, 3.4 s decay to 0.93 sustain, 48 ms release; velocity plus a separate 130 ms attack-lift envelope |
| bass-grit | 41–61, F2–Db4 | Saw A + quieter square B (3 cent detune) → HP12 → LP12 → tape saturation → light compression → EQ | 6 ms onset, 1.1 s decay to 0.79 sustain; 430 ms filter-color decay; mono, no glide/space |
| shadow-pad | 67–80, G4–Ab5 | Warm saw A + triangle B + very low brown noise → HP12 → MgLP12 → Hall reverb → EQ | 580 ms attack, 480 ms release; slow 0.085/0.11 Hz triangle motion gated by MOTION; mild unison supports width |
| ghost-bell | 76–88, E5–E6 | Sine A + sine B at 2 octaves + 2 semitones (4.48985x) → LP12 → dark eighth-note echo → small Hall | 11 ms attack, 1.2 s decay to zero sustain, 620 ms release; upper partial's 130 ms envelope decays earlier; no FM warp |
| tension-rise | Notes 77 trigger noise; pitch irrelevant | Pink noise → HP12 → LP12 → output, no pitched source or FX | 3.0 s amplitude rise, 2.75 s color rise, 1.95 s late tension gesture; release 20 ms; seven-beat MIDI gates are 3.088 s |

Source engine: wavetable for pitched voices and Noise engine for noise. Sample, granular, spectral, multisample, convolution, splitter and extra bus dependencies are unnecessary for these roles. All note generation is external MIDI; arpeggiators are explicitly off.

## Macros and endpoint intentions

Macro range is 0–100%. Defaults are the starting mix; endpoint behavior is structurally represented but has not been auditioned.

| Layer | Macro/default | 0 → 100 intention |
| --- | --- | --- |
| sub-bass | BODY 15 / PUNCH 28 | BODY: base sine level → modest added level; PUNCH: no extra transient → short envelope-led attack lift |
| bass-grit | BITE 18 / TONE 25 / ATTACK 35 | Saturation blend 62→87%; restrained→more open LP; no extra attack envelope depth→additional brief color opening |
| shadow-pad | SHADE 18 / MOTION 24 / SPACE 12 | Base tone→darker LP; static modulation depth→slow color/pan motion; Hall wet 18→40% |
| ghost-bell | GLASS 28 / ECHO 10 / SPACE 15 | Quiet upper partial→stronger short upper strike; delay wet 13→35%; Hall wet 9→23% |
| tension-rise | AIR 15 / TENSION 22 / LIFT 15 | Base sweep→brighter sweep; no added resonance→late envelope lift; base noise level→higher source level |

Normalized filter cutoff is not a literal Hertz value. Two-filter source-balance units are observed/partially understood; serialized routing and requested values are checked, while isolation tests in Serum remain untested. Envelope curve law and gain accumulation likewise require audio validation. Free LFOs explicitly use beat_sync=false and nonzero rate; description summaries round these slow rates to 0, but decoded readback retains exact requested values.

## Offline checks and future audition matrix

Offline checks: exact spec readback, macro/routes/curves/routing, resource paths and waveform metadata, CBOR numeric wire types, arpeggiator off, conservative normalized route bounds, unchanged MIDI hashes, native artifact hashes and README links.

Focused audition when loaded in Serum: compare v001/v002 at matched output level on the actual MIDI; test minimum/middle/maximum note, velocities 48/80/120, 0.125/0.5/3 beat gates, rapid repeats and held notes. For pad also test three-note chord changes, releases, stereo and mono. For each macro test 0/default/100 and interacting extremes. For the riser use its 7-beat gate at 136 BPM and inspect the final quarter-note gap. Check bass fundamental, grit low-band overlap, piano masking, bell attack/tail and noise buildup; audio peaks/phase/mono cancellation cannot be passed from a preset decoder.

Acceptance statuses: structural/resource checks PASS; real plugin load, render analysis, listening and audible preference UNTESTED. Source waveform FFT is analysis of installed assets only.
