"""Bundle the verified standalone MIDI layers and reproducibility materials."""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

base = Path(__file__).resolve().parent
output = base / "output"
receipt = json.loads((base / "verification.json").read_text(encoding="utf-8-sig"))
assert receipt["ok"] and len(receipt["files"]) == 12
assert all(item["ok"] and len(item["tracks"]) == 1 and item["end_tick"] == 614400
           for item in receipt["files"].values())

readme = """# Afterglow Circuit — Progressive House

Komposisi instrumental orisinal dengan nuansa progressive house melodis dan atmosferik.
126 BPM | F minor | 4/4 | 160 bar | sekitar 5:04.76 | 12 layer.

## Impor ke DAW

1. Ekstrak ZIP ini, atur tempo 126 BPM dan meter 4/4.
2. Impor seluruh MIDI di midi/layers/ mulai bar 1/beat 1 ke track terpisah.
3. Pertahankan posisi diam pada file; instrumen masuk bertahap dalam aransemen.
4. Pilih kit electronic house untuk tujuh layer percussion. Mapping GM:
   kick 36, clap 39, snare 38, closed hat 42, open hat 46, ride 51,
   shaker/maracas 70. Tiap file drum memakai channel 10.
5. Pilih instrumen synth tersendiri untuk synth-bass, poly-synth, pluck-arp,
   warm-pad dan lead-synth. Tiap file melodic memakai channel 1.

## Arah sound

- Synth bass: mono, fundamental kuat, envelope pendek; biarkan ruang untuk kick.
- Poly synth: saw chords lebar, low-pass filter; buka cutoff bertahap menjelang drop.
- Pluck arp: envelope pendek, delay sinkron tempo; kurangi level saat lead masuk.
- Warm pad: attack pelan, reverb lebar, low-cut untuk menjaga low-end.
- Lead synth: saw melodis, sedikit detune, delay ringan.
- Atur sidechain bass/chord/pad dengan kick untuk gerakan pumping.

Filter automation, sidechain, stereo widening, delay/reverb dan riser audio
diatur di DAW; file MIDI berisi not, velocity dan pengaturan mixer awal.
Lagu memakai dua build/drop dan satu beat hening sebelum setiap drop.

summary.md berisi tautan semua MIDI, request.md berisi keputusan musik,
musical-review.md berisi audit event, verification.json berisi receipt CLI.
Semua 12 file lulus validate/generate/verify, satu track per file dan panjang sama.
Audio belum didengarkan.
"""
archive = base / "Afterglow-Circuit-Progressive-House-MIDI.zip"
with ZipFile(archive, "x", ZIP_DEFLATED) as bundle:
    for path in sorted(output.rglob("*")):
        if path.is_file():
            bundle.write(path, path.relative_to(output).as_posix())
    for name in ["request.md", "musical-review.md", "verification.json", "build_composition.py"]:
        bundle.write(base / name, name)
    bundle.writestr("README.md", readme)
with ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    assert sum(name.endswith(".mid") for name in bundle.namelist()) == 12
print(json.dumps({"archive": str(archive), "bytes": archive.stat().st_size,
                  "midi_files": 12, "verification_ok": True,
                  "tracks_per_file": 1, "common_end_tick": 614400}, indent=2))
