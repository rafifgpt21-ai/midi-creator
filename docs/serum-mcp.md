# Native Serum presets with serum-mcp

Native Serum 2 presets are created with [Celian-mrc/serum-mcp](https://github.com/Celian-mrc/serum-mcp).
The local checkout is in `integrations/serum-mcp`; its pinned commit is recorded in
[`serum-mcp-source.json`](../integrations/serum-mcp-source.json). The upstream
environment is separate from MIDI Creator's environment. Dependencies were installed
from the upstream `uv.lock` using Python 3.13.3, already available on this computer.

The `serum-mcp` server is registered in the global Codex configuration. Restart the
Codex/T3 Code connection to make new tools available in the next session. Configuration
points to the original `Documents/Xfer/Serum 2 Presets` folder in OneDrive:
`SERUM_PRESETS_PATH` targets `Presets/User`, `SERUM_TABLES_PATH` targets `Tables`,
and `SERUM_SAMPLES_PATH` targets `Samples`. `SAMPLE_BANK_PATH` targets the user's
sample bank. A configuration copy for other MCP clients is in `integrations/mcp.local.json`.

## Preset workflow

1. Call `list_parameters()` before designing a preset to confirm field names, enums,
   ranges, units, and parameter confidence.
2. Use `find_reference_presets(query)` and `describe_preset(path)` for genre,
   character, or specific-preset references. Search uses names/folders; a search result
   does not establish sound quality.
3. Store the brief and `preset-spec.json` in the new revision's `_internal/`.
   Specify oscillators, filters, envelopes, LFOs, `fx_chain`, macros, and
   `mod_routes` according to their sonic functions. Use musically useful macros and modulation.
4. Call `generate_preset(spec, subfolder)` in a new subfolder of `Presets/User`.
   The upstream tool can overwrite an existing name; check the destination first.
   Revisions use new names/folders and preserve earlier presets. Before `edit_preset`,
   create a revision copy.
5. Call `describe_preset` on the result; decode it and compare the requested parameters.
   Store the ready preset in `Presets/`, and specifications, upstream commit,
   checksums, and receipts in `_internal/`. Complete the revision README with
   track/preset mappings, macros, loading instructions, and accurate test statuses.
6. Open the result through Serum 2's preset browser to check compatibility and sound.
   Structural verification does not establish successful plugin loading or actual
   listening; record each status separately.

`serum-mcp` writes `.SerumPreset` files directly and does not load the plugin,
render audio, or control Cubase. The existing MIDI/live Cubase workflow continues to
use `midi-studio`. MIDI Creator's offline host currently accepts `.vstpreset`;
to render a native result through that host, open it in Serum/Cubase and save it as
a VST preset. Do not convert by renaming the file extension.

Additional wavetables/samples created by upstream must be included when sharing
presets. Factory wavetables still depend on the installed Serum library.
The user's original sample bank remains a read-only source.

## Repeatable checks

The [`check_serum_mcp.py`](../integrations/check_serum_mcp.py) script opens a real
MCP stdio connection, retrieves the schema and references, and optionally creates a
preset and compares structural readback. Output and preset destinations must be new.

```powershell
& integrations/serum-mcp/.venv/Scripts/python.exe integrations/check_serum_mcp.py --out integrations/serum-mcp-check-new
& integrations/serum-mcp/.venv/Scripts/python.exe integrations/check_serum_mcp.py --spec projects/20261011-serum-mcp-demo/v002/_internal/preset-spec.json --subfolder 'MIDI Creator/20261011-serum-mcp-demo/v003' --out projects/20261011-serum-mcp-demo/_internal/check-v003
```

To reinstall, clone the URL in the source receipt into `integrations/serum-mcp`,
check out the recorded commit, and run
`uv sync --locked --no-dev --python C:/Python313/python.exe` in that repository.
The upstream checkout is ignored by `.gitignore`; generated presets, specifications,
guides, and receipts remain workspace artifacts.
