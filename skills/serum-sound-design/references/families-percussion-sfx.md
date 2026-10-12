# Synth percussion and sound effects

Authored design experiments using Serum source/filter/envelope/FX mechanisms. This reference covers sound design; the workspace's default drum performance still uses the user's selected kit/sample unless Serum percussion or agent sample selection is explicitly requested.

| Sound | Excitation/body | Envelope/motion | Key checks |
|---|---|---|---|
| Kick | Low sine/rounded body, optional noise/click | Fast pitch drop, short bright attack, decaying amplitude | Final tuning, pitch-drop duration, clicks, low-end peak |
| Snare | Short tonal body plus filtered noise | Body/noise decays differ; optional room | Noise-to-body ratio, repeat consistency, tail length |
| Clap | Multiple noise bursts plus tail | Designed retrigger/burst contour | Burst spacing and held-note behavior |
| Hi-hat/cymbal-like | Metallic/inharmonic sources and upper noise | Very short closed versus longer open tail | Harsh aliasing, pitch character, choke behavior external unless implemented |
| Tom | Rounded tonal body, mild pitch decay | Longer pitch settling than click layer | Tuning across requested hits |
| Shaker | Short high-noise events | Varied excitation and repeated gesture | Dynamics/timing in performance, not preset randomness alone |
| Rim/click | Short impulse/bright resonant body | Fast decay with controlled peak | Enough audible energy without discontinuity-only artifact |
| Riser | Noise/harmonic source with increasing energy | Upward pitch/brightness/density/width, endpoint | Duration, starting phase, final stop/tail, tempo alignment |
| Downlifter | Noisy/tonal body | Falling pitch/filter/energy | Tail length and low-end accumulation |
| Impact | Transient plus resonant low/mid body, optional space | Brief pitch/noise burst, body decay, space tail | Peaks, body tuning, impact remains intelligible wet |
| Whoosh | Filtered noise or recorded motion | Rise/fall amplitude and band trajectory | Physical/spatial implication and event length |
| Laser/zap | Tonal/FM source | Fast large pitch/index sweep | Sweep range and clicks, register |
| Glitch | Fragment/step/quantized source behavior | Deliberate discontinuous rhythm/position | Intentional versus accidental timing/aliasing |
| Sci-fi/mechanical | FM, frequency shift, resonance, sampled mechanism | Coherent repeated gestures or evolving interaction | Complexity has a function; no unsupported exact identity claim |
| Reverse-like hit | Increasing envelope and bright endpoint, or reversed recording | Shape leads to impact/stop | An amplitude swell alone does not reverse a transient's detailed structure |

## One-shot versus musical voice

Decide whether notes transpose the sound, trigger fixed events, or sustain an evolving process. A true one-shot and a voice envelope that releases on note-off can behave differently. Test both short gate and held gate. Large pitch sweeps require correct envelope polarity/range; the final settled pitch should match the musical brief.

For transitions specify duration in seconds or musical bars, trigger phase, endpoint, and tail. A synced LFO envelope can provide deterministic rise when rate/shape mapping is verified; external automation may be necessary if the internal tool cannot encode the needed duration. Record which approach was implemented.

## Synthetic percussion packages

Create distinct sounds/presets for different percussion roles when the user requests them. Mapping MIDI pitches to presets/kit voices is a separate instrument/host setup; a folder of Serum presets is not automatically a playable drum kit. For arrangement work read `docs/default-drum-map.md` and the user's kit mapping. Choking open hats, round robins, and multi-output routing need actual host/plugin support and evidence.

## Event QA

Repeat the trigger at several intervals, test velocity and note length, inspect peak/tail levels, and verify no accumulating feedback or overlapping releases overwhelms the next event. Compare at the intended tempo and in context. With source recordings preserve original files and document conversions, truncation, reversal, or channel balancing.
