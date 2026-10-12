# Envelopes, movement, and performance

Manual: S2 pp. 183-218; theory excerpt T PDF pp. 113-120. Numerical design ranges below are authored starting points. Current tool fields/units override cached examples.

## Envelope design

Serum 2 provides four envelope sources. UI Env 1 corresponds to `env0`, Env 2 to `env1`, and so on in the current schema. Env 1 controls voice amplitude; other envelopes independently shape filter, pitch, warp/index, or layer level.

| Articulation | Main amplitude prototype | Independent timbral prototype |
|---|---|---|
| Pluck | Fast attack, zero sustain, decay fits note spacing | Brightness/index drops faster than amplitude |
| Struck key/bell | Fast onset, longer decay, zero/low sustain | Upper partials decay earlier; optional brief noise |
| Held bass | Fast controlled onset, high sustain, short release | Short bright burst, then stable body |
| Singing lead | Moderate/fast onset, sustained body | Initial brightness change, delayed vibrato |
| Pad | Slow attack/release, sustained body | Slower independent color envelope/LFO |
| Swell/reverse-like event | Increasing amplitude toward an endpoint | Coordinated brightness/width, abrupt or designed endpoint |

Use hold only for an intentional plateau. Main release starts at note-off; long processor tails remain after voice amplitude fades. Envelope curves change perceived impact without changing nominal duration. The tool's curve controls are 0-100 and their stage mapping is partly inferred; verify before claiming exact exponential law.

Route a brief pitch envelope only to appropriate pitched components. A 1-3 semitone transient can add bite; an octave-scale sweep creates kick/laser behavior. These ranges are hypotheses; judge register and note length. Avoid accidentally bending a modulator and carrier differently unless the evolving ratio is desired.

## Route specification

For every route record:

`source -> destination | base | amount | unipolar/bipolar | curve | auxiliary scaling | trigger/time | intended endpoint range`

A conceptual linear destination is `base + sum(amount * source * aux)`, but actual Serum parameter scaling and clamping may be nonlinear. Compute endpoints in the schema's units, then verify UI/audio. Envelopes are often useful unipolar sources; vibrato around a stable pitch needs centered bipolar modulation. Depth signs and destination meaning must be checked rather than inferred from source shape alone.

## LFO behavior

- **Free:** ongoing phase behavior; verify per-voice versus shared mono configuration.
- **Retrig:** starts from a defined phase with note triggering, useful for repeatable wobble/pluck patterns.
- **Envelope:** follows the shape as a note-related contour rather than indefinitely cycling; check hold/release and trigger behavior.
- **Tempo sync:** uses musical subdivisions rather than Hz; dotted/triplet options modify durations.
- **Delay/rise:** postpone and fade in modulation for expressive vibrato/evolution.
- **Smoothing:** reduces steps and sharp edges; changes the audible rhythmic shape too.

UI LFO 1 maps to `lfo0`. Serum 2 includes ten LFOs, eight macros, and an expanded 64-slot modulation matrix in the inspected implementation. Source/destination availability remains subject to current schema and plugin version.

For the current tool, set `beat_sync=False` explicitly for free-Hz intent and verify `rate` interpretation in the schema; `mode` and sync both matter. Tempo-synced rates are not generically `1/4` floats or plain Hz. `rate10x` and global LFO time scaling can alter effective cycle time. Record the displayed division or measured period when timing defines the sound.

The inspected writer omits `rate=0.0`; it does **not** produce a frozen 0 Hz source. For dormant motion controlled by a macro, scale the route depth to zero and raise it with the gesture, rather than assuming a zero base rate disables the LFO. Use a small nonzero rate for deliberately slow continuous motion, and verify its period.

### Curves and randomness

Use explicit supported curve points for sine/triangle/ramp/custom rhythms. The current tool supports named random/chaotic algorithms separately, not `shape='sine'` as a friendly preset. Do not set both algorithmic shape and drawn curve. Curve `y` uses the implementation's convention; inspect its documentation before designing inverted shapes. Falling two-point curves have an upstream rendering constraint: use a third midpoint, as documented in the semantic schema.

Stepped randomness suits sample-and-hold changes; smooth random/chaotic motion suits organic texture. Keep variation within a perceptually coherent range. A shared LFO synchronizes voices; per-voice motion produces different chord behavior. If high-rate motion resets with every fast arp note, it may appear static; test mono/free-running versus retrigger according to intent.

## Performance mapping

| Gesture | Useful mapping | Verify |
|---|---|---|
| Velocity | Amplitude plus attack brightness/index | Quiet notes remain audible; loud notes retain headroom |
| Mod wheel | Vibrato depth, motion, or brightness | Default wheel position is playable |
| Channel aftertouch | Intensity of all held voices | Host/controller actually sends it |
| Poly aftertouch | Individual note expression | Source exists and behaves per note |
| MPE pressure/timbre/pan | Per-note expressive shaping | MPE enabled, pitch range and host routing agree |
| Key tracking | Brightness, resonance, envelope time | Entire required register remains balanced |
| Release velocity | Release color/length when supplied | Test a fallback when controller omits it |
| Pitch bend | Musical bends | Range, sign, MPE/channel mode, oscillator relations |

MPE sources in the inspected tool include `expr_press`, `expr_timbre`, and `expr_pan`; these alone do not prove the MPE enable flag, pitch range, or host routing was configured. Use verified template/UI settings if semantic fields are absent. Record expression controls that remain untested.

## Macros as a playable interface

Choose a few relevant outcomes rather than filling eight slots by default. Examples:

- **Tone:** cutoff/table/index movement with level compensation.
- **Attack:** main attack, transient level, and brightness contour.
- **Motion:** movement depth; rate only when useful and calibrated.
- **Space:** delay/reverb send/mix and decay within safe musical bounds.
- **Width:** unison/stereo processing with low-band stability.
- **Character:** warp/drive plus compensating output and tone shaping.

Store default values and describe minimum/maximum behavior. Test macros independently and in high-risk combinations such as Drive+Brightness+Space. Avoid naming a control Warmth when its only effect is louder output. A macro with no routes does not provide performance control.

## Mono, legato, and glide

Mono limits simultaneous notes; legato suppresses certain retriggers when notes overlap; portamento changes pitch between notes. They are separate choices (S2 pp. 215-218). Test detached notes, overlap, repeated same pitch, upward/downward leaps, and fast passages. Porta Always and Scaled/curve options affect behavior; use schema confidence and actual tests. Polyphony includes voices sustaining in release, so long pads can steal voices unexpectedly.
