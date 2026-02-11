import os
import sys
import subprocess

# Change to the script's directory for path consistency
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_command(command):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def setup():
    # 1. Install uv if not present
    try:
        subprocess.run("uv --version", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Installing uv...")
        run_command("pip install uv")

    # 2. Create venv if not exists
    if not os.path.exists(".venv"):
        print("Creating virtual environment...")
        run_command("uv venv")

    # 3. Install dependencies
    print("Installing dependencies...")
    # Using uv pip install as per user rules
    # PyMuPDF (fitz) for PDF extraction, Pillow for image processing
    run_command("uv pip install -p .venv pymupdf Pillow PyPDF2 pdfplumber")

    print("\nSetup complete!")

if __name__ == "__main__":
    setup()
