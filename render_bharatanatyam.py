import json
import os

def render_html():
    json_path = "extracted_data.json"
    if not os.path.exists(json_path):
        print("JSON not found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bharatanatyam Collection</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');

        :root {
            --primary: #8e24aa;
            --secondary: #ff6f00;
            --bg: #fafafa;
            --card-bg: #ffffff;
            --text: #333;
        }
        body {
            font-family: 'Lato', sans-serif;
            background-color: var(--bg);
            margin: 0;
            padding: 40px 20px;
            color: var(--text);
        }
        h1 {
            font-family: 'Playfair Display', serif;
            text-align: center;
            color: var(--primary);
            font-size: 3em;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 50px;
            font-size: 1.2em;
        }
        .catalog {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 40px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .item-card {
            background: var(--card-bg);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            display: flex;
            flex-direction: column;
        }
        .item-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        }
        .image-container {
            width: 100%;
            height: 400px;
            background: #eee;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .item-image {
            width: 100%;
            height: 100%;
            object-fit: contain; /* Show full costume */
            transition: transform 0.5s ease;
        }
        .item-card:hover .item-image {
            transform: scale(1.05);
        }
        .details {
            padding: 25px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        .product-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.5em;
            color: var(--primary);
            margin: 0 0 15px 0;
            line-height: 1.3;
        }
        .specs-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95em;
            margin-top: auto;
        }
        .specs-table th {
            text-align: left;
            padding: 8px;
            border-bottom: 2px solid #eee;
            color: #888;
            font-weight: 700;
        }
        .specs-table td {
            padding: 8px;
            border-bottom: 1px solid #f5f5f5;
        }
        .price {
            font-weight: 700;
            color: var(--secondary);
        }
        .badge {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--secondary);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>

    <header>
        <h1>Bharatanatyam Collection</h1>
        <div class="subtitle">Exquisite Costumes & Accessories</div>
    </header>

    <div class="catalog">
"""

    for page_obj in data:
        items = page_obj.get("items", [])
        for item in items:
            images = item.get("images", [])
            rows = item.get("rows", [])
            
            # Skip empty items
            if not images and not rows:
                continue
                
            # Get Image
            img_src = ""
            if images:
                # Use the largest image or first
                main_img = max(images, key=lambda x: x['width'] * x['height'])
                img_src = main_img['path']
            
            # Extract Product Name & Variants
            product_name = "Unknown Product"
            variants = []
            
            if rows:
                # Heuristic: First row, second column often has name
                # Row 0: ['', 'NAME', 'SIZE', ...]
                header_row = rows[0]
                if len(header_row) > 1 and header_row[1]:
                    product_name = header_row[1].replace("\n", " ")
                
                # Parse variants
                # Look for rows with Size/Price
                # Adjust indices based on column count (Page 1 has 6, Page 2/3 have 5)
                for r in rows[1:]:
                    if len(r) == 6:
                        size = r[2]
                        qty = r[4]
                        rate = r[5]
                    elif len(r) == 5:
                        size = r[2]
                        qty = r[3]
                        rate = r[4]
                    else:
                        continue
                        
                    if size or rate:
                        variants.append({
                            "size": size if size else "-",
                            "rate": rate if rate else "-",
                            "qty": qty if qty else "0"
                        })

            # HTML Construction
            html += f"""
        <div class="item-card">
            <div class="image-container">
                {f'<img src="{img_src}" alt="{product_name}" class="item-image" loading="lazy">' if img_src else '<div style="padding:20px;color:#ccc">No Image</div>'}
            </div>
            <div class="details">
                <h2 class="product-title">{product_name}</h2>
                
                {render_variants_table(variants)}
            </div>
        </div>
"""

    html += """
    </div>
</body>
</html>
"""
    
    with open("bharatanatyam_catalog.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Created bharatanatyam_catalog.html")

def render_variants_table(variants):
    if not variants:
        return "<p>No pricing details available.</p>"
        
    rows_html = ""
    for v in variants:
        rows_html += f"<tr><td>{v['size']}</td><td>{v['qty']}</td><td class='price'>₹{v['rate']}</td></tr>"
        
    return f"""
    <table class="specs-table">
        <thead>
            <tr>
                <th>Size</th>
                <th>Qty</th>
                <th>Rate</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """

if __name__ == "__main__":
    render_html()
