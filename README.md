# MIDI Creator

Ask the agent for a song, open the project README, and drag the MIDI into Cubase. Defaults: a complete arrangement from beginning to end, **Serum 2** for every melodic instrument, and your chosen drum kit/samples. Each instrument has **one MIDI file with exactly one track**, aligned from bar 1 through the song's end.

## Ready-to-use projects

| Project | Tempo / key / length | Start here |
| --- | --- | --- |
| Afterglow Circuit — Progressive House | 126 BPM · F minor · 160 bars · 12 tracks | [README](projects/20261009-afterglow-circuit-progressive-house/v002/README.md) |
| Neon Step — New Jack Swing | 108 BPM · F# minor · 96 bars · 15 tracks | [README](projects/20261009-neon-step-new-jack-swing/v004/README.md) |
| Serum Synthwave Starter | 110 BPM · A minor · 16 bars · 10 tracks | [README](projects/20261010-synthwave-studio-starter/v002/README.md) |
| Neon di Ujung Malam — dark synth-pop | 118 BPM · F# minor · 112 bars · 8 tracks | [README](projects/20261011-neon-di-ujung-malam/v003/README.md) |
| Warm Motion — Serum MCP preset test | Native pad with chorus/reverb and 4 macros | [README](projects/20261011-serum-mcp-demo/v002/README.md) |

Latest timing revisions: Neon Step v004 preserves 11 core layers and aligns four supporting layers to a 60:40 groove; Neon di Ujung Malam v002 removes jitter and arp offsets. New export checks reject off-grid onsets not explicitly declared intentional. See the [diagnostic report](docs/timing-repair-20261011.md).

Previous versions remain intact in each project's `_internal/previous-revisions/`. Three compositions were re-exported without changing notes, timing, velocity, volume/pan, or song length. The starter includes six existing VST3 presets and stems; the Serum MCP demo includes a native `.SerumPreset`.

## Requesting a song

> Create a 3-minute synthwave song with a warm nighttime mood at 110 BPM. Use a thick bass, wide chords, a light arp, and a memorable lead.

You can specify genre, mood, tempo, key, length, or particular sounds. The agent chooses unspecified details and explains them in the README. Explicit requests for one melody, an excerpt, or instruments outside Serum still take precedence. Combined files are created only when requested.

Every project includes import guidance, a MIDI/preset table, song form, drum-character suggestions and pitch mapping, and external-instrument instructions when needed. Native Serum presets are created through [serum-mcp](https://github.com/Celian-mrc/serum-mcp).

## Producer-facing folders

```text
projects/project-name/
  README.md          link to the latest revision
  v002/
    README.md        song details and instructions
    MIDI/            drag these files into Cubase from bar 1
    Presets/         when available
    Audio/           when requested/included
    Drums/           when the kit/samples have been selected
    _internal/       technical data; not needed for import
  _internal/         previous revision archives
```

## Cubase import

New MIDI uses **SMF format 1 with one track**, without SysEx, Program Change, or extra text/key/marker metadata. Tempo, meter, notes, velocity, volume/pan, and global length are retained. The README contains the key and song sections.

For locators, time base, and tempo, follow the [import timing guide](docs/cubase-studio.md#timing-saat-impor-cubase).

In **Preferences > MIDI > MIDI File**, enable **Import Dropped File as Single Part**. For older format 0 MIDI, disable **Auto Dissolve Format 0**. The [official Cubase guide](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html) explains both options. Select the Serum preset before importing MIDI.

Older files contain no SysEx messages. The “SysEx Data” track shown in a screenshot has not been automatically reproduced in Cubase; the new format mitigates import issues, and live drag-and-drop behavior still needs checking in your Cubase installation.

## Agents and development

The [Serum 2 sound-design guide and seven agent skills](docs/serum-sound-design/README.md) cover theory, five engines, modulation, FX, sound families, reference reconstruction, native presets, and verification. Start with `$serum-sound-design` for a complete sound request.

The [detailed Serum 2 analog and retro guide](skills/serum-sound-design/references/analog-retro.md) is the default for analog/vintage/retro analog sounds and approaches to real analog gear. It distinguishes VCO/DCO behavior, voice variation and drift, five analog-character techniques, instrument recipes, and verification.

[AGENTS.md](AGENTS.md) defines defaults and delivery criteria. [Project layout](docs/project-layout.md), the [composition contract](docs/composition-guide.md), [Serum MCP](docs/serum-mcp.md), and [Cubase/live studio](docs/cubase-studio.md) explain technical workflows. Root-level code/dependencies/integrations form the framework; producers can work from `projects/`.

```powershell
uv sync --locked
uv run midi-creator --help
uv run midi-creator validate examples/multi-layer/composition.json
uv run midi-creator generate examples/multi-layer/composition.json --out projects/demo-output
uv run midi-creator verify projects/demo-output
uv run python -m unittest discover -s tests -v
```

Exports use a new folder containing `MIDI/*.mid`, `README.md`, and all snapshots/manifests/validation under `_internal/`. `--combined` adds `MIDI/arrangement.mid` when requested. Verification of older exports remains supported. Grid/swing policy is in the [timing contract](docs/composition-guide.md#pemeriksaan-grid-onset). Restart the Codex/T3 Code connection after framework changes so the MCP server loads the latest implementation.
