# Creating MIDI music in this workspace

## Serum 2 sound design

- When creating a new sound or choosing sounds for composition layers, use [serum-sound-design](skills/serum-sound-design/SKILL.md). The [main guide](docs/serum-sound-design/README.md) and [reference index](skills/serum-sound-design/references/index.md) provide theory, engines, sound families, recipes, and templates; read only the relevant branches.
- A request for one sound/preset produces that sound/preset. The full-arrangement defaults below apply to music composition requests; explanation or documentation requests follow the requested deliverable.
- For analog/vintage/retro analog sounds or emulation of real analog gear, use the [Serum 2 analog and retro guide](skills/serum-sound-design/references/analog-retro.md) as the required default, including sound choices for individual layers. Start from the gear architecture and a maintained instrument; distinguish VCO/DCO behavior, variation between voices, continuous drift, and recording coloration. Select the five techniques as needed rather than enabling all of them automatically. Explicit user choices take precedence; record assumptions, implementation limits, and verification evidence. Retro alone does not automatically mean analog.
- Select the focused skill for the task below. Skills are available in the workspace's `skills/` folder and as installed copies in the skill home; workspace copies are the maintenance source.

| Task | Skill |
|---|---|
| Design a complete sound from a brief | [serum-sound-design](skills/serum-sound-design/SKILL.md) |
| Match reference audio or a preset | [serum-reference-match](skills/serum-reference-match/SKILL.md) |
| Choose oscillators/engines, wavetables, FM/AM, filters, and routing | [serum-synthesis](skills/serum-synthesis/SKILL.md) |
| Shape envelopes, LFOs, macros, expression, glide, arps, and clips | [serum-modulation](skills/serum-modulation/SKILL.md) |
| Design FX, dynamics, stereo, space, and buses | [serum-effects](skills/serum-effects/SKILL.md) |
| Create or revise native presets and dependencies | [serum-preset-build](skills/serum-preset-build/SKILL.md) |
| Inspect, audition, or repair the resulting sound | [serum-preset-qa](skills/serum-preset-qa/SKILL.md) |

- Base musical choices on the brief and theory; use the Serum manual for UI behavior and the current tool schema/runtime for implementation parameters. The [source index](skills/serum-sound-design/references/sources.md) distinguishes available PDF content, omitted theory-demo sections, and supplemental guidance. Recipes are starting points to evaluate against the brief.
- Before a native build, read [Serum MCP](docs/serum-mcp.md) and call `list_parameters()`. For controls not supported by the tool, read the [capability boundaries](skills/serum-sound-design/references/tool-capabilities.md), use verified templates/UI when available, or record unmet requirements. Store specs, resource manifests, readback, and receipts in `_internal/`; package custom dependencies with the preset and installation instructions.
- Evaluate the sound's register, articulation, spectrum, motion, stereo behavior, and requested gestures using the [verification guide](skills/serum-sound-design/references/verification.md). Report structural verification, plugin loading, audio rendering/analysis, and actual listening separately. If live/audio access is unavailable, finish offline checks and mark the relevant musical checks untested.

## Delivery contract

- Every music request defaults to a complete multi-instrument arrangement from beginning to end. All instruments except drums use **Serum 2**. The number of layers follows musical needs; explicit requests for one melody, an excerpt, or another plugin override this default.
- Every music request also defaults to a native **`.SerumPreset`** file for each Serum 2 sound/layer, without a separate request. Build through the `serum-mcp` repository; read `docs/serum-mcp.md` before creating or editing presets. Store ready-to-use files in `Presets/`, named to match their MIDI layers, and specifications/bindings/receipts in `_internal/`. The README must link every MIDI–preset pair and explain loading. Explicit user requests can override this; drums retain the user's kit/sample choice.
- Each layer is one instrument exported as one `.mid` with exactly one instrument track. Create separate layers for different instruments. Drums may use one kit or one percussion part per layer, according to the brief.
- MIDI defaults to on-grid timing with `timing.mode: "strict"` and no swing; use swing only when requested. Dotted notes and meters other than 4/4 remain allowed when musically appropriate. Read the [MIDI timing guide](docs/midi-timing-guide.md) when creating music, using references, or revising rhythm.
- All layers in a composition share tempo, meter, resolution, start position, and total length. Preserve silence at its original positions so files align when imported into a DAW.
- Drums use the user's chosen kit/samples. Create drum MIDI performances when the arrangement needs them, then describe suitable drum character and pitch mapping in the README. Select or copy concrete samples only after the user chooses them or asks the agent to choose.
- When creating or revising drum MIDI, read the [default drum mapping](docs/default-drum-map.md) and choose either the separate-drum-layer or single-kit branch. Separate drum layers follow the guide's default Cubase Sampler root unless the user supplies another mapping; kit/sample selection remains the user's choice.
- Musical style, instruments, layer count, and arrangement follow the user. Create a combined file only when requested, using `--combined`.
- Every revision has a producer-facing `README.md`: tempo/key/meter/length, song form, track/MIDI/preset table, Cubase import from bar 1, song-specific drum suggestions, mapping, assumptions, and verification/listening status. If instruments outside Serum are needed or requested, include the reason, plugin/library, loading instructions, note range, articulations, and mapping.
- The producer-facing delivery area contains only `README.md`, `MIDI/`, `Presets/`, and `Audio/` or `Drums/` when requested. All agent working material—briefs, specifications, scripts, bindings, schemas, manifests, receipts, logs, intermediate output, and old revision archives—belongs in one `_internal/` folder. Read `docs/project-layout.md` when creating, revising, or organizing projects.

