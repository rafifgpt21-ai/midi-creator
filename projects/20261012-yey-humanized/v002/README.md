# Yey — Piano and BBC Discover · v002

**120 BPM · 4/4 · 76 bars · 2:32 · 480 PPQN · F# Dorian, with D natural on D6**

The original piano chord progression and all chord-change positions are preserved. The performances are rewritten around a gentler, more connected piano part and BBC Symphony Orchestra Discover. **The Precision Bass is replaced by bowed BBC Basses.** Cellos carry the recognizable source theme, violas and first violins connect the harmony, and flute/clarinet provide short answers.

Four opening bars remain silent. Piano begins at **bar 5 / 0:08**; import every file from **bar 1**. The last chord remains **B/D#**, with no extra cadence or bars. [Previous v001](../v001/README.md) and [original MIDI](../_internal/references/yey.mid) are preserved.

## Start in Cubase

1. Set **120 BPM, 4/4**, and use **Musical Time Base** on all seven instrument tracks. Set the left locator to **1.1.1.0**.
2. Load your preferred acoustic piano on the piano track. Create six separate instances of **BBC Symphony Orchestra**, select **Discover**, then load each instrument and **Long** articulation from the table below. These are section patches, not solo strings. Select channel **1** or **All** in each plugin.
3. Import each MIDI onto its matching track from **bar 1** using **Import to Left Locator**. For dragging, enable **Import Dropped File as Single Part**. On a fixed-tempo project, **Ignore Master Track Events on Merge** preserves your project tempo.
4. Keep the leading silence and full 76-bar parts. Do not align the first played note of each instrument to bar 1. All files are straight on a 1/32 grid; no swing or onset jitter is added.
5. Retain the BBC CC1/CC11 lanes. Set **Dynamics to CC1**, **Expression to CC11**, with the default mapping. Avoid additional automation on those same controls during the first playback. Balance the piano first, then bring the orchestra up behind it.

These MIDIs do not load patches automatically. All use SMF format 1, exactly one instrument track and channel 1, end at **145920 ticks**, and contain no SysEx, Bank Select, Program Change, key/section markers or extra conductor track.

## Tracks and sound loading

Ranges are **sounding/concert pitches, C4=60**. Cubase may label octaves differently: use MIDI numbers as the reference and **no extra octave transposition**. GM numbers in the internal spec are schema hints; they are not transmitted.

| Track / MIDI | Function | Load on the track | Written range / notes |
| --- | --- | --- | --- |
| [Piano](MIDI/piano.mid) | Foreground harmony and upper contour; open left hand and quiet moving inner voices | Your velocity-sensitive acoustic piano; a warm, clear response suits the writing | F#1–B5 / **30–83** / 489 |
| [BBC Basses](MIDI/bbc-basses.mid) | Sustained bowed roots and original slash basses, entering bar 9 | Discover → Strings → **Basses**, **Long / Long (vib)** | F#1–A2 / **30–45** / 68 |
| [BBC Celli](MIDI/bbc-celli.mid) | Lyrical source theme, revoiced with breaths and smoother register | Discover → Strings → **Celli**, **Long / Long (vib)** | C#3–A4 / **49–69** / 71 |
| [BBC Violas](MIDI/bbc-violas.mid) | Restrained inner common-tone line, entering bar 13 | Discover → Strings → **Violas**, **Long / Long (vib)** | E4–F#4 / **64–66** / 26 |
| [BBC 1st Violins](MIDI/bbc-violins-1.mid) | Upper harmonic line, entering bar 17; steps aside at bars 53–54 | Discover → Strings → **1st Violins**, **Long / Long (vib)** | B4–C#5 / **71–73** / 52 |
| [BBC Flutes](MIDI/bbc-flutes.mid) | Six two-note replies in deliberate cello rests; last response ends during bar 72 | Discover → Woodwinds → **Flutes a3**, **Long** | D#5–A5 / **75–81** / 12 |
| [BBC Clarinets](MIDI/bbc-clarinets.mid) | Six warm descending responses in the two B sections | Discover → Woodwinds → **Clarinets a3**, **Long** | D#4–C#5 / **63–73** / 12 |

Each BBC file has one monophonic section line, rather than stacking a four-note chord in one ensemble patch. The strings remain restrained while the piano supplies the full harmony. The flute/clarinet patches are **a3 sections**. Patch wording may vary slightly by installed version; select the sustained **Long** technique and lock it if needed. No keyswitch notes or articulation changes are written.

## Piano playing and transitions

The new right-hand chord anchors retain three stable voice positions. Across adjacent bars, each voice moves by at most **4 semitones**, averaging **1.296**; **71 of 213** voice transitions retain the same pitch. The widest anchor spans **9 semitones**, and there is no crossing between its voices. The upper bar-anchor line moves by at most **3 semitones**, compared with **19** in the source. These measurements describe the written anchors, not a listening score or every connecting note.

The upper voice has a stronger touch than the accompaniment. Inner figures move quietly, with varied gate and small velocity differences. Low piano notes are open and sparse; once the orchestral bass enters, the piano's left hand moves higher. Held common pitches connect selected changes, while notes outside the next chord release before the change. A handful of brief chord-tone links lead into structural seams.

