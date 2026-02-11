import os
import sys
import subprocess
import io

# Self-bootstrapping
os.chdir(os.path.dirname(os.path.abspath(__file__)))
venv_python = os.path.join(".venv", "Scripts", "python.exe")
if os.path.exists(venv_python) and sys.executable != os.path.abspath(venv_python):
    print(f"Relaunching with venv: {venv_python}")
    subprocess.run([venv_python] + sys.argv)
    sys.exit()

import PyPDF2
from PIL import Image

def convert_pdf():
    pdf_filename = "BHARTNATYAM HAVI.pdf"
    pdf_path = os.path.join("pdf", pdf_filename)
    output_base = "assets"
    output_folder = "bharatanatyam"
    output_dir = os.path.join(output_base, output_folder)
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Opening {pdf_path}...")
    reader = PyPDF2.PdfReader(pdf_path)
    
    extracted_images = []
    
    for i, page in enumerate(reader.pages):
        page_num = i + 1
        print(f"Scanning Page {page_num}...")
        
        # PyPDF2 3.x image extraction
        if hasattr(page, "images"):
            for img_file_obj in page.images:
                try:
                    img_name = img_file_obj.name
                    img_data = img_file_obj.data
                    
                    # Verify and Filter
                    image = Image.open(io.BytesIO(img_data))
                    
                    # Filter tiny images (often logos, lines)
                    if image.width < 50 or image.height < 50:
                        continue
                        
                    # Generate filename
                    # Ensure extension matches
                    ext = os.path.splitext(img_name)[1]
                    if not ext:
                        ext = ".png" # default
                        
                    # save as page_N_name.ext
                    safe_name = os.path.splitext(img_name)[0]
                    save_name = f"page_{page_num}_{safe_name}{ext}"
                    save_path = os.path.join(output_dir, save_name)
                    
                    with open(save_path, "wb") as f:
                        f.write(img_data)
                        
                    extracted_images.append(save_path)
                    print(f"  Extracted: {save_name} ({image.width}x{image.height})")
                    
                except Exception as e:
                    print(f"  Error extracting image: {e}")
        else:
            print("  No images found or PyPDF2 version outdated.")

    # Generate HTML
    print(f"Generating HTML for {len(extracted_images)} images...")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bharatanatyam Costumes</title>
    <style>
        :root {{
            --primary: #d32f2f;
            --bg: #f5f5f5;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg);
            margin: 0;
            padding: 20px;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid var(--primary);
            display: inline-block;
            padding-bottom: 10px;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
        }}
        img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .caption {{
            padding: 15px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Bharatanatyam Costumes</h1>
        <p>Extracted from PDF Catalogue</p>
    </header>
    
    <div class="gallery">
"""

    for img_path in extracted_images:
        # relative path for HTML
        rel_path = os.path.relpath(img_path, os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
        name = os.path.basename(img_path)
        html_content += f"""
        <div class="card">
            <img src="{rel_path}" alt="{name}" loading="lazy">
            <div class="caption">{name}</div>
        </div>"""

    html_content += """
    </div>
</body>
</html>"""

    with open("bharatanatyam.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Done! Open bharatanatyam.html to view.")

if __name__ == "__main__":
    convert_pdf()
