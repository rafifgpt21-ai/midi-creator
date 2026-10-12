# Wavetable, additive tables, and oscillator modulation

Source controls: S2 pp. 37-57; editor/import/formulas pp. 274-311. Theory: T PDF pp. 73-77, 81-84. Recipes/ranges here are authored starting points.

## Wavetable workflow

1. Choose the simplest spectrum consistent with the brief. Read actual frame content; a factory table name is not a waveform guarantee.
2. Set table position and audition static frames. Identify whether body, transient, and motion use different parts of the table. A frame scan can change amplitude as well as spectrum.
3. Set phase, random phase, and phase memory according to repeatability. Fixed phase helps consistent bass/transients; randomness can reduce mechanical repetition but can also destabilize layered low-end peaks (S2 pp. 41-44).
4. Add unison only for a needed thickness/width/beat pattern. Set count, detune, distribution, blend, and stereo spread where supported. More voices are not equivalent to more useful sound.
5. Apply warp modes in a deliberate order. Recheck high-register artifacts and output level after each nonlinear stage.
6. Add envelopes/LFOs to position or warp, keeping base and depth inside the useful table region.

### Warp choices

| Warp | Design effect | Useful experiment |
|---|---|---|
| Sync | Changes harmonic structure while preserving sync fundamental | Envelope the internal ratio for a bright attack |
| Bend/asymmetry | Remaps the cycle's timing | Small envelope sweep for animated pluck |
| PWM | Changes effective duty/cycle distribution | Slow small-depth motion around a stable center |
| Mirror | Repeats mirrored structure; can produce octave-like change | Compare at matched level and verify pitch |
| Remap | User-designed cycle mapping | Start with identity graph and add one deformation |
| Quantize | Waveform-domain staircase/redux character following pitch | Compare low/high notes to FX sample-rate reduction |
| Odd/even | Changes harmonic parity emphasis | Sweep around original/missing-fundamental states |
| LPF/HPF warp | Source-local spectral shaping | Use before downstream distortion if desired |
| Clip/fold/rectify/tape/tube | Nonlinear harmonics and character | Lower source gain, then compare input/output spectrum |
| FM/AM from source | Inter-oscillator/filter spectral interaction | Verify selected source and pitch relationship |

Manual UI choices are broader than the current tool's curated friendly names. Refer to the live schema; raw names and undocumented numeric IDs require evidence, not guesses.

## Custom harmonic tables

For a controlled harmonic fingerprint, define amplitudes for `n=1..N`. Useful seeds: sine `[1]`; softened saw `[1,1/2,1/3,...]`; odd-heavy `[1,0,1/3,0,1/5,...]`; soft odd `[1,0,1/9,0,1/25,...]` (phase/sign information can affect exact waveform). The current `custom_harmonics` is amplitude-frame synthesis, not a full independent partial bank.

Use several frames for a trajectory: fundamental-heavy -> odd-heavy -> dense bright -> reduced upper spectrum. Name the frame progression and useful scan range. Avoid turning a harmonic amplitude list into claims of arbitrary inharmonic synthesis. The helper normalizes generated frames; check level continuity and add compensating modulation if necessary.

For editor work (S2 pp. 274-290), distinguish time-domain drawing, FFT harmonic editing, frame sorting, and waveform/spectral morphing. Align periodic cycles before interpolation when phase discontinuities dominate. Keep authored tables and installation destinations in the resource manifest.

### Audio import

Manual import has multiple algorithms (S2 pp. 291-303). Match the algorithm to periodicity and goal: a single-cycle source, multiple cycles with detected/specified period, or a spectrum-derived texture. The preset tool's `sample_source` slices audio into 2048-sample frames; it is a particular conversion, not the complete UI import system. A vocal/drum transient converted this way becomes a repeating synthesized texture. Use sample playback when recognizable original timing/attack is required.

### Formula parser

S2 pp. 304-311 defines parser functions, variables, and multi-frame uses. Verify exact supported syntax and variable conventions before evaluating; do not paste generic Python/JavaScript formulas as Serum syntax. Preview one cycle, verify DC/peak level and harmonic behavior, then generate frame progression. Store the formula and parser settings as reproducible source. A formula is a table-generation instruction, not a native preset on its own.

## FM/AM workflow

1. Identify carrier and modulation source. Confirm both source enabled state and actual source selection (manual S2 pp. 54-56).
2. Set a simple carrier and simple modulator first. Reduce the modulator's audible level if it should contribute only through modulation. Check output with modulation amount at zero and at a small value.
3. Choose pitch ratio. Equal octave offsets are useful harmonic ratios; semitone/fine offsets allow other ratios. For a desired ratio `r`, pitch offset is `12*log2(r)` semitones, implemented within available fields/ranges.
4. Envelope modulation amount independently from amplitude: a fast-decaying index creates a bright/metallic onset with a simpler tail; sustained index creates a stable bright body.
5. Decide whether the modulator tracks the played note, remains fixed, or changes independently. A fixed-frequency source makes timbre change across the keyboard.
6. Add warp/unison/feedback-like interactions only after source routing is proven. Through-zero and other modes have specific behavior; use the manual, not generic equivalence claims.

The tool's friendly `warp_mode='fm'` writes `kFM_OSC`; it does not document every UI source selector. Preserve/verify the correct source connection through a known preset or UI when necessary. Diagnose a flat timbre by checking source enablement, source selection, carrier amount, pitch relation, and route depth before adding effects.
