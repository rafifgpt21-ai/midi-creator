# Symptom-driven troubleshooting

Read [verification](verification.md) for evidence levels. Isolate one source/path at a time; keep a working revision.

| Symptom | Inspect first | Bounded corrective experiment |
|---|---|---|
| Silence | Source enable/volume, main/Direct/bus levels, envelopes, routing, missing resource, arp repeat/chance | Disable note generators and isolate one source to a verified audible output |
| Nearly silent table | Frame content/position, source gain, filter | Audition a known energetic frame; tool documents special low-energy frames for some tables |
| Wrong source identity | Conflicting engine-selector fields, slot index, resource file | Set one intended engine selector per slot and verify native/UI engine |
| Original sample sounds buzzy/unrecognizable | `sample_source` table conversion versus playback | Use `sample_playback_source` when preservation is intended |
| Sample layers clash in pitch | Actual recorded root, fixed reference note, transposition | Measure each layer, isolate, correct semitone/fine offset |
| Sample gets shorter on high notes | Resampling pitch/duration coupling | Limit range, loop sustain, or choose engine/source strategy supporting intended behavior |
| Granular result absurdly tiny/long | Milliseconds versus seconds | Enter `150` for 150 ms in documented semantic field, not `0.15` |
| Grain cloud not moving | Scan/position, density mode, static source region, retriggers | Freeze other controls and verify each intended scan/position control in UI |
| FM has no effect | Source enabled/selection, carrier warp amount, route/ratio | Simple carrier/modulator, source on, low audible modulator, verified source link |
| Resonant/comb sound harsh or unlike reference | Filter type, Var, key tracking, drive, cutoff units | Match type-specific Var and source pitch first; reduce nonlinear stages |
| Filter motion weak | Dry bypass/parallel sources, cutoff endpoints, source harmonics | Solo filtered path and sweep base/depth; then recombine |
| Pluck sustains | Main sustain, sample loop, separate amplitude paths | Set intended main sustain/decay and inspect parallel layers/tails |
| Clicks at onset/off/loop | Phase/discontinuity, zero envelope time, sample seam, stepped routes | Add minimal appropriate attack/release/crossfade/smoothing and retest |
| Low end varies or vanishes in mono | Detune/random phase/duplicate low sources, stereo processors | Isolate root, compare phase states, constrain low-band width |
| Patch biased left/right | Sample imbalance, filter stereo, per-voice pan, rack/bus balance | Inspect documented neutral settings and actual channel levels |
| LFO rate wrong | BPM/HZ flag, `rate10x`, global time scaling, retrigger | Explicit sync state, displayed rate, long held note, period measurement |
| LFO moves despite requested zero rate | Writer omission of `rate=0.0` and inherited defaults | Gate route depth to zero for dormant motion; use a nonzero slow rate when motion is intended |
| LFO appears frozen/too fast | Note reset/mono setting, host clock, short gates | Compare one held note with retriggered phrase and shared LFO |
| Blank/falling LFO curve | Two-point descending shape constraint | Use a third midpoint and verify readback/UI curve |
| Spectral filter shift has little effect | Flat generated spectral curve | Use a real curve through verified template/UI rather than more shift depth |
| Delay interval wrong | Missing beat-sync flag, raw/unit mapping | Explicit free-time seconds or verified synced division |
| Arp stuck/silent/too slow | Actual rate tier, pattern data, repeats/chance, note zone | Test held chord with simple algorithmic pattern and schema-documented rate |
| Notes doubled or timing changes | Internal arp/clip and host MIDI, Thru, swing | Assign one owner for note generation; remove unintended generators |
| Glide absent | Mono/overlap/Always, portamento time, legato | Test a controlled two-note overlap and detached pair |
| Voice cuts during pad/chords | Polyphony, release stacking, unison/grain cost | Reduce unused voices/release or increase available polyphony intentionally |
| Harshness at high register | FM/warp/distortion aliases, resonance, upper spectrum | Lower depth/drive, use appropriate quality and compare actual high notes |
| FX too loud/muddy | Wet/dry doubled paths, bus gains, makeup, long release+space | Bypass-match level, mute returns, restore stages incrementally |
| Native load fails/crashes | Format/wire types, unsupported raw enum/payload, version, resource state | Use upstream parser/type scan and known-good Init; fix before live retry |
| Name/path differs from spec | Sanitization and edit renaming | Use returned actual path; verify file and revision receipt |
| Preset works only on original machine | External tables/samples/IR/factory dependency | Package custom files and document required factory content/installation |
| Measurements contradict UI/ear | Detection range, FFT window, pitch ambiguity, transport test conditions | Verify algorithm assumptions with a simpler held-note/control experiment |

For CPU/dropouts read S2 p. 348: manage unison, polyphony, quality and expensive processing before concluding the design itself is broken. A saved preset may depend on global preferences/tuning/quality behavior; record those separately where not stored per preset.
