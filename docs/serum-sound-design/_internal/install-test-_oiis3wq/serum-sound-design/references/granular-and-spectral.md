# Granular and spectral engines

Manual: granular S2 pp. 85-103; spectral pp. 104-122. Theory of these engines below is supplemental, with control behavior grounded in the manual.

## Granular: design event statistics

Treat grain position, size, spawning, window, pitch, and stereo placement as independent contributors.

| Control | Audible question | Diagnostic |
|---|---|---|
| Source region/position | Which recorded material forms each grain? | Freeze position and compare regions |
| Scan rate/direction | Does the cloud move through material or hover? | Separate scan from grain density |
| Grain length | Fragments, buzz, mini-loops, or overlapping phrases? | Sweep with constant source/density |
| Density | Sparse events versus continuous cloud? | Observe onset build and max-grain limit |
| Window amount/shape/skew | Soft fades versus hard edges? | Listen to isolated/sparse grains |
| Pitch/random pitch | Tonal stability versus detuned/unpitched cloud? | Start with zero random pitch |
| Position/length randomization | Repeated slice versus varied material? | Add one random dimension at a time |
| Pan randomization/unison | Width versus diffuse instability? | Compare mono and channel balance |

The UI density modes are Free (Hz), BPM Sync, and Grains; Jump Start spawns multiple grains at note start, while Max Grains caps overlap/CPU (S2 p. 101). Grain length and density interact: longer grains with the same spawn rate increase overlap. Window choices shape per-grain onset/tail (S2 pp. 91-93), separate from the voice envelope.

Scan moves the playhead; zero freezes it, negative reverses it. Scan key tracking, range, tempo lock, and sample-length-to-BPM alter interpretation (S2 pp. 99-100). The current tool exposes only part of this behavior; consult [capabilities](tool-capabilities.md).

### Authored prototypes

- **Tonal cloud:** pitched sustained source; moderate/long grains; sufficient overlap; small pitch/position variation; slow scan; soft main envelope. Preserve a stable tone path if the cloud lacks a clear fundamental.
- **Fragmented glitch:** transient-rich source; sparse short grains; intentional discontinuities; position jumps; restrained tail. Tempo behavior comes from verified density/scan timing rather than assuming all randomness is on-grid.
- **Frozen atmosphere:** select a rich region; stationary/very slow scan; overlapping windows; low random pitch; slow spectral/filter movement. Reverb extends the result but is not the source of the grain texture.

Tool units: `granular_grain_length` is milliseconds; `granular_density` uses a documented UI-related 0-30 scale, not a universal spawn-Hz argument. `granular_random_pitch` is semitones; random pan/length/offset values use percentages. The tool labels several flags uncertain. Use the UI's established meaning to plan, but treat a particular raw-field mapping as unverified until checked.

## Spectral: design frequency behavior

1. Select source and region. Decide whether original transients/timing should remain recognizable.
2. Establish scan speed/direction, phase-lock and transient behavior before extreme transformation. Spectral time/pitch behavior differs from simple resampling.
3. Define the frequency range for processing. Preserve the low region while transforming upper bands when the fundamental must remain clear.
4. Design a frequency-domain filter curve if required. Cut, Filter, and Mix have separate behaviors (S2 pp. 117-121); a flat curve with shift modulation may produce little useful change.
5. Select a warp mode matching the goal: gating/smearing/robotic change, spectral shift, mask/vocode interaction, or a special moving spectral pattern. Confirm source connections for modes dependent on other oscillators/filters.
6. Audition sustained and transient sources, different notes, and tails; evaluate phasey/smeared artifacts against the requested character.

Spectral warp vocabulary is different from wavetable warp vocabulary. The local tool accepts some raw strings without semantic validation; acceptance by the spec is not proof that Serum recognizes the value. Drawn spectral filter curves and several scan/transient controls are outside its current generated semantic model. A factory/template edit may preserve existing data, but must be inspected and reloaded to prove that preservation.

## Hybrid strategies

Use a clean oscillator for stable pitch plus grain/spectral source for evolving texture. Apply independent envelopes to recorded transient and resynthesized tail. Separate direct fundamental from processed upper texture only when actual routing is implemented. For identifiable vocals, use playback for intelligibility and a parallel transformed layer for atmosphere; synthesis cannot infer missing spoken/sung content from a descriptor.
