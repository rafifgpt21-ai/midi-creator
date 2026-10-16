# Black Glass — v003 chord piano

**136 BPM · 68 BPM half-time feel · F minor · 4/4 · 112 bars · 3:17.65 · 13 layers**

This revision replaces the piano with fuller, simultaneous chords, connected extended voicings, longer holds and sparse melodic answers. Bass drops, drums and five Serum sounds are preserved from v002. The main drops remain at **bars 33, 77 and 101**.

## Replace the piano in an existing project

Replace the old piano MIDI part with [piano.mid](MIDI/piano.mid), starting at **1.1.1.0**. Keep your chosen piano sound. The other twelve MIDI files and all five presets are identical to v002, so existing tracks can remain in place.

Piano is now dominated by chord strikes rather than broken-chord accompaniment: **94.4% of its note-ons belong to simultaneous groups of four or more notes**. The 19 short melodic answers occur at selected phrase endings, leaving most bars focused on harmony. Top voices receive more weight than inner notes; bass-hand notes stay softer. Section/phrase dynamics, rests and varied releases provide expression. Timing is still straight and on-grid, without swing, rolled attacks or random timing jitter.

## Import the complete bundle into Cubase

1. Set the project to **136 BPM, 4/4** and instrument tracks to **Musical Time Base**. Set the left locator to **1.1.1.0**.
2. Create one instrument track per MIDI. Use your piano, five Serum 2 instances and your selected drum sampler/kit.
3. Load the native Serum preset paired below through Serum's **Load Preset** menu/browser. These are unchanged v002 sounds; the installed bank remains **User > MIDI Creator > 20261012-black-glass > v002**. Local copies are included in this revision's `Presets/`.
4. Use **File > Import > MIDI File > Import to Left Locator**, importing every file at bar 1. For drop, enable **Import Dropped File as Single Part** and place all parts at bar 1. Preserve leading silence. **Ignore Master Track Events on Merge** retains the already configured project tempo.
5. Keep the piano velocities and gates. Every MIDI is SMF format 1 with one track, 480 PPQN, and the same global end at bar 113 / tick 215040.

## Tracks, MIDI and sounds

| Track | MIDI | Preset / instrument | Macro defaults and use |
| --- | --- | --- | --- |
| Chord piano | [piano.mid](MIDI/piano.mid) | Your chosen piano; no preset | Preserve velocity response and note lengths |
| Sub bass | [sub-bass.mid](MIDI/sub-bass.mid) | [sub-bass.SerumPreset](Presets/sub-bass.SerumPreset) | BODY 15% adds level; PUNCH 28% adds short attack lift |
| Bass grit | [bass-grit.mid](MIDI/bass-grit.mid) | [bass-grit.SerumPreset](Presets/bass-grit.SerumPreset) | BITE 18% adds tape blend; TONE 25% opens LP; ATTACK 35% adds attack color |
| Shadow pad | [shadow-pad.mid](MIDI/shadow-pad.mid) | [shadow-pad.SerumPreset](Presets/shadow-pad.SerumPreset) | SHADE 18% darkens; MOTION 24% adds slow filter/pan motion; SPACE 12% adds reverb |
| Ghost bell | [ghost-bell.mid](MIDI/ghost-bell.mid) | [ghost-bell.SerumPreset](Presets/ghost-bell.SerumPreset) | GLASS 28% adds short upper partial; ECHO 10% / SPACE 15% add dark echoes/room |
| Tension rise | [tension-rise.mid](MIDI/tension-rise.mid) | [tension-rise.SerumPreset](Presets/tension-rise.SerumPreset) | AIR 15% brightens; TENSION 22% adds late resonance; LIFT 15% raises noise |
| Kick | [kick.mid](MIDI/kick.mid) | Your kick sample | Pitch **36**, channel 10 |
| Snare | [snare.mid](MIDI/snare.mid) | Your center-hit snare | Pitch **38**, channel 10 |
| Rim | [rim.mid](MIDI/rim.mid) | Your rim sample | Pitch **41**, channel 10 |
| Closed hat | [closed-hat.mid](MIDI/closed-hat.mid) | Your closed hat | Pitch **54**, channel 10 |
| Open hat | [open-hat.mid](MIDI/open-hat.mid) | Your open hat | Pitch **57**, channel 10 |
| Crash | [crash.mid](MIDI/crash.mid) | Your left crash | Pitch **64**, channel 10 |
| Floor tom | [floor-tom.mid](MIDI/floor-tom.mid) | Your floor tom | Pitch **47**, channel 10 |

## Form and piano phrasing

