---
name: serum-preset-qa
description: Verify, audition, troubleshoot, and iteratively improve Serum 2 sounds or presets against a brief, distinguishing structural, plugin-load, rendered-audio, and listening evidence.
---

# Verify the sound and its artifact

Read [verification](../serum-sound-design/references/verification.md) and [troubleshooting](../serum-sound-design/references/troubleshooting.md). Use the evidence template in [templates](../serum-sound-design/references/templates.md).

1. Turn the brief into observable acceptance checks. Prioritize identity/articulation over incidental polish. Confirm the exact revision and file hashes being evaluated.
2. Structural pass: decode the native file, scan unsafe wire types where supported, compare spec/readback and unchanged edit regions, resolve every dependency, verify copied-file hashes, and check link/loading documentation.
3. Plugin pass when available: load the exact delivered native file in real Serum 2, record version/host, inspect missing resources and control readouts, play notes, and reload after saving. A decoded file is not evidence of successful plugin loading.
4. Render/listening pass when available: audition the intended range, three velocity levels, short and held notes, repeated notes, overlaps, chords when appropriate, macro endpoints, expression, mono/stereo, and tails. Compare to references at matched levels with identical note/timing conditions. Record whether a render was analyzed, listened to, or both.
5. Diagnose the largest failure by isolating oscillator, routing, envelope, modulation, or FX stages. Propose a cause, make a bounded change in a new revision, and repeat the check that failed plus adjacent behavior affected by that change. Keep the previous working revision.
6. Deliver the best verified revision and a receipt listing passed, failed, and untested checks. For absent host/audio access complete offline verification and provide the focused audition plan; never mark unheard behavior as passed.

Complete when the user's constraints have supported pass/fail statuses, files and resources are consistent, and remaining uncertainty is accurately stated. Measurements support decisions but do not replace audible judgment about musical identity.
