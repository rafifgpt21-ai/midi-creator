# Default drum mapping

Choose the mapping by drum layout unless the current request specifies another map. Numeric MIDI pitches are authoritative.

## Separate drum layers: Cubase Sampler

When drums are requested per layer (one sample/instrument per MIDI file, such as kick, snare, closed hi-hat or shaker), use MIDI pitch **60** for every note in each drum layer. This is **C3 in Cubase**, the default sampler root for this workspace. Set each sample's root to C3 and load it on its own Sampler Track. Write integer `60` in `composition.json`; the generator calls this pitch C4, so writing `"C3"` would produce pitch 48. Keep drum layers on MIDI channel 10 and document `C3 (MIDI 60)` for each layer in the README.

If a combined file is also requested, assign distinct pitches to drum parts in that combined kit and document its separate mapping; the per-layer files retain pitch 60. If the export workflow cannot provide both mappings, treat the combined export as requiring a separate specification.

## Single kit: articulation map

For one drum kit with multiple articulations, use the user-supplied map below. The note labels reproduce the user's kit/DAW labels; write integer pitches in `composition.json` rather than converting these labels through the generator's C4 = 60 convention.

This map defines articulations, not a selected sample kit. Load the user's chosen kit/sampler and map its pads to these pitches. Drum layers use MIDI channel 10. Configure hi-hat choke groups in the drum instrument so closed/tight/pedal articulations close open/loose hats.

## Kick

| Kit label | MIDI pitch | Articulation |
| --- | ---: | --- |
| C0 | 36 | Kick Hit |

## Snare

| Kit label | MIDI pitch | Articulation |
| --- | ---: | --- |
| D0 | 38 | Snare Hit (Center) |
| E0 | 40 | Snare Rimshot |
| F#0 | 41 | Snare Rim |

## Toms

| Kit label | MIDI pitch | Articulation |
| --- | ---: | --- |
| A0 | 45 | Rack Tom High |
| A#0 | 46 | Rack Tom Low |
| B0 | 47 | Floor Tom |

## Hi-hat

| Kit label | MIDI pitch | Articulation |
| --- | ---: | --- |
| F1 | 53 | Hi-Hat Tight |
| F#1 | 54 | Hi-Hat Closed |
| G1 | 55 | Hi-Hat Loose |
| G#1 | 56 | Hi-Hat Loose / Semi-Open |
| A1 | 57 | Hi-Hat Open |
| A#1 | 58 | Hi-Hat Open |
| B1 | 59 | Hi-Hat Open |
| C2 | 60 | Hi-Hat Pedal |

Pitches 57, 58 and 59 are all user-defined open-hat articulations. Use 57 as the default open hat; use 58/59 when the selected kit or brief calls for those alternatives.

## Cymbals and ride

| Kit label | MIDI pitch | Articulation |
| --- | ---: | --- |
| E2 | 64 | Crash 1 Left |
| F2 | 65 | Crash 1 Choke |
| A#2 | 70 | Crash 2 Right |
| B2 | 71 | Crash 2 Choke |
| C#3 | 73 | Ride Bell |
| D3 | 74 | Ride Bow |
| D#3 | 75 | Ride Edge / Crash Ride |

## Percussion and FX

| Kit label | MIDI pitch | Articulation |
| --- | ---: | --- |
| F3 | 77 | Shaker |
| F#3 | 78 | Shaker |
| D4 | 86 | Hand Tambourine |
| D#4 | 87 | Hand Tambourine |
| E4 | 88 | Stick |

## Revision checks

Remap existing notes by articulation, using the source revision's map to identify their meaning. Preserve onset, duration, velocity, tempo, meter, global length and mixer settings when the request changes only mapping. Record any substitute for an articulation absent from this map in the revision README/request. For example, snare-rim 41 can replace sidestick, and stick 88 can replace a sparse cowbell accent; these are documented substitutions, not equivalent sounds.

Validate, generate and verify the revised specification. For separate sample layers, confirm every emitted drum pitch is 60 unless explicitly overridden; for a single kit, confirm every emitted pitch belongs to its articulation map. Confirm every event differs from its source only as requested. Keep prior revisions intact.
