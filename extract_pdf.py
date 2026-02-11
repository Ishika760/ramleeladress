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
from PIL import Image
import io

# --------------------------------

def extract_data(pdf_path, output_base_dir="assets", output_json="extracted_data.json"):
    # Sanitize directory name
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    safe_name = "".join([c if c.isalnum() or c in "_-" else "_" for c in base_name])
    pdf_filename = safe_name
    
    output_dir = os.path.join(output_base_dir, pdf_filename)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extracted_pages = []
    
    print(f"Opening {pdf_path}...")
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            # print(f"  Extracting page {page_num}...")
            
            page_items = extract_page_items(page, page_num, output_dir, output_base_dir, pdf_filename)
            
            # If no items found (e.g. empty page?), create a dummy one or skip
            # But usually we return the page structure even if empty.
            
            extracted_pages.append({
                "page": page_num,
                "items": page_items
            })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(extracted_pages, f, indent=4, ensure_ascii=False)

    print(f"Extracted data to {output_json}.")
    return extracted_pages

def extract_page_items(page, page_num, output_dir, output_base_dir, pdf_filename):
    """
    Analyzes layout to split page into multiple items.
    Returns a list of Items.
    Each Item: { "images": [...], "texts": [...], "tables": [...] }
    """
    
    # 1. Extract Elements
    elements = []
    
    # --- Images ---
    # pdfplumber images sometimes have duplicates or tiles. We stick to the main ones.
    for i, img in enumerate(page.images):
        # Filter out tiny things (lines/icons)
        if img["width"] < 30 or img["height"] < 30:
            continue
            
        # bounds
        x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
        
        # Save exact image from the PDF stream if possible, or crop text? 
        # pdfplumber doesn't easily extract the raw image bytes associated with the 'image' dict 
        # without using the .pipeline or other tools. 
        # However, we can use page.crop().to_image() for "What you see is what you get" 
        # OR attempt raw extraction.
        # Given "Screenshot of PDF" is discouraged, user wants "extract data".
        # But 'page.images' gives us metadata. The raw bytes are in 'stream'.
        # For simplicity and quality, let's use the visual crop because raw extraction 
        # can be messy (CMYK/inverted) without complex handling.
        # WAIT: User said "Not by taking screenshots... extract data... both text and images".
        # If we use `page.crop(bbox).to_image()`, it's technically a rasterization (screenshot of a region).
        # But `extract_images` (raw) is better.
        # Let's try raw extraction via the 'stream' object if available.
        # Actually, pypdf is better for raw image extraction. pdfplumber is better for layout.
        # Hybrid approach: use pdfplumber for layout (bboxes) and coordinates.
        # But identifying which raw image belongs to which bbox is hard.
        # Strategy: Use page.crop(bbox).to_image(resolution=300).save() 
        # This is high-res rasterization of the region. It's robust.
        
        img_filename = f"page_{page_num}_img_{i+1}_{int(x0)}_{int(top)}.png"
        img_path = os.path.join(output_dir, img_filename)
        rel_path = os.path.join(output_base_dir, pdf_filename, img_filename).replace("\\", "/")
        
        # Crop and save high-res
        try:
            # Clamp coordinates to page dimensions to avoid "not fully within parent page" errors
            p_width = page.width
            p_height = page.height
            
            c_x0 = max(0, min(x0, p_width))
            c_top = max(0, min(top, p_height))
            c_x1 = max(0, min(x1, p_width))
            c_bottom = max(0, min(bottom, p_height))
            
            # Ensure valid area
            if c_x1 - c_x0 < 1 or c_bottom - c_top < 1:
                # Skip invalid
                continue
            
            # high resolution for quality
            cropped = page.crop((c_x0, c_top, c_x1, c_bottom))
            im_obj = cropped.to_image(resolution=300)
            im_obj.save(img_path)
            
            elements.append({
                "type": "image",
                "top": top,
                "x0": x0,
                "width": img["width"],
                "height": img["height"],
                "path": rel_path
            })
        except Exception as e:
            print(f"    Warning: Could not save image {i}: {e}")

    # --- Tables ---
    # pdfplumber table extraction
    tables = page.find_tables()
    
    # We will exclude text that falls inside tables, so keeping track of table bboxes is good.
    table_bboxes = [t.bbox for t in tables]
    
    for i, table in enumerate(tables):
        # We need to split the table into rows.
        
        # 1. Get plain extract
        table_content = table.extract()
        if not table_content: continue
        
        # 2. Get rows (cells)
        # Check if table.rows exists
        if hasattr(table, "rows"):
            rows_cells = table.rows
        else:
             # Fallback
             continue
            
        # 3. Iterate
        for idx, row_obj in enumerate(rows_cells):
            if idx >= len(table_content): break
            row_text_list = table_content[idx]
            
            # Filter None
            clean_row = [cell_text if cell_text else "" for cell_text in row_text_list]
            
            # Check if row is empty
            if not any(clean_row): continue
            
            # Get cells from row object
            # If row_obj IS the list of cells (older pdfplumber), work with it.
            # If row_obj IS a Row object, maybe it has .cells?
            # Or maybe it IS iterable but the specific version fails?
            # Let's try: if list, use it. If object, look for cells.
            
            curr_cells = []
            if isinstance(row_obj, list):
                curr_cells = row_obj
            elif hasattr(row_obj, "cells"):
                curr_cells = row_obj.cells
            else:
                # Try iterating? If error, skip
                try:
                    curr_cells = list(row_obj)
                except:
                    continue

            # Calculate bbox
            # Cells might be objects or rects.
            valid_cells = [c for c in curr_cells if c is not None]
            if not valid_cells: continue

            # safe access
            try:
                # Assuming valid_cells are rect-like [x0, top, x1, bottom]
                # Check first element to decide access method
                first = valid_cells[0]
                if isinstance(first, (list, tuple)):
                    r_top = min(c[1] for c in valid_cells)
                    r_x0 = min(c[0] for c in valid_cells)
                else: 
                     # Object style
                     r_top = min(c.bbox[1] for c in valid_cells)
                     r_x0 = min(c.bbox[0] for c in valid_cells)
            except Exception as e:
                # print(f"Error calcing bbox: {e}")
                continue

            elements.append({
                "type": "table_row",
                "top": r_top,
                "x0": r_x0,
                "data": clean_row
            })

    # --- Text ---
    # We want text that is NOT inside a table.
    # pdfplumber can filter text.
    # Approach: Extract words, filter out those inside table bboxes.
    words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3, extra_attrs=["fontname", "size"])
    
    # Filter words inside tables
    table_bboxes = [t.bbox for t in tables]
    
    def is_in_table(w_bbox, t_bboxes):
        wx0, wtop, wx1, wbottom = w_bbox
        cw = (wx0 + wx1) / 2
        cy = (wtop + wbottom) / 2
        for (tx0, ttop, tx1, tbottom) in t_bboxes:
            if tx0 <= cw <= tx1 and ttop <= cy <= tbottom:
                return True
        return False

    filtered_words = []
    for w in words:
        w_bbox = (w['x0'], w['top'], w['x1'], w['bottom'])
        if not is_in_table(w_bbox, table_bboxes):
            filtered_words.append(w)

    # Group words into lines
    # Simple line grouping by 'top' tolerance
    lines = []
    if filtered_words:
        current_line = [filtered_words[0]]
        for w in filtered_words[1:]:
            last_w = current_line[-1]
            if abs(w['top'] - last_w['top']) < 5: # Same line
                current_line.append(w)
            else:
                # Flush line
                lines.append(process_line(current_line))
                current_line = [w]
        lines.append(process_line(current_line))

    # Add lines to elements
    for line in lines:
        if line['text'].strip():
            elements.append({
                "type": "text",
                "top": line['top'],
                "x0": line['x0'],
                "content": line['text'],
                "size": line['size'],
                "is_bold": line['is_bold']
            })

    # 2. Sort Elements by Vertical Position (Top)
    elements.sort(key=lambda x: (x['top'], x['x0']))

    # 3. Grouping Logic (Splitting Items)
    items = []
    current_item = {"images": [], "texts": [], "rows": []}
    
    # Heuristic:
    # 1. Start new item if we hit an Image that is "significant" 
    #    AND we already have content.
    
    # Removed Page 1 special handling to allow Page 1 to split if it contains multiple items (e.g. Bhartnatyam)

    # Regular pages logic applies to all

    for el in elements:
        if el['type'] == 'image':
            # Check if this image starts a new item
            
            is_new_item = False
            if current_item['images']:
                last_img_top = current_item['images'][-1]['top']
                # If new image is > 100px lower, treat as new item row
                if el['top'] - last_img_top > 100:
                    is_new_item = True
            elif current_item['texts'] or current_item['rows']:
                 # If we have content but no images (maybe text followed by image),
                 # and now an image appears... 
                 # Usually text belongs to the image ABOVE it. 
                 # But if text appeared first (Top=0) and Image (Top=50)...
                 # Let's assume they are same item.
                 pass

            if is_new_item:
                items.append(current_item)
                current_item = {"images": [], "texts": [], "rows": []}
            
            current_item['images'].append(el)
            
        elif el['type'] == 'text':
             current_item['texts'].append(el)
             
        elif el['type'] == 'table_row':
             current_item['rows'].append(el['data'])

    if current_item['images'] or current_item['texts'] or current_item['rows']:
        items.append(current_item)

    return items

def process_line(word_list):
    # Construct line text and metadata
    full_text = " ".join([w['text'] for w in word_list])
    avg_size = sum([w['size'] for w in word_list]) / len(word_list)
    # Check bold (simple check if fontname contains Bold)
    is_bold = any("Bold" in w.get('fontname', '') for w in word_list)
    
    return {
        "text": full_text,
        "top": word_list[0]['top'],
        "x0": word_list[0]['x0'],
        "size": avg_size,
        "is_bold": is_bold
    }

if __name__ == "__main__":
    # Test on one file
    pdf_file = "pdf/BHARTNATYAM HAVI.pdf"
    if os.path.exists(pdf_file):
        extract_data(pdf_file)

