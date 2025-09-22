import pdfplumber
import glob
import os

RAW_DIR = "data/raw"

pdf_files = glob.glob(f"{RAW_DIR}/*.pdf")
for pdf_path in pdf_files:
    txt_path = pdf_path.replace(".pdf", ".txt")
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved {txt_path}")