| Bars | Section | Piano and arrangement |
| --- | --- | --- |
| 1–8 | Intro | Soft sustained chords, exposed voicings, a short answer at bar 4; gradual atmosphere |
| 9–24 | Verse 1 | Restrained chord comping with small answers at bars 12/20; higher quiet bass |
| 25–32 | Pre-chorus 1 | More chord pressure and tension, bass withdrawal, rise and final-beat cutoff |
| 33–48 | Chorus 1 | Fuller chord accents and restrained stepwise responses over the heavy bass drop |
| 49–52 | Aftershock | Longer harmony and one gentle answer while drums recede |
| 53–68 | Verse 2 | Varied inversions and comping; a few additional responses |
| 69–76 | Pre-chorus 2 | Dynamic build, then a one-beat MIDI break |
| 77–92 | Chorus 2 | Strong chords with a small rhythmic variation, preserved bass/drum arrangement |
| 93–100 | Bridge | Spacious long holds and exposed piano, late rebuild into cutoff |
| 101–108 | Final chorus | Strongest chord dynamics and final short answers |
| 109–112 | Outro | F minor resolution, soft chord holds; last 1.5 bars reserved for decay |

Harmony follows **Fm9/Fm7 → Dbmaj9 → Bbm9 → Csus4(b9)/C7(b9)**. Inversions and octave/register choices vary the piano without changing the harmony underneath. Suspended F is released before the C7 E enters. Dominant E natural and b9 Db are intentional. The improvisations are short authored melodic fragments; the reference song's melody was not transcribed.

## Your piano sound

Piano range is **MIDI 36–75 (C2–Eb5, C4 = 60)**, with **958 notes** and velocities **26–104**. Use your preferred velocity-sensitive acoustic piano VST/library, loaded with a normal piano articulation; no keyswitch or drum mapping is required. No piano preset is included, as requested.

Keep the difference between softer left/inner voices and stronger top voices. A warm dark tone fits the track. Avoid fixed-velocity playback and heavy compression that erases the phrase dynamics. Sustain-pedal CC is not present; note holds, selective overlap between different pitches and varied releases supply connected phrasing. Optional pedal/reverb can be added in the DAW, but keep chord changes and drop cutoffs clear.

## Drums and bass weight

Choose a short, punchy kick whose sub tail leaves room for the sustained bass; a dry weighty snare with a little metallic/clap-like edge; a quiet rim; dark crisp closed hats; brief open hats; a washed crash; and a muted low floor tom. The snare anchors beat 3 in the half-time groove. Sample choice remains yours; no concrete samples were selected or copied.

Map by the numeric pitches in the track table, following your default kit map; octave labels vary by DAW. Put pitches 54/57 in a hat choke group. Separate drum files each use one pitch and channel 10, with independent CC7/CC10. Use separate sampler tracks to retain volume/pan settings, or filter these controllers when using a shared kit and set gain/pan per pad.

The first chorus root is F1 / **43.65 Hz**, paired with a driven octave, kick and crash. Keep sub centered and balance grit below it. All three major drops retain the final quarter-note MIDI gap. Piano/plugin releases and reverb may continue after note-off; duck long tails in that gap if you want an abrupt audio cutoff.

## Preset dependencies and verification

- Five native presets are exact v002 copies; previous structural parameter readbacks are retained, copied SHA-256 hashes match, and native wire-type scans pass for the delivered files. Installed Serum 2 factory tables are required: `Analog/Basic Shapes.wav`, `S2 Tables/Default Shapes.wav`, and `S2 Tables/Analog/DM - OSCAR.wav`. No custom wavetable/sample/IR installation is needed.
- MIDI **validate/generate/verify PASS**, `ok: true`; 13 single-track aligned files, strict straight grid, zero off-grid note-ons. No SysEx, Bank Select, Program Change, extra text/key/marker events.
- The twelve non-piano specifications and MIDI exports match v002 exactly. All v002 presets remain unchanged. v001/v002 are preserved.
- Performance audit checks simultaneous chord dominance, dynamic variation, fill locations, harmony boundaries, repeated-key separation and the three pre-drop gaps. Musical review used note data.
- **Plugin loading, live Cubase import, rendered-audio analysis and listening: untested.** The user's selected piano has not been auditioned; natural expression is encoded in performance data, with audible results dependent on the chosen piano.
- Piano revision seed **2026101203**; other layers retain original seed 20261012. Tempo, key, meter, length and section layout are preserved. No combined MIDI or audio was requested.

[MIDI verification](_internal/verify-receipt.json) · [Revision audit](_internal/revision-audit.json) · [Preset readback receipts](_internal/preset-receipts.json) · [Resource manifest](_internal/resource-manifest.json)
