import pdfplumber
import os

pdf_path = "pdf/BIRDS DRESSES.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\n--- PAGE {i+1} ---")
        
        # Images
        print("IMAGES:")
        for img in page.images:
            print(f"  Img at Top: {img['top']:.1f}, X0: {img['x0']:.1f}, W: {img['width']:.1f}")
            
        # Words with positions
        print("TEXT:")
        # Group words into lines for readability
        words = page.extract_words()
        lines = {}
        for w in words:
            top = round(w['top'], 1)
            if top not in lines: lines[top] = []
            lines[top].append(w)
        
        for top in sorted(lines.keys()):
            line_text = " ".join([w['text'] for w in sorted(lines[top], key=lambda x: x['x0'])])
            x0 = min(w['x0'] for w in lines[top])
            print(f"  {top:>5} | {x0:>5.1f} | {line_text}")
