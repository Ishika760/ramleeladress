import pdfplumber
import os

pdf_path = "pdf/State Dress New 2024.pdf"
output_dir = "assets/State_Dress_New_2024"
os.makedirs(output_dir, exist_ok=True)

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        img = page.to_image(resolution=150)
        output_path = f"{output_dir}/page_{i + 1}_full.png"
        img.save(output_path)
        print(f"Saved {output_path}")
