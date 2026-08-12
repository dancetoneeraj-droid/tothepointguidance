import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "p", Path(__file__).resolve().parent / "parse-geometry-sheets.py"
)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

import fitz

doc = fitz.open(Path(__file__).resolve().parent.parent / "datas/maths/geometry/Geometry-Sheet-4.pdf")
text = "\n".join(page.get_text() for page in doc)
doc.close()
block = p.find_block(text, 3)
body = p.strip_header(block)
found = p.extract_options(body)

out = Path(__file__).resolve().parent.parent / "datas/maths/geometry/debug-q3.txt"
lines = [f"opt_start={found[0] if found else None}", f"options={found[1] if found else None}", "---body---", body[:500]]
out.write_text("\n".join(lines), encoding="utf-8")

# test marker split
pairs = p.split_by_markers(body)
lines.append(f"marker pairs: {len(pairs)}")
if pairs:
    lines.append(f"first marker: {pairs[0]}")
out.write_text("\n".join(lines), encoding="utf-8")
print("written")
