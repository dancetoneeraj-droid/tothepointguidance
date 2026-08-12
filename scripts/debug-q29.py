import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "p", Path(__file__).resolve().parent / "parse-geometry-sheets.py"
)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

import fitz

doc = fitz.open(Path(__file__).resolve().parent.parent / "datas/maths/Geometry-10.pdf")
text = "\n".join(page.get_text() for page in doc)
doc.close()
block = p.find_block(text, 29)
try:
    r = p.parse_question(10, 29, block)
    out = f"OK\nQ={r['question']}\nopts={r['options']}"
except Exception as e:
    body = p.strip_header(block)
    found = p.extract_options(body)
    out = f"ERR {e}\nfound={found}\nbody={body}"
Path(__file__).resolve().parent.parent.joinpath("datas/maths/geometry/debug-q29.txt").write_text(
    out, encoding="utf-8"
)
print("done")
