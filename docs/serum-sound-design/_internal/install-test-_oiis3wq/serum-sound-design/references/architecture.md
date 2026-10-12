# Choose an architecture

S2 pp. 28-33 introduces sources/routing; pp. 37-132 covers engines; pp. 133-151 covers filters/mixer. This decision framework is authored from that architecture.

## Engine selection

| Defining requirement | First choice | Alternate when |
|---|---|---|
| Stable harmonic oscillator tone | Wavetable plus subtractive shaping | Add custom harmonics for precise spectral balance |
| Metallic or dynamic sidebands | FM/AM/warp plus independent amplitude/index contour | Use a real sample when the recorded attack defines identity |
| Exact recognizable transient/voice/foley | Sample playback | Granular/spectral when transformation is requested |
| Acoustic-like instrument across notes | Available multisample plus performance shaping | Approximate with synthesis if samples unavailable or user wants synthetic character |
| Clouds, smear, fragments, stretched ambience | Granular | Spectral for frequency-domain structure rather than grain events |
| Frozen/resynthesized/robotic bands | Spectral | Wavetable if a repeating harmonic fingerprint is sufficient |
| Breath, hiss, friction, broad excitation | Noise or sample noise | Granular field recording for a structured texture |
| Fundamental independent of aggression | Separate clean pitched source/path | Filter/split low band when topology supports it |
| Percussive resonant body | Excitation plus FM/comb/resonance | Sample engine for faithful recorded hit |

## Decompose the sound

Use as many components as needed, each with a purpose:

1. **Attack/excitation:** a short pitched sweep, noise burst, click, scrape, or sample.
2. **Body:** stable oscillator/sampler spectrum carrying identity and pitch.
3. **Motion:** evolving table/filter/index/grain behavior.
4. **Tail/space:** oscillator release plus processor decay.

Components need not map one-to-one to slots. A single oscillator with independent amplitude and warp envelopes can provide attack and body. Avoid adding identical full-spectrum sources without identifying what the addition changes.

## Draw the signal path before values

Write a compact graph: `A (body) -> F1 -> Main FX -> output`; `B (FM source, inaudible level) -> A warp source`; `Sub/body fundamental -> Direct`; `Noise -> F2 -> Bus1 reverb -> Main`. This is a design sketch, not a guaranteed preset-tool representation. Verify graph implementation against readback/UI.

Serum 2 has A/B/C source slots plus Noise and Sub, two voice filters, Main/Bus1/Bus2 FX racks, and Direct signal handling (S2 pp. 31-33, 133-182). Each A/B/C slot uses one engine at a time. Resource identity, oscillator input routing, filter output routing, aux sends, bus outputs, and mixer gain are separate decisions. Disable unused sound sources and unintended note generators explicitly when editing a reference.

## Choose voicing and register early

- Bass: test root stability at intended low MIDI numbers; use mono only when the part is monophonic.
- Lead: decide retriggered articulation versus connected legato; glide depends on note overlap/always settings.
- Chords/pads: budget polyphony for held notes plus releases; detuned voices multiply CPU and peaks.
- Percussion/SFX: decide fixed pitch versus keyboard tracking; held-note behavior can be inappropriate for one-shots.
- Instrument emulation: source register and transposition must match the recorded/excitation range.

## Minimal prototype to full voice

Start with a reduced architecture that reproduces the defining temporal and spectral behavior. Add independent transient/noise layers, expression, and processing as evidence requires. A named preset or sound family is a starting hypothesis, not a reason to inherit hidden modulation, arp, gain, or factory-resource assumptions.

Document the architecture before translating units. Completion for this stage is a graph and component table with no unresolved audible paths, plus a test register and rationale for the chosen engines.
