import os
import json
import extract_pdf

pdfs = [
    "pdf/national leaders 2024.pdf",
    "pdf/Ramleela Accesories 2025.pdf",
    "pdf/Ramleela Dresses 2025.pdf",
    "pdf/State Dress New 2024.pdf",
    "pdf/Western dance Costumes 2025...pdf"
]

def process_all():
    catalog_links = []
    
    for pdf in pdfs:
        if not os.path.exists(pdf):
            print(f"Skipping {pdf}: Not found.")
            continue
            
        base_name = os.path.basename(pdf).replace(".pdf", "").replace(" ", "_").lower()
        json_out = f"{base_name}_data.json"
        
        print(f"--- Extracting {pdf} ---")
        extract_pdf.extract_data(pdf, output_json=json_out)
        
        print(f"--- Rendering {pdf} ---")
        render_generic_catalog(json_out, f"{base_name}_catalog.html", os.path.basename(pdf).replace(".pdf", ""))
        catalog_links.append({"name": os.path.basename(pdf).replace(".pdf", ""), "link": f"{base_name}_catalog.html"})

    update_index(catalog_links)

def render_generic_catalog(json_path, html_out, title):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        :root {{ --primary: #1a237e; --bg: #f5f5f5; --card-bg: #ffffff; }}
        body {{ font-family: 'Outfit', sans-serif; background: var(--bg); margin: 0; padding: 40px 20px; }}
        h1 {{ text-align: center; color: var(--primary); font-size: 2.5em; }}
        .catalog {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; max-width: 1400px; margin: 40px auto; }}
        .item-card {{ background: var(--card-bg); border-radius: 12px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: flex; flex-direction: column; }}
        .img-container {{ width: 100%; padding-bottom: 120%; position: relative; background: #fff; }}
        .img-container img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 10px; box-sizing: border-box; }}
        .details {{ padding: 15px; border-top: 1px solid #eee; }}
        .specs-table {{ width: 100%; border-collapse: collapse; font-size: 0.85em; margin-top: 10px; }}
        .specs-table td, .specs-table th {{ padding: 5px; border-bottom: 1px solid #f0f0f0; text-align: left; }}
        .btn-back {{ display: block; width: fit-content; margin: 20px auto; padding: 10px 30px; background: var(--primary); color: white; text-decoration: none; border-radius: 50px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="catalog">
"""

    for page in data:
        for item in page.get("items", []):
            images = item.get("images", [])
            rows = item.get("rows", [])
            if not images: continue
            
            # Simple metadata extraction
            name = "Item"
            for r in rows:
                if len(r) > 0 and r[0] and len(str(r[0])) > 3:
                   name = str(r[0])
                   break
            
            # Table construction
            table_html = ""
            if rows:
                table_html = '<table class="specs-table"><tbody>'
                for r in rows[:10]: # Limit for preview
                    cells = "".join([f"<td>{c}</td>" for c in r if c])
                    if cells: table_html += f"<tr>{cells}</tr>"
                table_html += "</tbody></table>"

            for img in images:
                html += f"""
        <div class="item-card">
            <div class="img-container"><img src="{img['path']}" loading="lazy"></div>
            <div class="details">
                <strong>{name}</strong>
                {table_html}
            </div>
        </div>"""

    html += f"""
    </div>
    <a href="index.html" class="btn-back">← Back to Dashboard</a>
</body>
</html>"""
    
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html)

def update_index(new_links):
    # This will append the new links to the index.html
    # For now, let's keep it simple and just list them.
    print(f"Generated catalogs: {[l['link'] for l in new_links]}")

if __name__ == "__main__":
    process_all()
