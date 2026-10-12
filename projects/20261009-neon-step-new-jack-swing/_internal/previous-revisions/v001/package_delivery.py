"""Package verified per-layer MIDI exports without creating a combined MIDI."""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

base = Path(__file__).resolve().parent
output = base / "output"
validation = json.loads((output / "validation.json").read_text(encoding="utf-8"))
assert validation["ok"]
assert len(validation["files"]) == 15
assert all(info["ok"] and len(info["tracks"]) == 1 and info["end_tick"] == 368640
           for info in validation["files"].values())

readme = """# Neon Step — New Jack Swing

108 BPM | F# minor | 4/4 | 96 bar | sekitar 3:33 | 15 layer.

1. Ekstrak arsip ini.
2. Atur project DAW ke 108 BPM dan meter 4/4.
3. Impor seluruh file di midi/layers/ pada bar 1, beat 1, masing-masing ke track terpisah.
4. Pertahankan keheningan di awal file; bass/gitar sengaja masuk setelah intro dimulai.
5. Pilih instrumen/preset sesuai nama layer. Gunakan kit drum machine, gated snare,
   slap bass, Rhodes, muted guitar, synth brass, saw synth lead, pad dan FM bell.
6. Drum memakai channel 10 dan mapping GM/GM2. Shaker memakai pitch 82 (GM2);
   pada kit lain, arahkan note 82 ke sample shaker. Instrumen bernada memakai
   channel 1 dalam file masing-masing dan perlu instrumen DAW tersendiri.
7. Timing swing 60:40 sudah ditulis pada event. Pertahankan timing saat impor.

summary.md memuat tautan ke 15 MIDI, request.md memuat keputusan dan mapping,
musical-review.md memuat audit musikal. composition.json adalah snapshot sumber.
validate/generate/verify lulus: satu track per file, panjang sama, tanpa overlap
pitch sama. MIDI berisi performa; audio belum didengarkan.
"""
archive = base / "Neon-Step-New-Jack-Swing-MIDI.zip"
with ZipFile(archive, "x", ZIP_DEFLATED) as z:
    for path in sorted(output.rglob("*")):
        if path.is_file():
            z.write(path, path.relative_to(output).as_posix())
    for name in ["request.md", "musical-review.md", "build_composition.py"]:
        z.write(base / name, name)
    z.writestr("README.md", readme)
with ZipFile(archive) as z:
    assert z.testzip() is None
    assert len([name for name in z.namelist() if name.endswith(".mid")]) == 15
print(json.dumps({"archive": str(archive), "bytes": archive.stat().st_size,
                  "midi_files": 15, "verification_ok": validation["ok"],
                  "tracks_per_file": 1, "common_end_tick": 368640}, indent=2))
