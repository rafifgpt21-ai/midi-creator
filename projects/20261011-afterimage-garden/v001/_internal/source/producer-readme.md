# Afterimage Garden

**108 BPM · D minor · 4/4 · 104 bars · approximately 3:51 · seven instrument layers**

An original instrumental psychedelic pop arrangement: sweeping Juno-inspired pads, bright arpeggios, a warm chorus hook, thick phasing bass, offbeat synth keys, an airy harmonic halo, and disco-funk drums. Minor-key verses open into major-colored choruses. All six pitched layers use Serum 2.

## Start in Cubase

1. Set your project to **108 BPM, 4/4**, every instrument track to **Musical Time Base**, and the left locator to **1.1.1.0**.
2. Create six Serum 2 instrument tracks and one drum instrument track. Open each native preset inside Serum using its preset browser or **Load Preset** command. They are also installed under **User / MIDI Creator / 20261011-afterimage-garden / v001**. On another computer, copy `Presets/` files into Serum 2's User preset folder and rescan.
3. Import matching MIDI using **File > Import > MIDI File** with **Import to Left Locator**. On a project already set to the correct tempo, **Ignore Master Track Events on Merge** preserves its tempo. For drag-and-drop, enable **Import Dropped File as Single Part** and place every part at bar 1.
4. Preserve leading silence. The lead first enters in bar 21; do not move its first note to bar 1. Every file ends at the start of bar **105**, including four bars of release space.
5. Load your chosen kit in **Groove Agent SE**, your existing drum plugin, or a MIDI sampler. Map the numeric drum pitches below and receive channel 10. Configure exclusive choking between open/loose and closed/tight/pedal hats.
6. Begin with saved synth macro values and adjust balances against your actual kit. The arp rhythm is written into MIDI; keep Serum's internal arp disabled.

These are native `.SerumPreset` files, loaded inside Serum. Their factory dependencies are **DM - OSCAR**, **PWM Juno**, **Basic Mini**, and **Harmonic Series Smooth**. These files exist in the local Serum library; no custom wavetable or external sample is required by the synth patches.

## Tracks and sounds

Melodic pitch names use C4 = MIDI 60. Drum names follow your supplied guide; numeric pitch takes precedence over a DAW's octave labels.

| Track | Function / MIDI range | MIDI | Native preset | Macros 1–4 |
| --- | --- | --- | --- | --- |
| Juno Memory Pad | Slow detuned saw/PWM harmony, chorus and filter breathing; 53–67 / F3–G4 | [juno-pad.mid](MIDI/juno-pad.mid) | [juno-pad.SerumPreset](Presets/juno-pad.SerumPreset) | BRIGHT, CHORUS, SPACE, PWM COLOR |
| Hypnotic Phase Bass | Mono root/octave/fifth groove with phaser; 31–53 / G1–F3 | [phase-bass.mid](MIDI/phase-bass.mid) | [phase-bass.SerumPreset](Presets/phase-bass.SerumPreset) | BITE, PHASE, SUB BODY, SATURATION |
| Prismatic Arpeggio | Bright short plucks, eighth pulse and sixteenth lift runs; 70–88 / Bb4–E6 | [prism-arp.mid](MIDI/prism-arp.mid) | [prism-arp.SerumPreset](Presets/prism-arp.SerumPreset) | BRIGHT, ECHO, SPACE, LENGTH |
| Afterimage Hook Lead | Chorus motif, gentle delayed vibrato, sparse answers; 57–81 / A3–A5 | [afterimage-lead.mid](MIDI/afterimage-lead.mid) | [afterimage-lead.SerumPreset](Presets/afterimage-lead.SerumPreset) | BRIGHT, ECHO, SPACE, COLOR |
| Velvet Synth Keys | Mellow offbeat chord stabs; 57–67 / A3–G4 | [velvet-keys.mid](MIDI/velvet-keys.mid) | [velvet-keys.SerumPreset](Presets/velvet-keys.SerumPreset) | BRIGHT, CHORUS, SPACE, DECAY |
| Halo Air Texture | Quiet high harmonic atmosphere; 82–91 / Bb5–G6 | [halo-texture.mid](MIDI/halo-texture.mid) | [halo-texture.SerumPreset](Presets/halo-texture.SerumPreset) | AIR, COLOR, SPACE, CHORUS |
| Disco Funk Kit | Kick/backbeat, articulate hats, tom fills and sparse cymbal/percussion accents; 17–56 | [disco-kit.mid](MIDI/disco-kit.mid) | Your selected external drum kit | User map below |

All macros start at **0%**; base patches already include their intended effects. BRIGHT/BITE/AIR open the filter; SPACE adds reverb; ECHO adds delay; CHORUS adds chorus; PHASE increases phaser wet amount; SUB BODY increases direct triangle support. PWM COLOR/COLOR change oscillator color; SATURATION adds tape wet amount; LENGTH/DECAY lengthen amp decay. Raise gradually. Pad/halo use slow free-running movement. Bass triangle bypasses filter/FX to support stable low end. Arp/lead echoes are fixed at **277.78 ms**, an eighth note at 108 BPM.

## Song form

Two bars per chord. Verse: **Dm9 – Bbmaj7 – Fmaj9 – Cadd9**. Lift: **Gm9 – Bbmaj7 – Dm9 – Cadd9**. Chorus: **Bbmaj7 – F/A – Cadd9 – Dm9**. The outro resolves to Dm9.

