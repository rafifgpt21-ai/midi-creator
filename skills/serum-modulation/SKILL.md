---
name: serum-modulation
description: Shape Serum 2 envelopes, LFO movement, modulation routes, macros, velocity, MPE, mono/legato/glide, arpeggiators, and clips for expressive or rhythmic sounds.
---

# Articulation, motion, and expression

For analog/retro analog, use [analog and retro](../serum-sound-design/references/analog-retro.md) by default. Separate voice calibration offsets, phase randomness, continuous drift, and performance vibrato; calibrate total pitch depth in cents. Choose shared versus per-voice/per-oscillator motion and DCO stability deliberately; preserve the target's envelope/legato/expression behavior.

Read [modulation and performance](../serum-sound-design/references/modulation-and-performance.md). For rhythmic note generation read [arp and clips](../serum-sound-design/references/arp-and-clips.md). For exact controls consult [Serum control map](../serum-sound-design/references/serum-control-map.md).

1. Convert the requested behavior into note-level events, cyclic motion, phrase-level automation, and performance gestures. Keep amplitude, brightness, and pitch contours separate unless coupling is intentional.
2. Give each route a source, destination, base value, depth/polarity, curve, rate or duration, trigger behavior, and useful output range. Account for simultaneous route sums and macro endpoints.
3. Set Env 1 (schema `env0`) for voice amplitude and additional envelopes for timbre/transients. Evaluate the shape at actual note lengths: a short gate can release before decay finishes; legato can skip envelope retriggers.
4. Choose retriggered, free-running, or envelope-mode LFO behavior deliberately. Set tempo-sync explicitly. Confirm displayed/measured rate; the current tool's `rate` is not universally Hz. Use smooth changes for fluid motion and discontinuities only when their clicks/sidebands are intended.
5. Map performance controls to musical outcomes: velocity to attack/brightness, mod wheel/pressure to vibrato or intensity, note tracking to register compensation. Distinguish channel aftertouch, poly aftertouch, and MPE note expression; only claim mappings supported by the tool/host actually used.
6. Name macros by audible outcome. Test minimum, default, maximum, and interactions; compensate gain when necessary. For rhythmic voices decide whether external MIDI, the arp, or clips owns note generation, and keep the other generators inert unless layered generation is requested.
7. Build via [serum-preset-build](../serum-preset-build/SKILL.md) and verify overlapping/non-overlapping notes, release, transport sync, and macro endpoints via [serum-preset-qa](../serum-preset-qa/SKILL.md).

Complete when gestures and timing meet the brief and the route table agrees with readback. If required internal curves, MIDI expression, or clock settings are not representable, document the exact manual/UI step and testing status rather than substituting an invented parameter.
