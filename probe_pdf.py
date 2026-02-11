import os
import sys
import subprocess
import pdfplumber

# Self-bootstrapping
os.chdir(os.path.dirname(os.path.abspath(__file__)))
venv_python = os.path.join(".venv", "Scripts", "python.exe")
if os.path.exists(venv_python) and sys.executable != os.path.abspath(venv_python):
    subprocess.run([venv_python] + sys.argv)
    sys.exit()

def probe_text():
    pdf_path = "pdf/BHARTNATYAM HAVI.pdf"
    print(f"Probing {pdf_path}...")
    
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        print("--- PAGE 1 TEXT ---")
        print(text)
        print("-------------------")
        
        tables = page.extract_tables()
        if tables:
            print(f"Found {len(tables)} tables.")
            print("--- TABLE 1 ---")
            for row in tables[0]:
                print(row)
        else:
            print("No tables found.")

if __name__ == "__main__":
    probe_text()
