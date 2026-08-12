"""Solve all questions in geo-batch-m1.json and write geo-solutions-out-m1.json."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
BATCH = SCRIPTS / "geo-batch-m1.json"
OUT = SCRIPTS / "geo-solutions-out-m1.json"

EXTRA_IDS = (
    "maths_geometry_393",
    "maths_geometry_396",
    "maths_geometry_398",
    "maths_geometry_404",
    "maths_geometry_407",
    "maths_geometry_426",
    "maths_geometry_427",
    "maths_geometry_435",
    "maths_geometry_441",
)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build_solvers():
    b1 = _load("solve_geo_batch_1", SCRIPTS / "solve-geo-batch-1.py")
    b2 = _load("solve_geo_batch_2", SCRIPTS / "solve-geo-batch-2.py")
    solvers = dict(b1.SOLVERS)
    for qid in EXTRA_IDS:
        num = qid.split("_")[-1]
        solvers[qid] = getattr(b2, f"solve_{num}")
    return solvers


def main() -> None:
    solvers = build_solvers()
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    out: list[dict] = []
    failed: list[str] = []

    for item in batch:
        qid = item["id"]
        opts = item["options"]
        fn = solvers.get(qid)
        if not fn:
            failed.append(qid)
            continue
        try:
            ans, solution = fn(opts)
            out.append({"id": qid, "correctAnswer": ans, "solution": solution})
        except Exception as exc:
            failed.append(f"{qid}: {exc}")

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Solved {len(out)}/{len(batch)}; failed: {len(failed)}")
    if failed:
        (SCRIPTS / "_fail-m1.txt").write_text("\n".join(failed), encoding="utf-8")
        print("\n".join(failed[:20]))


if __name__ == "__main__":
    main()
