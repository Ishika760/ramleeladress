import json
import os

def generate_html(json_path, output_path="index.html"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ramleela Dresses 2025 Catalog</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #1a1a1a;
            --accent: #d4af37;
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text: #333333;
            --shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }

        header {
            background: var(--primary);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            margin-bottom: 4rem;
            clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
        }

        header h1 {
            font-size: 3.5rem;
            margin: 0;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: var(--accent);
        }

        header p {
            font-size: 1.2rem;
            opacity: 0.8;
            margin-top: 1rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        .page-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 3rem;
            margin-bottom: 5rem;
        }

        .card {
            background: var(--card-bg);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease;
            position: relative;
            display: flex;
            flex-direction: column;
        }

        .card:hover {
            transform: translateY(-10px);
        }

        .card-image-container {
            width: 100%;
            height: 400px;
            overflow: hidden;
            background: #eee;
            position: relative;
        }

        .card img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            transition: scale 0.5s ease;
            padding: 10px;
        }

        .card:hover img {
            scale: 1.05;
        }

        .card-content {
            padding: 2rem;
            flex-grow: 1;
        }

        .card h2 {
            margin-top: 0;
            font-size: 1.5rem;
            color: var(--primary);
            border-bottom: 2px solid var(--accent);
            display: inline-block;
            margin-bottom: 1rem;
        }

        .card-text {
            font-size: 1rem;
            color: #666;
            margin-bottom: 0.5rem;
            outline: none;
        }

        .card-text:focus {
            background: #fffef0;
            border-radius: 4px;
        }

        .tag {
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
        }

        footer {
            text-align: center;
            padding: 4rem 2rem;
            background: #eee;
            margin-top: 5rem;
        }

        /* Cover Page Special Styling */
        .cover-page {
            grid-column: 1 / -1;
            display: flex;
            flex-direction: row;
            height: auto;
            min-height: 600px;
            background: white;
            border-radius: 30px;
            overflow: hidden;
            box-shadow: var(--shadow);
        }

        .cover-visuals {
            flex: 1;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
            padding: 20px;
            background: #f4f4f4;
        }

        .cover-visuals img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 10px;
        }

        .cover-content {
            flex: 1;
            padding: 4rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            background: linear-gradient(135deg, #ffffff 0%, #fdfdfd 100%);
        }

        .cover-content h1 {
            font-size: 4rem;
            color: var(--primary);
            margin: 0;
            line-height: 1;
        }

        .cover-content h2 {
            font-size: 2rem;
            color: var(--accent);
            margin: 1rem 0;
        }

        [contenteditable]:hover {
            cursor: text;
            background-color: rgba(212, 175, 55, 0.05);
        }

        @media (max-width: 768px) {
            .page-grid {
                grid-template-columns: 1fr;
            }
            .cover-page {
                flex-direction: column;
            }
            header h1 {
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body>

<header>
    <h1>Ramleela Dresses</h1>
    <p>Premium Collection 2025 Catalog</p>
</header>

<div class="container">
    <div class="page-grid">
"""

    for page in data:
        page_num = page["page"]
        blocks = page["blocks"]
        
        images = [b for b in blocks if b["type"] == "image"]
        texts = [b["content"] for b in blocks if b["type"] == "text"]

        if page_num == 1:
            # Special Cover Page Handling
            html_content += f"""
        <div class="cover-page">
            <div class="cover-visuals">
                {" ".join([f'<img src="{img["path"]}" alt="Catalog Item">' for img in images])}
            </div>
            <div class="cover-content">
                <h1 contenteditable="true">Ramleela</h1>
                <h2 contenteditable="true">Dresses</h2>
                <p contenteditable="true">Exclusive Religious & Cultural Attire since 2025</p>
            </div>
        </div>
"""
        else:
            # Regular Item Card
            title = texts[0] if texts else f"Page {page_num}"
            description = texts[1:] if len(texts) > 1 else []
            
            # Smart image selection: pick the largest area, but skip common background sizes
            main_image = ""
            if images:
                # Filter out the common background/logo overlay (usually ~1600x2100)
                product_images = [img for img in images if not (1590 <= img.get("width", 0) <= 1610 and 2100 <= img.get("height", 0) <= 2120)]
                
                if not product_images:
                    product_images = images # Fallback if only the background exists
                
                # Find the image with the max area
                main_image_obj = max(product_images, key=lambda x: x.get("width", 0) * x.get("height", 0))
                main_image = main_image_obj["path"]
            
            html_content += f"""
        <div class="card">
            <span class="tag">Collection 2025</span>
            <div class="card-image-container">
                {f'<img src="{main_image}" alt="{title}">' if main_image else '<div style="height:100%; display:flex; align-items:center; justify-content:center; color:#ccc;">No Image</div>'}
            </div>
            <div class="card-content">
                <h2 contenteditable="true">{title}</h2>
                <div class="card-text-container">
                    {" ".join([f'<div class="card-text" contenteditable="true">{t}</div>' for t in description])}
                </div>
            </div>
        </div>
"""

    html_content += """
    </div>
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
    generate_html("extracted_data.json")