Bars 13–16 hold the harmony instead of filling every beat. Piano activity reduces under the cello theme and thins again across the last four bars. The second B passage and final A return differ in density, touch and orchestral presence.

**Pedal:** no CC64 sustain pedal is encoded. Connection is written with note lengths and ties. For additional resonance, edit a light pedal lane in Cubase, clearing it at each chord change; retain the written note lengths and avoid carrying the outgoing harmony into the next bar. The files are usable without that optional edit.

## Form and preserved progression

Every chord lasts one bar at its original position. Octave/register changes do not change its root or inversion. D6 is D–F#–A–B.

| Bars | Progression | This revision |
| --- | --- | --- |
| 1–4 | Silence | Original empty lead-in |
| 5–12 | F#m–B/D# ×4 | Piano alone for four musical bars; bass joins at bar 9 |
| 13–16 | F#m–B/D# ×2 | Held piano, violas enter softly |
| 17–20 | F#m–B/D# ×2 | Piano motion returns; first violins enter |
| 21–24 | D6–E–F#m–E/G# | Connected inversions and restrained lift |
| 25–32 | A–E–B–F#m ×2 | Piano leads, clarinet gives selective descending replies |
| 33–48 | F#m–B/D# ×8 | Cello theme starts at bar 33 beat 3; piano becomes lighter, flute answers in its rests |
| 49–52 | D6–E–F#m–E/G# | Strongest brief lift; no brass or percussion swell |
| 53–60 | A–E–B–F#m ×2 | First violins leave bars 53–54 open; clarinet returns with the B passage |
| 61–76 | F#m–B/D# ×8 | Theme returns, six response windows total across the two theme sections; winds leave before the final four bars and the piano/orchestra recede |

The cello preserves all **71 source melody pitch classes in order**, with new octave choices, note lengths and six delayed re-entrances after flute answers. It uses a lyrical ensemble sound. This is a newly phrased arrangement of the motif, rather than an unchanged copy of the former solo-string performance.

## BBC expression and instrument exceptions

**CC1 starts at 100 and stays there. CC11 carries sampled phrase and section curves.** CC7 sets an initial balance, and CC10 sets a slight pan offset. The curves swell within sustained gestures and recede into releases and the ending. Discover has one recorded dynamic layer: level shaping does not create new recorded timbres. Long notes are written for connection; there is no claim of a true legato articulation.

The official manual lists the selected string and wind instruments, Long techniques, sounding ranges, and the default CC1/CC11 assignments. See the [BBC Discover manual](https://d1t3zg51rvnesz.cloudfront.net/p/files/product-manuals/3088/1588857494/BBCSODiscover_Manual_v1.6.pdf) and [current Discover FAQ/manual download](https://support.spitfireaudio.com/en/articles/11815834-bbc-symphony-orchestra-discover-faq).

This revision continues your **user-selected piano** exception from v001 and uses the **BBC library you requested** for every orchestral part. There are no Serum layers, so no native Serum presets are needed or generated. Load the named BBC factory patches manually. The binding map is in `_internal/source/bindings.json`; it records intended instruments, not saved or verified plugin state. No third-party preset files, sample copies or library content are bundled.

## Drums

No drum MIDI or samples are included. The piano supplies the pulse and the bowed bass supplies weight; percussion would change this revision's intimate character. Drum-kit choice and pitch mapping are not applicable.

## Verification and assumptions

- **Validate, generate and verify passed**, exit code 0 and `ok: true`. Seven files have exactly one instrument track each, matching tempo, meter, PPQN and global length, complete note pairs and no same-pitch overlap. All **730 note-ons** are on-grid.
- Independent musical checks confirm all **72 sounding bars** of piano harmony and every bass root/inversion, four-bar silence, original reference checksum, instrument ranges, single-line orchestral writing and flute/cello separation. Piano anchor movement and hand spans were audited separately from MIDI structure.
- `mc-workflow`, `mc-harmony`, `mc-counterpoint`, `mc-development`, `mc-orchestration` and its piano reference, `mc-symbolic-score`, and `mc-ai-tell-audit` guided the rewrite. Strict timing, original harmonic rhythm and open ending take precedence over generic skill suggestions to add timing offsets or alter the form.
- **Cubase connection:** read-only status responded, with BBC-named instrument tracks visible. This establishes bridge availability only. **These MIDI files have not been imported into that session, and these specific patches have not been loaded or tested by the agent.**
- **Preset structure/loading:** no preset files created; named BBC factory patches and your piano require manual loading. **Audio render and actual listening: not performed.** Musical assessment is symbolic, so sample attack/release, playback balance and audible connection still need auditioning in your piano/BBC instances.
- The final chord and 152-second MIDI timeline are locked to the reference. Release notes precede the end, but the acoustic/plugin reverb tail has not been measured; allow that tail to ring when exporting audio in Cubase.

Reproduction script, source analysis, arrangement specification, binding map and audit receipts are stored in `_internal/source/`; `_internal/composition.json` is the verified export snapshot. All producer MIDI links above point to the ready-to-import files.
