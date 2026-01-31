import pypdfium2 as pdfium
import os
import sys
import subprocess

# --- Self-bootstrapping block ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))
venv_python = os.path.join(".venv", "Scripts", "python.exe")
if os.path.exists(venv_python) and sys.executable != os.path.abspath(venv_python):
    subprocess.run([venv_python] + sys.argv)
    sys.exit()

def debug_images(pdf_path, page_num):
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[page_num - 1]
    
    # List all objects on the page to see if images are there
    # pypdfium2 doesn't easily list images like fitz, but it can show the whole page
    # Let's try to crop the page to just the image area if we can find it?
    # Or let's use pdfplumber to find image boxes
    pass

if __name__ == "__main__":
    import pdfplumber
    with pdfplumber.open("pdf/Ramleela Dresses 2025.pdf") as pdf:
        page = pdf.pages[22]
        print(f"Page 23 Images: {len(page.images)}")
        for i, img in enumerate(page.images):
            print(f"Image {i}: {img['width']}x{img['height']} at ({img['x0']}, {img['top']})")

