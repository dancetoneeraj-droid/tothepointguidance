import re
from pathlib import Path
import fitz

p = Path(__file__).resolve().parent.parent / "datas" / "maths" / "geometry" / "Geometry-Sheet-8.pdf"
doc = fitz.open(p)
text = "\n".join(page.get_text() for page in doc)
doc.close()
m = re.search(r"24\.\s*Find the distance", text)
out = Path(__file__).resolve().parent.parent / "datas" / "maths" / "geometry" / "sheet8-q24.txt"
if m:
    out.write_text(text[m.start() : m.start() + 2000], encoding="utf-8")
    print("written", len(out.read_text(encoding="utf-8")))
else:
    print("not found")
