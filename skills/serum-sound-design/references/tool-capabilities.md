# Tool capabilities and boundaries

Snapshot: local `serum-mcp` commit `7299f2eea1acd2ae5a863965f5bd4beedf107ee8`, inspected 2026-10-12. The supplied manual describes Serum 2.0.18 (manual 1.0.3); upstream format notes are reverse-engineered and include observations of other plugin versions. Refresh runtime schema before every build. Neither an enum in a file nor structural success guarantees plugin compatibility.

| Feature | Current exposed path | Boundary/required evidence |
|---|---|---|
| A/B/C harmonic tones | Wavetable choice, frame, warp, unison, pitch/level | Friendly vocabulary is a subset of UI |
| Custom additive table | `custom_harmonics` frames | Harmonic amplitude synthesis, not arbitrary independently timed partials |
| Audio-to-table | `sample_source`, `sample_frames` | 2048-sample slicing; not faithful original playback or full UI import |
| Sample playback | `sample_playback_source`, loop controls | WAV; resampling pitch/time coupling, source/root behavior must be checked |
| Granular | `granular_source`, length/density/random controls | Several flags uncertain; full scan/window/density-mode UI not all exposed |
| Spectral | `spectral_source`, band/warp/shift/wet fields | New drawn spectral filter curves absent; generated curve is neutral |
| Multisample | Curated `multisample_source` identifiers | Not a general user key/velocity-zone editor |
| Noise/Sub | Curated source names/shapes | Manual has more source behaviors/shapes than friendly schema |
| Source phase/randomness | Raw introspection; verified reference/UI | No general friendly phase/random fields in inspected OscillatorSpec |
| FM/AM source selection | Warp enum plus existing/template/UI data | Generic `fm` does not express every UI source selector |
| Two voice filters/routing | Filters, input/output routes, bus sends | Some balance/unit semantics uncertain; graph must be verified |
| Envelopes | Four semantic envelopes and curve parameters | Curve stage mapping partially inferred |
| LFO graph | Explicit points or named algorithmic shape | Curve/rate/trigger details require care; not every UI option exposed |
| Macro/mod matrix | Routes, polarity, aux source, named macro/value | Arbitrary custom matrix remap curves not exposed as general friendly fields |
| FX racks | `fx_chain` units with `rack`, typed params | Module schema differs; `flex` is opaque copied data, not proven authoring semantics |
| Splitter nested branches | Preserve verified graph/UI | Flat module insertion does not construct all child processing paths |
| Convolve IR | Preserve/reference/UI with resource resolution | Semantic FX params alone do not supply arbitrary IR payload/path construction |
| Arp/pattern | Algorithmic and custom `arp` | Discrete rates, uncertain clock fields; live timing proof needed |
| Clip bank | Existing template/UI | No general clip-bank field in inspected PresetSpec |
| MPE | Expression mod sources, template/UI global state | Sources alone do not enable MPE or configure host/channel/pitch ranges |
| Quality/tuning/global scaling | Some GlobalSpec/VoiceUnisonSpec fields | Some confidence uncertain; custom tuning file setup may need UI/host |
| Native writing/readback | Generate/edit/describe + parser/checker | Reverse-engineered format, not official Xfer API |
| Audio rendering or listening | Separate actual plugin/host/audio tools | Not provided by `serum-mcp` generation tools |
| Cubase/session/MIDI | Separate midi-studio/local workflow | Call studio status first for live studio tools |

## Resolve a missing capability

1. Confirm it is absent from current schema/tool implementation, rather than merely absent from this cached map.
2. Try a verified existing preset/template that contains the data and preserves it during a focused edit.
3. If UI/live control is available and authorized for the sound request, use exact manual controls and save a native revision.
4. If neither can implement the required behavior, deliver the available candidate/spec with the exact unmet requirement. Use an equivalent only when it is acceptable to the user's sonic goal.

Record field confidence as **confirmed**, **observed**, or **uncertain** from upstream, separately from the current run's evidence. Upstream's past listening observations are not evidence that this run's preset was heard. Raw unknown enums or payload blobs must be sourced from actual supported state rather than guessed.
