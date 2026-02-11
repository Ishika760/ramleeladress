import os
import sys
import subprocess
import json

# --- Self-bootstrapping block ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))
venv_python = os.path.join(".venv", "Scripts", "python.exe")
if os.path.exists(venv_python) and sys.executable != os.path.abspath(venv_python):
    print(f"Relaunching with venv: {venv_python}")
    subprocess.run([venv_python] + sys.argv)
    sys.exit()

import extract_pdf
import generate_html
# --------------------------------

def process_catalogs(pdf_dir="pdf", output_dir="pages", assets_dir="assets"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    all_catalogs_data = []
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    
    print(f"Found {len(pdf_files)} PDFs. Starting processing...")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        base_name = os.path.splitext(pdf_file)[0]
        # json_path = os.path.join(output_dir, f"{base_name}_data.json")
        
        print(f"\nProcessing: {pdf_file}")
        try:
            # 1. Extract Data
            # We don't necessarily need to save the intermediate JSON to disk if we pass it directly, 
            # but keeping it might be good for debugging or caching.
            # Let's trust extract_pdf to return the data structure.
            data = extract_pdf.extract_data(pdf_path, output_base_dir=assets_dir, output_json=os.path.join(output_dir, f"{base_name}_data.json"))
            
            if data:
                all_catalogs_data.append({
                    "title": base_name,
                    "data": data
                })
            
        except Exception as e:
            print(f"Failed to process {pdf_file}: {e}")

    # 2. Generate Single Aggregated HTML
    if all_catalogs_data:
        print(f"\nGeneratng single page catalog for {len(all_catalogs_data)} items...")
        generate_html.generate_html(all_catalogs_data, output_path="index.html")
        print("Done!")
    else:
        print("No data extracted.")

if __name__ == "__main__":
    process_catalogs()
