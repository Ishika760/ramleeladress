import json
import os

def render_html():
    json_path = "birds_data.json"
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
    <title>Birds Dresses Collection</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');

        :root {
            --primary: #2e7d32;
            --secondary: #f9a825;
            --bg: #f1f8e9;
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
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .item-card {
            background: var(--card-bg);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
            display: flex;
            flex-direction: column;
        }
        .item-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        }
        .image-container {
            width: 100%;
            height: 300px;
            background: #fff;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            box-sizing: border-box;
        }
        .item-image {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        .details {
            padding: 20px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        .product-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.4em;
            color: var(--primary);
            margin: 0 0 10px 0;
        }
        .art-no {
            font-size: 0.9em;
            color: #888;
            margin-bottom: 15px;
        }
        .specs-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }
        .specs-table th {
            text-align: left;
            padding: 6px;
            border-bottom: 2px solid #eee;
            color: #888;
        }
        .specs-table td {
            padding: 6px;
            border-bottom: 1px solid #f5f5f5;
        }
        .price {
            font-weight: 700;
            color: var(--secondary);
        }
        .nav-back {
            text-align: center;
            margin-top: 40px;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #1b5e20;
        }
    </style>
</head>
<body>

    <header>
        <h1>Birds Dresses Collection</h1>
        <div class="subtitle">Nature Inspired Outfits for Kids</div>
    </header>

    <div class="catalog">
"""

    # Birds Dresses PDF has a specific layout
    # Page 1: 2 columns, 5 rows of items
    # Page 2: 2 columns, 2 rows, plus one single item at the bottom
    
    # We will process each page and group by visual proximity
    for page in data:
        items = page.get("items", [])
        page_num = page.get("page", 0)
        
        # Collect all significant images
        all_images = []
        for item in items:
            for img in item.get("images", []):
                if img['width'] > 50 and img['height'] > 50:
                    all_images.append(img)
        
        # Robust Row-based Sorting:
        # 1. Sort by top coordinate first
        all_images.sort(key=lambda x: x['top'])
        
        # 2. Group into rows with a tolerance of 15px
        visual_rows = []
        if all_images:
            current_row = [all_images[0]]
            for img in all_images[1:]:
                if abs(img['top'] - current_row[0]['top']) < 15:
                    current_row.append(img)
                else:
                    # Sort the completed row by x0 (Left to Right)
                    current_row.sort(key=lambda x: x['x0'])
                    visual_rows.extend(current_row)
                    current_row = [img]
            # Final row
            current_row.sort(key=lambda x: x['x0'])
            visual_rows.extend(current_row)
            
        all_images = visual_rows
        
        # Extract names and data in a structured way per page
        if page_num == 1:
            bird_names = [
                "BUTTERFLY", "COCK WHITE", 
                "COCK YELLOW", "CROW",
                "DUCK", "EGALE",
                "HONEYBEE", "KOYAL",
                "MAINA", "OWL"
            ]
            art_nos = [
                "9013", "9001",
                "9008", "9002",
                "9003", "9012",
                "9014", "9011",
                "9010", "9004"
            ]
        elif page_num == 2:
            bird_names = ["PARROT", "PEACOCK", "PIGEON", "SWAN", "YELLOW BIRD"]
            art_nos = ["9005", "9006", "9007", "9009", "9020"]
        else:
            bird_names = []
            art_nos = []

        for i, img in enumerate(all_images):
            title = bird_names[i] if i < len(bird_names) else "Bird Costume"
            art = art_nos[i] if i < len(art_nos) else ""
            
            # Universal pricing for kids bird dresses in this catalogue
            vars = [
                {"size": '32"', "age": "3-4 YEAR", "rate": "275.00"},
                {"size": '36"', "age": "5-6 YEAR", "rate": "275.00"},
                {"size": '40"', "age": "7-8 YEAR", "rate": "275.00"}
            ]
            
            html += f"""
        <div class="item-card">
            <div class="image-container">
                <img src="{img['path']}" alt="{title}" class="item-image" loading="lazy">
            </div>
            <div class="details">
                <h2 class="product-title">{title}</h2>
                <div class="art-no">{art}</div>
                {render_variants(vars)}
            </div>
        </div>
"""

    html += """
    </div>
    <div class="nav-back">
        <a href="index.html" class="btn">Back to Home</a>
    </div>
</body>
</html>
"""
    
    with open("birds_catalog.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Created birds_catalog.html")

def render_variants(variants):
    if not variants: return ""
    rows = ""
    for v in variants:
        rows += f"<tr><td>{v['size']}</td><td>{v['age']}</td><td class='price'>₹{v['rate']}</td></tr>"
    return f"""
    <table class="specs-table">
        <thead><tr><th>Size</th><th>Age</th><th>Rate</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """

if __name__ == "__main__":
    render_html()
