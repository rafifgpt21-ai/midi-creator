# Working templates

Use these compact formats when they help reproducibility. Sound design intent and native tool JSON are separate documents. Fill real values or state unknown/untested; do not pass design prose keys into the tool schema.

## Brief/design

```yaml
request: "User's exact sound request"
role: bass | lead | pluck | pad | keys | percussion | texture | sfx
reference: {path: null, sha256: null, interval_seconds: null}
tempo_bpm: null
register_midi: [36, 60]
note_behavior: "Short notes plus sustained notes; mono/legato choice"
target:
  attack: "Observable behavior"
  body: "Pitch and spectrum"
  motion: "Rate, shape, depth, trigger"
  tail: "Release and processor decay"
  stereo: "Center/width/mono expectations"
components:
  - slot: A
    function: "Pitched body"
    engine: wavetable
    source: "Verified table/frame or custom table"
    path: "A -> Filter 1 -> Main -> output"
routes:
  - intent: "Brightness decays faster than amplitude"
    source: env1
    destination: filter0.cutoff
    implementation: "Exact amount and unit after schema inspection"
macros:
  - name: Tone
    default: "Value and unit"
    endpoints: "Dark body to bright body, gain compensated if needed"
required_resources: []
capability_gaps: []
assumptions: []
acceptance_checks: []
```

The role vocabulary is design metadata, not a tool restriction. MIDI range and tempo should reflect the actual brief rather than remain copied defaults.

## Minimal semantic spec example

This authored pure-tone prototype is compatible with the inspected semantic schema. It uses a custom harmonic frame (therefore creates an external table dependency), not a hypothetical Sub sine enum. It is a schema/build example, not an auditioned final sound.

```json
{
  "name": "Pure Body v001",
  "description": "Single harmonic body; no effects; offline example",
  "oscillators": [
    {"enabled": true, "custom_harmonics": [[1.0]], "unison": 1.0, "volume": 0.6},
    {"enabled": false},
    {"enabled": false},
    {"enabled": false},
    {"enabled": false}
  ],
  "envelopes": [{"attack": 0.004, "decay": 0.25, "sustain": 0.9, "release": 0.06}],
  "global": {"master_volume": 0.45, "mono": true},
  "arp": {"enabled": false}
}
```

A useful named macro has both a `macros` entry and `mod_routes`; add them after checking desired endpoint scaling. A triangle LFO in the inspected natural coordinate convention can use `curve=[{"x":0,"y":0},{"x":0.5,"y":1},{"x":1,"y":0}]`; set `mode`, `beat_sync`, and `rate` explicitly according to intended behavior. Triangle is not a sine, and a piecewise approximation should be described accurately.

For a literal 250 ms delay the inspected implementation requires `params={"kParamTimeL":0.25,"kParamTimeR":0.25,"kParamBeatSync":false}` with a supported `FXDelay` unit. The absent beat-sync state otherwise defaults to synchronized behavior. Refresh keys and defaults before use.

## Readback comparison

| Requested path | Requested value/unit | Actual stored/effective value | Tolerance/transformation | Result |
|---|---|---|---|---|
| `envelopes[0].attack` | seconds | readback | serialization/calibration tolerance | pass/fail |
| source engine | desired engine | payload/UI | exact identity | pass/fail |
| FM source | desired connection | native graph/UI | exact source | pass/fail/untested |
| LFO timing | desired period/division | UI/onsets | task-specific | pass/fail/untested |

Include every requested field; a small illustrative table does not substitute for complete comparison.

## Verification receipt

```json
{
  "revision": "v001",
  "implementation_commit": "actual commit",
  "schema_captured_at": "ISO date/time",
  "preset": {"path": "actual path", "sha256": "actual hash"},
  "resources": [
    {"path": "actual resource", "sha256": "actual hash", "install_destination": "documented destination", "factory": false}
  ],
  "structural": {"status": "pass|fail|untested", "evidence": []},
  "plugin_load": {"status": "pass|fail|untested", "plugin_version": null, "host": null, "evidence": []},
  "render": {"status": "pass|fail|untested", "path": null, "conditions": null},
  "listening": {"status": "pass|fail|untested", "checks": [], "notes": []},
  "unresolved_requirements": []
}
```

Receipt placeholder strings must be replaced before delivery. A spec that was only validated has `structural` untested for the absent native file.

## Producer README content

Explain what the sound does, preset filename/link, how to install required resources and load through Serum's preset browser, MIDI-number register and tempo dependencies, intended note lengths/voicing, useful macros with defaults and endpoints, expression mappings, variants, and verification status. Link actual delivered files. Include a focused audition checklist when live testing remains unperformed. For a composition use the workspace's project README template and MIDI-preset pair table.

## Revision log

`origin revision | requested preserved properties | changed components/fields | reason | comparison evidence | unresolved items`

Store with request/spec in `_internal/`; keep previous native artifacts intact. Source design and exact tool spec jointly explain intent and implementation, while `composition.json` remains the source of truth for notes/timing when composing.
