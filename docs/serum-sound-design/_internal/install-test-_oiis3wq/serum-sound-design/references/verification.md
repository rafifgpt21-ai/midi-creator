# Verification and evaluation

## Evidence levels

| Level | Evidence | Does not prove |
|---|---|---|
| Design | Written architecture/spec and criteria | A native artifact exists |
| Semantic validation | Current schema accepts all intended fields | Correct native mapping or audio |
| Structural readback | Exact native file decodes, safe wire types, requested stored state/dependencies checked | Serum loads it or produces the intended sound |
| Plugin load | Exact native file loads in real Serum, resources/readouts inspected | Musical match across range/gestures |
| Render analysis | Audio generated under recorded conditions and measured | The agent listened or judged musical identity |
| Listening | Audio actually auditioned against specific criteria | Other untested registers/hosts/controllers work |

Report these independently. Past upstream evidence is not a test of this deliverable. File decoding and genuine plugin loading use different paths.

## Structural checklist

- Native extension and format are real; parser accepts the exact delivered file.
- Unsafe plainParams CBOR type scan passes where available.
- Every active source, engine, pitch, level, resource, filter, route, envelope, LFO, macro, FX rack, and note generator meets the spec or has an explained transformation/limitation.
- Defaults/omissions are interpreted correctly; zero, false, None, and absent are not conflated.
- All dependencies exist, packaged copies hash-match, and install paths are documented.
- Revisions preserve required unchanged state/resources and original files.
- Producer-facing links resolve; technical working artifacts are in `_internal/`.

If the requested graph or curve is missing from summary output, inspect the decoded payload rather than declaring success based on a partial description.

## Plugin checklist

Load the delivered preset path in the intended Serum version, inspect engine/routing/curve/FX/arp/global readouts, verify no missing-resource warnings, play a basic test note, then reload from saved native state. Document host/plugin version, actual file, and any screenshots/log/audio evidence. If a UI step is needed for unsupported parameters, save a new native revision and structurally verify that revision too.

## Musical test matrix

| Test | Detects |
|---|---|
| Lowest/middle/highest intended MIDI numbers | Tuning, brightness, aliasing, sample stretch, range failures |
| Quiet/medium/loud velocities | Dynamic response and unusable quiet notes/peaks |
| Short/held notes | Gate/envelope interactions and missing decay |
| Rapid repeats/same pitch | Phase variation, retrigger, stacking/stealing |
| Detached/overlapping notes and leaps | Mono/legato/glide rules |
| Chords and release overlap | Polyphony, unison/FX headroom, voice stealing |
| Macro min/default/max plus interacting extremes | Range/clamping, unsafe feedback, pitch/color discontinuity |
| Wheel/pressure/bend/MPE actually supplied | Real expression response and host mapping |
| Tempo changes/transport starts when synced | Correct period/division, phase/retrigger, arp/clip behavior |
| FX bypass and routing isolation | Source identity and unintended parallel paths |
| Stereo/mono/channel balance | Cancellation, low-band stability, asymmetric resources |
| Long hold and silence after note-off | Loop seam, drones, release, delay/reverb feedback/tail |

Scale tests to the request: one-shot percussion does not need chord play unless intended; drone/ambient patches need extended holds; a mono bass needs overlap/glide tests. In this workspace a generated MIDI test phrase uses the local timing/schema conventions and one-track layer format.

## Audio measurements

Use peak/RMS/loudness checks for gain and overload; pitch tracking for tonal tuning; onsets/autocorrelation for rhythmic motion; spectra/spectrograms for envelope/partial behavior; stereo correlation/band comparison for compatibility. Record render tempo, sample rate, MIDI, velocities, gate lengths, macro states, plugin quality, and reference gain. A measurement can be wrong outside its assumptions (fast rate alias, polyphonic pitch, masked attack).

## Iteration and stopping

Identify the largest unmet sonic criterion, isolate likely causes, predict the change, make a new revision, and retest affected criteria. Preserve a known good revision and a concise mismatch log. Stop when criteria pass; when a required live capability/resource is absent, complete offline checks and mark the precise untested/unimplemented part. Avoid publishing a failed structural preset as ready to load.
