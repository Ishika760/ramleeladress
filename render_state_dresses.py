import json
import os

def render_html():
    json_path = "state_dress_new_2024_data.json"
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
    <title>State Dress Collection 2024</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        :root { --primary: #4527a0; --secondary: #ff6f00; --bg: #f3e5f5; --card-bg: #ffffff; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); margin: 0; padding: 40px 20px; color: #333; }
        header { text-align: center; margin-bottom: 50px; }
        h1 { color: var(--primary); font-size: 3em; margin: 0; }
        .subtitle { color: #666; font-size: 1.2em; }
        .catalog { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; max-width: 1400px; margin: 0 auto; }
        .item-card { background: var(--card-bg); border-radius: 15px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: transform 0.3s ease; display: flex; flex-direction: column; }
        .item-card:hover { transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,0.12); }
        .img-container { width: 100%; padding-bottom: 141%; position: relative; background: #fff; overflow: hidden; }
        .item-image { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; }
        .details { padding: 20px; border-top: 1px solid #eee; flex-grow: 1; }
        .product-title { color: var(--primary); font-size: 1.4em; font-weight: 700; margin: 0 0 5px 0; }
        .art-no { color: #888; font-size: 0.9em; margin-bottom: 15px; font-weight: 600; }
        .specs-table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
        .specs-table th { text-align: left; padding: 6px; border-bottom: 2px solid #eee; color: #666; }
        .specs-table td { padding: 6px; border-bottom: 1px solid #f9f9f9; }
        .price { font-weight: 700; color: #c62828; }
        .nav-back { text-align: center; margin-top: 50px; }
        .btn { display: inline-block; padding: 14px 35px; background: var(--primary); color: white; text-decoration: none; border-radius: 50px; font-weight: 600; transition: all 0.3s; }
    </style>
</head>
<body>
    <header>
        <h1>Traditional State Dresses</h1>
        <div class="subtitle">Ethnic Collection of India and Beyond</div>
    </header>
    <div class="catalog">
"""

    # Data for State Dresses based on probe
    # Note: These are often pairs (Boy/Girl), so we list them as such.
    state_dresses = {
        1: [
            {"name": "ANDHRA PRADESH (Boy/Girl)", "art": "303/304", "prices": "350 - 600"},
            {"name": "BENGALI (Boy/Girl)", "art": "305/306", "prices": "300 - 700"},
            {"name": "BIHARI (Boy/Girl)", "art": "307/308", "prices": "300 - 650"}
        ],
        2: [
            {"name": "GARWALI (Boy/Girl)", "art": "309/310", "prices": "450 - 750"}
        ],
        3: [
            {"name": "GOA (Boy/Girl)", "art": "311/312", "prices": "350 - 650"},
            {"name": "GUJRATI (Boy/Girl)", "art": "313/314", "prices": "500 - 1000"},
            {"name": "HARYANVI (Boy/Girl)", "art": "315/316", "prices": "400 - 1000"},
            {"name": "HIMACHALI (Boy/Girl)", "art": "317/318", "prices": "400 - 750"},
            {"name": "KASHMIRI (Boy/Girl)", "art": "319/320", "prices": "400 - 900"}
        ],
        4: [
            {"name": "MARATHI (Boy/Girl)", "art": "321/322", "prices": "300 - 700"},
            {"name": "PUNJABI (Boy/Girl)", "art": "323/324", "prices": "300 - 800"},
            {"name": "RAJASTHANI (Boy/Girl)", "art": "325/326", "prices": "350 - 600"},
            {"name": "NAGALAND (Boy/Girl)", "art": "327/328", "prices": "350 - 700"},
            {"name": "MANIPURI (Boy/Girl)", "art": "331/332", "prices": "450 - 900"}
        ],
        5: [
            {"name": "CHINESE (Boy/Girl)", "art": "333/334", "prices": "450 - 700"},
            {"name": "JAPNESE (Boy/Girl)", "art": "335/336", "prices": "450 - 750"},
            {"name": "ODISSI GIRL / MEGHALAYA", "art": "330/337", "prices": "650 - 1500"}
        ]
    }

    # Helper pricing templates based on common ranges in PDF
    def get_standard_ranges():
        return [
            ("20\" (3-4 Y)", "₹300-500"),
            ("24\" (5-6 Y)", "₹350-550"),
            ("28\" (7-8 Y)", "₹400-600"),
            ("32\" (9-12 Y)", "₹450-700"),
            ("36\" (13-16 Y)", "₹550-800"),
            ("40\" (Adult)", "₹600-900")
        ]

    for p_num in sorted(state_dresses.keys()):
        img_src = f"assets/State_Dress_New_2024/page_{p_num}_full.png"
        group = state_dresses[p_num]
        
        # In this catalog, multiple items are on one page. 
        # We'll render the full page image first, then list the items below it or as separate cards if images were cropped.
        # But here we used full-page rendering, so we can either:
        # 1. Page-based cards (Easiest and cleanest with full-page images)
        # 2. Extract coordinates (More complex)
        
        # Let's do a card per group member, but they all share the page image. 
        # This highlights the info clearly.
        
        for item in group:
            title = item["name"]
            art = item["art"]
            price_range = item["prices"]
            
            rows_html = "".join([f"<tr><td>{p[0]}</td><td class='price'>{p[1]}</td></tr>" for p in get_standard_ranges()])
            
            html += f"""
        <div class="item-card">
            <div class="img-container">
                <img src="{img_src}" alt="{title}" class="item-image" loading="lazy">
            </div>
            <div class="details">
                <h2 class="product-title">{title}</h2>
                <div class="art-no">NO. {art}</div>
                <div style="font-weight: 700; color: #c62828; margin-bottom: 10px;">Range: ₹{price_range}</div>
                <table class="specs-table">
                    <thead><tr><th>Size / Age</th><th>Estimated Rate</th></tr></thead>
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
    
    with open("state_dress_new_2024_catalog.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Created state_dress_new_2024_catalog.html")

if __name__ == "__main__":
    render_html()
