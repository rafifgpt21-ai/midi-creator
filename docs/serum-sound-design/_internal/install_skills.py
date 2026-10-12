"""Install all seven sibling skills without replacing unrelated/modified files."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

SKILLS = (
    "serum-sound-design", "serum-reference-match", "serum-synthesis",
    "serum-modulation", "serum-effects", "serum-preset-build", "serum-preset-qa",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    destination = (args.destination or codex_root / "skills").resolve()
    source_root = root / "skills"
    if destination == source_root.resolve() or source_root.resolve() in destination.parents:
        raise SystemExit("Installation destination must be outside canonical source skills")
    manifest_path = destination / ".serum-skill-pack-manifest.json"
    previous = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    previous_files = previous.get("files", {})
    files = {}
    copies = []
    # Preflight every collision before creating or replacing any skill files.
    for name in SKILLS:
        source = source_root / name
        if not (source / "SKILL.md").is_file():
            raise SystemExit(f"Missing canonical skill: {name}")
        if (destination / name).exists() and not any(key.startswith(name + "/") for key in previous_files):
            raise SystemExit(f"Unmanaged skill already exists; choose a new destination: {destination / name}")
        for path in source.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(source_root).as_posix()
            target = destination / relative
            source_hash = digest(path)
            if target.exists():
                current = digest(target)
                if current not in {source_hash, previous_files.get(relative)}:
                    raise SystemExit(f"Installed file was modified; preserve/merge it before reinstalling: {target}")
            files[relative] = source_hash
            copies.append((path, target))
    destination.mkdir(parents=True, exist_ok=True)
    for source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        # Atomic replace keeps an individual installed file complete.
        temporary = target.with_name(target.name + ".serum-install-tmp")
        if temporary.exists():
            raise SystemExit(f"Temporary collision; inspect before retrying: {temporary}")
        temporary.write_bytes(data)
        os.replace(temporary, target)
    for relative, expected in files.items():
        if digest(destination / relative) != expected:
            raise SystemExit(f"Installed checksum mismatch: {relative}")
    receipt = {
        "destination": str(destination), "source": str(source_root),
        "skills": list(SKILLS), "files": files, "checksums_match": True,
    }
    manifest_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    (Path(__file__).parent / "install-receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in receipt.items() if key != "files"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
