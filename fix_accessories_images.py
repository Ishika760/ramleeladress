import pdfplumber
import os

pdf_path = "pdf/Ramleela Accesories 2025.pdf"
output_dir = "assets/Ramleela_Accesories_2025"
os.makedirs(output_dir, exist_ok=True)

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        img = page.to_image(resolution=150)
        output_path = f"{output_dir}/page_{i + 1}_full.png"
        img.save(output_path)
        print(f"Saved {output_path}")
