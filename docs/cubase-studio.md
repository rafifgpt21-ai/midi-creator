# Cubase + Serum studio

This workspace now prepares MIDI performances, real Serum VST3 presets, a copied drum kit, and aligned audio stems. A local MCP server exposes the same operations to agents. The MIDI Remote driver adds a separate route for live Cubase control.

The installed setup targets Cubase 15.0.20, Serum 2.0.23, and the existing LoopBe Internal MIDI ports. Your sample bank is read-only. Personal paths and explicit drum mappings live in `studio.local.json`; dependencies are pinned in `uv.lock`.

## Open the ready-made starter

Open [the starter guide](../projects/20261010-synthwave-studio-starter/v002/README.md). It links every MIDI, preset, and audio stem. Original v001 assets and receipts are archived intact under the project's `_internal/previous-revisions/v001/studio/`.

- 110 BPM, A minor, 4/4, 16 bars, 480 PPQN.
- Serum bass, lead, arpeggio pluck, pad, synth brass, and sine-based keys.
- Separate kick, snare, closed hat, and open hat from your bank.
- Every MIDI has one track and retains its leading silence. All ten stems are stereo, 48 kHz, and 1,675,638 frames long.

Create a separate Cubase project at 48 kHz and 110 BPM. Browse the bundle's `presets` folder in MediaBay and create an instrument track from each `.vstpreset`. Import the corresponding MIDI onto it at bar 1. The preset contains actual Serum state, not a General MIDI sound selection. Keep the intended preset when Cubase offers to interpret a MIDI program change.

For drums, import the four audio stems at bar 1, or load the copied one-shots into Groove Agent SE using `drum-kit.json`: kick 36, snare 38, closed hat 42, open hat 46. `samples/kit.sfz` is an alternative for an SFZ-compatible sampler; Groove Agent does not use that SFZ file. Choose either MIDI playback or the matching audio stem for each part.

The separate drum MIDIs contain independent CC7 volume and CC10 pan settings. Use separate sampler instrument tracks to retain those settings, or filter those two controllers when routing all four parts into one shared kit and set gain/pan per pad there. Their shared MIDI channel 10 cannot carry four independent kit-wide mixer settings at once.

Save the resulting project as a new `.cpr`, then use **File > Save as Template** if you want this instrumentation available whenever you start a song. This first import is manual. The framework does not fabricate Cubase's proprietary project format or report a native project as created before Cubase saves it.

These are dry foundation patches. Add chorus to the pad/brass, tempo delay to the lead/pluck, and a shared reverb to taste. Internal effects routing, modulation-matrix assignments, and macro mappings are not part of these recipes. Their state was saved, reopened in your installed Serum, and rendered; the audio has not been listened to. `.vstpreset` is the host's VST3 format, not Serum's native `.SerumPreset` format.


## Timing saat impor Cubase

Atur tempo/meter project sesuai README dan instrument track pada **Musical Time Base** (ikon not). Untuk posisi deterministik gunakan **File > Import > MIDI File**, left locator **1.1.1.0**, dan **Import to Left Locator**. Pada project bertempo tetap yang sudah disetel sesuai lagu, **Ignore Master Track Events on Merge** mempertahankan tempo project. Untuk drop, **Import Dropped File as Single Part** menjaga file sebagai satu part; tempatkan semua part pada bar 1 dan pertahankan keheningan awal. Periksa start part melalui Info Line dan onset dalam Key Editor Bars+Beats. Snap menentukan posisi part, bukan mengkuantisasi isi nada. Hindari menggeser nada pertama dari layer yang masuk belakangan ke bar 1.

Grid straight dan swing harus mengikuti kebijakan README lagu. Mengkuantisasi seluruh New Jack Swing ke grid straight mengubah groove yang disengaja. Jika file asli sudah pada grid tetapi hasil impor berbeda, diperlukan posisi part/nada yang tersimpan di Cubase untuk membedakan offset impor dari ritme komposisi; pemeriksaan offline tidak membuktikan hasil drop live.

[Opsi impor resmi](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/preferences/preferences_midi_midi_file_import_options_r.html?contentId=u1NHlJBAfqTrfj0eW_QNMQ) menjelaskan locator, single part dan master events. [Time base track](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/track_handling/track_handling_defining_the_track_time_base_t.html) menjelaskan musical/linear.

## Enable live Cubase control once

The shortest route is **Studio > MIDI Remote Manager**. Click **Reload Scripts**, open the **Scripts** tab, and search for **Studio Bridge** (vendor **MIDI Creator**). If disabled, select it and use **Enable Controller Script**. This checks installation without finding the lower-zone tab first. The controller should auto-detect the LoopBe port pair; the **MIDI Controllers** tab shows its status and port assignments. For loading errors, use the Script Console below.

