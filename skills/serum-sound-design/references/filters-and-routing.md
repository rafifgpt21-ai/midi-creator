# Filters, mixer, and topology

Source: S2 pp. 31-33, 133-151; FX filters/splitters pp. 170-182. Supplemental filter theory is in [theory](theory.md).

## Choose a filter by function

| Function | Candidate | Checks |
|---|---|---|
| Remove upper harmonics/round body | LP 12/24, modeled low-pass | Fundamental level, resonance peak, drive |
| Remove rumble/isolate attack | HP | Body loss, resonance, stereo low band |
| Emphasize a resonant band | BP | Center movement, bandwidth, output gain |
| Hollow/moving spectral gaps | Notch | Phase cancellation and useful depth |
| Vocal-like resonances | Formant/filter combination | Vowel centers independent of fundamental |
| Plucked resonant/metallic body | Comb/resonant variants | Pitch tracking, decay, feedback, Var meaning |
| Aggressive source transformation | Distortion/comb/ring-mod hybrids | Added harmonics, nonlinear gain, actual type-specific controls |

The Var/Fat/extra control is filter-type dependent (S2 pp. 135-143). A numeric value copied across types can mean a different operation. Resonance is not universally Q and cutoff's tool-normalized value is not necessarily the UI frequency in Hz.

## Two filters

For serial shaping, verify the first filter actually feeds the second. For parallel colors, document source split and both output paths, then evaluate recombination. For different components (tone versus noise), verify source assignment/balance, not just that two filters are enabled. A bypassed dry component can make a filter sweep seem weak; a silent unused filter can make readback look complete without affecting sound.

Use key tracking to keep a resonant body/brightness behavior sensible across register when the brief needs it. For fixed formants, deliberately avoid full note-following. With resonant combs, pitch tracking and Var determine perceived body; test exact notes and tuning, not only one middle note.

## Mixer graph

Serum 2 separates oscillator/filter routing, aux sends, three FX racks, Main/Direct output, and bus level/destination. Document each edge:

| Node | Required information |
|---|---|
| Source A/B/C/Noise/Sub | Enabled, main destination, filter balance, bus sends, level/pan |
| Filter 1/2 | Input assignment, wet/dry, output routing, bus sends, output gain |
| Bus 1/2 | Rack, level, return destination, tail behavior |
| Main | Rack order, output gain, summed headroom |
| Direct | Which sources bypass filters/FX and aggregate level |

An aux send adds another path; it does not necessarily replace the main path. A clean sub routed Direct bypasses the effects, so it will not acquire the distortion/reverb character of Main. This is desirable only when the design calls for it. Verify amplitude/release behavior of the direct route in the plugin.

## Tool-specific cautions

`OscillatorSpec.filter_routing` and `FilterSpec.output_routing` are different fields. `filter_balance` has uncertain exact scale in the inspected implementation. `FilterSpec.stereo=50` is the documented neutral setting there; zero is not an assumed neutral pan/width value. Use field confidence and real readout. Bus level values may exceed 1 in raw representations; unity/headroom assumptions must use documented units.

Splitters in FX create branch graphs. Confirm nested child chains and gains are represented/preserved; writing `FXSplit` in a flat list alone does not prove multiband processing. When limited, prefer a simple verified graph that achieves the brief or use a confirmed template/UI route for the full graph.

## Test routing in isolation

Solo or disable one source at a time; bypass each filter; mute bus returns; compare Direct/Main. Every audible component should respond to the controls expected for its route. Recombine and test low/high notes, stereo/mono, and long tails. Structural parameter presence is evidence of stored settings; audible control influence is separate evidence of path behavior.
