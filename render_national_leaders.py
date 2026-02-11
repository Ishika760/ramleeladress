import json
import os

def render_html():
    json_path = "national_leaders_2024_data.json"
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
    <title>National Leaders 2024 Collection</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        :root { --primary: #1a237e; --secondary: #c62828; --bg: #f5f5f5; --card-bg: #ffffff; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); margin: 0; padding: 40px 20px; color: #333; }
        header { text-align: center; margin-bottom: 50px; }
        h1 { color: var(--primary); font-size: 3em; margin: 0; }
        .subtitle { color: #666; font-size: 1.2em; }
        .catalog { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; max-width: 1400px; margin: 0 auto; }
        .item-card { background: var(--card-bg); border-radius: 15px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: transform 0.3s ease; display: flex; flex-direction: column; }
        .item-card:hover { transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,1.2); }
        .img-container { width: 100%; padding-bottom: 125%; position: relative; background: #fff; display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .item-image { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 15px; }
        .details { padding: 20px; border-top: 1px solid #eee; flex-grow: 1; }
        .product-title { color: var(--primary); font-size: 1.4em; font-weight: 700; margin: 0 0 5px 0; }
        .art-no { color: #888; font-size: 0.9em; margin-bottom: 15px; font-weight: 600; }
        .specs-table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
        .specs-table th { text-align: left; padding: 8px; border-bottom: 2px solid #eee; color: #666; font-weight: 600; }
        .specs-table td { padding: 8px; border-bottom: 1px solid #f9f9f9; }
        .price { font-weight: 700; color: var(--secondary); }
        .nav-back { text-align: center; margin-top: 50px; }
        .btn { display: inline-block; padding: 14px 35px; background: var(--primary); color: white; text-decoration: none; border-radius: 50px; font-weight: 600; transition: all 0.3s; }
        .btn:hover { background: #0d1245; transform: scale(1.05); }
    </style>
</head>
<body>
    <header>
        <h1>National Leaders 2024</h1>
        <div class="subtitle">Premium Freedom Fighter & Historical Costumes</div>
    </header>
    <div class="catalog">
"""

    # Structured data from PDF probe
    leaders_info = {
        1: [
            {"name": "Abdul.kalam", "art": "601"},
            {"name": "Bal Ganga Dhar Tilak", "art": "602"},
            {"name": "Bhagat Singh", "art": "603"},
            {"name": "BHARAT MATA", "art": "604"}
        ],
        2: [
            {"name": "BRITISH OFFICER", "art": "605"},
            {"name": "CHANDRA SHEKHAR AZAD", "art": "606"},
            {"name": "CHRISTIAN", "art": "607"},
            {"name": "GANDHI JI", "art": "608"}
        ],
        3: [
            {"name": "HINDU", "art": "609"},
            {"name": "INDIRA GANDHI", "art": "610"},
            {"name": "JAWAHAR LAL NEHRU", "art": "611"},
            {"name": "LAL BAHADUR SHASTRI", "art": "612"}
        ],
        4: [
            {"name": "MANGAL PANDEY", "art": "613"},
            {"name": "MOTHER TERESA", "art": "614"},
            {"name": "MUSLIM", "art": "615"},
            {"name": "NETA JI", "art": "616"}
        ],
        5: [
            {"name": "POLITICAL MAN", "art": "617"},
            {"name": "RAJ GURU", "art": "618"},
            {"name": "RANI LAXMI BAI", "art": "619"},
            {"name": "SARDAR VALLABH BHAI PATEL", "art": "620"}
        ],
        6: [
            {"name": "SHIVA JI MAHARAJ", "art": "621"},
            {"name": "SUBHASH CHANDRA BOSS", "art": "622"},
            {"name": "SUKH DEV", "art": "623"},
            {"name": "SWAMI VIVEKANAND", "art": "624"}
        ],
        7: [
            {"name": "TERRORIST", "art": "625"},
            {"name": "TIPU SULTAN", "art": "626"}
        ]
    }

    # Helper function to get variants (pricing etc)
    # Most leaders have the same 3-4 sizes per page structure
    def get_pricing_for_leader(p_num, l_idx):
        # We'll use a standard template based on the PDF probe results
        # Bhagat Singh (P1)
        if p_num == 1 and l_idx == 1: # Bhagat Singh
            return [
                {"sz": "20\"", "age": "3-4 YEAR", "rate": "500.00"},
                {"sz": "24\"", "age": "5-6 YEAR", "rate": "500.00"},
                {"sz": "28\"", "age": "7-8 YEAR", "rate": "550.00"},
                {"sz": "32\"", "age": "9-12 YEAR", "rate": "600.00"},
                {"sz": "36\"", "age": "13-16 YEAR", "rate": "700.00"},
                {"sz": "40\"", "age": "17 ADULT", "rate": "700.00"}
            ]
        # Sardar Vallabh Bhai (P5)
        if p_num == 5 and l_idx == 3:
            return [
                {"sz": "20\"", "age": "3-4 YEAR", "rate": "450.00"},
                {"sz": "24\"", "age": "5-6 YEAR", "rate": "450.00"},
                {"sz": "28\"", "age": "7-8 YEAR", "rate": "450.00"},
                {"sz": "32\"", "age": "9-12 YEAR", "rate": "500.00"},
                {"sz": "36\"", "age": "13-16 YEAR", "rate": "600.00"},
                {"sz": "40\"", "age": "17 ADULT", "rate": "600.00"}
            ]
        # Default pricing for most
        return [
            {"sz": "20\"", "age": "3-4 YEAR", "rate": "400.00"},
            {"sz": "24\"", "age": "5-6 YEAR", "rate": "450.00"},
            {"sz": "28\"", "age": "7-8 YEAR", "rate": "500.00"},
            {"sz": "32\"", "age": "9-12 YEAR", "rate": "550.00"}
        ]

    for page in data:
        p_num = page.get("page", 0)
        items = page.get("items", [])
        
        # Sort images visually (Top to Bottom)
        all_imgs = []
        for item in items:
            for img in item.get("images", []):
                if img['width'] > 50: all_imgs.append(img)
        all_imgs.sort(key=lambda x: x['top'])
        
        info_list = leaders_info.get(p_num, [])
        
        for i, img in enumerate(all_imgs):
            if i < len(info_list):
                info = info_list[i]
                title = info['name']
                art = info['art']
                vars = get_pricing_for_leader(p_num, i)
                
                rows_html = "".join([f"<tr><td>{v['sz']}</td><td>{v['age']}</td><td class='price'>₹{v['rate']}</td></tr>" for v in vars])
                
                html += f"""
        <div class="item-card">
            <div class="img-container">
                <img src="{img['path']}" alt="{title}" class="item-image" loading="lazy">
            </div>
            <div class="details">
                <h2 class="product-title">{title}</h2>
                <div class="art-no">{art}</div>
                <table class="specs-table">
                    <thead><tr><th>Size</th><th>Age</th><th>Rate</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </div>
"""

    html += """
    </div>
    <div class="nav-back">
        <a href="index.html" class="btn">← Back to Collections</a>
    </div>
</body>
</html>
"""
    
    with open("national_leaders_2024_catalog.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Corrected national_leaders_2024_catalog.html")

if __name__ == "__main__":
    render_html()
