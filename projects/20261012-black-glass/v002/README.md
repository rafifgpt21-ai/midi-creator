# Black Glass — v002

Original dark trap R&B inspired by the ominous mood and verse-to-chorus contrast of **The Hills**, with expressive acoustic piano and heavy layered bass drops.

**136 BPM · 68 BPM half-time feel · F minor · 4/4 · 112 bars · 3:17.65 · 13 layers**

The main drops start at **bar 33 (0:56.47), bar 77 (2:14.12), and bar 101 (2:56.47)**. Each combines a low F1 sub, distorted bass octave, kick and crash after a one-beat MIDI break. Piano keeps its dynamics throughout the song.


**Revisi preset v002:** kelima sound Serum didesain ulang untuk aransemen ini. Sub memakai sine bersih tanpa distorsi; grit memiliki serangan filter, saturasi tape dan EQ; pad bergerak pelan; bell memiliki partial atas yang cepat mereda; riser berubah dari gelap ke terang dengan release 20 ms. Seluruh 13 MIDI identik dengan v001, termasuk dinamika piano. Versi ini tetap 136 BPM, F minor, 4/4, 112 bar / 3:17.65.

Gunakan **User > MIDI Creator > 20261012-black-glass > v002**, atau **Load Preset** dari file `Presets/` di revisi ini. Cukup ganti lima preset pada track Serum yang sudah ada; MIDI lama juga dapat tetap dipakai. [v001](../v001/README.md) dipertahankan.

| Layer | Macro dan default | Rentang yang berguna |
| --- | --- | --- |
| Sub bass | BODY 15%; PUNCH 28% | BODY menambah level sine secara terbatas; PUNCH mengatur tambahan serangan singkat. Mulai di default |
| Bass grit | BITE 18%; TONE 25%; ATTACK 35% | BITE: blend distorsi 62–87%; TONE membuka LP; ATTACK menambah pembukaan singkat filter |
| Shadow pad | SHADE 18%; MOTION 24%; SPACE 12% | SHADE menggelapkan tone; MOTION mengatur gerakan filter/pan lambat; SPACE: wet reverb 18–40% |
| Ghost bell | GLASS 28%; ECHO 10%; SPACE 15% | GLASS mengatur partial serangan atas; ECHO: wet delay 13–35%; SPACE: wet reverb 9–23% |
| Tension rise | AIR 15%; TENSION 22%; LIFT 15% | AIR membuka sweep; TENSION menambah resonansi di akhir; LIFT menambah level noise |

Seluruh macro memakai rentang 0–100%. Default adalah titik awal; nilai ekstrem belum didengarkan. Cutoff filter memakai unit normalized, bukan frekuensi Hz yang sudah terkalibrasi. Bell memakai lapisan sine atas, tanpa FM. Pad memakai LFO free 0.085 dan 0.11 Hz; echo bell fixed 220.588 ms cocok dengan eighth note pada 136 BPM.

**Dependensi:** hanya factory wavetable Serum 2 yang telah terpasang (`Analog/Basic Shapes.wav`, `S2 Tables/Analog/DM - OSCAR.wav`, dan `S2 Tables/Default Shapes.wav`, termasuk slot nonaktif). Tidak ada file custom/sample/IR tambahan. [Manifest resource](_internal/resource-manifest.json).

**Status:** struktur/readback lima preset, wire-type scan, resource dan checksum **PASS**. MIDI validate/generate/verify **PASS**; seluruh file sama byte demi byte dengan v001. **Pemuatan plugin native, render/analisis audio dan listening aktual belum diuji.** Analisis FFT hanya memeriksa file wavetable sumber, bukan audio keluaran Serum. Perbaikan di atas adalah target desain; preferensi suara perlu dinilai saat dimuat dan dibandingkan pada level yang sama.

[Receipt QA v002](_internal/revision-qa.json) · [Desain dan rencana audition](_internal/source/sound-design.md)

## Import into Cubase

