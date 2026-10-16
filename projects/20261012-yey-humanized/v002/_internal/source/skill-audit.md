# Post-arrangement audit

This is the `mc-ai-tell-audit` review of symbolic arrangement evidence. No audio-quality score is assigned without audio. Seed: 20261014. Backend: workspace MIDI generator; note pitches, onsets, gates, velocity and CC are exact; patch attack/release, timbre, sonic depth and audio dynamics are untested.

| Flag | Finding |
| --- | --- |
| 1. All sections eight-bar multiples | No: four-bar held/transitional segments are retained for musical/source reasons. |
| 2. Energy only increases | No in design: held section, lighter cello entrance, B2 subtraction and final retreat. Audible RMS untested. |
| 3. Same instrumentation all the way | No: piano starts alone; bass, viola, violin, cello and winds enter successively; clarinet and flute leave early. |
| 4. One loop throughout | No: alternating A harmony, borrowed D6 transitions and four-chord B passages all preserved. |
| 5. Periodic fills | Deliberate piano connectors at bars 20, 24, 52, 60 and 71; responses serve gaps rather than a drum-fill template. |
| 6. No instrumental hook | Piano's held top/quiet inner motion and recognizable cello source theme are specified. Memorability requires listening. |
| 7. Flat dynamics/spectral centroid | Velocity hierarchy, density and CC11 arcs vary. Actual spectral/loudness measurements unavailable. |
| 8. Fully gridded timing | Intentional exception: workspace strict timing policy; no swing/offset request. Naturalness pursued through phrasing and touch. |
| 9. Default 3:30 with no ending design | Source-fixed 2:32; final B/D# retained, winds gone and dynamics reduced; audio release tail unmeasured. |
| 10–14. Vocal sameness, breath, ad-lib and tuning | Not applicable: instrumental arrangement. |

Voice-leading checks passed: 72 piano chord bars match the source; bass inversions match; right-hand anchor voice travel <=4 semitones and span <=9; orchestral supporting notes remain chord tones for their whole gates; cello pitch-class sequence retained; flute has no cello overlap. Full symbolic results are in `musical-audit.json`.

The stable viola and violin ranges are intentional common-tone supporting lines, not solo melodies. The cello and piano carry the changing foreground; forcing more string movement would compete with them. Discover section samples and Long techniques are documented honestly; no fake solo, legato-transition or timbral dynamic-crossfade claims.

Skill generic exports that suggest sending Program Change, textual metadata or extra controller types were not applied: the workspace's MIDI contract and current schema remain authoritative.
