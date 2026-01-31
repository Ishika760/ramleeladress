import os
import sys
import subprocess

# --- Self-bootstrapping block ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))
venv_python = os.path.join(".venv", "Scripts", "python.exe")
if os.path.exists(venv_python) and sys.executable != os.path.abspath(venv_python):
    print(f"Relaunching with venv: {venv_python}")
    subprocess.run([venv_python] + sys.argv)
    sys.exit()

import pypdfium2 as pdfium
# --------------------------------

def render_page(pdf_path, page_num, output_path):
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[page_num - 1]
    bitmap = page.render(scale=2) # 144 DPI
    pil_image = bitmap.to_pil()
    pil_image.save(output_path)
    print(f"Saved rendered page to {output_path}")

if __name__ == "__main__":
    pdf_file = "pdf/Ramleela Dresses 2025.pdf"
    render_page(pdf_file, 23, "page_23_render.png")
