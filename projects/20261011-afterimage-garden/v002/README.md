# Afterimage Garden — v002 drum update

**108 BPM · 4/4 · 104 bars · approximately 3:51 · one drum layer**

This is the requested drum-only revision. Replace the old drum MIDI with [disco-kit.mid](MIDI/disco-kit.mid). Use it alongside the six unchanged Serum layers and presets in [v001](../v001/README.md). The song's harmonic context remains D minor.

## Import in Cubase

1. Keep the existing song at **108 BPM, 4/4**. Set the drum track to **Musical Time Base** and the left locator to **1.1.1.0**.
2. Load your chosen mapped kit in **Groove Agent SE**, your existing drum plugin, or a MIDI sampler. Assign the used numeric pitches below; receive MIDI channel 10. The new guide defines articulations, not a sample-kit selection.
3. Replace the old drum part with this file using **File > Import > MIDI File** and **Import to Left Locator**. On an already configured project, **Ignore Master Track Events on Merge** preserves the project tempo. For drop, enable **Import Dropped File as Single Part**, then position the part at bar 1.
4. Preserve the four-bar opening silence. The first hit remains in **bar 5**; the file extends to the start of **bar 105**. Configure hat choke groups so tight/closed/pedal hits close loose/open hats.

| Track | MIDI | Instrument / controls |
| --- | --- | --- |
| Disco Funk Kit | [disco-kit.mid](MIDI/disco-kit.mid) | Your chosen external drum kit; channel 10; CC7 = 101, CC10 = 64 |

No synth MIDI or Serum preset was regenerated. Existing v001 synth files remain the companions for this drum update. The drum kit is the only external instrument; no keyswitches or new plugin/library are required. Its used numeric range is **36–88**.

## Mapping changes

The [default drum guide](../../../docs/default-drum-map.md) contains every supplied pitch, including unused alternatives and choke articulations. Numeric MIDI values are authoritative; the guide preserves your kit's note labels rather than the generator's octave naming convention.

| Articulation / role | Old pitch | New pitch | New kit label |
| --- | ---: | ---: | --- |
| Kick | 36 | 36 | C0 |
| Snare center | 38 | 38 | D0 |
| Snare rimshot | 40 | 40 | E0 |
| Sidestick ghost / intro hit → **snare rim** | 37 | 41 | F0 |
| Rack tom high | 47 | 45 | A0 |
| Rack tom low | 45 | 46 | A#0 |
| Floor tom | 41 | 47 | B0 |
| Tight hat | 17 | 53 | F1 |
| Closed hat | 42 | 54 | F#1 |
| Loose / semi-open hat | 21 | 56 | G#1 |
| Open hat | 46 | 57 | A1 |
| Pedal hat | 44 | 60 | C2 |
| Crash left | 49 | 64 | E2 |
| Crash right | 55 | 70 | A#2 |
| Ride bell | 53 | 73 | C#3 |
| Cowbell accent → **stick** | 56 | 88 | E4 |

**Substitutions:** the new map has no explicit sidestick or cowbell. Snare rim 41 replaces sidestick; stick 88 replaces the sparse cowbell accents. Their timing and velocity are preserved, but their timbres depend on the new kit. Open-hat alternatives 58/59, loose hat 55, shakers and tambourines are unused; no additional hits were introduced.

## Form and drum sound

The original beat and dynamics remain: restrained intro, syncopated verses, four-on-the-floor chorus pulse, open-hat accents, quiet ghosts, descending high/low/floor tom fills, and sparse cymbals/ride bell.

| Bars | Section |
| --- | --- |
| 1–8 | Intro; first drum hits in bar 5 |
| 9–24 | Verse 1 |
| 25–32 | Lift 1 |
| 33–48 | Chorus 1 |
| 49–56 | Prismatic interlude |
| 57–64 | Verse 2 |
| 65–72 | Lift 2 |
| 73–88 | Final chorus |
| 89–100 | Outro; percussion ends before the last pad chord releases |
| 101–104 | Release space, no new notes |

Use a short round disco kick, dry snare with a little room, articulate tight/closed/loose/open hats and warm descending toms. Keep the stick accents quieter than the backbeat and cymbal tails clear of the bright synth arp. For vintage density, start with gentle tape saturation and drum-bus compression near **4:1**, **10–20 ms attack**, **80–140 ms release**, **3–5 dB gain reduction**, adjusted by ear. MIDI carries performance, not audio compression. Individual drum gain/pan belongs in the kit mixer; MIDI CC7/CC10 affect the whole kit.

No sample kit was selected or copied. Load your chosen samples/plugin using this map.

## Verification

- Validate, generate and verify passed: format 1, exactly one drum track, 480 PPQN, channel 10, **199,680 ticks**, **1,375 notes**, no SysEx, Bank Select or Program Change.
- Strict straight 1/16 grid, on-grid, **no swing**. Every onset, gate, velocity, tempo/meter, mixer setting and total length matches v001; only pitches were remapped.
- All emitted pitches belong to the new map. Tom sequence preserves high → low → floor, hat roles and crash left/right remain distinct, and substitutions are disclosed above.
- All prior v001 MIDI and preset checksums remain unchanged. Technical receipts, specification and reproducible remap script are under `_internal/`.
- Cubase import, kit/plugin playback and listening were **not tested**. No audio rendered or native `.cpr` created. No new Serum presets are needed for this drum-only request.
