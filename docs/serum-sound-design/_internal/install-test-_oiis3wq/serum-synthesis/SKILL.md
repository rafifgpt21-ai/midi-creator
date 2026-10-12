---
name: serum-synthesis
description: Design Serum 2 oscillator, wavetable, FM, sample, multisample, granular, spectral, filter, and routing architecture for a requested timbre, including custom waveform design.
---

# Design the source and signal path

Read [architecture](../serum-sound-design/references/architecture.md) and the relevant foundations in [theory](../serum-sound-design/references/theory.md). Select conditional references from [index](../serum-sound-design/references/index.md): wavetable/FM, sample engines, granular/spectral, filters/routing, and the requested sound family.

1. Separate the desired excitation (periodic tone, noise, impulse, recorded attack) from resonant body, time evolution, and processing. Identify which components must be independently shaped.
2. Choose an engine for the defining property. Use wavetable/subtractive for controllable harmonic tones, oscillator FM/AM for sideband structure, sampler for recognizable recorded events, multisample for an available instrument over a usable range, granular for grain behavior, spectral for frequency-domain transformation. Add hybrid components only for a named sonic function.
3. Specify each active slot's source, pitch, level, phase/randomness, unison, warp order, routing, and dependencies. In the current tool slot numbering A/B/C/Noise/Sub is 0/1/2/3/4; UI envelopes and LFOs use different human labels from zero-based schema indices.
4. For FM/AM, verify the actual source routing rather than assuming a friendly `fm` enum selects a particular oscillator. Enable the source; reduce its audible level if it is a modulator only. Check whether its pitch tracks the carrier and whether the modulator is itself warped/unison.
5. Specify filters and all bypass/parallel paths. Confirm every audible source reaches the intended output. Keep a clean fundamental path when the brief needs a stable bass; distinguish intended beating from phase cancellation.
6. Translate through [serum-preset-build](../serum-preset-build/SKILL.md). Keep unsupported details in the design document and implement them through a verified UI/template path when available.

Complete when each sound component has a justified source and path, resources are resolvable, and a dry test across the required note range demonstrates the intended excitation/body behavior or is explicitly marked untested. Hand off amplitude/movement to [serum-modulation](../serum-modulation/SKILL.md) and processing to [serum-effects](../serum-effects/SKILL.md).

Local customization
