import json
import os

def render_html():
    json_path = "imported_data.json"
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
    <title>Imported Items Collection</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');

        :root {
            --primary: #4527a0;
            --secondary: #00acc1;
            --bg: #f3e5f5;
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
            padding-bottom: 141%; /* A4 Aspect Ratio roughly 1:1.41 */
            background: #fff;
            position: relative;
        }
        .item-image {
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .details {
            padding: 15px;
            text-align: center;
            background: var(--primary);
            color: white;
        }
        .page-tag {
            font-weight: 700;
            font-size: 1.1em;
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
            background: #311b92;
        }
    </style>
</head>
<body>

    <header>
        <h1>Imported Items Collection</h1>
        <div class="subtitle">Exclusive International Designs</div>
    </header>

    <div class="catalog">
"""

    for page in data:
        page_num = page.get("page", 0)
        items = page.get("items", [])
        
        for item in items:
            images = item.get("images", [])
            if not images: continue
            
            for img in images:
                # Page 1 is usually the cover
                title = f"Page {page_num}" if page_num > 1 else "Cover Page"
                
                html += f"""
        <div class="item-card">
            <div class="image-container">
                <img src="{img['path']}" alt="{title}" class="item-image" loading="lazy">
            </div>
            <div class="details">
                <span class="page-tag">{title}</span>
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
    
    with open("imported_catalog.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Created imported_catalog.html")

if __name__ == "__main__":
    render_html()
