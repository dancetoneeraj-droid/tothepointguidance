"""OCR datas/English/qna.pdf -> datas/English/qna-ocr-full.txt"""
from __future__ import annotations

from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "datas" / "English" / "qna.pdf"
OCR_DIR = ROOT / "datas" / "English" / "qna-pages"
OCR_FULL = ROOT / "datas" / "English" / "qna-ocr-full.txt"


def main() -> None:
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF_PATH)
    image_paths: list[Path] = []
    for i in range(doc.page_count):
        out = OCR_DIR / f"page-{i + 1:02d}.png"
        if not out.exists():
            pix = doc[i].get_pixmap(matrix=fitz.Matrix(2.5, 2.5))
            pix.save(str(out))
        image_paths.append(out)
    doc.close()

    if OCR_FULL.exists() and OCR_FULL.stat().st_size > 2000:
        print(f"Using cached {OCR_FULL}")
        return

    import easyocr

    reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    chunks: list[str] = []
    for i, img in enumerate(image_paths, start=1):
        print(f"OCR page {i}/{len(image_paths)}...", flush=True)
        per_page = OCR_DIR / f"page-{i:02d}.txt"
        if per_page.exists() and per_page.stat().st_size > 50:
            text = per_page.read_text(encoding="utf-8")
        else:
            lines = reader.readtext(str(img), detail=0, paragraph=False)
            text = "\n".join(lines)
            per_page.write_text(text, encoding="utf-8")
        chunks.append(f"\n--- PAGE {i} ---\n{text}")
    OCR_FULL.write_text("\n".join(chunks), encoding="utf-8")
    print(f"Wrote {OCR_FULL}")


if __name__ == "__main__":
    main()
