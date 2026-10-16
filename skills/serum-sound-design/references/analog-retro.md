# Detailed guide to analog and retro sounds in Serum 2

This guide is the **default for briefs requesting analog, vintage, retro analog, or the character of real analog gear**, including sound choices for individual composition layers. More specific user instructions or references take precedence. For an analog brief without a named instrument, start with a well-maintained instrument and small variations; choose an architecture family suited to the sound's role and record the assumption. Retro alone does not define an architecture: retro recordings can also use digital FM, samplers, or acoustic instruments.

The goal is to reproduce instrument behavior: sources, oscillator interaction, filters, envelopes, voice allocation, playing response, and signal paths. The five techniques from the user's attachment are options selected for the behavior they produce. Noise FM, stereo noise, fast compression, tape, and large reverb are **not automatically enabled** on every analog patch.

All recipe values here are **design starting points**, not hardware measurements or auditioned presets. Cents/Hz/ms/dB describe physical or musical targets; convert them to the correct Serum/tool parameters and verify them. A knob percentage is not a universal unit.

## Contents and reading paths

- [1. Choose the target and architecture](#1-choose-the-target-and-architecture)
- [2. Build the sources and phase behavior](#2-build-the-sources-and-phase-behavior)
- [3. Filters, envelopes, and playing behavior](#3-filters-envelopes-and-playing-behavior)
- [4. Technique 1: variation between voices](#4-technique-1-variation-between-voices)
- [5. Technique 2: filtered-noise FM](#5-technique-2-filtered-noise-fm)
- [6. Technique 3: smoothed S&H drift](#6-technique-3-smoothed-sh-drift)
- [7. Technique 4: oscillator-to-noise-level modulation](#7-technique-4-oscillator-to-noise-level-modulation)
- [8. Technique 5: drive, dynamics, and tape](#8-technique-5-drive-dynamics-and-tape)
- [9. Recipes by instrument family](#9-recipes-by-instrument-family)
- [10. Macros and implementation specifications](#10-macros-and-implementation-specifications)
- [11. Native implementation and tool boundaries](#11-native-implementation-and-tool-boundaries)
- [12. Verification and troubleshooting](#12-verification-and-troubleshooting)
- [13. Sources and corrections to the attachment](#13-sources-and-corrections-to-the-attachment)

For a new patch, read sections 1–4, the required technique sections, the relevant recipe, then sections 10–12. To repair an existing sound, start with its symptoms in section 12 and preserve the character requested by the user.

## 1. Choose the target and architecture

Record the role, MIDI range, gate lengths, mono/poly behavior, legato/retrigger settings, instrument model/revision when known, calibration condition, and whether the target is a dry synth output or a processed recording. Recorded hardware can include chorus, amplification, a console, tape, EQ, and space; separate the instrument hypothesis from the recording-chain hypothesis.

| Target | Priority foundations | Variation and stereo treatment |
|---|---|---|
| VCO monosynth, such as the Minimoog family | Separate oscillators, mixer, resonant low-pass filter, envelopes, and glide | Relative oscillator offsets and movement; mono center; no need for a six-voice pattern |
| VCO polysynth, such as a Prophet-inspired design | Oscillators, filters, and envelopes per voice; polyphony limit | Calibration offsets between voices and small drift; pan spread only when the target provides or needs it |
| DCO polysynth, such as the Juno-106 | One pitch core per voice with related saw/pulse/sub sources, filter/envelope, and chorus | Relatively stable pitch; PWM, filter, and chorus provide motion; avoid starting from two freely detuned VCOs |
| String ensemble or analog organ | Generators/registers and envelope sharing appropriate to the target; ensemble as a defining process | Ensemble motion differs from VCO drift; do not assume every instrument has a VCF and ADSR per note |
| Aged recording or broken synth | Instrument foundations first, then faults or recording-medium behavior | Larger wow/flutter, hiss, dropouts, and pitch wander only when the brief calls for them |

A family name gives a design direction. Similar filter names or oscillator counts do not prove circuit emulation. For a specific instrument, consult its manual/model/revision and reference audio when available; label the result **inspired by** or an **approximation** until comparison supports a stronger claim.

Default decisions for a general analog brief:

1. Use appropriate simple waveforms, one unison voice per oscillator as the foundation, and a subtractive path that can be inspected easily.
2. Match attack, body, release, filter response, and playing mode before increasing instability.
3. Add variation between polyphonic voices or relative drift between VCOs when needed. For DCOs, start with zero or very small pitch drift.
4. Preserve the low end and stereo center. Widen through a mechanism appropriate to the target, such as chorus or specifically requested pan spread.
5. Add only the required nonlinearity and compare at matched levels. Choose noise FM or noise modulation only when a texture requirement remains unmet.
6. Separate the instrument from recording coloration. Keep external FX optional and document their dependencies.

## 2. Build the sources and phase behavior

### Waveforms, oscillator count, and tuning

Start with saw, pulse/square, triangle, or an appropriate mixture. Choose a table/frame that has actually been inspected; its name alone does not guarantee its shape. A fixed WT position is a reasonable starting point for a subtractive source unless shape movement/PWM is required. Use complex warps for a named, tested property.

Use A/B/C as separate oscillators when their intervals, levels, phases, and drift need independent control. Unison stacks oscillator copies; it does not automatically replace a two- or three-VCO architecture. Hard sync, ring modulation, or cross-modulation can define particular hardware, so use them when the target calls for them rather than decorating every retro patch.

For two VCOs tuned in unison, try a total tuning difference of 3–8 cents. Distinguish **fixed offsets between oscillators**, **offsets between voices**, and **drift over time**. All three contribute to the final pitch and can produce excessive beating when increased together. Start smaller on bass and audition long sustains.

Pitch and beating relationships for two nearby sine waves:

`f2 = f1 × 2^(cents/1200)`; `beat_Hz ≈ |f2 − f1|`.

For example, a 5-cent difference is about 0.29 Hz at 100 Hz, but about 2.89 Hz at 1 kHz. The same depth in cents does not produce the same beating rate across registers. Partials and filters also affect complex sounds.

In a DCO-inspired design, saw/pulse/sub sources derived from one core are not free oscillators continuously drifting relative to one another. Use controlled pitch and phase relationships, or a combined source/verified template when an exact relationship is required. Playing saw and pulse in separate slots without detuning is only an approximation; verify their phase relationship and articulation.

### Phase: randomness, memory, and continuity

S2 pp. 41–44 distinguish PHASE, RAND, and Phase Memory. RAND randomizes a new voice's starting phase; it does not move pitch during a held note. Phase Memory offers All Voices, Contiguous, and Per Voice with different behaviors. Choose according to the required note-on behavior rather than assuming maximum RAND is always more analog.

- Repeat one note with short gates. If each attack produces an identical phase sweep that does not suit the target, inspect phase reset, RAND, and Phase Memory.
- For oscillator continuity, evaluate Contiguous according to the manual and test note overlap/voice stealing. Do not equate this option with a complete simulation of continuously running hardware VCOs.
- For a punchy bass with controlled phase, retain consistent attacks when the music needs them; add filter or sustain variation without weakening the initial impact.
- If clicks occur, inspect phase discontinuities, attack/release, envelope retriggering, and DC. Randomizing phase is not a universal fix.

### PWM

Choose a pulse source and the correct duty-cycle modulation method for the UI/template. A slow LFO around 0.1–0.6 Hz with a limited duty-cycle range is a starting experiment for pads; a saw-to-square WT scan is not equivalent PWM. Limit the range so the pulse does not disappear at the extremes, and check that its body remains clear in low registers. A shared PWM source may suit hardware with one shared LFO; per-voice sources produce different behavior.

## 3. Filters, envelopes, and playing behavior

### Filters and gain paths

Choose the slope and response character for the target: a 24 dB/oct low-pass for some families, a 12 dB/oct or multimode filter for others. Compare cutoff, resonance, key tracking, input level, and driven response. A Serum mode name does not prove a match to a ladder, OTA, or particular hardware circuit.

Make sure every source that should be filtered actually passes through the filter; inspect Sub/Direct and parallel paths so they do not add a fundamental absent from the target. Conversely, if production requires a clean sub, document it as a musical adaptation. Resonance can change fundamental level depending on the filter model; do not always compensate when that behavior defines the target.

Specify cutoff as testable endpoints, such as a 300 Hz base rising to about 2 kHz at the envelope peak. On a logarithmic scale, octaves are more useful than adding Hz: `new_cutoff = base_cutoff × 2^(octave_offset)`. An offset of ±0.02 octave is approximately ±1.4% in frequency. Do not insert a UI cutoff percentage directly into this equation without calibration.

### Envelopes and articulation

Use Env 1 for amplitude and a separate timbre envelope when the target needs it. Match curves, gate behavior, sustain, and retriggering. A 10 ms attack on two synths may not produce the same transient because their curves and starting levels differ.

| Role | Amp: attack / decay / sustain / release | Filter-envelope starting point |
|---|---|---|
| Short bass | 3 ms / 250 ms / 65% / 70 ms | Attack 2 ms, decay 180 ms, low sustain |
| Pluck/key | 4 ms / 650 ms / 0–15% / 180 ms | Decay 200–400 ms; brightness falls faster than the body |
| Poly brass | 25 ms / 500 ms / 70% / 250 ms | Attack 35 ms, decay 450 ms, medium sustain |
| Pad | 500 ms / 1 s / 80% / 1.5 s | Attack 900 ms, release 1.8 s; limited cutoff range |
| Legato lead | 8 ms / 350 ms / 80% / 130 ms | Fast attack, sustained body; test legato and detached notes |

These values do not represent hardware calibration. Adapt them to the actual tempo and gates; note-off can occur before decay finishes. To approximate a panel with ADS or linked decay/release, follow the target's control relationships; independent ADSR controls in Serum are an implementation convenience, not evidence of the original instrument's features.

### Polyphony, note priority, and expression

Set the polyphony limit separately from the Voice Control sequence. Account for release overlap: a six-note chord followed by a new chord can steal voices even when each chord contains only six notes. For mono sounds, specify note priority, legato/retrigger behavior, and glide; if the schema does not support the required priority, verify it through the UI/template or report the gap.

Velocity, aftertouch, and MPE should follow the target. Some older hardware does not respond to velocity like a modern synth. When matching original behavior, do not automatically add a large velocity-to-cutoff response; if useful for production, label it as a performance adaptation. Tuning drift inside the synth does not change MIDI timing: the workspace's on-grid/no-swing contract still applies.

## 4. Technique 1: variation between voices

**Purpose:** give each voice its own calibration identity, producing small differences in repeated notes/chords without making the entire sustained chord wobble together.

S2 pp. 316–318 describe Global → Voice Control, the affected oscillator selection, the 1–8 sequence, and RANDOM for PAN, DETUNE, CUTOFF, and ENVS. The numbers 1–8 set the **sequence length**; they are neither Serum's maximum polyphony nor the oscillator unison count. The tool's `voice_unison` name is also not a reason to equate these three settings.

UI procedure:

1. Start with the panel's Init configuration and select the oscillators that should be affected. Record the A/B/C/Noise/Sub selections.
2. Choose the sequence length for the design, such as six steps for a six-voice polysynth experiment. Set the polyphony limit separately in Voicing.
3. Enter small DETUNE variations with a mean near zero; check their result in cents through suitable UI readouts or measurement. Do not assume the SEQ bars use cents.
4. Add small CUTOFF and ENVS differences when the target needs timbre/articulation variation. Start at zero so each group's effect can be heard.
5. Keep PAN centered for mono instruments or targets without pan spread. When needed, use a small left/right pattern and check the mono sum. Prophet-6 pan spread is not a mandatory feature of every retro synth.
6. Start RANDOM at zero, then raise it slightly if the fixed pattern is too obvious. The manual lists RANDOM DETUNE in cents and other random parameters in percentages; the tool has some scale uncertainty, so match the readout before entering values.
7. Test 16–24 detached note-ons at one pitch, a held chord, then overlap/voice stealing. Confirm that repeated behavior comes from allocation/the sequence rather than LFO retriggering or velocity changes.

Example **six-step musical targets** for calibration; this is not a tool JSON array:

| Step | Target pitch offset | Target relative cutoff | Target relative envelope time | Pan when needed |
|---|---|---|---|---|
| 1 | −2 cents | −1% frequency | +1% time | slightly left |
| 2 | +1 cent | +1% frequency | −1% time | slightly right |
| 3 | −1 cent | 0% | +2% time | near center |
| 4 | +2 cents | +2% frequency | 0% | slightly left |
| 5 | 0 cents | −2% frequency | −2% time | slightly right |
| 6 | 0 cents | 0% | 0% | center |

Do not apply identical patterns to every parameter without a reason: one voice would always be simultaneously highest, brightest, fastest, and furthest right. A particular target may require that correlation, but it is not the general default. Note-on offsets do not replace drift during sustain; use section 6 for that motion.

## 5. Technique 2: filtered-noise FM

**Purpose:** add a very small amount of fast instability or rough texture. Default **off**; try it after the foundations and slow drift are adequate. Noise FM generates sidebands/spectral broadening; it is not identical to changing VCO calibration or tape wow/flutter.

Experimental procedure:

1. Use Osc C as the noise modulator when needed to keep the Noise slot available. Choose an engine/source that produces continuous noise. A repeated single-cycle table can produce periodic patterns; do not claim it is the same broadband random noise as a continuous source.
2. Apply low-pass filtering **to the modulator before the FM tap**. An LPF warp on C before the next warp/modulation stage is a path to evaluate; inspect warp order and tap position in the UI/manual/template.
3. Disable source key tracking if its bandwidth/fluctuation should remain constant as carrier notes change. If that engine control is unavailable, use a prefiltered source or verified filter path and document the difference.
4. On A, select FM whose actual source is C. The source must be enabled, but its audible level can be reduced to zero for modulation only, according to S2 p. 54. Solo/bypass to confirm that C is not leaking as direct hiss and that FM still works.
5. Start the amount at zero. Raise it until the difference is easy to identify, then reduce it to fit the brief. Test low, middle, and high notes; the same percentage amount may not yield the same deviation in cents.
6. If B should share this behavior, design its route explicitly; FM on A does not automatically modulate B. Check whether a shared source makes them too correlated.

As an experiment, start with a modulator dominated by very low frequencies, such as a low-pass around 5–30 Hz, if the engine/filter actually supports it. Increase bandwidth only when faster texture is needed; the result can become roughness/noise rather than drift. This is an experimental range, not a value verified from the video or a hardware-flutter measurement.

A low-pass in the main audio path after the carrier does not filter noise that has already entered the FM tap. An `FM (Filter 1/2)` alternative is valid only when the filter source and routing to the carrier are confirmed; changing a destination name does not complete the graph.

Signs of excess include a shifted pitch center, hiss in the sustain, harsh transients, and metallic FM in upper notes. Reduce amount/bandwidth and inspect FM mode and tracking; use smoothed S&H if only clean pitch wander is needed. Increasing the amount for a broken-synth character is a separate creative choice and must be labeled.

## 6. Technique 3: smoothed S&H drift

**Purpose:** move pitch slowly during held notes without directly adding audio noise. Unsmoothed stepped S&H can create jumps/zipper artifacts; pitch modulation also changes the spectrum. Hiss-free does not guarantee artifact-free.

1. Select the S&H LFO type in the UI; the inspected schema names the algorithm `random_sh`. Its use in generation still has the verification limits described by the tool.
2. Use a free rate in Hz, Free mode, and an appropriate HOST configuration. For motion that remains free between playback passes, evaluate HOST off; when reproducibility matters, record the host/reset behavior used. S2 pp. 191–193 distinguish FREE, MONO, BPM/HZ, and HOST.
3. Raise Smooth until transitions are gentle enough. Smoothing changes effective depth and response; inspect the output and actual period.
4. For drift in each voice, choose a poly source and the correct oscillator-pitch destination. For a shared wobble across the instrument, use a shared mono source and Main Tuning if available. These are different models.
5. Use a centered bipolar route. Start around ±1–3 cents and a 0.05–0.3 Hz update rate for maintained VCOs. Start at zero or smaller amounts for bass/DCOs; adjust to the target.
6. Reduce amount/OUTPUT and use AUX scaling when fine calibration is needed. The attachment's roughly 1% Matrix amount does not determine pitch depth without its destination, range, curve, and scaling.
7. Hold a note for 20–30 seconds, then play chords. If every chord tone bends together, inspect the source MONO setting and global destination. If short notes sound identical each time, inspect retriggering and host phase.

Relative motion between two oscillators requires routes that are not completely identical. Combine a small shared component with independent components when the target requires it; do not simply maximize the number of random sources. Main Tuning shifts overall pitch and does not automatically reproduce disagreement between VCOs.

Guidance for the **final pitch target**, including the sum of all routes:

| Condition | Continuous-drift starting point | Initial choice |
|---|---|---|
| Maintained DCO/very stable bass | 0 to about ±1 cent | Prioritize PWM/filter/chorus |
| Maintained VCO | about ±1–3 cents | Small slow motion; separate fixed oscillator offsets |
| Looser vintage VCO | about ±3–6 cents | Check chord intonation and beating across registers |
| Broken instrument/worn recording | Determined by the brief and comparison | Wander/wow/flutter is not the general analog default |

These ranges do not characterize all hardware. Pitch wander can occur at many time scales; regular sine vibrato readily sounds like a player/LFO and does not automatically substitute for random drift. If a periodic curve is used as a fallback, state that its behavior repeats.

## 7. Technique 4: oscillator-to-noise-level modulation

**Purpose:** add grit that follows waveform movement instead of static hiss. This is audio-rate amplitude modulation of noise, not the main method for creating analog pitch behavior.

1. Prepare a mono bass with an appropriate main oscillator and centered low end. Audition the version without noise as a reference.
2. Enable Noise with a known source and a very low or zero base level. Confirm its route to the filter/output.
3. In the Matrix, select Osc A output as SOURCE and Noise Level as DESTINATION, using the oscillator/filter modulation-source capability described in S2 p. 208 and pp. 210–212.
4. Choose polarity and base deliberately: a bipolar signal routed to a nonnegative level can be clipped at zero. A remap curve can create a one-sided or rectified response; base, amount, curve, and clamping jointly determine the result.
5. Start with a small amount; check whether the texture follows the body without masking the fundamental. Bypass the route, then bypass Noise, to distinguish modulation from the base level.
6. Use Editable Curve with RISE/FALL when available to shape the remap. The friendly tool schema does not expose every such remap curve; a curve described only in the design spec has not been implemented.
7. Stereo Noise is an option for upper texture. Start mono for bass, and use stereo only when the target needs it and the mono sum remains good. Do not widen the fundamental simply to sound vintage.

Noise whose level follows an oscillator remains modulated noise; do not promise a conversion into pure harmonics. If grit dominates, reduce the amount, restrict the noise spectrum, or evaluate light saturation as an alternative against the brief. Leave this route off for clean pads or gear emulations without that behavior.

## 8. Technique 5: drive, dynamics, and tape

### Nonlinearity and chain position

An ideal saw does not automatically sound bad because it is digital. A saw is also not a symmetric sine wave; its harmonic series differs. Analog character comes from specific source, circuit, filter, control, and level interactions. Asymmetric waveshaping can change harmonics and DC, but it is not required for every analog sound.

Compare Tube, soft clipping/saturation, or an asymmetric mode that is actually available. The manual distinguishes the oscillator's Asym warp (p. 53) from FX Distortion modes including X-Shaper (Asym) (pp. 167–168). Do not assume they share enum names, curves, positions, or responses.

| Nonlinearity location | What changes | Use |
|---|---|---|
| Oscillator warp/saturation before the voice filter | Source harmonics enter the filter and follow voice articulation | Shapes excitation; differs from bus drive |
| Voice-filter input/drive | Level, resonance, and filter-model interaction | Approximates driven-filter behavior when supported by the model |
| FX after voice summing | All chord tones interact in one nonlinearity | Bus coloration; can create intermodulation between notes |
| FX before/within/after space | Attacks, repeats, or tails are distorted differently | Recording/production coloration |

Choose one stage first. Start with low drive, trim the output, and compare at matched levels. If pre-filter drive is needed but only FX after the voice filter is used, document the different approximation. The Distortion module's internal PRE/POST filter order is also not the same as moving the entire module before the voice filter.

### Compression and headroom

Fast compression is not the analog default. It can reduce punch, raise hiss, or flatten the voice differences just created. When needed, start with single-band compression and small gain reduction around 1–3 dB in the loudest passages; adapt attack/release to transients and tempo. Use aggressive multiband processing only when it fits the target.

When a stage overloads, reduce gain at that stage; final output trim does not remove earlier clipping. Soft clipping is an additional color choice, not a universal repair. Test dense chords and release overlap, not just a single note. Leave adequate output headroom and record rendered peaks when available.

### Chorus, tape, and space

For DCO families with chorus, chorus can define the sound and deserves attention early in the design. Serum's generic chorus is an approximation; it does not prove replication of a particular BBD circuit. Add chorus hiss only when important to the target/reference; noise is not a prerequisite for warmth.

Tape is a **recording-medium layer**. Separate saturation, bandwidth limits, wow, flutter, and noise; a Tape Sat mode does not automatically implement every tape-machine behavior. Pitch modulation inside a Serum voice differs from processing the full recording, including tails, after the synth.

Start reverb/delay bypassed unless they define the target. Blackhole Immersive, Airwindows ToTape, and Ableton Saturator in the attachment are examples from the tutorial chain, not required dependencies, not part of a native Serum preset, and not default Cubase instructions. When using requested external FX, document plugin/version/order/settings and loading instructions; a Serum preset alone does not contain those DAW inserts.

## 9. Recipes by instrument family

These recipes are authored prototypes that **have not been rendered or auditioned**. Target registers use MIDI numbers to avoid ambiguity between DAW octave labels. Adjust parameters and final values through [verification](verification.md).

### A. Maintained VCO mono bass

- Trial range MIDI 28–55; mono, stereo center, unison 1 per oscillator.
- A saw supplies the body; B saw or pulse is 2–5 cents apart at a lower level. Use C only when a third oscillator has a function. Sub is not mandatory when absent from the target.
- Mixer → best-matching 24 dB/oct low-pass → amp. Start with cutoff 150–400 Hz and an envelope rising to about 1–2 kHz, low/medium resonance, and key tracking suited to the range.
- Amp A/D/S/R around 3 ms / 250 ms / 65% / 70 ms; filter decay around 180 ms with low sustain. Start drift at ±1 cent; noise FM/noise AM off.
- Start glide at 40–90 ms only when requested; specify legato and priority. Light drive before/in the filter when implemented; chorus/reverb initially off.
- Test held notes, overlaps, octave leaps, and fundamental level. This configuration alone does not justify a Minimoog-replica claim.

### B. VCO polysynth brass

- Trial range MIDI 48–84; two saws, 4–7 cents apart; unison 1. Polyphony might be 6, according to the target.
- Use the family's appropriate low-pass filter; base around 500–900 Hz with the envelope rising to 2–5 kHz. Amp and filter follow the brass row in section 3.
- Six-step Voice Control with small pitch/cutoff/envelope differences; convert section 4's targets through UI/readback. Start continuous drift at ±1–2 cents; noise FM off.
- Light pan spread only when appropriate. Start with low saturation; optional short reverb after the dry character is established.
- Test close chords, transposition, repeated notes, and release overlap. If collective vibrato appears, evaluate Main Tuning routes and LFO MONO.

### C. DCO/chorus-family pad

- Trial range MIDI 48–84; one saw/pulse core with a related square sub when needed. Do not start with two widely detuned saws.
- Slow PWM around 0.2–0.5 Hz with moderate duty cycle; low-pass/high-pass as required by the target; one shared envelope when the target links VCA/VCF behavior.
- Amp attack 400–800 ms, release 1–2 s; the filter envelope opens slowly. Start with zero pitch drift; very small voice-timbre differences when needed.
- Chorus provides the main width/motion, with a wet level that retains body in mono. Noise FM and oscillator→Noise Level modulation off.
- Compare chorus off/on at matched levels. For a specific Juno, compare sources/phase/sub/chorus with the reference; generic chorus and independent ADSR routing do not establish circuit replication.

### D. Retro poly pluck/key

- Range MIDI 48–84; one pulse or two oscillators 2–4 cents apart. Amp decay 500–900 ms, sustain 0–15%, release 100–250 ms.
- Filter decay 180–350 ms; cutoff closes faster than amplitude. Add small voice differences in cutoff and envelope rather than large pitch variation at every attack.
- Choose phase behavior to avoid an identical attack zap when inappropriate. Very small drift; optional subtle chorus or dark delay.
- Test rapid repeats and sustain pedal/release overlap when used. Overly fast compression and large reverb can erase articulation.

### E. Expressive VCO lead

- Range MIDI 55–88; saw/pulse, mono, retrigger for detached notes and legato as specified. Try glide at 50–120 ms.
- Amp attack 5–15 ms, release 80–180 ms; the filter follows playing behavior. Start drift at ±1–2 cents.
- Separate performance vibrato from drift: around 4–6 Hz with depth starting at zero via mod wheel/aftertouch; the brief determines the upper limit. Do not apply permanent deep vibrato and call it VCO drift.
- Test note priority, bend range, overlap, and register changes. Label expression features absent from the original gear as adaptations.

### F. Aged/broken variant

Start from a stable version of one recipe, then save a new revision. Add one cause first: larger drift, small noise FM, noise AM for grit, or tape processing after the instrument. Keep **Age** separate from **Drift** so the user can obtain aged spectral color without unstable pitch. Test pitch center, level dropouts, stereo/mono, and tails. Choose this variant only when the brief requests faults or a worn recording.

## 10. Macros and implementation specifications

Macro names describe audible outcomes. Use those that help the patch; the entire list is not required.

| Macro | Candidate destinations | Boundaries to check |
|---|---|---|
| Drift | Pitch-motion depth, not the basic interval | Zero to a musical cents limit; account for the sum of all routes |
| Voice Character | Cutoff/envelope variation and voice offsets when modulatable | Preserve intonation/attack; if static controls cannot be modulated, use a verified alternative route or preset variant |
| Drive | Drive and compensating trim | More than a loudness increase; check chord overload |
| Tone | Cutoff/envelope amount | Measurable endpoints in the target register |
| Width | Appropriate chorus or pan spread | Preserve mono body; do not automatically move bass |
| Age | Recording coloration, noise/bandwidth/wow when implemented | Named mechanisms; do not enable every fault together |
| Space | Delay/reverb wet level | Controlled tails, feedback, and gain |

Add the following notes to the internal design spec, separately from tool JSON:

```yaml
analog_target:
  family: "VCO mono | VCO poly | DCO poly | ensemble | other"
  model_revision: "model/revision or assumed family"
  condition: "maintained | looser | aged/broken as requested"
  claim: "inspired by | approximation | comparison against a reference"
  reference_scope: "dry instrument or recording chain"
  oscillator_relationship: "count, waveforms, intervals, phase/sub relationships"
  polyphony_and_priority: "voice limit, legato/retrigger, glide, note priority"
  voice_sequence: "length, affected oscillators, offset targets and calibration"
  continuous_drift: "shared/per-voice/per-oscillator, rate, target cents, smoothing"
  optional_techniques: "noise FM / noise AM / nonlinearity / tape: reasons for on/off"
  signal_path: "actual modulation taps and processing order"
  historical_adaptations: "additional velocity/MPE/sub/stereo features, if any"
  calibration: "physical target -> tool field/unit -> readback/UI/audio"
  unmet_requirements: []
```

For each route, record source, destination, base, amount, polarity, curve, AUX, OUTPUT, trigger, and effective endpoints. Record macro min/default/max states and interactions. Do not pass this design-metadata block as extra fields in the preset schema.

## 11. Native implementation and tool boundaries

Follow [native build](native-build.md), [tool capabilities](tool-capabilities.md), and the workspace's Serum MCP guide before creating a preset. Call `list_parameters()` for every build and read the current semantic schema. This guide does not authorize guessing unknown raw keys/enums.

This documentation was inspected on 2026-10-16 using runtime `list_parameters()` and the local checkout. Important boundaries include:

| Requirement | Available path | What still needs proof during a build |
|---|---|---|
| Voice patterns and randomness | `voice_unison` with pan/detune/filter_cutoff/env_time lists and random fields | Cents/cutoff/envelope scales; upstream still marks the sequence meaning of `voice_count` uncertain |
| Voice counts | Voicing/polyphony, oscillator unison, and Voice Control are separate states | Do not use one number for all three; inspect native state and UI |
| Phase/RAND/Phase Memory | Verified template/UI/raw state | Friendly OscillatorSpec does not expose every phase option |
| S&H drift | `lfos` with `shape: random_sh`, smooth, mode/rate/sync; available pitch routes | Upstream limits evidence for algorithmic generation; inspect output and distribution/polarity |
| Shared versus poly LFO | Mono field and mode/HOST settings where available | MONO, FREE, and HOST have separate functions; the schema may not expose every switch |
| Noise C → FM A | Verified engine/source and warp/mod-source | Generic `fm` does not guarantee source C; inspect pre/post-filter taps and tracking |
| Audio-rate A → Noise Level | Supported Matrix source/destination | Arbitrary remap curves and stereo noise may not be writable through the friendly schema |
| Per-voice versus bus drive | Oscillator warp/filter drive or FX chain, as supported | Topology, summing point, PRE/POST, and output gain |
| Tape/external FX | Separate DAW workflow when requested | Not automatically stored in `.SerumPreset` |

Unit documentation is inconsistent: the manual describes RANDOM DETUNE in cents, while semantic-tool descriptions use conventions that remain partly uncertain/percentage-like. Upstream inspection has also not calibrated SEQ DETUNE bars in cents. Retain the cents target and read or measure the result; do not invent a conversion. Schema acceptance of `voice_count` does not prove a six-step setting is correct in the plugin.

If a required control is unavailable, use a verified template or available UI, save a new native file, and read it back. If neither path exists, state the unmet detail and candidate status. Do not claim gear emulation is complete simply because JSON passes the schema. `.SerumPreset` files, dependencies, specifications/bindings/receipts, and test statuses follow the workspace contract.

## 12. Verification and troubleshooting

### Targeted tests

Use [verification](verification.md) for structure, loading, rendering, and listening. For analog sounds, add the following checks and record MIDI, velocity, gate, tempo, quality, and macro states:

1. **Dry baseline:** bypass optional processing and level-match against the character version. Attack/body/release and filter type should already approach the target.
2. **Repeats:** play the same note 16–24 times with identical velocity/gates. Observe voice patterns, phase attacks, cutoff, and level. Adjust the repeat count for longer sequences.
3. **Held notes:** hold for 20–30 seconds in low/middle/high registers. Extend the test for slower motion until it covers several updates/cycles. Separate tuning center, cents deviation, beating, regular vibrato, and hiss.
4. **Chords:** use 3/4/6-note chords as appropriate, including release overlap. Check shared/per-voice drift against the spec, voice stealing against the limit, and whether bus drive obscures the chord.
5. **Articulation:** detached, legato, overlaps, register leaps, velocity, and the gestures actually used. Test mono note priority/glide.
6. **Mono/stereo:** check body, channel balance, bass fundamental, and chorus/pan spread. Correlation meters help but do not replace mono listening.
7. **Technique isolation:** bypass voice offsets, drift LFOs, noise FM, noise AM, and drive individually. Judge whether each technique solves a specific requirement.
8. **Macros/level/tails:** min/default/max and extreme combinations, chord peaks, hiss after release, and delay/reverb feedback. Reload the final preset and check dependencies.

When measuring pitch from audio, start with one clean oscillator. FM, noise, strong harmonics, chorus, and chords can mislead pitch trackers. Convert frequency deviation using `cents = 1200 × log2(measured_f / target_f)`; separate the median offset from deviations around that median. Compare references with matched notes/gates and levels, then judge the musical context.

### Diagnosis

| Symptom | Likely causes and focused actions |
|---|---|
| Still static despite pitch wobble | Inspect source shapes/relationships, envelopes, filter response, and phase; more drift does not fix the wrong architecture |
| Out of tune or excessively chorused | Reduce combined offsets + drift + unison + chorus; measure each source; check mean pitch and polarity |
| Every note wobbles together | Main Tuning/shared MONO LFO; use per-voice sources/destinations if required |
| Identical zap at every attack | Inspect phase reset/RAND/memory and LFO retriggering; adjust without weakening bass impact |
| Excess hiss/roughness | Solo sources; check C leakage, noise level, FM bandwidth/amount; bypass compression that raises noise |
| DCO patch is too unstable | Reduce drift/detune; restore core pitch relationships; use PWM/chorus for movement |
| Bass loses body in mono | Reduce chorus/stereo noise/pan on low components; inspect phase, Sub routing, and resonance |
| Chords break up while solo notes are clean | Check gain before bus nonlinearity, active voice count, release overlap, and intermodulation |
| Drift is too fast/slow | Check Hz versus BPM, HOST/retrigger, `rate10x`, global scaling, and smoothing; measure its period |
| Vintage color appears only when louder | Repeat bypass comparisons at matched levels and listen for transients/spectrum rather than loudness |

The final report still separates **structure/readback**, **successful plugin loading**, **render/analysis**, and **actual listening**. This guide is a design document; writing it does not mean its recipes have been tested in the plugin or auditioned.

## 13. Sources and corrections to the attachment

Technique basis: the user's attachment *panduan_analog_sound_serum_2.md*, which attributes five techniques to Undulae Music's video [You can throw away your analog synths now](https://www.youtube.com/watch?v=EWrwVgzyu6U). Attachment-supplied timestamps: [voices 0:44](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=44s), [noise FM 3:10](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=190s), [S&H 4:47](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=287s), [noise modulation 5:44](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=344s), [drive 7:09](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=429s). **The video/transcript could not be accessed during preparation; its title, channel, sequence, and timestamps come from the attachment and have not been independently verified.**

Control behavior was checked against the locally available *Serum 2 User Guide*, plugin 2.0.18/manual 1.0.3: phase pp. 41–44; warp/LPF/FM pp. 49–55; filter/routing pp. 133–151; distortion pp. 167–168; envelopes pp. 183–187; LFOs pp. 191–193; audio modulation sources p. 208; Matrix pp. 209–214; voicing pp. 215–218; Voice Control pp. 316–318. See the [source index](sources.md) for provenance. Additional designs and values were authored for this guide, not quoted or measured from the manual/video.

Primary hardware and context references:

- [Roland JUNO-106 owner's manual](https://cdn.roland.com/assets/media/pdf/JUNO-106_OM.pdf): six voices and a DCO with stable pitch; [Roland's technical article](https://www.roland.com/uk/blog/roland-icon-series-juno-106-synthesizer/) explains the DCO sources and chorus role. These support treating DCO designs separately from VCO drift.
- [Sequential Prophet-6 operation manual](https://www.sequential.com/wp-content/uploads/2019/03/Prophet-6-Operation-Manual.pdf): per-voice pan spread. A Serum pan pattern is a design approximation, not evidence of identical voice allocation.
- [Moog Minimoog Model D manual](https://api.moogmusic.com/sites/default/files/2018-01/Minimoog_Model_D_Manual.pdf): oscillator/mixer path, 24 dB/oct ladder low-pass, and envelope/key-tracking controls. These Serum examples do not claim circuit simulation.
- [Official Serum 2 page](https://xferrecords.com/products/serum-2): product oscillator/routing context. UI details in this guide use the manual version named above; compare them with the installed version.

Main corrections to the attachment: Voice Control sequence length is not the polyphony limit; not all analog gear uses integrated voice chips; phase RAND is not pitch drift; note-to-note randomness differs from continuous drift; noise FM is not a universal VCO/tape model; a digital saw is not automatically rigid because of symmetry; drive/filter order must be explicit; clipping is corrected at its source stage; compression, stereo noise, tape, and external reverb are target-dependent choices.
