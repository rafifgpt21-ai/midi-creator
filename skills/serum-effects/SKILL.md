---
name: serum-effects
description: Design or revise Serum 2 effects chains, multibus routing, distortion, EQ, compression, modulation, delay, convolution, reverb, and stereo processing for a requested sound.
---

# Process the sound in Serum 2

For analog/retro analog, use [analog and retro](../serum-sound-design/references/analog-retro.md) by default. Distinguish source/voice-filter nonlinearity from summed bus processing and recording coloration. Level-match comparisons; chorus, fast compression, stereo noise, tape, and external reverb are target-dependent choices, not mandatory analog processing.

Read [effects](../serum-sound-design/references/effects.md) and [filters and routing](../serum-sound-design/references/filters-and-routing.md). Consult the module-specific manual pages in [sources](../serum-sound-design/references/sources.md) when a control is uncertain.

1. Identify the required outcome for each processor: harmonic generation, transient/dynamic shaping, spectral balance, motion, width, distance, or a special transformation. Processing order and sends are part of the sound design.
2. Choose serial, parallel, Main, Bus 1, Bus 2, or Direct paths to achieve that outcome. A splitter is a routing operation; verify its child branches and recombination, not just its presence in a flat chain.
3. Work with conservative input levels and evaluate each stage with matched bypass level. Distortion/compression can make a change appear better simply by making it louder. Protect note intelligibility and fundamental energy where the brief needs them.
4. Configure frequency-dependent processing, attack/release, feedback/decay, modulation depth, wet/dry, and output levels. Read the current schema for actual units and enums; distinguish UI percentages, dB, milliseconds, seconds, normalized controls, and raw curve storage.
5. For synced delays confirm subdivision at the host tempo. For convolution resolve the actual impulse file and its availability. Test mono, lowest/highest notes, dense polyphony, processor bypass, and decay after note-off.
6. Build via [serum-preset-build](../serum-preset-build/SKILL.md), then [serum-preset-qa](../serum-preset-qa/SKILL.md). Revise only the requested characteristics of an existing sound.

Complete when each active effect serves the brief, all routes and resource dependencies are accounted for, and gain/tails/stereo behavior are tested or explicitly recorded as untested. When an advanced rack graph is outside tool support, preserve a verified reference rack or use the UI; a list of effect names alone does not implement its topology.
