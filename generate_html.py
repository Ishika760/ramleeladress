import json
import os

def generate_html(all_catalogs_data, output_path="index.html"):
    # all_catalogs_data is expected to be a list of dicts: {"title": str, "data": list_of_pages}


    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ramleela Dresses - Full Collection</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #1a1a1a;
            --accent: #d4af37;
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text: #333333;
            --shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}

        header {{
            background: var(--primary);
            color: white;
            padding: 2rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
        }}
        


        header h1 {{
            font-size: 3.5rem;
            margin: 0;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: var(--accent);
        }}

        header h1 {{
            font-size: 2.5rem;
            margin: 0;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--accent);
        }}

        .catalog-section {{
            margin-bottom: 8rem;
            border-bottom: 1px solid #ddd;
            padding-bottom: 4rem;
        }}

        .catalog-title {{
            text-align: center;
            font-size: 3rem;
            color: var(--primary);
            margin: 3rem 0;
            text-transform: uppercase;
            letter-spacing: 3px;
            position: sticky;
            top: 0;
            background: var(--bg);
            z-index: 100;
            padding: 1rem;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .page-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 3rem;
            margin-bottom: 5rem;
        }}

        .card {{
            background: var(--card-bg);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease;
            position: relative;
            display: flex;
            flex-direction: column;
        }}

        .card:hover {{
            transform: translateY(-10px);
        }}

        .card-image-container {{
            width: 100%;
            height: 400px;
            overflow: hidden;
            background: #eee;
            position: relative;
        }}

        .card img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            transition: scale 0.5s ease;
            padding: 10px;
        }}

        .card:hover img {{
            scale: 1.05;
        }}

        .card-content {{
            padding: 2rem;
            flex-grow: 1;
        }}

        .card h2 {{
            margin-top: 0;
            font-size: 1.5rem;
            color: var(--primary);
            border-bottom: 2px solid var(--accent);
            display: inline-block;
            margin-bottom: 1rem;
        }}

        .card-text {{
            font-size: 1rem;
            color: #666;
            margin-bottom: 0.5rem;
            outline: none;
        }}

        .card-text:focus {{
            background: #fffef0;
            border-radius: 4px;
        }}

        .tag {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--accent);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(212, 175, 55, 0.3);
        }}

        footer {{
            text-align: center;
            padding: 4rem 2rem;
            background: #eee;
            margin-top: 5rem;
        }}

        /* Cover Page Special Styling */
        .cover-page {{
            grid-column: 1 / -1;
            display: flex;
            flex-direction: row;
            height: auto;
            min-height: 600px;
            background: white;
            border-radius: 30px;
            overflow: hidden;
            box-shadow: var(--shadow);
        }}

        .cover-visuals {{
            flex: 1;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
            padding: 20px;
            background: #f4f4f4;
        }}

        .cover-visuals img {{
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 10px;
        }}

        .cover-content {{
            flex: 1;
            padding: 4rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            background: linear-gradient(135deg, #ffffff 0%, #fdfdfd 100%);
        }}

        .cover-content h1 {{
            font-size: 4rem;
            color: var(--primary);
            margin: 0;
            line-height: 1;
        }}

        .cover-content h2 {{
            font-size: 2rem;
            color: var(--accent);
            margin: 1rem 0;
        }}

        [contenteditable]:hover {{
            cursor: text;
            background-color: rgba(212, 175, 55, 0.05);
        }}

        @media (max-width: 768px) {{
            .page-grid {{
                grid-template-columns: 1fr;
            }}
            .cover-page {{
                flex-direction: column;
            }}
            header h1 {{
                font-size: 2.5rem;
            }}
        }}
    </style>
</head>
<body>

"""

    # Iterate Catalogs
    for catalog in all_catalogs_data:
        title = catalog["title"]
        pages = catalog["data"] # Now a list of pages, where each page has "items"
        
        html_content += f"""
    <div class="catalog-section" id="{title.replace(' ', '-').lower()}">
        <h2 class="catalog-title">{title}</h2>
        <div class="page-grid">
"""
        
        for page_obj in pages:
            page_num = page_obj["page"]
            items = page_obj["items"]
            
            for item in items:
                # Check if this is a valid item (has some content)
                if not (item["images"] or item["texts"] or item.get("rows")):
                    continue

                # 1. Cover Page Handling (First page of catalog)
                if page_num == 1:
                    images = item["images"]
                    html_content += f"""
            <div class="cover-page">
                <div class="cover-visuals">
                    {" ".join([f'<img src="{img["path"]}" alt="Catalog Item">' for img in images])}
                </div>
                <div class="cover-content">
                    <h1 contenteditable="true">{title}</h1>
                    <p contenteditable="true">Scroll down to view collection</p>
                </div>
            </div>
"""
                    # Only do this once per page 1. If page 1 has multiple items, 
                    # subsequent items should probably be regular cards? 
                    # Usually Page 1 is just cover. Let's assume one item for Page 1 for now 
                    # as enforced by extract_pdf logic.
                    break 

                # 2. Regular Item Card
                
                # Determine Title (First bold text, or first text line)
                item_title = f"Item {page_num}"
                description_html = ""
                
                texts = item["texts"]
                if texts:
                    # Heuristic: First text line is title if it looks like one
                    item_title = texts[0]["content"]
                    remaining_texts = texts[1:]
                else:
                    remaining_texts = []

                # Build Description HTML
                for t in remaining_texts:
                    # Simple size-based styling
                    style = ""
                    if t.get("is_bold"): style += "font-weight:bold;"
                    if t.get("size", 0) > 12: style += "font-size:1.1em;"
                    
                    description_html += f'<div class="card-text" style="{style}" contenteditable="true">{t["content"]}</div>'

                # Build Table HTML
                item_rows = item.get("rows", [])
                if item_rows:
                    description_html += '<table class="table table-bordered table-sm mt-2" style="width:100%; font-size:0.9rem; border-collapse: collapse;">'
                    for row in item_rows:
                        description_html += "<tr>"
                        for cell in row:
                            cell_text = cell if cell else ""
                            description_html += f'<td style="border:1px solid #eee; padding:4px;">{cell_text}</td>'
                        description_html += "</tr>"
                    description_html += "</table>"

                # Image Selection
                images = item["images"]
                main_image = ""
                if images:
                    # Pick largest
                    main_image_obj = max(images, key=lambda x: x["width"] * x["height"])
                    main_image = main_image_obj["path"]

                html_content += f"""
            <div class="card">
                <span class="tag">{title}</span>
                <div class="card-image-container">
                    {f'<img src="{main_image}" alt="{item_title}">' if main_image else '<div style="height:100%; display:flex; align-items:center; justify-content:center; color:#ccc;">No Image</div>'}
                </div>
                <div class="card-content">
                    <h2 contenteditable="true">{item_title}</h2>
                    <div class="card-text-container">
                        {description_html}
                    </div>
                </div>
            </div>
"""

        html_content += """
        </div>
    </div>
"""

    html_content += f"""
    </div>


<footer>
    <p>&copy; 2025 Ramleela Dresses. All rights reserved.</p>
    <p><i>Edit any text directly on this page for customization.</i></p>
</footer>

</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated {output_path}")







        





















            





                


                



            

































if __name__ == "__main__":
    pass