## Request workflow

1. Read `docs/agent-workflow.md` when creating new music, using references, or revising a composition. Read `docs/composition-guide.md` before writing a specification; the authoritative schema is `src/midi_creator/composition.schema.json`.
2. Translate the brief into tempo, meter, key when relevant, bar count, song form, and an instrument list. Choose unspecified details using musical judgment and record assumptions; ask only for information that genuinely blocks the work.
3. Prepare a new composition in `projects/YYYYMMDD-slug/_internal/source-v001/`; the generator creates the `v001/` output folder. Save the request, decisions, and acceptance criteria in `request.md` in the source folder using `templates/request.md`. Later revisions use `v002`, etc., and identify their source revision. The project-level README links the latest ready revision.
4. Write `composition.json` in the internal source folder. Use a local Python generator for large note counts, and save its script in the source folder for reproducibility. Fix and record random seeds. After publication, store source material in `vNNN/_internal/source/`. See `examples/`.
5. Run `uv sync --locked` if the environment is not ready. Run `uv run midi-creator validate <spec>`, then `uv run midi-creator generate <spec> --out projects/YYYYMMDD-slug/vNNN` into a folder that does not yet exist. Add `--combined` to both commands only when requested. Per-layer exports are always available.
6. Run `uv run midi-creator verify <output-folder>`. Technical completion requires exit code 0, `ok: true`, every requested file present, and one track/instrument per layer file with identical total lengths.
7. Evaluate musicality against the brief: harmony, register, instrument roles, drum rhythm, section development, dynamics, and phrase space. The validator checks MIDI structure; the agent must still judge musical decisions. Audition through the user's instruments when available and relevant. State accurately whether audio was actually heard.
8. Complete the README using `templates/project-readme.md`. Completion requires every linked file to exist, a structurally checked/read-back `.SerumPreset` for each Serum layer, song-specific drum suggestions, and guidance for every external instrument. JSON, a sound name/recommendation, or a `.vstpreset` alone does not complete a native preset. Provide links to the README, all MIDI files, and created native presets; summarize tempo/key/meter/bars/layers, verification status, and consequential assumptions. Report plugin loading and listening separately from preset structural verification.

## Revisions and maintenance

- For Cubase/Serum, read `docs/cubase-studio.md`. Keep plugin bindings separate from `composition.json`; use local configuration and explicit drum mappings. Call status first, verify the bundle, and distinguish offline results from live Cubase status. Do not claim a `.cpr`, native Serum preset, or auditioned audio without evidence.
- Treat `composition.json` as the source of truth. Correct the specification and export into a new folder to repair MIDI; exported output contains its own composition snapshot.
- New per-layer MIDI uses SMF format 1 with exactly one track, without SysEx, extra text/key/marker metadata, Bank Select, or Program Change. Key and song sections remain in the specification/README. Preserve tempo, meter, notes, velocity, CC7/CC10, and global end-of-track. File verification is separate from live Cubase drag-and-drop testing; report accurately when live import is untested.
- Preserve earlier revisions and user reference material. Musical revisions keep requested sections unchanged; document modified sections in `request.md`.
- A melody layer has one fixed program. Use two layers for two instruments; articulations and special drum maps follow the user's plugin.
- Use `uv run midi-creator --help` for CLI options. Fix validation errors before delivery.
- When changing the generator/schema, run `uv run python -m unittest discover -s tests -v` and check the single- and multi-layer examples. Update guides when the contract changes. Ordinary compositions need validate/generate/verify and musical evaluation.
