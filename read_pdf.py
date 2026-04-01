import pypdf
import sys

try:
    reader = pypdf.PdfReader("25WSB301-CW2.pdf")
    with open("pdf_content.txt", "w", encoding="utf-8") as f:
        for i, page in enumerate(reader.pages):
            f.write(f"--- PAGE {i+1} ---\n")
            f.write(page.extract_text() + "\n")
    print("Successfully extracted text to pdf_content.txt")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
