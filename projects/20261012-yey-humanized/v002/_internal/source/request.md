# Yey — piano and BBC Discover rewrite, v002

## Permintaan asli

> make new version of this project use the same based piano chord progression and use the new skill to improve the piano playing and make the transition between chord mor smoothe and natural sounding
>
> add additional instrumen from bbc orchestra discoveries vst if you thing it suits the vibe, re write everityng and remove the p bass to use the bass from bbc orchestra
>
> use skills that you thing will be helpfull and make it better

## Keputusan musikal

- Revision of `v001`; preserve all 72 sounding bars of harmony, four empty opening bars, 120 BPM, 4/4, 76 bars, 480 PPQN and final B/D#.
- Warm, intimate instrumental piano/orchestra treatment. Piano remains the foreground instrument; no percussion or brass escalation.
- Rewrite piano as a playable two-hand accompaniment/melody: connected inversions, quieter inner notes, open left hand, legato melodic notes, and less activity under the cello theme.
- Replace the electric Precision Bass with BBCSO Discover **Basses / Long**. Rewrite its performance for sustained bowed bass; keep every root/slash-bass pitch class.
- Split the former chord strings into monophonic BBC **Violas / Long** and **1st Violins / Long**; recast the source theme for BBC **Celli / Long**, and rewrite **Flutes a3 / Long** answers. Add **Clarinets a3 / Long** for warm responses in the B sections.
- Use strict straight 1/32 note-on grid. The piano is a fresh performance, so the source's old rolled off-grid timing is not retained. No random onset jitter or swing. Human character comes from voice leading, gate, dynamic hierarchy, phrase contour and rests.
- BBC CC1 is held at 100; CC11 carries the phrase/section level contour. Discover has one recorded dynamic layer: these are level changes, not timbral crossfades. No legato articulation or solo string patch is assumed.
- Continue the project's explicit user-selected piano/library exception to the Serum default. All six orchestral layers use the newly requested BBC library. No Serum layers or synthesized piano substitute, hence no Serum presets in this revision.
- No added bars or MIDI pedal messages. Sustaining note lengths and shared tones provide connection; optional chord-by-chord pedal editing is explained in the README.

| Layer ID | Target | Function | GM hint (0-based) |
| --- | --- | --- | --- |
| piano | User's piano VST | Harmony / upper melodic contour | 0 |
| bbc-basses | BBCSO Discover Basses, Long | Bowed bass | 43 |
| bbc-celli | BBCSO Discover Celli, Long | Lyrical theme | 42 |
| bbc-violas | BBCSO Discover Violas, Long | Inner harmony | 41 |
| bbc-violins-1 | BBCSO Discover 1st Violins, Long | Upper harmony | 40 |
| bbc-flutes | BBCSO Discover Flutes a3, Long | Airy phrase responses | 73 |
| bbc-clarinets | BBCSO Discover Clarinets a3, Long | Warm B-section responses | 71 |

## Asumsi dan referensi

Source MIDI remains at `../_internal/references/yey.mid` relative to the revision. Exact source analysis is copied beside the script; fixed seed **20261014** affects only small piano velocity variation. Original/reference files and v001 remain intact. Musical decisions use mc-workflow, mc-harmony, mc-counterpoint, mc-development, mc-orchestration (including the piano reference), mc-symbolic-score and mc-ai-tell-audit. Workspace composition schema takes precedence over the skills' generic MIDI emitter suggestions.

## Perubahan revisi

All instrumental performances are newly arranged; the progression and global timeline are the fixed reference. P-bass and unspecified solo-strings/ensemble patches are removed from v002. Piano rhythms/voicings are rewritten rather than preserving its 445 original note-on events. The source melody remains recognizable through its pitch-class material, voiced and phrased for cellos.

## Kriteria penerimaan dan hasil

- Seven one-track SMF-1 MIDI files, all 145920 ticks, 120 BPM, 4/4, 480 PPQN.
- Validate/generate/verify exit 0, `ok: true`, strict grid, no overlapping same-pitch notes.
- Bar-by-bar harmony/root/slash-bass match; common-tone ties never sustain a non-chord tone across an unsupported boundary.
- Piano right-hand anchors span at most an octave, voice crossings absent; record measurable voice-leading movement and comparison to v001.
- BBC parts fit official sounding ranges, independent line per section, clear entrance/exit and CC1/CC11 expression.
- Producer README links every file and explains patch loading, concert pitch, CC, import and verification limits.
- Cubase status may be inspected read-only; live MIDI import, actual patch playback and listening require separate evidence. They are not implied by MIDI validation.
