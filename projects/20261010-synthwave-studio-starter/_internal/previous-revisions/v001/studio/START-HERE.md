# Neon Workshop - Serum Synthwave Starter: Cubase starter

110 BPM | 4/4 | 16 bars

1. Create a separate Cubase project. Set its sample rate, tempo, and meter to the values above.
2. In MediaBay, browse this bundle's presets folder and create an instrument track from each Serum VST preset.
3. Import each matching MIDI onto that instrument track at bar 1. Keep the leading silence.
4. For drums, import the audio stems at bar 1, or load the copied samples into Groove Agent SE pads using drum-kit.json's MIDI numbers.
5. Save the result as a new .cpr and optionally use File > Save as Template for future sessions.

| Track | Instrument | Preset | MIDI | Audio |
| --- | --- | --- | --- | --- |
| Serum - Warm Neon Pad | Serum 2 | [preset](presets/pad.vstpreset) | [MIDI](performance/midi/layers/pad.mid) | [stem](audio/pad.wav) |
| Serum - Night Drive Bass | Serum 2 | [preset](presets/bass.vstpreset) | [MIDI](performance/midi/layers/bass.mid) | [stem](audio/bass.wav) |
| Serum - Skyline Arp | Serum 2 | [preset](presets/arp.vstpreset) | [MIDI](performance/midi/layers/arp.mid) | [stem](audio/arp.wav) |
| Serum - Midnight Lead | Serum 2 | [preset](presets/lead.vstpreset) | [MIDI](performance/midi/layers/lead.mid) | [stem](audio/lead.wav) |
| Serum - Retro Brass | Serum 2 | [preset](presets/brass.vstpreset) | [MIDI](performance/midi/layers/brass.mid) | [stem](audio/brass.wav) |
| Serum - Glass Keys | Serum 2 | [preset](presets/keys.vstpreset) | [MIDI](performance/midi/layers/keys.mid) | [stem](audio/keys.wav) |
| Drums - Kick | Drum samples / Groove Agent SE | drum-kit.json | [MIDI](performance/midi/layers/kick.mid) | [stem](audio/kick.wav) |
| Drums - Snare | Drum samples / Groove Agent SE | drum-kit.json | [MIDI](performance/midi/layers/snare.mid) | [stem](audio/snare.wav) |
| Drums - Closed Hat | Drum samples / Groove Agent SE | drum-kit.json | [MIDI](performance/midi/layers/closed-hat.mid) | [stem](audio/closed-hat.wav) |
| Drums - Open Hat | Drum samples / Groove Agent SE | drum-kit.json | [MIDI](performance/midi/layers/open-hat.mid) | [stem](audio/open-hat.wav) |

Serum state reload and MIDI structure are verified. Audio was rendered, not listened to.
The .vstpreset files are Cubase/VST3 presets, not Serum's proprietary .SerumPreset format.
Program changes in MIDI are GM hints; keep the intended Serum preset when importing.
Rendered stems stop at the composition end; leave silence in the specification when a long release is wanted.
Using MIDI and its rendered audio together doubles that part: choose one playback source per track.
