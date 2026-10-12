# Recreate a reference by controlled comparison

The theory excerpt promotes listening, analysis, and reverse engineering (T PDF pp. 12-13); the workflow below is an authored implementation.

## Preserve evidence

Record source path/hash, chosen time interval, sample rate/channels, and whether it is a full mix or isolated event. Preserve the original; derive crops/level-adjusted comparisons separately. For a named existing preset, locate exact path/version and describe its state. Name/folder search is only a retrieval aid, not sonic analysis.

## Analyze attack, body, tail

| Region | Observe | Initial causes to test |
|---|---|---|
| Attack | Time to peak, click/noise, brightness burst, pitch sweep | Envelope curve, short noise/sample layer, pitch/index envelope |
| Body | Fundamental, harmonic/noise balance, resonant bands, sustain | Source spectrum, filter, ratio/warp, layer balance |
| Motion | Period, phase, depth, repeatability, note-trigger relation | LFO, beats, arp, automation, grain scan |
| Tail | Note-off relation, exponential/irregular decay, echoes | Release, sample tail, delay/reverb/convolution |
| Stereo | Centered fundamental, different upper channels, changing correlation | Unison, pan motion, short delays, spatial processing |

Distinguish a repeating note pattern from a modulated held note. Distortion may hide fundamentals; spectral peaks may belong to other instruments. Echoes can look like repeated notes. Brightness may come from mixing/EQ rather than the preset. Write hypotheses with confidence and plausible alternatives.

## Measurements when useful

- Waveform/envelope: onset, attack/decay shape, gate/tail duration, clipping, discontinuities.
- STFT/spectrogram: partial trajectory, resonant bands, transient versus body spectrum.
- Pitch tracking: fundamental/glide/vibrato when monophonic and sufficiently tonal; manually inspect confidence.
- Autocorrelation/onsets: repeating modulation or note rate; check half/double-time ambiguity.
- Stereo/RMS/correlation: channel imbalance and width; correlate by band for low-end stability if relevant.

Use more than one FFT window for transient versus sustained analysis if needed. Align comparisons by onset and pitch and use the same analysis settings. Spectral centroid alone does not identify a timbre; two very different sounds can share it.

## Build competing prototypes only when ambiguity matters

Try a simple subtractive versus FM body, or sample playback versus resynthesis when those hypotheses explain different observations. Keep the dry amplitude contour comparable. Select by which candidate explains the reference, then discard incidental complexity. A reference cannot uniquely reveal every underlying parameter; the goal is audible behavior, not an unsupported assertion of identical architecture.

## Iteration order

1. Match pitch/register and note/gate behavior.
2. Match attack/body amplitude and basic spectral distribution.
3. Match time-varying brightness/partial structure.
4. Match motion timing/depth and retriggers.
5. Match width and space; include defining FX earlier when needed.
6. Add expression and polish without destroying the match.

Maintain: `revision | largest mismatch | hypothesis | changed controls | predicted result | measured/heard result | retain/revert`. One coherent cause group per change supports diagnosis. Level-match; compare dry and wet separately when accessible. Stop when acceptance criteria are met, or when the next improvement requires unavailable evidence/capability; state unresolved gaps accurately.

## Existing preset references

Inspect source engines/resources, modulation destinations, voicing, global timing/quality, all FX racks, routing, arp/clip behavior, and defaults omitted from the file. A description may omit custom curves or rely on version-specific defaults. Copy to a new revision before edits. Preserve requested properties and compare unchanged sections/resources; do not rebuild from a partial summary if exact preservation is required.

For references with layered instruments, choose either a single hybrid voice or multiple presets according to the user's scope. The workspace composition contract uses separate instruments/layers when creating an arrangement; a one-sound request can legitimately combine components inside one Serum preset.
