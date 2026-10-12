# Sound-design theory for decisions

## What the supplied excerpt supports

The theory PDF is a demo, not the complete book. Its actual excerpts cover basic synthesis/processing, frequency/amplitude/phase/perception, fixed-spectrum additive synthesis, additive signal summation, selected noise generators, and control-signal panning. Several headings announce omitted sections. The equations and techniques below extend those foundations with standard synthesis theory; see [sources](sources.md) for precise provenance. FM, granular, and spectral details primarily use the Serum manual and authored supplemental explanation.

## Frequency, pitch, and register

Period `T = 1/f`; an octave multiplies frequency by 2. Equal-tempered MIDI pitch: `f(n) = 440 * 2^((n-69)/12)` Hz. A change of `s` semitones multiplies frequency by `2^(s/12)`; `c` cents uses `2^(c/1200)`. MIDI number 69 is 440 Hz at standard tuning; octave labels differ between hosts. For presets, record MIDI numbers and actual sounding frequency where sample-root naming is ambiguous.

Detuning creates beats: two nearby sinusoids produce an amplitude fluctuation at approximately `abs(f1-f2)` Hz. Constant cents spread produces faster beats higher on the keyboard; a pad balanced in the low register can become rough in the high register. An equal-tempered fifth (7 semitones) differs slightly from the exact ratio 3:2. T PDF pp. 65-67 includes this distinction.

## Amplitude, level, and perception

For an amplitude ratio `a`, `dB = 20*log10(a)` and `a = 10^(dB/20)`. Doubling amplitude gives approximately +6.02 dB. Digital full scale, sound pressure level, and perceived loudness are different quantities. Frequency, spectrum, duration, and playback level affect perceived loudness; match levels when comparing timbre (T PDF pp. 28-33).

Summing coherent voices can increase peaks sharply; partial cancellation can remove energy instead. A limiter cannot repair an unintended source cancellation. Gain staging is both a musical and numerical decision. Normalizing a custom table changes absolute amplitude; it does not equalize perceived brightness/loudness across frames.

## Spectrum and timbre

A harmonic tone has components at integer multiples of its fundamental; inharmonic components need not follow that grid. A missing fundamental can still produce a pitch percept from upper harmonics. A spectrum is a time-local view; a spectrogram shows changes. Analyze attack, body, and tail independently (T PDF pp. 73-77, 81-84).

Idealized waveforms as design priors:

| Waveform | Component structure | Consequence |
|---|---|---|
| Sine | One sinusoidal component | Pure body, sub, simple FM source |
| Saw | All integer harmonics, roughly `1/n` amplitude | Dense subtractive source |
| Square at 50% duty | Odd harmonics, roughly `1/n` | Hollow body, clarinet-like starting point |
| Triangle | Odd harmonics, roughly `1/n^2`, alternating phase/sign | Softer upper spectrum |
| Variable pulse | Harmonics vary with duty cycle | Nasal/hollow shifts and PWM motion |
| White noise | Approximately equal average power per Hz | Air, noise attack, broad excitation |
| Pink noise | Approximately equal average power per octave | Less bright broad texture |
| Brown-like noise | More low-frequency weighting | Low rumble/wind-like base |

These ideal patterns are supplemental theory. Serum's actual factory tables, warps, antialiasing, and sample content may differ. Verify frame and waveform rather than assuming a table name guarantees a spectrum.

## Synthesis methods and what they control

- **Additive:** sum partials with chosen amplitude/phase/frequency behavior. Serum's harmonic table tools create a periodic harmonic waveform; arbitrary independent inharmonic partials require separate sources or a different method.
- **Subtractive:** begin with an excitation rich enough to contain the required spectrum, then shape it using filters/envelopes. A low-pass cannot create missing high harmonics; drive/resonance may create new behavior.
- **Wavetable:** scan a collection of cycles. Motion changes spectrum rather than replaying the original recording. Frame alignment, interpolation, phase, and gain affect smoothness.
- **FM/phase-like oscillator modulation:** creates sidebands. For ideal sinusoidal FM, frequencies are `fc +/- k*fm`; sideband strength depends on modulation index. Integer-related ratios tend to reinforce harmonic patterns, while noninteger ratios tend toward metallic/inharmonic results. Serum's warp is implemented behavior, not a promise of a mathematically pure textbook FM model.
- **AM/ring multiplication:** ideal multiplication generates sum/difference components. A DC-biased modulator retains carrier content (AM); a zero-mean product suppresses the original carrier in the ideal case (ring modulation). Confirm Serum's specific warp/source settings.
- **Sampling:** reproduces recorded structure; resampling changes pitch and duration together. Multisampling reduces transposition artifacts by providing recordings across ranges/velocities.
- **Granular:** schedules windowed excerpts; position/scan, grain length, density, pitch, and randomization determine texture. Independence between scan and pitch depends on engine/settings.
- **Spectral:** manipulates a time-frequency representation; frequency masks, warps, scan, and phase/transient handling shape the result.
- **Resonant/physical analogy:** excitation plus frequency-dependent ringing approximates struck, bowed, or blown bodies. Serum can imitate aspects, but a static filter or FM ratio alone does not recreate an acoustic instrument's full behavior.

## Filtering and topology

Low-pass removes upper spectrum; high-pass removes lower; band-pass isolates a band; notch removes a band. Increasing resonance emphasizes a cutoff/center region and can change amplitude and pitch perception. For a simple resonant band, `Q = center_frequency / bandwidth`; a UI resonance percent is not necessarily numerical Q. Nominal order changes the asymptotic slope (roughly 6 dB/octave per order), but actual response depends on the design, drive, and resonance.

Serial processing multiplies transfer responses; parallel processing sums paths. Phase differences at recombination can reinforce or cancel. Comb filtering creates repeated spectral peaks/notches related to delay; it can act like a resonant body. Formants emphasize bands whose positions need not follow the fundamental. These are supplemental foundations for the filter controls in S2 pp. 133-151.

## Time and control signals

An amplitude envelope describes energy over a note's lifetime; a filter envelope describes spectral evolution. Exponential-like decay often feels more natural for plucked/struck excitation than linear decay. Release is initiated by note-off, not by decay ending. Zero sustain gives a decaying note even if held; gate duration and retrigger rules still matter.

An LFO modulates a parameter: pitch gives vibrato, amplitude gives tremolo, pan gives spatial motion, filter gives timbral motion. Below the audio rate it is primarily heard as movement; at audio rate it can create new spectral components (T PDF pp. 113-114). Unipolar motion adds an offset; bipolar motion centers around a base. Discontinuities can cause clicks or broadband sidebands; smoothing changes both the artifact and the rhythm's edge.

Tempo math for quarter-note-based BPM: quarter duration `60/BPM` seconds; whole `240/BPM`; eighth `30/BPM`; sixteenth `15/BPM`. Dotted multiplies duration by 1.5; triplet by 2/3. A 4/4 bar is four quarter beats; other meters require explicit beat-unit interpretation.

## Digital limits

Nyquist is half the sample rate. Nonlinear processing, FM, and abrupt waveforms can generate components above Nyquist that fold into aliasing. Oversampling/antialiasing reduces some artifacts at CPU cost; it does not make every extreme patch artifact-free. An FFT uses finite windows: longer windows improve frequency resolution but blur transient timing. Pitch estimation of noisy/polyphonic signals is uncertain. Avoid equating a spectrum screenshot with a definitive reconstruction.