The driver was installed at:

```text
Documents/Steinberg/Cubase/MIDI Remote/Driver Scripts/Local/
  MIDI Creator/Studio Bridge/MIDI Creator_Studio Bridge.js
```

Windows may redirect Documents into OneDrive; the installer resolves the actual location.

1. Open the **MIDI Remote** tab in the lower zone of the Project window. Right-click its info line (the thin toolbar above the controller surface), enable **Scripting Tools**, open **MIDI Remote Script Console**, and click **Reload Scripts** there. The console's **Error Messages** tab shows script-loading failures.
2. Activate the **MIDI Creator / Studio Bridge** surface and its **Studio** page. If needed, choose LoopBe Internal MIDI as both input and output.
3. In Studio Setup's MIDI port settings, exclude LoopBe from **All MIDI Inputs**. Keep musical tracks' outputs on their instruments, not on LoopBe. This bus carries control messages only.
4. Run `uv run midi-studio doctor --live`, or ask the agent to call `cubase_status`. A real response is required before attempting live edits.

The desktop-control helper in this session could not load (`@oai/sky` was unavailable), so activation was left to the user. After opening the project and selecting **Serum 2 01**, the live bridge discovered Serum's 2,623 parameters. A reversible Main Vol change from 50% to 49%, followed by restoration to 50%, passed exact readback checks. The instrument slot's eligible-plugin list included Serum's installed class UID. The [live receipt](../integrations/cubase-live-20261010-072500.json) records the results. Assigning a plugin to a new slot remains untested; no native `.cpr` was created. Earlier no-target checks and simulated-host tests are preserved as separate evidence.

Once connected, the bridge can report transport and up to sixteen instrument tracks, select a track, discover objects on the selected track, inspect parameters, and write normalized parameters with readback. Cubase MIDI Remote API 1.3 exposes optional plugin-slot assignment: discover the slot, list its eligible plugins, and assign the configured Serum class UID. Capability detection must confirm that API before use. Existing occupied slots require an explicit replacement choice. Preset loading, MIDI import, note editing, track creation, and `.cpr` creation are not provided by this bridge.

Object discoveries produce tokens that expire after 30 seconds. A track switch, plugin replacement, or object removal invalidates the token. Discover again before writing. A command acknowledgment means dispatch, not a proven result: verify transport state or the saved file separately. If a mutation times out, inspect Cubase before repeating it.

## MCP connection

The `midi-studio` stdio server is registered in your global Codex configuration with a 30-second startup timeout and a 240-second tool timeout. Its launch command uses this workspace's Python environment, workspace working directory, and an absolute configuration path. T3 Code loaded all twenty tools during this session; its status and bundle verification calls succeeded. Registration was confirmed with `codex mcp get midi-studio --json`. An independent real MCP client also loaded your installed Serum successfully and verified the bundle. If tools are absent in a future session, restart the Codex connection to load the configuration.

Restart the current Codex connection once after setup to load the final worker fix. The server that was already running before that fix retains its old Python imports until restarted.

For another MCP client, merge the `mcpServers.midi-studio` entry from `integrations/mcp.local.json` into its configuration and allow at least 240 seconds for sound preparation. No HTTP server or API key is required. The tools run locally and use your installed, authorized Serum plugin.

| Tool group | Operations |
| --- | --- |
| Performance | Schema, validate, generate per-layer MIDI, verify |
| Serum | Inspect actual parameters, find presets, create and reload VST3 presets |
| Drums | Search filenames, configure roots and explicit pitch mappings |
| Session | Prepare the complete bundle, verify checksums/MIDI/audio alignment |
| Cubase | Status, object discovery, parameter read/write, slot plugins, Serum assignment, track selection, transport/save commands |

There are 20 tools. Start with `studio_status`; request its live check only when using Cubase. Assets written by tools stay inside the configured workspace, including symlink resolution. Sample reads are limited to configured roots. Outputs use new folders and preserve earlier revisions. Serum loads in an isolated subprocess with a 180-second limit, so a plugin crash does not run inside your Cubase process.

## Agent workflow for the next song

For native Serum 2 `.SerumPreset` generation and editing, use the separately installed
[`serum-mcp` workflow](serum-mcp.md). It provides native oscillator/filter/envelope/LFO,
effects, macro, and modulation-matrix file generation. Native preset checks and loading
in the real plugin are separate from the existing `.vstpreset` offline-host workflow.

Follow `AGENTS.md` and the existing composition guide. Store the brief, decisions, `composition.json`, and reproducible generation script in a new dated project revision. Do not add plugin-specific fields to the composition schema. Instrument choices live in a separate binding map:

