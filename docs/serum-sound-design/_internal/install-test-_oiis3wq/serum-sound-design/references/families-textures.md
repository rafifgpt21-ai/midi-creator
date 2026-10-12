# Pads, textures, and instrument analogies

Authored design families; mechanics in the wavetable, sample, granular/spectral, modulation, and effects references.

| Family | Source strategy | Evolution and space | Test |
|---|---|---|---|
| Warm sustained pad | Harmonic body, mild detune, LP shaping | Slow independent color motion, moderate space | Chord changes, low-mid crowding, release polyphony |
| Bright/shimmer pad | Rich/high partials with stable lower body | Upper-layer movement, controlled delay/reverb | High notes/upper macros do not become harsh |
| Dark drone | Lower spectrum and resonant color | Very slow motion, pitch stability or deliberate drift | Long hold remains interesting without unwanted beating |
| Granular cloud | Structured sample through grains | Position/length/density/random variation | Grain build, CPU, low/high notes, dependencies |
| Spectral/frozen texture | Sample resynthesis and spectral band treatment | Scan/warp/curve evolution | Flat-curve tool limitation, transients, spectral smearing |
| Air/breath layer | Noise or suitable recording | Slow/short envelope by role, upper shaping | Noise level fits mix and velocity |
| Choir-like pad | Available choir multisample or formant-rich synthesis | Slow amplitude/formant movement, expressive brightness | Synthetic approximation versus recognizable syllable/sample |
| String-like pad | Bow-like harmonic source/noise or multisample | Slow excitation, mild vibrato, register response | Static chorus alone does not give bow articulation |
| Wind/water/environment | Recording or shaped noise plus event components | Irregular correlated changes, spatial depth | Recognizability if requested; arbitrary noise is not exact foley |
| Hybrid acoustic/electronic | Recorded excitation plus synthesized body/tail | Separate transient and sustained evolution | Layer tuning and time alignment |

## Time-scale design

Pad attack 0.2-3 s and release 0.5-5 s are broad starting experiments, not defaults for every pad. The harmony's rhythm matters: a four-second release through fast chord changes may erase clarity. Give amplitude, color, grain position, and pan distinct but related rates. Randomizing all dimensions strongly tends toward incoherence; small correlated changes can sound more intentional.

For drones/long atmospheres, audition for much longer than an ordinary note. Check loops/seams, static regions, periodic reset, bus tails, and voice stealing. For a performance pad, the default macro positions should provide a usable balanced chord, with brighter/wider extremes still controlled.

## Acoustic instrument requests

Separate **imitation of timbral traits** from **faithful performance recreation**. Identify excitation, resonator, attack noise, partial decay, pitch variation, register, dynamic response, articulation, and recorded-room behavior. Use available multisamples when authentic body/attack across notes is essential. A bowed string needs different excitation behavior from a plucked string; a flute-like fundamental needs air/attack and register-dependent harmonics; a brass imitation needs dynamic spectral changes and articulation.

Serum is capable of hybrid sample/synthesis design, but its engines and finite slot/modulation resources are not a universal physical model. If the requested realism depends on unavailable recordings/articulations, finish a clearly labeled approximation or identify the missing resource. Do not invent a factory instrument, sample library, or load success.

## Texture design progression

Establish a source whose raw structure resembles the requested material. Make the main envelope fit use in music or SFX. Add movement that changes a meaningful sonic dimension over the intended time-scale. Add stereo/space after checking source width and pitch. Verify across sparse and dense chords, mono, low/high register, and long note-off tails.
