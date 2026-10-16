# Serum 2 sound-design skill pack

Seven focused skills and a shared Markdown handbook turn descriptive requests or references into a source architecture, modulation/performance design, effects plan, native preset, and evidence-based evaluation. The skill entrypoints stay short; agents load only the relevant references.

The pack covers all five main source engines, hybrid designs, custom wavetables, FM/AM/warp, noise/sub, filters/routing, envelopes/LFOs/macros, expression and MPE, voicing/glide, effects/busses, arp/clips, common sound families, reference reconstruction, native delivery, and troubleshooting. It supplies a method for unfamiliar sounds as well as twelve worked starting designs. Exact recreation still depends on the requested behavior, source resources, Serum's capabilities, and actual audition.

## Start here

Use `$serum-sound-design` for a full sound request. Examples:

> Use $serum-sound-design to make a warm plucked bass in Serum 2, with a short bright attack, stable mono low end, and Tone, Decay, and Space macros. Deliver a native preset.

> Use $serum-reference-match to recreate the sound at 0:12-0:16 in this audio. Preserve its attack, vowel movement, and note-length behavior.

> Use $serum-preset-qa to check this Serum preset against the brief and fix its clicks without changing the main timbre.

These are future task examples. This documentation task does not generate/audition those example sounds.

## Skills

| Skill | Purpose |
|---|---|
| [serum-sound-design](../../skills/serum-sound-design/SKILL.md) | End-to-end brief, routing, design, build and evaluation |
| [serum-reference-match](../../skills/serum-reference-match/SKILL.md) | Analyze and recreate audio/preset references |
| [serum-synthesis](../../skills/serum-synthesis/SKILL.md) | Choose and construct source/filter/engine architecture |
| [serum-modulation](../../skills/serum-modulation/SKILL.md) | Articulation, movement, expression, macros, arp/clips |
| [serum-effects](../../skills/serum-effects/SKILL.md) | Character, dynamics, width/space, multibus processing |
| [serum-preset-build](../../skills/serum-preset-build/SKILL.md) | Schema translation, native files, resources and receipts |
| [serum-preset-qa](../../skills/serum-preset-qa/SKILL.md) | Structural/load/audio checks and corrective iteration |

## Handbook reading paths

For analog, vintage, retro analog, or real analog gear requests, the default reference is the detailed English [analog and retro guide](../../skills/serum-sound-design/references/analog-retro.md). It expands the supplied five-technique notes into architecture choices, VCO/DCO behavior, voice calibration, continuous drift, optional noise modulation, drive/recording paths, six recipe directions, native-tool limits, and targeted verification. A maintained instrument is the starting assumption; explicit user/reference choices take precedence. The seven skill entrypoints and workspace `AGENTS.md` route to this reference automatically for matching requests.

The complete [reference index](../../skills/serum-sound-design/references/index.md) links every chapter. Choose a path rather than loading the whole handbook every time.

| Task | Reading path |
|---|---|
| New sound from words | Brief -> Architecture -> relevant engine/family -> Modulation/Effects -> Native build -> Verification |
| Reference recreation | Reference matching -> selected source/engine -> controlled revisions -> Verification |
| Analog/retro analog or hardware character | Analog and retro -> target engine/family -> selected techniques -> calibrated native build -> analog test matrix |
| Understand a technique | Theory -> relevant engine -> Serum control map/source pages -> recipe experiment |
| Make a playable patch | Modulation/performance -> Arp/clips if needed -> macro endpoint tests |
| Generate a native file | Native build -> current tool schema -> capability gaps -> resource/readback checks |
| Fix a bad result | Troubleshooting -> isolated experiment -> new revision -> affected QA checks |

Useful direct references:

- [Theory and equations](../../skills/serum-sound-design/references/theory.md)
- [Wavetable and FM/AM](../../skills/serum-sound-design/references/wavetable-and-fm.md)
- [Samples and multisamples](../../skills/serum-sound-design/references/sample-engines.md)
- [Granular and spectral](../../skills/serum-sound-design/references/granular-and-spectral.md)
- [Filters and routing](../../skills/serum-sound-design/references/filters-and-routing.md)
- [Modulation and performance](../../skills/serum-sound-design/references/modulation-and-performance.md)
- [Effects](../../skills/serum-sound-design/references/effects.md)
- [Sound families and recipe index](../../skills/serum-sound-design/references/index.md)
- [Twelve worked experiments](../../skills/serum-sound-design/references/recipes.md)
- [Native build and schema units](../../skills/serum-sound-design/references/native-build.md)
- [Tool capability boundaries](../../skills/serum-sound-design/references/tool-capabilities.md)
- [Brief/spec/receipt templates](../../skills/serum-sound-design/references/templates.md)
- [Verification matrix](../../skills/serum-sound-design/references/verification.md)
- [Sources and page index](../../skills/serum-sound-design/references/sources.md)

## Source basis and limits

The supplied [Serum 2 User Guide](<_internal/sources/Serum 2 User Guide.pdf>) is 354 pages, version 2.0.18/manual 1.0.3. The supplied [Electronic Music and Sound Design Theory](<_internal/sources/Electronic_Music_and_Sound_Design_Theory.pdf>) is a **122-page demo excerpt**. The source index identifies actual excerpt coverage and omitted sections. Supplemental theory, descriptor interpretations, recipes, and workflows are authored guidance, clearly distinguished from source-supported control behavior.

The source texts were extracted for search; manual diagrams/control tables were also visually spot-checked. Originals, page-text extraction, tool/schema snapshots, scripts, hashes, and validation evidence are under [_internal/](./_internal/). The skills can be used without loading full PDF text.

## Installation and maintenance

Editable canonical copies live in `skills/`. Install all seven together; focused skills refer to the shared references in the sibling `serum-sound-design` folder. The installation script copies only this pack into the configured skill home (`CODEX_HOME/skills`, otherwise `~/.codex/skills`), checks name collisions, and records checksums. It refuses to replace a modified installed file. Run from this workspace:

```powershell
python docs/serum-sound-design/_internal/install_skills.py
```

After editing canonical files, run the pack check and then rerun installation:

```powershell
& integrations/serum-mcp/.venv/Scripts/python.exe docs/serum-sound-design/_internal/check_pack.py
python docs/serum-sound-design/_internal/install_skills.py
```

Skill metadata allows normal discovery; the pack introduces no separate approval policy. Install receipts identify the exact location. New sessions can discover installed skills; an existing session's skill catalog may need refresh/restart. Workspace [AGENTS.md](../../AGENTS.md) also points agents to the guide, so repository work can find the pack directly.

## Local production integration

Follow [Serum MCP](../serum-mcp.md), [project layout](../project-layout.md), and [Cubase studio](../cubase-studio.md). For music creation also read the local composition/workflow/timing guides. Sound-only requests remain sound-only. Composition work keeps one instrument per MIDI layer, matching Serum preset names and aligned MIDI timelines; drums retain the user's kit/sample choice.

The tool creates/edits native `.SerumPreset` files but does not render/load Serum. Each future sound delivery distinguishes structural validation, real plugin load, audio render/analysis, and actual listening. No audio match is inferred from a schema pass.

## This pack's verification

All seven skills passed the bundled skill validator. The 26-reference library passed local link, source-checksum, and documented semantic-spec checks. The installer passed fresh-install, repeat-install, and modified-file protection checks; installed files were checksum-verified. Canonical and installed copies are recorded in the internal receipts. These checks validate the documentation/package and selected implementation invariants; they do not establish end-to-end sound recreation quality. No presets or audio were produced or auditioned for this documentation task.
