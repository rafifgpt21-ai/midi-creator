# Brief komposisi

- Proyek: Synthwave Studio Starter
- Revisi: v001
- Revisi asal: none
- Tanggal: 2026-10-10

## Permintaan asli

Build a framework and MCP for Cubase, with instruments ready as a useful starting point.
Focus on Serum; use drums from `C:\Users\rafif\Music\Sample Bank`.
Serum version: 2.0.23. The main genres are 80s synth music and synthwave.

## Keputusan musik

- Gaya / mood: restrained 80s synthwave sound-check, with room for additional effects.
- Tempo: 110 quarter-note BPM.
- Meter: 4/4.
- Key: A minor; Am(add9), F major, C, G(add9) foundations.
- Panjang: 16 bars, 34.909 seconds.
- Bentuk: atmosphere, bass/drums, arp, lead/brass, release.
- Groove: straight eighth-note bass/arp, four-on-the-floor kick, backbeat snare, alternating hat velocity.
- DAW: Cubase 15.0.20; Serum 2.0.23 VST3 presets; sample drums.

| Layer | Sound | Function | GM hint / drum pitch |
| --- | --- | --- | --- |
| pad | Warm polyphonic Serum pad | harmony | 89 |
| bass | Mono analog-style Serum bass with sub | bass | 38 |
| arp | Short Serum pluck | arpeggio | 81 |
| lead | Restrained unison Serum lead | melody | 80 |
| brass | Polyphonic Serum brass | chord accents | 62 |
| keys | Glassy sine Serum keys | accents | 10 |
| kick | Sample-bank kick | percussion | 36 |
| snare | Sample-bank snare | percussion | 38 |
| closed-hat | Sample-bank closed hat | percussion | 42 |
| open-hat | Sample-bank open hat | percussion | 46 |

## Asumsi dan referensi

The demo is a reusable starting arrangement, not a commissioned finished song. Each sound has a
real .vstpreset created by the installed plugin. These presets are dry foundations for genre-specific
chorus/delay/reverb in Cubase; native Serum modulation matrix and effects insertion are not claimed.
Sample files are copied into the output with source paths and checksums. The original bank is read-only.
`build_composition.py` is deterministic; no random seed is needed. The framework preserves the existing MIDI schema.

## Perubahan revisi

New composition. Existing user projects and references are preserved.

## Kriteria penerimaan dan hasil

- Exactly one MIDI track/instrument per layer; all layers aligned to the same end tick.
- Validate/generate/verify pass; no combined MIDI.
- Serum presets reload with matching changed parameters.
- Stereo audio stems share sample rate and frame count; no non-finite or silent render.
- Framework tests and an actual MCP stdio handshake pass.
- Cubase connection and native project status are reported separately from offline checks.
- Audio is not described as listened to unless actual audition occurs.
- Output: `output/` for MIDI; `studio/` for the full starter bundle.

## Review receipt

MIDI validation, generation, and reopening passed: 10 layers, 468 notes, 30,720 ticks each.
The studio bundle passed checksums, preset state round-trips, and all 10 audio frame-count checks.
All six Serum renders were non-silent and finite; no peak reduction was necessary for the synth stems.
The phrase entries build from pad/keys to bass/drums, then arp and lead/brass. Bass uses a low
register with a sine sub; upper arpeggios and lead have distinct functions. Drum hits are on the
four-beat pulse with backbeat snare and alternating eighth-note hat velocities. The final bar
leaves room for releases. The chords share common tones to limit pad movement.
This is a sound-check starting arrangement, with dry patches and no commissioned final mix.
The audio was rendered through the real installed Serum but was not auditioned.
All 34 framework tests passed, including real Serum inspection and preset save/reload through MCP,
a real MCP MIDI client, and a simulated MIDI Remote host. The opt-in Serum test uses a 60-second
deadline per call; production tools have a 240-second deadline and a bounded 180-second worker.
Isolating worker stdin fixed the MCP launch timeout. The final source also passed a wheel build;
the 40-file starter ZIP passed CRC checks.
A real Cubase handshake succeeded and reported plugin assignment capability. Object discovery
returned the host's no-target sentinel (-1); a selected instrument track is still needed.
Live parameter changes and slot assignment are not yet verified. No native .cpr was created.

Follow-up live check, 2026-10-10: the selected Serum 2 01 track exposed 2,623 plugin parameters.
Main Vol was changed from normalized 0.50 to 0.49 and restored to 0.50, with exact readback
verification of both operations while transport was stopped. Serum appeared in the instrument
slot's eligible-plugin list. New-slot assignment remains untested. Evidence:
`integrations/cubase-live-20261010-072500.json` in the workspace. Earlier receipts remain preserved.