1. Set the project to **136 BPM, 4/4** and instrument tracks to **Musical Time Base**. Set the left locator to **1.1.1.0**.
2. Create a separate instrument track for each MIDI below. Use your chosen piano for `piano`, Serum 2 for the five synth layers, and your chosen drum sampler/kit for the drum files.
3. Load each native preset from Serum 2's preset menu/browser using **Load Preset**. The presets are also installed under **User > MIDI Creator > 20261012-black-glass > v002**. Refresh/rescan the preset browser if needed. MIDI does not select the sound automatically.
4. Import all MIDI files at **bar 1** using **File > Import > MIDI File > Import to Left Locator**. For drag-and-drop enable **Import Dropped File as Single Part** and place every part at bar 1. Preserve leading silence. **Ignore Master Track Events on Merge** keeps an already correctly configured project tempo.
5. Retain the piano velocities and note lengths. Keep the drum pitches in the table. Each file is format 1 with exactly one track; all files end at bar 113 and use 480 PPQN.

## Tracks and paired sounds

| Track | MIDI | Sound / preset | Useful controls |
| --- | --- | --- | --- |
| Expressive piano | [piano.mid](MIDI/piano.mid) | Your piano; no preset requested | Velocity-sensitive acoustic sound; leave velocity dynamics intact |
| Sub bass | [sub-bass.mid](MIDI/sub-bass.mid) | [sub-bass.SerumPreset](Presets/sub-bass.SerumPreset) | BODY adds sine level; PUNCH controls a brief attack lift |
| Chorus bass grit | [bass-grit.mid](MIDI/bass-grit.mid) | [bass-grit.SerumPreset](Presets/bass-grit.SerumPreset) | BITE adds tape blend; TONE opens LP; ATTACK adds transient color |
| Shadow pad | [shadow-pad.mid](MIDI/shadow-pad.mid) | [shadow-pad.SerumPreset](Presets/shadow-pad.SerumPreset) | SHADE darkens tone; MOTION adds slow movement; SPACE adds reverb |
| Ghost bell | [ghost-bell.mid](MIDI/ghost-bell.mid) | [ghost-bell.SerumPreset](Presets/ghost-bell.SerumPreset) | GLASS adds the short upper partial; ECHO/SPACE add dark delay/reverb |
| Tension rise | [tension-rise.mid](MIDI/tension-rise.mid) | [tension-rise.SerumPreset](Presets/tension-rise.SerumPreset) | AIR opens the sweep; TENSION adds late resonance; LIFT adds noise level |
| Kick | [kick.mid](MIDI/kick.mid) | Your short kick sample; pitch **36** | Strong chorus downbeats |
| Snare | [snare.mid](MIDI/snare.mid) | Your snare center hit; pitch **38** | Half-time backbeat on beat 3 |
| Rim | [rim.mid](MIDI/rim.mid) | Your rim sample; pitch **41** | Soft verse/chorus ghost accents |
| Closed hat | [closed-hat.mid](MIDI/closed-hat.mid) | Your closed hat; pitch **54** | Straight eighths/sixteenths with selected 32nd rolls |
| Open hat | [open-hat.mid](MIDI/open-hat.mid) | Your open hat; pitch **57** | Offbeat lift |
| Crash | [crash.mid](MIDI/crash.mid) | Your left crash; pitch **64** | Main chorus entries and eight-bar punctuation |
| Floor tom | [floor-tom.mid](MIDI/floor-tom.mid) | Your floor tom; pitch **47** | Sparse section-ending fills |

## Song form

| Bars | Section | Development |
| --- | --- | --- |
| 1–8 | Intro | Exposed soft piano, gradual atmosphere, sparse hats and bass hint |
| 9–24 | Verse 1 | Higher, quieter sub, restrained half-time drums, piano question/answer phrases |
| 25–32 | Pre-chorus 1 | Increasing tension; bass drops out for the last two bars; noise rises, then beat 4 of bar 32 is empty |
| 33–48 | Chorus 1 | Deep sub and distorted octave enter together; accented piano hook and denser hats |
| 49–52 | Aftershock | Bass/drums recede, leaving piano and atmosphere |
| 53–68 | Verse 2 | Verse groove returns with individual velocity/gate variations |
| 69–76 | Pre-chorus 2 | Rebuild and one-beat cutoff before the second big entry |
| 77–92 | Chorus 2 | Full bass/drums return with fills and varied piano performance |
| 93–100 | Bridge | Piano and atmosphere exposed; late sparse hats and noise rise into a cutoff |
| 101–108 | Final chorus | Full drop and final eight-bar hook statement |
| 109–112 | Outro | F minor piano resolution and thinning texture; last 1.5 bars allow decay |

