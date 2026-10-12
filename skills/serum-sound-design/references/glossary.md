# Agent glossary

| Term | Working meaning and design consequence |
|---|---|
| Excitation | Energy-producing event: oscillator, impulse, bow/breath/noise/sample attack |
| Resonator/body | Frequency-dependent response that shapes/rings after excitation |
| Fundamental | Base repetition/pitch frequency; can be perceptually present without an actual strong lowest component |
| Harmonic/partial | Harmonic is an integer-related component; partial is a general component |
| Spectrum/spectral envelope | Component distribution and broader band contour; changes across attack/body/tail |
| Formant | Emphasized band associated with resonant/vowel-like identity, not simply fundamental pitch |
| Phase/random phase | Position in a cycle and note-start variation; affects summed transients/cancellation |
| Beating | Amplitude fluctuation from nearby frequencies; differs from deliberate tremolo |
| Unison | Multiple related voices per note with spread/detune/other variation |
| Wavetable frame | One periodic-cycle representation inside a table; not a full time-domain sample event |
| Morph/interpolation | Transition between frame representations; choice affects continuity and harmonic behavior |
| Warp | Engine-specific source transformation; same label family can have different control/source semantics |
| Carrier/modulator | Output-bearing source and source that changes it in FM/AM; may both be audible intentionally |
| Modulation index | Strength relative to modulator frequency in ideal FM theory; a normalized Serum amount is not automatically textbook index |
| Filter cutoff/center | Boundary/central frequency depending on filter; normalized tool value may not be Hz |
| Resonance/Q | Peak/band selectivity; resonance UI percent and numerical Q are not interchangeable |
| Serial/parallel | Cascaded processors versus summed paths; order and phase matter |
| Send/return | Additional path to a processor/bus and its rejoined output; may coexist with dry/main path |
| Direct | Serum route bypassing filter/FX path according to mixer configuration |
| ADSR/hold | Attack, decay, sustain level, release plus optional full-level plateau |
| Gate | How long a note/trigger is held; does not equal envelope decay or total processor tail |
| Retrigger/legato | Restart versus connected-note behavior; source/envelope/LFO rules can differ |
| Unipolar/bipolar | One-sided versus centered modulation; affects endpoints and base position |
| Auxiliary source | Scales another modulation route's depth, useful for gesture-controlled motion |
| Macro | Named performance control mapped to one or more sound changes |
| Velocity/aftertouch/MPE | Note-on dynamics, pressure, and per-note expression protocols; verify actual host/controller data |
| Resampling | Pitch changes with playback speed/duration |
| Multisample | Multiple recorded sources assigned across key/dynamic regions; curated source selection is not a zone editor |
| Grain/window/density/scan | Audio fragment, its amplitude shape, spawning/overlap behavior, and source traversal |
| Spectral mask/warp | Frequency-domain shaping/transformation; a neutral curve cannot imply drawn resonant bands |
| Frequency versus pitch shift | Add a Hz offset to components versus multiply their frequencies |
| Convolution/IR | Filtering with an impulse response, potentially a room/body/special response |
| Nyquist/aliasing | Half sample rate and high-frequency folding artifacts |
| Oversampling | Higher internal processing rate to reduce some artifacts, at CPU cost |
| Readback | Inspect actual stored native state; not proof of plugin loading/listening |
| Factory/external/embedded resource | Installed stock dependency, separately referenced file, or included preset payload |
| Schema confidence | Upstream evidence category for mapping/units; separate from current-run verification |

See [theory](theory.md) for equations and [sources](sources.md) for source coverage and supplemental material distinctions.
