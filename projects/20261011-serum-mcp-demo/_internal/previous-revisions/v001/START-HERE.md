# Serum MCP: preset uji

Preset native: [PD - Warm Motion MCP.SerumPreset](native-verified/PD%20-%20Warm%20Motion%20MCP.SerumPreset).

File yang sama sudah dipasang di browser Serum 2:
`User > MIDI Creator > 20261011-serum-mcp-demo > v001 > PD - Warm Motion MCP`.
Buka preset itu di Serum 2 dan mainkan chord sekitar C3-C5.

Target sound: pad analog hangat, attack 650 ms, release 1.7 detik, gerakan wavetable
perlahan, chorus, dan hall reverb. Empat macro: BRIGHT, MOTION, SPACE, COLOR.
MOTION/SPACE/COLOR mulai dari nol sebagai kontrol tambahan ketika dimainkan.

Koneksi MCP nyata, file native, dan readback struktural lulus;
lihat [receipt](native-verified/receipt.json) dan [deskripsi](native-verified/description.txt).
Preset belum dimuat pada instance Serum sebenarnya, belum dirender, dan belum didengarkan.

[Spesifikasi desain](preset-spec.json), [brief dan asumsi](request.md), dan
[panduan instalasi/workflow](../../../docs/serum-mcp.md) tersimpan untuk penggunaan ulang.
Server `serum-mcp` telah didaftarkan di Codex; restart koneksi Codex/T3 Code untuk
memuat tool baru ke sesi berikutnya.