```json
{"bass": "bass", "lead": "lead", "arp": "pluck", "pad": "pad", "brass": "brass", "keys": "keys"}
```

A binding can alternatively reference a `.vstpreset` inside the workspace. Missing bindings are inferred from layer roles. Existing native Serum presets are searchable, but the offline loader accepts only `.vstpreset`; load a native preset through Serum/Cubase and save its VST preset before reusing it offline. A base preset used by `create_serum_preset` also receives the chosen profile's controls, followed by explicit overrides.

Map every used drum pitch to an approved one-shot before preparing a session. Filename discovery is a heuristic and does not establish sample quality. Configure `drum_roots` and `drum_samples` through the CLI/MCP instead of silently substituting a kit. Renders apply MIDI layer volume/pan after synthesis. All stems retain the global start/end; leave space for release tails in the specification.

```powershell
uv sync --locked
uv run midi-studio doctor
uv run midi-studio prepare projects/NEW/_internal/source/composition.json --bindings projects/NEW/_internal/source/bindings.json --out projects/NEW/v001
uv run midi-studio verify projects/NEW/v001
uv run python -m unittest discover -s tests -v
```

Use `--no-audio` to prepare only MIDI, presets, and kit assets. Bundle publication happens only after its checks pass. Audio rendering is separate from listening and musical evaluation. Do not claim the complete session was created inside Cubase without checking the native project there.

New studio bundles use `README.md`, `MIDI/`, `Presets/`, `Audio/`, and `Drums/`.
All manifests, snapshots, kit maps, and worker receipts live under `_internal/`.
Complete the README with the brief's drum character and sound decisions. Per-layer
MIDI has one format-1 track with minimal metadata and no Program Change. Old
version-1 studio bundles and their `performance/` exports remain verifiable.
For MIDI-only work, leave sample choice to the user and deliver the drum performance
plus README guidance; studio rendering requires an explicit approved kit mapping.

## Implementation and sources

`studio.config` owns settings and paths, `session` owns verified bundle publication, `serum` isolates the plugin worker, and `drums` owns sample discovery/rendering. CLI and MCP both call those services. `bridge` and `protocol` own bounded MIDI requests; `cubase_remote.js` handles them in Cubase. Request/response direction bytes prevent a reply on the shared bus from becoming a command. No automatic mutation retry is implemented.

The MIDI schema now includes an optional timing policy; new validation/export checks onset grids, while legacy verification reports timing separately. See [composition timing](composition-guide.md#pemeriksaan-grid-onset). Tests cover late entries, consistent frame counts, sample velocity, path boundaries, tampered assets, actual stdio tool calls, and remote stale-object/invalid-batch behavior. The remote host simulation remains distinct from live Cubase validation.

For the opt-in real Serum regression test, set `MIDI_STUDIO_TEST_CONFIG` to the absolute `studio.local.json` path before running the test suite. It checks plugin inspection and real preset save/reload through MCP under a 60-second deadline per call. The worker's standard input is isolated from JSON-RPC; inheriting that pipe stalled Windows child startup in the original test. `integrations/check_mcp.py --bundle <workspace-bundle> --out <new-receipt.json>` performs a separate real MCP check and can add `--live` for Cubase.

`uv run python integrations/check_cubase.py` reads the selected live Serum instance and writes a new timestamped receipt. Add `--test-write` for the reversible one-percentage-point volume change and restoration; it requires playback and recording to be stopped. This tests live control independently of offline audio generation.

- [Steinberg MIDI Remote API](https://steinbergmedia.github.io/midiremote_api_doc/codedoc_api_reference/) and [API 1.3 additions](https://steinbergmedia.github.io/midiremote_api_doc/new_in_v1.3/) describe DirectAccess and plugin-slot operations.
- [Steinberg instrument track presets](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/track_handling/track_handling_instrument_track_presets_c.html) describes creating instrument tracks from VST presets.
- [Steinberg Script Console](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/midi_remote/midi_remote_script_console_r.html) locates the scripting controls; [MIDI input setup](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/setting_up/setting_up_midi_inputs_setting_up_t.html) explains excluding remote ports.
- [MIDI Remote Manager](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/midi_remote/midi_remote_device_manager_r.html) is accessible from the Studio menu; its [Scripts tab](https://www.steinberg.help/r/cubase-pro/15.0/en/cubase_nuendo/topics/midi_remote/midi_remote_manager_scripts_tab_r.html) enables installed scripts.
- [Pedalboard API](https://spotify.github.io/pedalboard/reference/pedalboard.html) documents instrument hosting and VST3 preset state.
- [Official OpenAI MCP documentation](https://learn.chatgpt.com/docs/extend/mcp) describes Codex registration and timeout configuration.
