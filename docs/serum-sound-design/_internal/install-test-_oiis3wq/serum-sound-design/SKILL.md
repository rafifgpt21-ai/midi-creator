---
name: serum-sound-design
description: Design requested sounds in Serum 2 from descriptive briefs or references, choosing synthesis, modulation, effects, and a native preset delivery workflow. Use for end-to-end sound creation; focused stages have companion Serum skills.
---

# Serum sound design

Turn the user's requested sonic behavior into a playable Serum 2 sound. Use the supplied manual for control behavior, theory for causal decisions, and the current tool schema for implementation. The shared reference library lives in this skill's `references/`; install the seven sibling skills together.

## Workflow

1. Read [brief-and-analysis.md](references/brief-and-analysis.md). Record role, register, note duration, amplitude contour, harmonic/noise balance, spectral movement, stereo behavior, expression, and the user's constraints. Resolve ordinary musical details yourself. Ask only for missing information that blocks an important choice, such as an unavailable reference or required sample.
2. For an audio/preset reference, use [serum-reference-match](../serum-reference-match/SKILL.md). Distinguish observed properties from inferred architecture. For words alone, translate the descriptors into testable behaviors.
3. Read [architecture.md](references/architecture.md), then the relevant engine/family reference via [index.md](references/index.md). Use [serum-synthesis](../serum-synthesis/SKILL.md) to design excitation, pitch, filters, and signal paths. Establish the defining dry sound before optional polish; processing may itself define the sound when the brief requires it.
4. Use [serum-modulation](../serum-modulation/SKILL.md) for articulation, movement, performance, macros, arp/clip behavior. Use [serum-effects](../serum-effects/SKILL.md) for character, space, width, or dynamics that the brief needs.
5. Use [serum-preset-build](../serum-preset-build/SKILL.md) to translate the design into the available schema and deliver `.SerumPreset`. Record unsupported controls explicitly; choose a supported equivalent only when it meets the request. Consult the plugin UI/manual for exact controls that automation cannot represent.
6. Use [serum-preset-qa](../serum-preset-qa/SKILL.md). Iterate on the largest audible mismatch one variable group at a time. Preserve earlier revisions. Deliver the preset, dependencies, loading instructions, useful macro ranges, and evidence of checks.

Completion means each user constraint is met or identified as unresolved, native files and dependencies exist, structural checks pass, and plugin/loading/listening status is reported separately. If the environment cannot render or audition, finish the available build/readback work and label sonic evaluation untested. A broad vocabulary and an iterative process support unfamiliar requests; no recipe guarantees exact reproduction of every recording or acoustic instrument.

## Scope and local integration

A request for one sound stays a sound request; it does not require composing a song. In the `midi-creator` workspace, follow its `AGENTS.md` and read `docs/serum-mcp.md`. For composition work additionally read its composition, timing, layout, and studio guides. Use one instrument per MIDI layer and match layer/preset names. Respect the user's drum/sample selection. Keep producer-facing output separate from specifications and receipts in `_internal/`.

## Read only what the task needs

- Theory or unfamiliar descriptors: [theory.md](references/theory.md), [glossary.md](references/glossary.md).
- Exact Serum control location or manual evidence: [serum-control-map.md](references/serum-control-map.md), [sources.md](references/sources.md).
- Synthesis, sampling, resynthesis: [index.md](references/index.md).
- Worked starting points: [recipes.md](references/recipes.md); all numbers are authored starting points, not source presets or verified listening results.
- Build specification and handoff: [templates.md](references/templates.md).
