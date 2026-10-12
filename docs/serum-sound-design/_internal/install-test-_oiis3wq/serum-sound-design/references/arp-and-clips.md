# Arpeggiators, clips, and note ownership

Manual: clips S2 pp. 219-243; arp pp. 244-266; keyboard/scale/swing/mapping pp. 267-273.

## Choose who generates notes

| Requirement | Use | Consequence |
|---|---|---|
| Host MIDI already contains the complete phrase | External MIDI; internal arp/clip inactive | Timing and pitches remain owned by the composition |
| Held chord becomes a repeated pattern | Arp | Test held input notes, note order, gate, repeats, clock |
| Preset contains an authored phrase | Clip | Document trigger, transposition, clip length, loop, MIDI out |
| Held voice gains rhythmic timbral gates | LFO/amplitude routes | Does not generate separate MIDI notes by itself |

Combining these can retrigger, double notes, or change intended pitches. Layer generators only when requested. In this workspace strict on-grid/no-swing is the default; swing requires explicit user intent. Dotted notes and other meters can still be musically appropriate.

## Arp design

Specify note-selection pattern, pitch/transpose pattern, rate, gate, retrigger policy, velocity behavior, range/wrap, chance/repeats, latch, key zone, swing, and transport relationship only as needed. Distinguish algorithmic order from an explicit custom pattern. For custom patterns record positions, pitches relative to input/root, lengths, ties/overlaps, and pattern duration.

Gate near 100% fills each step; above 100% overlaps and can engage legato; below 100% creates separation. Release and delay tails can still bridge gaps. Chance/repeats can make a held input go silent; diagnose those before assuming a broken oscillator. Thru adds the held notes alongside generated notes in supported configurations.

The current tool `ArpSpec.rate` is normalized with discrete divisions. Its documentation gives empirical tiers, not a timeless universal mapping. Around 0.5 is documented as a 1/16 tier for the inspected revision; verify at the actual host tempo and mode. Do not pass Hz into it. Several clock/retrigger fields are marked uncertain and need live checking. Pattern stepping and algorithmic arp may interact differently with these settings.

## Clip design

The UI supports clip banks, piano-roll editing, grid, length, triggering, recording, transposition, and MIDI out. The inspected semantic preset schema has an `arp` field but no general clip-bank authoring field. For internal clips use a confirmed UI/template workflow; external MIDI is an alternative only when acceptable to the brief. Report which mechanism was delivered.

Test key-triggered clip selection against playable notes, transposition/key/scale behavior, loop endpoint, transport start/stop, and note-off handling. A scale constrain setting can alter pitches; record it. Host support/routing determines whether generated MIDI reaches another instrument. Saving a native preset does not create the host's MIDI routing.

## Completion checks

Hold the intended input chord for multiple cycles; start on and off the transport grid; release and replay; change input while playing; test pattern wrap and note-off. Measure onsets if exact subdivision matters. Preserve the external MIDI composition's tempo, meter, start position, and total duration when sound design accompanies music generation.
