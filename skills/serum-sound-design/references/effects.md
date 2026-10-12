# Effects and processing strategy

Source: S2 pp. 152-182. FX-specific ordering and starting recommendations are authored design heuristics; exact tool parameters come from `list_parameters().fx_params`.

## Chain order follows cause

`tone shaping -> nonlinear character -> dynamics -> stereo/motion -> echo/space -> output trim` is a useful prototype, not a rule. Distortion after delay/reverb changes repeats/tails; compression after space changes decay; EQ before distortion changes generated harmonics while EQ after changes the result. Choose intentionally and level-match bypass comparisons.

## Module decisions

| Processor | Purpose | Decisions and failure checks |
|---|---|---|
| Distortion | Add harmonic density, grit, clipping/folding character | Mode, input drive, pre/post filtering, wet, output; check aliasing and fundamental |
| EQ | Shape spectral balance/resonances | Band shape, frequency, gain, Q; avoid replacing missing source behavior with huge boosts |
| Voice/FX filter | Sweep or isolate bands | Cutoff/resonance/type-specific parameter; verify dry/bypass path |
| Compressor | Control dynamics or reshape transient/body | Threshold/ratio/knee, attack/release, makeup, multiband; bypass-match level |
| Chorus | Detuned/moving thickening | Rate/depth/delay/spread/mix; check pitch blur and mono loss |
| Hyper/Dimension | Voice/spatial thickening | Retrigger/unison/depth and short-delay width; preserve center/low band |
| Flanger | Moving short-delay comb coloration | Delay, depth, feedback, polarity/mix; sharp notches may remove body |
| Phaser | Moving all-pass-derived notches | Rate/depth/frequency/feedback/stages where available; check resonance |
| Delay | Rhythmic echoes and spatial repeat | Time/subdivision, ping-pong, feedback, tone, wet; check actual echo interval |
| Reverb | Distance, room/body, sustained space | Predelay, size/decay, damping/filtering, width, wet; preserve attack intelligibility |
| Convolve | Recorded impulse response/body/space | Actual IR, length, timing and filtering; resource dependency and CPU |
| Bode | Frequency-shift/ring-like transformations | Shift versus pitch transpose, mix, feedback/source options; check altered partial spacing |
| Utility | Gain/pan/width/other supported utility control | Actual mode and placement; output trim cannot repair earlier clipping |
| L/H splitter | Independent low/high processing | Crossover, child graph, recombination gains/phase |
| L/M/H splitter | Three-band processing | Crossovers and branch order; inspect graph, not just module count |
| M/S splitter | Mid/side-specific processing | Correct encode/process/decode; mono and channel balance |

Frequency shifting translates each component by an absolute Hz offset, unlike pitch shifting which multiplies frequencies. It can turn harmonic material inharmonic; even a small shift changes low tones proportionally more. Convolution is not synonymous with algorithmic reverb; the IR can be a resonant body or special effect (manual S2 pp. 161, 164-166).

## Rack and bus design

Serum 2 has Main plus two Bus racks. Use aux buses for independently adjustable space/parallel color and Main for desired shared processing. Track each send, bus gain, return destination, processor order, and dry-path contribution. Cascading one bus into another/Main changes effective order and accumulation. Direct bypasses processing according to mixer routing; verify with isolation tests.

A branch splitter changes topology and needs child data. In the current spec `fx_chain` records module/rack and parameter dictionaries but does not expose a full authored splitter graph. Preserve a known graph or use UI for unsupported construction. A generated Convolve module also needs a real resolved IR; default/preserved content is not proof of the requested impulse.

## Space without losing articulation

Separate main release from space decay. Short plucks can carry long echoes; a pad with long release plus long reverb may overwhelm chord changes. Predelay can preserve attack separation. Filter wet paths according to the brief: less low end often keeps bass intelligible, darker repeats recede, bright early reflections increase proximity/air. These are musical choices, not mandatory filters.

For a bass requiring clean low end, keep fundamental on a verified clean route or use an actual frequency split. A global high-pass on the whole instrument defeats that requirement. For wide atmospheric sounds, test side content in mono and avoid confusing stereo loudness with spectral improvement.

## Dynamics and nonlinearities

Set compression time constants around the sound's actual transient and rhythmic interval. Very fast attack can erase punch; slow release can accumulate gain reduction; multiband settings can exaggerate highs/lows. Saturation input matters: a drive change plus output trim is different from simply reducing the source. Compare both sparse and dense/polyphonic passages.

## Completion

Every processor has a declared sonic purpose, all external IRs/resources are resolved, rack order/topology matches the design, and macro extremes/tails retain usable levels. Render/listen where possible; store untested status when only parameters were read back.
