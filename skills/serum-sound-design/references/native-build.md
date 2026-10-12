# Native preset workflow

This is an implementation guide based on the inspected local `serum-mcp` revision and workspace rules. It is not an official Xfer file-format specification. Manual loading/saving: S2 pp. 18-22, 302-303, 327-336.

## Authorities and discovery

Use the user's brief for the target, the supplied manual for UI behavior, `list_parameters()` for raw names/units/enums/confidence, and current `generation/spec.py::PresetSpec` for semantic input. Record implementation commit/version. In `midi-creator` read `docs/serum-mcp.md`; local checkout is `integrations/serum-mcp`, pinned by `integrations/serum-mcp-source.json`. Other environments must discover their own checkout and configuration rather than assume this path exists.

Available MCP operations in this environment: `list_parameters`, `find_reference_presets`, `describe_preset`, `list_sample_files`, `analyze_sample_file`, `generate_preset`, `edit_preset`. These inspect and write preset files; they do not load Serum, render audio, or control Cubase.

## Field mapping

| Human label | Semantic spec | Verify |
|---|---|---|
| Osc A/B/C/Noise/Sub | `oscillators` indices 0/1/2/3/4 | List indexing and enabled state |
| Filter 1/2 | `filters` indices 0/1 | Input/output paths |
| Env 1-4 | `envelopes` indices 0-3 / sources `env0`-`env3` | Main amplitude is Env 1 |
| LFO 1-10 | `lfos` indices 0-9 / `lfo0`-`lfo9` | Mode, curve, sync and rate |
| Macro 1-8 | `macros` indices 0-7 / `macro0`-`macro7` | Name/default and actual routes |
| Main/Bus 1/Bus 2 | FX `rack` 0/1/2 | Sends, returns, graph and gains |

Lists identify slot positions; placeholder entries can invoke defaults or edits, so inspect mapping behavior. Explicitly disable unwanted sources. Build from Init for a new design; copy a verified reference when preserving complex data the semantic model cannot construct.

## Units that commonly fail

| Field | Inspected semantic convention |
|---|---|
| Oscillator `volume` | 0-1, not dB or percentage |
| Oscillator `pan` | -50..50 in current model |
| `octave`, `semitone`, `fine` | Octaves, semitones, approximately cents respectively |
| `unison` | 1..16, whole count represented as float |
| `detune`, `warp_amount` | Normalized 0..1 |
| `table_position` | Frame-related 0..256; actual table length/content matters |
| Envelope attack/hold/decay/release | Seconds |
| Envelope sustain | Normalized 0..1 |
| Envelope curves | 0..100 with partially inferred stage semantics |
| Filter cutoff | Normalized 0..1, not literal Hz |
| Filter resonance/drive/wet | Percent-like 0..100 |
| Filter stereo | 50 documented neutral; do not assume zero neutral |
| Route amount | -100..100 percent; destination scaling varies |
| Macro value | Check current schema, commonly 0..100 |
| Granular grain length | Milliseconds |
| Granular density | Documented UI-related 0..30, not assumed Hz |
| Sample loop positions/crossfade | Percent |
| LFO `rate` | Mode/sync dependent; explicit `beat_sync=False` for free-Hz intent |
| Arp `rate` | Normalized discrete division dial, not Hz |
| FX wet | 0..100; actual per-module keys have their own units |

Defaults may be omitted from serialized state. An absent parameter does not equal zero. `None`, explicit false, and an untouched section can differ materially in edit/generate behavior. Store the submitted spec, not only a `model_dump()` full of defaults.

In particular, LFO `rate=0.0` is omitted by this writer and cannot request a genuinely frozen 0 Hz LFO. Gate its modulation depth instead when motion should remain dormant until a macro acts.

## Safe creation and revision

1. Resolve target folder/name and verify no collision. Use a new revision/subfolder and source brief/spec under `_internal/`.
2. Call `list_parameters()`; inspect semantic model and focused raw schema sections. Validate the spec locally when available. Pydantic may ignore extra fields: identify unknown keys rather than silently losing them.
3. Resolve and analyze resources before generation. Keep one engine selector per source slot. Verify field support, especially FM source, phase/randomness, spectral curves, IR/splitter topology, clips, and MPE enablement.
4. Call `generate_preset(spec, subfolder)` for new Init-based work. For editing, first copy the original to a new revision; call `edit_preset(preset_path, spec)` on the copy. The latter edits in place, may rename, and can remove its old copied path.
5. Parse the tool response: first line is returned native path; following lines list dependencies. Record complete response and actual paths rather than deriving the sanitized filename by hand.
6. Run `describe_preset` on the exact output; decode/check every requested field and all required resources. Omitted defaults and numeric transformations require documented explanation. Inspect native payload directly with the upstream parser when a summary omits curves/routes/resources.
7. Run upstream `scripts/check_preset.py` or equivalent wire-type validation. In `plainParams`, the implementation normalizes numeric/boolean state to CBOR doubles. Top-level booleans and module/source IDs can use different types; do not globally rewrite every integer/boolean.
8. Copy the ready file/dependencies into the deliverable and compare SHA-256 hashes. Record source/installed/copy locations separately.
9. Load/audition if available and produce a truthful verification receipt. Write README instructions and links.

## Local offline alternatives

Use the upstream environment, not the MIDI environment, for upstream helpers:

```powershell
& integrations/serum-mcp/.venv/Scripts/python.exe integrations/serum-mcp/scripts/check_preset.py 'C:/absolute/path/Sound.SerumPreset'
```

The repository's `integrations/check_serum_mcp.py` opens a real MCP stdio connection and can generate/read back a spec. Inspect `--help` and use a new output/subfolder. Native render workflows need a host path: loading `.SerumPreset` in Serum and saving a genuine VST preset is a conversion step, not extension renaming.

## Portable delivery

Producer-facing files: `README.md`, `Presets/`, and requested `MIDI/`, `Audio/`, or resources folder. Technical files live in `_internal/`. In this workspace custom dependencies can reside under `Presets/Resources/` with documented destinations in Serum `Tables`/`Samples`/IR locations. Separate factory content required from custom files included. If embedding through the UI, inspect/reload to confirm it; generated external content is not assumed embedded.

README states native preset path, install/load procedure, target note range, macro defaults/endpoints, sample/IR/table dependencies, and structural/load/listening statuses. Composition README also links every MIDI-preset pair and follows the local song template. A sound-only request does not manufacture an arrangement to satisfy composition defaults.
