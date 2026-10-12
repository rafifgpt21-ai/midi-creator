# Leads, plucks, keys, and bells

Authored architectures/ranges; source mechanics: S2 pp. 37-84, 183-218. These are starting hypotheses, not genre guarantees.

| Family | Architecture | Time/performance | Failure to avoid |
|---|---|---|---|
| Saw/unison lead | Saw-rich A, optional supporting B, filtered body | Sustained envelope; mono/legato or poly by brief; delay/vibrato | Detune obscures pitch, long tail masks fast notes |
| Singing/whistling lead | Sine/triangle-like body, subtle harmonic layer | Gentle onset, delayed vibrato, wheel/pressure expression | Sterile sustain or excessive continuous wobble |
| PWM/nasal lead | Pulse/square-like source and PWM/band emphasis | Small evolving pulse width, stable amplitude | Extreme duty loses energy; wrong range becomes thin |
| Sync lead | Bright source with sync warp | Sync amount envelope/gesture | Assumed pitch stability without testing warp |
| Brass-like synth | Saw-rich spectrum, filter opening with attack | Amplitude/brightness rise then settle, velocity to bite | Pad-like onset or static brightness on every note |
| Soft pluck | Sine/triangle/filtered source | Zero sustain, fast onset, short color envelope | Held body from accidental sustain or too-long release |
| Bright/digital pluck | Dense table/FM source | Index/brightness falls faster than amplitude | Sharp onset but sustained harshness |
| Chord stab | Poly source with rich midrange | Fast onset, short/medium decay, limited tail | Mono setting prevents chords; unison overloads peaks |
| FM/electric key | Simple carrier + harmonic modulator, optional attack layer | Index/brightness decays, velocity to attack and depth | Body remains metallic after attack; no dynamic response |
| Bell/chime | FM with noninteger-related spectrum or layered modes | Upper partials decay faster, long controlled tail | Generic sine plus reverb lacking metallic onset |
| Mallet | Harmonic/inharmonic body with short attack | Fast decaying upper spectrum, softer body | Too-long bright tail makes it a bell |
| Organ-like | Harmonic-table/additive-like body, optional transient click | Held amplitude, little velocity if style needs, modulation/rotation FX | Treating rotating effect as actual moving-source physics |
| Piano/acoustic keys | Installed multisample or sampled layers | Source envelopes plus velocity/key-range shaping | Claiming faithful piano from one static saw/filter |
| Vocal-like lead | Controlled excitation through formant pattern | Vowel motion, articulation and expressive pitch | Formant sweep mistaken for intelligible words |

## Starting articulation experiments

- Pluck: attack 1-10 ms, decay 150-700 ms, sustain 0, release 50-250 ms. Test held notes to confirm decay and short notes to observe premature note-off.
- Melodic lead: attack 5-40 ms, substantial sustain, release 80-400 ms. Adapt to speed and desired legato.
- Key/bell: attack 1-15 ms, decay roughly 0.4-3 s, low/zero sustain, release appropriate to phrase. Long ringing decay is a source behavior, not only added reverb.
- Brass-like: brightness rises and then settles; main attack roughly 10-80 ms can establish a pronounced swell without pad slowness.

## Register and expression

High notes expose aliasing and detune; low chords expose crowding and phase. Choose key tracking and velocity mappings to preserve identity. A bell's inharmonic upper partials may shift perceived pitch; compare playing pitch and fundamental. Delay rhythm and tail density should support the melody rather than obscure its articulation.

For connected expressive leads, test detached versus overlapping notes: mono, legato, portamento, envelope retrigger, and LFO retrigger are independent. For chord sounds count both sounding notes and release voices when setting polyphony. For acoustic realism use source availability and articulations honestly; deliver a synthetic approximation as such.
