# Bass families

All architectures and ranges are authored starting points. Read [wavetable/FM](wavetable-and-fm.md), [filters/routing](filters-and-routing.md), and [modulation](modulation-and-performance.md) for implementation. Use actual MIDI numbers; octave labels vary.

| Family | Source/body | Articulation/motion | Critical checks |
|---|---|---|---|
| Pure sub | Sine-like A/custom harmonic `[1]`, or suitable rounded source | Fast click-free onset, held or decaying as brief needs | Fundamental consistency, pitch, repeated-note phase, headroom |
| Rounded analog bass | Saw/square/triangle-like source through low-pass | Brief positive filter envelope, high/medium sustain | Body survives resonance; cutoff/key tracking balance |
| Plucked acid-like bass | Single bright source, resonant modeled LP | Zero/low sustain, accented brightness/decay, glide where requested | Accent changes spectrum/energy; sequenced slides actually overlap |
| Reese | Two near-pitched saw-rich sources or unison | Sustained body, slow beat/notch evolution | Mono low-band cancellation, beating rate across register |
| FM bass | Simple carrier with enabled inaudible modulator | Fast index decay plus stable sustain | Actual FM source, harmonic ratio, clear root |
| Growl/vowel bass | Rich/FM/table source, formant/notch/comb movement | Coordinated table/warp and resonant bands, slower amplitude contour | Independent vowel centers, intelligible fundamental, macro bounds |
| Wobble | Harmonic source plus LP/BP/resonant movement | Retriggered synced LFO, amount/rate macros | Actual rhythmic division, initial phase, gate versus filter sweep |
| Distorted mid-bass | Source/warp/distortion with clean low component when needed | Deliberate transient and nonlinear sustain | Separation of low/mid paths, output trim, high-register artifacts |
| 808-like pitched bass | Sine/triangle body with brief downward pitch excursion | Decay/release tuned to phrase; optional transient/saturation | Sustained bass identity versus short kick, tuning after sweep, glide |
| Electric/plucked approximation | Harmonic body plus short noise/attack component, filter decay | Velocity alters excitation/brightness, subtle pitch settling | Natural decay/register changes; use sample/multisample for faithful attack |

## Authored starting ranges

- Stable held bass: main attack roughly 2-10 ms, high sustain, release roughly 30-120 ms; adapt to click behavior and phrase space.
- Pluck bass: main decay roughly 100-500 ms with zero sustain; brightness often decays faster than amplitude.
- Reese: start with two voices or sources, small detuning, then increase only enough to create the intended beat/roughness.
- FM/index transient: start small; audition the low note and an octave above before adding drive.

Numbers specify perceptual prototypes, not final presets. Serum Sub's current curated shape list does not include a friendly sine; use a verified sine-like table/custom harmonic source rather than inventing `sub_shape='sine'`.

## Bass design sequence

Establish root and envelope with FX bypassed. Add upper spectrum for audibility on small speakers if the brief requires it. Check phase/randomness before making wide layers. Add nonlinear/formant motion above a stable low body when appropriate. Evaluate the part against kick and other low instruments; a solo impressive bass can occupy too much spectrum or tail length in context.

Test repeated roots, octave changes, short/held notes, overlaps/glides, low velocity, mono fold-down, and macro combinations. Exact fundamental level may vary intentionally for Reese textures; document that intent rather than applying a universal fixed-phase rule.
