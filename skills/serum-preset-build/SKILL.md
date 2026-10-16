---
name: serum-preset-build
description: Generate or safely revise native Serum 2 .SerumPreset files using serum-mcp, resolving schema units, resource dependencies, structural readback, and producer-ready delivery.
---

# Build and deliver a native preset

For analog/retro analog builds, use [analog and retro](../serum-sound-design/references/analog-retro.md), especially its implementation boundaries. Voice Control sequence length, polyphony, and unison are separate; detune units, phase options, FM source/tap, key tracking, and remap curves require explicit calibration or verified template/UI evidence. Never treat a generic FM enum or schema-accepted voice count as proof of the intended behavior.

Read [native build](../serum-sound-design/references/native-build.md), [capability boundaries](../serum-sound-design/references/tool-capabilities.md), and [templates](../serum-sound-design/references/templates.md). In `midi-creator`, read `docs/serum-mcp.md` before creating/editing presets and respect `AGENTS.md`.

1. Discover `serum-mcp` tools or its local checkout. Call `list_parameters()` before translating the design; inspect the current semantic `PresetSpec` when available. Record version/commit and field confidence. The manual specifies UI behavior, not a public file-format API.
2. Write a semantic design and exact tool spec separately. Validate types, units, enum strings, slot indices, routes, and resource paths. Record every required control as supported, uncertain, or unsupported; resolve unsupported requirements through a verified template/UI route or report the limitation.
3. Verify the destination is new. `generate_preset` can overwrite a same-named file; `edit_preset` mutates in place and can rename/remove its input. Copy an existing preset into a new revision first. Preserve custom resource/curve/rack data during edits and compare unchanged sections.
4. Generate/edit through the tool; retain its returned first-line path and all subsequent dependency paths. Verify the real `.SerumPreset` exists. Parse/read back the file and compare every requested field, accepting only justified numerical tolerances or known transformations. Use the upstream wire-type scan when available.
5. Copy the ready preset to the deliverable's `Presets/`; package non-factory sample/wavetable/IR dependencies with their install destinations and hashes. Store specifications, schema snapshot, tool responses, checksums, and receipts in `_internal/`.
6. Use [serum-preset-qa](../serum-preset-qa/SKILL.md) for plugin-load and sound evaluation. Write loading instructions, key/register, macro behavior, dependency installation, and separate structural/load/listening statuses.

Complete when native files, dependencies, and instructions exist, structural verification passes, and gaps in implementation or audition are visible. A JSON spec, renamed extension, `.vstpreset`, or sound recommendation does not satisfy a native preset request. No actual sound generation is necessary when the user asks only for design advice or skills/documentation.
