---
name: serum-reference-match
description: Analyze an audio excerpt, recording, or existing preset and recreate its sound in Serum 2 using observable timbre, articulation, motion, and controlled comparisons.
---

# Match a reference in Serum 2

For analog/retro analog gear references, use [analog and retro](../serum-sound-design/references/analog-retro.md) by default. Separate the dry instrument architecture and condition from recording-chain effects. Preserve observed DCO/VCO stability and voice behavior; identify model/revision uncertainty and avoid claiming circuit equivalence from a similar sound.

Read [brief and analysis](../serum-sound-design/references/brief-and-analysis.md) and [reference matching](../serum-sound-design/references/reference-matching.md). For existing presets also read [native build](../serum-sound-design/references/native-build.md).

1. Preserve the source and identify the precise event/time range. Establish whether it is isolated, layered, or mixed with other instruments. Record pitch/register, note/gate timing, tempo when motion is synced, and any reference gain adjustment.
2. Extract an evidence table for attack, body, tail, spectrum, pitch stability, modulation, stereo, and effects. Listen if audio access permits. When useful, use waveform, spectrogram, pitch estimation, and channel analysis; retain uncertainty from polyphony, drums, distortion, and masking.
3. Propose the smallest plausible architecture that accounts for those observations. Rank alternatives rather than declaring an original synthesizer or signal chain from audio alone. Read only the selected engine and sound-family references in [the reference index](../serum-sound-design/references/index.md).
4. Match note and amplitude behavior, then dry spectrum and spectral evolution, then motion, then width/space. Use the same notes, velocity, duration, tempo, sample rate, and approximate perceived level in comparisons. For an FX-defined sound, include its defining processing earlier.
5. Build through [serum-preset-build](../serum-preset-build/SKILL.md), evaluate through [serum-preset-qa](../serum-preset-qa/SKILL.md), and preserve a mismatch log. Change one cause group per revision and retain improvements.

Complete when the important observed properties match to the stated tolerance, the user-specific constraints are met, and the deliverable/evidence is available. For a mixed reference, state which properties remain ambiguous. Without audition, deliver a structurally checked candidate and the comparison plan; do not claim an audible match. Reuse supplied samples when their recognizable character is required and permitted by the brief.