The eight-bar harmonic cycle is **Fm9 → Dbmaj7(add9) → Bbm9 → Csus4(b9)/C7(b9)**. The E natural in the dominant is intentional harmonic-minor tension. Piano melody is original; no reference melody was transcribed.

## Piano expression and your sound choice

The piano contains **935 notes**, pitches **36–80 (C2–Ab5, C4 = 60)**, and velocities **18–109**. Inner notes and left-hand support sit below melody accents; phrase crescendos, soft endings, intentionally broken chords, and varied gates provide expressive movement. Onsets remain on-grid, with no swing or random timing jitter.

Use your preferred acoustic piano VST/library, as requested. Load a normal piano patch on its instrument track, import `piano.mid` at bar 1, and enable the patch's velocity response. A warm, slightly dark tone will fit; preserve the difference between quiet inner notes and stronger attacks. No keyswitches, articulation map, or sustain-pedal events are required. Notes of different pitches overlap selectively for connected phrasing. Avoid fixed-velocity processing or heavy compression if you want the written dynamics to remain audible. No piano preset is included.

## Drum character and mapping

Choose a **short, punchy kick** with limited sub tail so the sustained bass carries the chorus weight. A dry, weighty snare with a subtle metallic/clap-like edge suits the beat-3 backbeat; a separate quiet rim gives the verses intimacy. Use dark, crisp closed hats, a brief open hat, a washed crash, and a low, muted floor tom. An F-family tuning can work for a clearly pitched tom; tune by ear against the bass.

All seven files are **MIDI channel 10**, each with exactly one sound/pitch. Numeric pitches above follow your default map; DAW octave names may differ. Map sampler pads by numbers. Put closed/open hats in a choke group so pitch 54 closes pitch 57. Sample choice remains yours; no kit or audio samples were selected or copied.

Separate files include independent CC7 volume and CC10 pan. Use separate sampler tracks to retain those settings, or filter these controllers when routing all parts to one shared kit and set levels/pan per pad. Shared channel 10 cannot carry seven independent kit-wide mixer settings.

## Getting the bass drop to hit

Keep the sub centered. Verse notes are quieter and an octave higher; the chorus moves down to F1 (**43.65 Hz**) at its first hit, uses higher velocities, and adds the separate driven octave. Keep the grit below the clean sub and balance kick against both. These three layers are designed to work together.

The last beat before each main entry has no sounding MIDI notes. Reverb/delay and a chosen piano's release may continue after note-off; duck or mute long effect tails over that beat if you want an abrupt audio cutoff. MIDI velocity and layering establish contrast; the final perceived weight depends on your piano, drum choices and mix.

## Verification and assumptions

- **MIDI validate/generate/verify: PASS**, `ok: true`; 13 files, one track each, identical global end at tick 215040. No SysEx, Bank Select, Program Change, extra text, key or marker events.
- **Timing: strict, straight 1/32 grid, no swing**; zero off-grid note-ons. Gates vary independently of the onset grid.
- **Five native Serum 2 presets: structural/readback PASS**, requested oscillator/filter/envelope/FX/macro/modulation settings match, with SHA-256 receipts. They use installed Serum factory tables; no custom wavetables or sample dependencies were generated.
- Performance audit checks piano dynamics, drop entrances and rests, drum isolation/pitches and chorus-only grit. Harmony, register, groove, phrase space and section contrast were reviewed from note data.
- **Plugin loading: untested. Live Cubase import: untested. Audio rendered/listened to: no.** Structural readback does not establish plugin playback or sound quality.
- Tempo, key, length and form were chosen from the brief. Source seed is 20261012. Technical material is in `_internal/`; no combined MIDI was requested.

[MIDI verification receipt](_internal/verify-receipt.json) · [Preset receipts](_internal/preset-receipts.json) · [Performance audit](_internal/performance-audit.json)
