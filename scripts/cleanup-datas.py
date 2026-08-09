"""Remove imported PDFs and intermediate files from datas/ (keep unimported staging)."""
from __future__ import annotations

import os
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "datas"
KEEP = {
    "maths/noun.json",
    "maths/README.md",
}


def _unlink(path: Path) -> None:
    os.chmod(path, stat.S_IWRITE)
    path.unlink()


def main() -> None:
    removed: list[str] = []
    failed: list[tuple[str, str]] = []
    freed = 0

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in KEEP:
            continue
        try:
            freed += path.stat().st_size
            _unlink(path)
            removed.append(rel)
        except OSError as e:
            failed.append((rel, str(e)))

    # Remove empty directories (bottom-up)
    for path in sorted((p for p in ROOT.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        try:
            if not any(path.iterdir()):
                path.rmdir()
                removed.append(f"{path.relative_to(ROOT).as_posix()}/")
        except OSError as e:
            failed.append((path.relative_to(ROOT).as_posix(), str(e)))

    print(f"Removed {len(removed)} items (~{freed / 1024 / 1024:.1f} MB)")
    if failed:
        print(f"Failed {len(failed)}:")
        for rel, err in failed:
            print(f"  ! {rel}: {err}")
    print("Remaining:")
    for f in sorted(ROOT.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
