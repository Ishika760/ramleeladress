import pdfplumber
import os

pdf_path = "pdf/State Dress New 2024.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\n--- PAGE {i+1} ---")
        words = page.extract_words()
        if not words:
            print("  No text found.")
        else:
            lines = {}
            for w in words:
                top = round(w['top'], 1)
                if top not in lines: lines[top] = []
                lines[top].append(w)
            for top in sorted(lines.keys()):
                line_text = " ".join([w['text'] for w in sorted(lines[top], key=lambda x: x['x0'])])
                print(f"  {top:>5} | {line_text}")
