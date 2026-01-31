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

import json
import pdfplumber
from pypdf import PdfReader
from PIL import Image
# --------------------------------

def extract_data(pdf_path, output_dir="assets"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    
    # Extract images using pypdf
    reader = PdfReader(pdf_path)
    image_map = {} # Map page to image paths
    
    for page_num, page in enumerate(reader.pages):
        image_map[page_num + 1] = []
        try:
            for img_index, image_file_object in enumerate(page.images):
                try:
                    image_filename = f"page_{page_num+1}_img_{img_index+1}_{image_file_object.name}"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    with open(image_path, "wb") as f:
                        f.write(image_file_object.data)
                    
                    # Store image metadata using PIL to get dimensions
                    with Image.open(image_path) as img:
                        w, h = img.size
                    
                    image_map[page_num + 1].append({
                        "path": f"assets/{image_filename}",
                        "width": w,
                        "height": h
                    })
                except Exception as e:
                    print(f"Error saving image {img_index} on page {page_num+1}: {e}")
        except Exception as e:
            print(f"Error extracting images on page {page_num+1}: {e}")

    # Extract text using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            page_data = {
                "page": page_num,
                "blocks": []
            }
            
            # Add images first for this page
            for img_info in image_map.get(page_num, []):
                page_data["blocks"].append({
                    "type": "image",
                    "path": img_info["path"],
                    "width": img_info["width"],
                    "height": img_info["height"]
                })
            
            # Extract text blocks
            text = page.extract_text()
            if text:
                # Split by lines or paragraphs
                for line in text.split('\n'):
                    if line.strip():
                        page_data["blocks"].append({
                            "type": "text",
                            "content": line.strip()
                        })
            
            data.append(page_data)

    with open("extracted_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Extracted data from {len(reader.pages)} pages.")

if __name__ == "__main__":
    pdf_file = "pdf/Ramleela Dresses 2025.pdf"
    if os.path.exists(pdf_file):
        extract_data(pdf_file)
    else:
        print(f"Error: PDF file not found at {pdf_file}")
