from pathlib import Path
import hashlib

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader


def dump(pdf: Path, out_txt: Path) -> None:
    reader = PdfReader(str(pdf))
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    print(pdf.name, "pages", len(reader.pages), "sha256", digest)
    chunks = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        chunks.append(f"\n\n===== PAGE {i + 1} =====\n{text}")
    out_txt.write_text("".join(chunks), encoding="utf-8")


base = Path(__file__).resolve().parent
dump(base / "picg_sgf_2025.pdf", base / "picg_sgf_2025.txt")
dump(base / "mufap_sgr2023.pdf", base / "mufap_sgr2023.txt")
print("done")
