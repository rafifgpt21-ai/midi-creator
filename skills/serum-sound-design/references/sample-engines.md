# Samples and multisamples

Manual: multisample S2 pp. 58-67; sampler pp. 68-84; Noise pp. 128-132; content embedding pp. 21-22, 302-303. Tool semantics are derived from inspected `generation/spec.py`, not from the manual's UI unit labels.

## Preserve or transform the recording

Choose `sample_playback_source` to retain a recognizable one-shot, attack, voice, or foley recording. Choose `sample_source` only when making a wavetable texture from slices is intended. Choose granular/spectral engines for the distinct transformations in [granular and spectral](granular-and-spectral.md). One source engine per A/B/C slot prevents precedence from silently selecting the wrong engine.

## Recorded-source preparation

Record path, format, sample rate/channels, duration, pitch/root estimate, transient/loop locations, permission context, and desired edits. Analyze with `analyze_sample_file` when useful; estimates of noisy/inharmonic/polyphonic material are not exact root notes. Source audio remains intact; derived conversions/crops belong in the revision's `_internal/` or resource package.

For a pitched recording, align layers by measured pitch, not filename or host octave label. The local schema describes the sample engine's reference as C5, with pitch and playback duration coupled. Verify actual MIDI-number reference in the installed Serum version before calculating transposition. If source frequency is `fsrc` and desired sounding reference is `ftarget`, correction is `12*log2(ftarget/fsrc)` semitones. High/low notes alter length in resampling, including the initial attack even when a loop sustains the tail.

## Sampler controls

- **Start/end:** isolate the intended event; abrupt cuts can click. Preserve the defining attack unless the brief calls for its removal.
- **Loop region:** choose a stable sustain portion, excluding an attack or unwanted silence. Forward, ping-pong, and tailed modes have different transitions.
- **Crossfade:** reduce seam discontinuities, balancing smoothness against transient blur and periodic cancellation.
- **Scan/playback:** UI scan/tempo modes have specific speed, stretch, and key-tracking behavior; do not infer their units from a generic sampler.
- **Slicing:** maps events into playable segments (S2 pp. 74-76). A WAV path alone does not encode a slice map; record actual slice settings and MIDI behavior when using the UI.
- **Warp and voicing:** processing can change the recording strongly. Establish identity before transforming it; recheck loop pitch and tails afterward.

Current semantic sample loop positions/crossfade are percentages, while other audio tools may use samples/seconds. Convert deliberately and verify readback plus audible seam behavior. `sample_center_pan=True` gain-balances channels before copying in this implementation; set false if preserving the recorded channel relationship is required. This transformation needs disclosure in the resource receipt.

## Multisample design

Select an actually installed factory multisample or a confirmed supported instrument identifier. Layer the oscillator-level envelope with the main voice envelope deliberately; the source's recorded decay/articulation still matters. Use velocity tracking and timbre/random controls where the chosen path supports them. Compare across key zones to detect abrupt tonal transitions and overly stretched recordings.

The current tool exposes a curated instrument list, not a general multisample-zone editor. It cannot be assumed to build arbitrary user multisample mappings, round robins, articulations, or velocity layers. For those requests, use the verified UI/import capability if available or state the exact gap. Factory resources are installation dependencies, not files the agent may silently replace.

## Noise as a sampled layer

Serum's Noise oscillator can load recordings as well as noise presets. One-shot/loop, start, randomization, pitch/key tracking, pan, and level determine whether it is an attack layer, pitched sample component, or continuous noise (S2 pp. 128-132). The tool's curated noise names cover less than this UI. Verify all required one-shot/keytracking controls before claiming a faithful noise-slot sample instrument.

## Delivery

For each resource list source, derived file, SHA-256, engine/slot, embed versus external state, factory versus custom status, and target installation path. In the UI, saving with embedding can improve portability; confirm what was embedded by reload/inspection. Tool-generated external files must travel with the preset. Merely copying the `.SerumPreset` is insufficient when it references external content.
