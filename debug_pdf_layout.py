import pdfplumber
import sys
import os

# Self-bootstrapping
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# (Assume venv logic is handled by user rule/env)

def analyze_layout(pdf_path):
    print(f"Analyzing {pdf_path}...")
    with pdfplumber.open(pdf_path) as pdf:
        # Check Page 2 specifically as it had multiple items
        if len(pdf.pages) > 1:
            page = pdf.pages[1] 
            print(f"--- Page {page.page_number} Layout ---")
            
            # 1. Images
            print(f"Found {len(page.images)} images.")
            for i, img in enumerate(page.images):
                print(f"IMG {i}: x={img['x0']:.1f}, y={img['top']:.1f}, w={img['width']:.1f}, h={img['height']:.1f}")

            # 2. Text layout grouping
            # Let's extract words with details
            words = page.extract_words(extra_attrs=["fontname", "size"])
            
            # Group by vertical position (simple clustering)
            print(f"\nFound {len(words)} words. Sample of distinct vertical blocks:")
            
            last_top = -1
            current_line = []
            
            for w in words:
                if last_top == -1: last_top = w['top']
                
                # New line detection (approx)
                if abs(w['top'] - last_top) > 5:
                    print(f"Y={last_top:.1f}: {' '.join(current_line)}")
                    current_line = []
                    last_top = w['top']
                
                current_line.append(f"{w['text']}({w['size']:.1f})")
            
            if current_line:
                print(f"Y={last_top:.1f}: {' '.join(current_line)}")

if __name__ == "__main__":
    analyze_layout("pdf/BHARTNATYAM HAVI.pdf")
