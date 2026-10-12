# Worked sound-design experiments

These are authored starting designs, expressed in perceptual/UI terms. They are not copied factory patches, exact tool JSON, or auditioned presets. Translate through the current schema, then test. Keep one working baseline and change one cause group per iteration.

## 1. Clean sub with controllable audibility

- A: custom harmonic `[1]` or verified sine-like frame; one voice, repeatable phase if needed.
- Main amp: attack 4 ms, decay irrelevant for held body, sustain high, release 60 ms.
- Optional upper body: restrained harmonic source or light saturation, independently leveled; avoid phase-conflicting low duplication.
- Macros: Harmonics (upper content plus trim), Length (release within useful range).
- Expected: stable pitch and root, clean center, increased upper audibility at the Harmonics macro.
- Check: repeated MIDI 36/48/60 or the requested range, short/held notes, mono, no unintended arp.

## 2. Rounded filter pluck

- A: moderate saw/odd-rich source, one or few lightly detuned voices.
- F1: low-pass, modest resonance; low base cutoff.
- Amp: attack 4 ms, decay 350 ms, sustain 0, release 100 ms.
- Env 2: faster 180 ms decay to zero -> positive cutoff movement, independent from main amplitude.
- FX: small dark delay or room if needed.
- Macros: Tone (base cutoff), Decay (amp plus related filter decay), Space.
- Expected: bright onset settles into rounder tail; held note still decays.
- If flat: confirm Env 2 route, cutoff endpoints, source harmonics, and filter path.

## 3. Electric/FM key

- A carrier: sine/soft harmonic source. B modulation source: simple tone, enabled but low/zero audible level.
- Verify A's FM source points to B. Begin with a harmonic pitch ratio, then change if the brief requires more clang.
- Amp: attack 5 ms, decay 1.2 s, low sustain, release 300 ms.
- Index envelope: faster decay than amplitude; velocity increases initial index and level.
- Optional subtle chorus and small space after dry identity works.
- Expected: harder bright strike at higher velocities, simpler rounded tail.
- Check: actual FM connection, velocity levels, range, no accidental second audible body.

## 4. Reese with protected root

- A/B: saw-rich, near-pitched with small opposing fine offsets; sustained amplitude.
- Keep low-frequency stability through actual routing/filter strategy or a separate clean root when needed.
- Slow movement: shallow filter/table modulation; avoid arbitrary movement on every parameter.
- FX: distortion/EQ on the intended mids, restrained stereo expansion.
- Macros: Motion depth, Aggression plus trim, Width with useful minimum.
- Expected: moving dense body, intentional beats, usable low-end in mono.
- Check: beating speed across register and phase cancellation before adding compression.

## 5. Expressive mono lead

- A: saw/pulse-rich body with restrained detune; F1 for tone.
- Amp: attack 15 ms, sustained body, release 180 ms.
- Mono, optional legato, glide chosen for phrase overlap.
- LFO: centered small pitch motion with delayed/rising depth; wheel/pressure scales it.
- Delay: verified musical subdivision, filtered repeats.
- Expected: articulate detached notes and smooth connected phrase; expression changes vibrato/intensity.
- Check: overlapped/nonoverlapped leaps, pitch-bend range, wheel at zero/default/max.

## 6. Evolving warm pad

- A: harmonic body, few lightly detuned voices; B adds a different spectral contribution if needed.
- Amp: attack 800 ms, sustained body, release 1.8 s.
- Slow independent table/filter motion; small source/voice variation.
- Space: enough to support sustain; avoid doubling long release and huge reverb indiscriminately.
- Macros: Tone, Motion, Width, Space.
- Expected: coherent warm chords with audible evolution and clear harmony changes.
- Check: long holds, dense chords, mono, voice stealing and low-mid build.

## 7. Granular recorded cloud

- Source: actual pitched/structured WAV; document root, region, and dependencies.
- Granular: start with grain lengths near 100-200 ms and moderate density in the tool's documented scale; small pitch/position randomization.
- Slow scan/position evolution through supported fields or verified UI; soft main envelope.
- Add stable pitched source only if the intended cloud needs a strong root.
- Macros: Density/texture, Motion/position, Space; tool support determines exact implementation.
- Expected: overlapping source fragments with recognizable underlying character and evolving texture.
- Check: grain milliseconds, engine selected, scan behavior, max-grains/CPU, dependencies and long hold.

## 8. Spectral robotic texture

- Source: provided voice/texture WAV, spectral engine.
- Choose confirmed spectral warp; process a useful frequency range while preserving or deliberately removing lower body.
- Define source interaction for mask/vocode modes; verify required source enabled state.
- If target requires drawn spectral filter bands, use a supported template/UI path; generated flat curve is insufficient.
- Expected: frequency-domain transformation, not unchanged playback or arbitrary wavetable buzz.
- Check: UI warp recognition, scan/transients, note range, resource loading.

## 9. Bell with a simpler tail

- Carrier plus noninteger-related FM source or a verified metallic table/mode architecture.
- Fast onset; amplitude decay about 2 s; upper index/partials decay faster.
- Velocity controls index/attack, restrained space extends the ring.
- Macros: Metal (index/ratio only within useful bounds), Damping, Space.
- Expected: clear strike, inharmonic ring, tail loses brightness naturally.
- Check: pitch perception, high notes, input level and macro extremes.

## 10. Tuned impact or kick prototype

- A: sine/rounded body; short positive pitch-envelope amount decays down to the desired final note.
- Noise/click component has its own very short contour.
- Amp decay fits event role; impact can have a separate long space/body tail.
- Macros: Punch (transient/pitch burst), Body length, Space when relevant.
- Expected: initial excitation plus settled tuned body; it should not simply be a loud sine.
- Check: final pitch after sweep, short/held gate, repeated hits and peak headroom.

## 11. Deterministic riser

- Source: noise plus harmonic tension if needed.
- Designed one-shot contour over requested seconds/bars -> amplitude, cutoff, pitch/warp, and optional width.
- Establish actual contour duration/trigger using verified LFO-envelope/automation settings.
- FX feedback stays bounded; endpoint/tail specified.
- Expected: energy trajectory reaches endpoint exactly when intended.
- Check: different host tempos, retrigger, short-gate behavior, endpoint and tail.

## 12. Sample-preserving hybrid instrument

- A: sample playback of the identifying attack/voice; align reference pitch and note number.
- B: separately shaped harmonic/granular tail matched in tuning; independent level/envelope.
- Preserve original channel relationship when requested (`sample_center_pan=False` in current tool).
- Macros: Hybrid blend, Tone, Tail, Space.
- Expected: recognizable original transient plus controllable synthesized continuation.
- Check: source identity, transposition/duration coupling, loop seam, root alignment, resource installation.