| Bars | Section | Development |
| --- | --- | --- |
| 1–8 | Intro | Pad/halo first; restrained bass, arp and drums enter in bar 5, sidestick later. |
| 9–24 | Verse 1 | Syncopated bass/kick and quiet stabs; arp gaps, low hook previews near the end. |
| 25–32 | Lift 1 | More regular kick, rising density, sixteenth arp runs in the last four bars, tom pickup. |
| 33–48 | Chorus 1 | Brighter harmony, four-on-the-floor kick, open hats, main hook and sparse cowbell. |
| 49–56 | Prismatic interlude | Rhythm drops back; descending melodic responses, then drum/bass density returns. |
| 57–64 | Verse 2 | Short verse return with low melodic replies. |
| 65–72 | Lift 2 | Eight-bar buildup and tom pickup. |
| 73–88 | Final chorus | Stronger dynamics, extra lead answers, occasional rimshot and late ride-bell accents. |
| 89–100 | Outro | Notes and pad velocities diminish; stabs/arp leave, rhythm retreats, Dm9 remains. |
| 101–104 | Release tail | No new notes; space for pad release, reverb and echoes. |

## Drum character and production

Choose a **short, round acoustic/disco kick**, **dry snare with a little room**, sharp rimshot, crisp hats with distinct tight/loose articulation, and warm descending toms. Keep cymbal tails restrained so the arp stays clear. Sidestick ghost notes should sit below the main backbeat; cowbell and ride bell are occasional accents.

For the requested compressed vintage sound, start with gentle tape saturation and drum-bus compression around **4:1**, **10–20 ms attack**, **80–140 ms release**, and **3–5 dB gain reduction**, then adjust by ear. A short snare room/plate and restrained parallel compressed return add density. Separate kick and bass low end; a little kick-triggered bass gain reduction can help. These are mixing starting points: **MIDI contains the performance, not audio compression or saturation**.

You supplied a drum map but no specific kit/sample selection. **No drum samples were selected or copied.** One kit MIDI sends **CC7 = 101, CC10 = 64**, applying to the whole kit. Set individual drum gain/pan in its mixer. Each melodic file has its own initial CC7/CC10 values.

| User note | MIDI pitch | Articulation | Used |
| --- | ---: | --- | --- |
| C1 | 36 | Kick Hit | Yes |
| C#1 | 37 | Snare Sidestick / Cross Stick | Yes |
| D1 | 38 | Snare Hit (Center) | Yes |
| D#1 | 39 | Snare Flam | No |
| E1 | 40 | Snare Rimshot | Yes |
| F#1 | 42 | Hi-Hat Closed | Yes |
| G#1 | 44 | Hi-Hat Pedal (Foot Close) | Yes |
| A#1 | 46 | Hi-Hat Open | Yes |
| F0 | 17 | Hi-Hat Tight | Yes |
| A0 | 21 | Hi-Hat Loose / Semi-Open | Yes |
| F1 | 41 | Floor Tom Low (Tom 4) | Yes |
| G1 | 43 | Floor Tom High (Tom 3) | No |
| A1 | 45 | Rack Tom Low (Tom 2) | Yes |
| B1 | 47 | Rack Tom High (Tom 1) | Yes |
| C#2 | 49 | Crash 1 (Left) | Yes |
| A2 | 57 | Crash 1 Choke | No |
| G2 | 55 | Crash 2 (Right) | Yes |
| B2 | 59 | Crash 2 Choke | No |
| D#2 | 51 | Ride Bow | No |
| F2 | 53 | Ride Bell | Yes |
| A#2 | 58 | Ride Edge / Crash Ride | No |
| E2 | 52 | China / FX Cymbal | No |
| F#2 | 54 | Splash | No |
| G#2 | 56 | Cowbell / Percussion Hit | Yes |

## Instrument outside Serum

Only drums use an external instrument: **Groove Agent SE or your mapped kit plugin/sampler**, for drum articulations and sample playback. Load your chosen kit, map used pitches above, and configure hat choking. A generic GM kit needs custom mapping for **17, 21, 55 and 56** to match your guide. No other external instruments or keyswitches are required.

## Verification and assumptions

- **MIDI validate/generate/verify: PASS.** Seven format-1 files, one track each, 480 PPQN, 199,680 ticks each, 3,839 notes total; identical tempo/meter/global start and length. Leading silence preserved. No SysEx, Bank Select or Program Change.
- **Strict straight 1/16 onset grid, on-grid, no swing.** Groove comes from syncopation, accents, velocity and gate variation. No onset jitter, strum offsets or performed flams.
- **Native preset structure/readback: PASS.** Six patches generated through serum-mcp, described and decoded; oscillator/filter/envelope/LFO/FX/macro/global values and modulation routes match specifications. The arp patch's internal arp is disabled. Factory dependencies exist locally. Checksums and upstream revision are in `_internal/preset-receipt.json`.
- Musical review covered harmony, register, bass/kick interplay, phrase rests, density, transitions and release space. Tempo, key, duration and instrumental form were chosen from the brief. All motifs are original; no source recording or vocal was supplied.
- **Plugin loading: not tested. Cubase import: not tested. Audio rendering: not performed. Listening: not performed.** Structural checks do not establish installed-plugin sound. Studio status reports Serum 2.0.23 installed; final balance, macro response and drum compression need auditioning with your kit.
- No combined MIDI or native Cubase project was requested or produced. Source, binding, mapping, schema, audit and receipts are grouped under `_internal/`. Producer deliverables are this README, `MIDI/` and `Presets/`.
