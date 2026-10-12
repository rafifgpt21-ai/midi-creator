# Sources and provenance

## Supplied documents

**S2:** *Serum 2 User Guide*, Xfer Records, plugin version 2.0.18, manual version 1.0.3, April 27, 2025; 354 PDF pages. The source declares its version on PDF p. 2. The guide's printed numbers align with the PDF page numbering used here.

**T:** *Electronic Music and Sound Design: Theory and Practice with Max 7*, Volume 1, Alessandro Cipriani and Maurizio Giri, ConTempoNet, demo excerpt, 122 PDF pages. PDF p. 2 explicitly identifies it as a demo. Printed book pagination jumps between excerpts. A table-of-contents entry is not evidence that the full section text is included.

The workspace guide at `docs/serum-sound-design/README.md` links preserved originals and the internal source receipt with SHA-256 hashes. Installed skills use this provenance/index without depending on the original attachment path. Original synthesis explanations and recipes are paraphrased applications; the references do not reproduce the manuals or the book.

## Serum manual page index

| Topic | PDF pages | Guide using it |
|---|---|---|
| Getting started, Init, native save/embed | 18-22 | Native build |
| Tooltips, controls, pitch, routing, menus | 23-36 | Control map, architecture |
| Table anatomy, phase/random/memory, position/unison | 37-48 | Wavetable/FM |
| Warp modes, source FM/AM, level/pan | 49-57 | Wavetable/FM |
| Multisample sources/envelopes/velocity/timbre | 58-67 | Sample engines |
| Sampler bounds, operations, slices, loops, parameters | 68-84 | Sample engines |
| Granular bounds, windows, XY, scan/density/length/random | 85-103 | Granular/spectral |
| Spectral bounds, range, filter curve, scan, phase/transients | 104-122 | Granular/spectral |
| Sub shapes/pitch/phase | 123-127 | Architecture, bass |
| Noise/sample, one-shot/start/random/pitch | 128-132 | Sample engines, percussion |
| Voice filter types/Var/parameters | 133-143 | Filters/routing |
| Mixer, sends, filters, busses, Main/Direct | 144-151 | Filters/routing |
| FX racks, insertion/reordering/copy/bypass/modulation | 152-160 | Effects |
| Bode | 161 | Effects |
| Chorus, compressor | 162-163 | Effects |
| Convolve | 164-166 | Effects |
| Distortion | 167-168 | Effects |
| EQ, FX filter | 169-171 | Effects |
| Flanger, Hyper/Dimension, phaser | 172-174 | Effects |
| Reverb | 175-176 | Effects |
| L/H, L/M/H, M/S splitters and Utility | 177-182 | Effects |
| Envelopes | 183-187 | Modulation |
| LFO graph, controls, timing, point modulation | 188-200 | Modulation |
| Velocity and note settings | 201-205 | Modulation |
| Macros; oscillator/filter mod sources | 206-208 | Modulation |
| Modulation matrix, curves/polarity/aux/output | 209-214 | Modulation |
| Voicing, mono/legato/poly, portamento | 215-218 | Modulation |
| Clips, piano roll, recording, triggers, MIDI out | 219-243 | Arp/clips |
| Arp patterns, transpose, playback/retrigger/velocity | 244-266 | Arp/clips |
| Keyboard scale/swing/oscillator mapping | 267-273 | Arp/clips, control map |
| Wavetable editor, FFT, frame operations/morph | 274-290 | Wavetable/FM |
| Audio/image imports and embedding | 291-303 | Wavetable/FM, sample engines |
| Formula parser/functions/variables/examples | 304-311 | Wavetable/FM |
| Global preferences/MPE, voice control/scaling | 312-318 | Modulation, control map |
| Quality/compatibility, tuning/MTS-ESP, build version | 319-322 | Control map, QA |
| Main menu/MIDI maps/MPE/render-related commands | 323-326 | Control map, native build |
| Preset browser/loading/preview/metadata/rescan | 327-336 | Native build |
| File types and sound location | 337-344 | Resource packaging |
| LFO shape file location | 345 | Modulation/resources |
| Creating coherent tables and interpolation | 346-347 | Wavetable/FM |
| CPU optimization | 348 | Troubleshooting |
| Keyboard shortcuts | 349-353 | Control map |

The manual's FX module catalog on pp. 161-182 does not provide a separate Delay subsection in its contents, although delay is available in the inspected tool. Delay parameter behavior in this pack is attributed to implementation/schema inspection, not an invented manual page.

## Theory excerpt coverage

| PDF pages | Actual supplied coverage | Limit |
|---|---|---|
| 2-8 | Demo identification, publication details, complete-book contents | Contents include sections not present |
| 9-15 | Foreword/introduction, theory-practice/listening/reverse-engineering approach | Max support assets are not attached |
| 16-33 | Chapter 1T agenda and opening sections: synthesis/processing, frequency, phase/amplitude, level/perception | Later envelopes/intervals/sampling/panning chapters are listed but omitted from this theory excerpt |
| 34-59 | Chapter 1P opening Max practice and partial section list | Not a complete Max course |
| 60-70 | Interlude A opening operators, transposition, tempered/natural interval discussion | Later programming subsections omitted |
| 71-78 | Chapter 2T opening additive spectrum/waveform/spectrogram, harmonic/inharmonic distinctions | Beats/vector/variable-spectrum sections not supplied in full |
| 79-86 | Chapter 2P opening additive partial-amplitude construction/summation/phase | Selected excerpt only |
| 87-94 | Chapter 3T opening noise/subtractive sources, including white/pink noise | Full filter/Q/equation/series-parallel sections omitted |
| 95-104 | Chapter 3P noise generators and interpolation, source types, later-section list | Full filter implementation sections omitted |
| 105-110 | Interlude B opening MIDI/messages/note handling | Later interlude sections omitted |
| 111-115 | Chapter 4T control signals and LFO panning; audio-rate consequence | Later PWM/vibrato/filter control text omitted |
| 116-121 | Chapter 4P panning control/scale/waveform transition behavior | Later practice sections omitted |

## Supplemental and implementation knowledge

Equations for ideal wave harmonics, FM/AM sidebands, Q/order, digital aliasing/Nyquist, detailed envelope choices, descriptor mappings, instrument analogies, recipes, test strategy, and workflow templates are authored supplemental guidance. They are not attributed to absent pages of T. Exact Serum behavior uses S2 when provided; exact file/tool semantics use local implementation.

Implementation inspected: `integrations/serum-mcp/src/serum_mcp/generation/spec.py`, `preset/schema.py`, `preset/mapping.py`, `preset/packer.py`, `preset/safety.py`, tool create/edit code, `docs/PARAMETER_SCHEMA.md`, runtime `list_parameters()`, and workspace `docs/serum-mcp.md`. Snapshot commit is documented in [tool capabilities](tool-capabilities.md). Refresh schemas rather than relying on version-specific remembered values.
