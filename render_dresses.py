import json
import os

def render_html():
    json_path = "ramleela_dresses_2025_data.json"
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
    <title>Ramleela Dresses 2025 Collection</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        :root { --primary: #2e7d32; --secondary: #fbc02d; --bg: #f1f8e9; --card-bg: #ffffff; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); margin: 0; padding: 40px 20px; color: #333; }
        header { text-align: center; margin-bottom: 50px; }
        h1 { color: var(--primary); font-size: 3em; margin: 0; }
        .subtitle { color: #666; font-size: 1.2em; }
        .catalog { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; max-width: 1400px; margin: 0 auto; }
        .item-card { background: var(--card-bg); border-radius: 15px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: transform 0.3s ease; display: flex; flex-direction: column; }
        .item-card:hover { transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,0.12); }
        .img-container { width: 100%; padding-bottom: 135%; position: relative; background: #fff; display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .item-image { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 15px; }
        .details { padding: 20px; border-top: 1px solid #eee; flex-grow: 1; }
        .product-title { color: var(--primary); font-size: 1.4em; font-weight: 700; margin: 0 0 5px 0; }
        .usage { color: #558b2f; font-size: 0.9em; font-weight: 600; margin-bottom: 15px; display: block; }
        .specs-table { width: 100%; border-collapse: collapse; font-size: 0.9em; margin-top: 10px; }
        .specs-table th { text-align: left; padding: 8px; border-bottom: 2px solid #eee; color: #666; font-weight: 600; }
        .specs-table td { padding: 8px; border-bottom: 1px solid #f9f9f9; }
        .price { font-weight: 700; color: #c62828; }
        .nav-back { text-align: center; margin-top: 50px; }
        .btn { display: inline-block; padding: 14px 35px; background: var(--primary); color: white; text-decoration: none; border-radius: 50px; font-weight: 600; transition: all 0.3s; }
        .btn:hover { background: #1b5e20; transform: scale(1.05); }
    </style>
</head>
<body>
    <header>
        <h1>Ramleela Dresses 2025</h1>
        <div class="subtitle">Complete Costume Collection for Epic Performances</div>
    </header>
    <div class="catalog">
"""

    # Structured data from PDF probe
    dresses_info = {
        2: {"name": "Barahbandi", "for": "Ram ji / Laxman ji / Sadhu", "prices": [("20\"", "165"), ("24\"", "175"), ("28\"", "250"), ("32\"", "375"), ("36\"", "400"), ("40\"", "400")]},
        3: {"name": "Barahbandi", "for": "Ravana Sadhu / Ravana Sena / Rakshas Sena", "prices": [("20\"", "165"), ("24\"", "175"), ("28\"", "250"), ("32\"", "375"), ("36\"", "400"), ("40\"", "400")]},
        4: {"name": "Saree", "for": "Seeta Vanwasi", "prices": [("20\"", "250"), ("24\"", "300"), ("28\"", "350"), ("32\"", "400"), ("36\"", "450"), ("40\"", "500")]},
        5: {"name": "Dhoti Patka", "for": "All Characters", "prices": [("20\"", "100"), ("24\"", "120"), ("28\"", "140"), ("32\"", "160"), ("36\"", "180"), ("40\"", "200")]},
        6: {"name": "Chester (3-8 Yrs)", "for": "Ramji / Laxmanji / Ravana / Raja", "prices": [("Small", "180")]},
        7: {"name": "Chester (10-12 Yrs)", "for": "Ramji / Laxmanji / Ravana / Raja", "prices": [("Medium", "275")]},
        8: {"name": "Chester", "for": "All Characters", "prices": [("Standard", "250")]},
        9: {"name": "Raja Coat", "for": "All Characters", "prices": [("20\"", "250"), ("24\"", "250"), ("28\"", "350"), ("32\"", "350")]},
        10: {"name": "Raja Dress", "for": "All Characters", "prices": [("20-28\"", "225")]},
        11: {"name": "Raja Dress", "for": "All Characters", "prices": [("Adult", "325")]},
        12: {"name": "Hanuman ji Dress", "for": "Hanuman ji / Sugreev / Bali", "prices": [("20\"", "285"), ("24\"", "300"), ("28\"", "325"), ("32\"", "350"), ("36\"", "700"), ("40\"", "700")]},
        13: {"name": "Vanara Sena Dress", "for": "Vanara Sena", "prices": [("20\"", "225"), ("24\"", "225"), ("28\"", "225"), ("32\"", "225")]},
        14: {"name": "White Jumpsuit", "for": "Jatau", "prices": [("32\"", "190"), ("36\"", "220"), ("40\"", "230"), ("44\"", "280"), ("48\"", "350")]},
        15: {"name": "Black Jumpsuit", "for": "Jamvant", "prices": [("32\"", "190"), ("36\"", "220"), ("40\"", "230"), ("44\"", "280"), ("48\"", "350")]},
        16: {"name": "Golden Jumpsuit", "for": "Maarich / Heeran", "prices": [("32\"", "190"), ("36\"", "220"), ("40\"", "230"), ("44\"", "280"), ("48\"", "350")]},
        17: {"name": "Bhoot Dress", "for": "Rakshas / Bhoot", "prices": [("24-32\"", "165"), ("40\"", "400")]},
        18: {"name": "Lehenga", "for": "Rani Seeta ji / Rani Character", "prices": [("20\"", "250"), ("24\"", "250"), ("28\"", "350"), ("32\"", "350"), ("36\"", "650"), ("40\"", "650")]},
        19: {"name": "Lehenga", "for": "Surphanaka / Trijata / Lady Rakshas", "prices": [("20\"", "250"), ("24\"", "250"), ("28\"", "350"), ("32\"", "350"), ("36\"", "650"), ("40\"", "650")]},
        20: {"name": "Mrigshala", "for": "Bhagwan Parshuram / Shankar ji", "prices": [("20-24\"", "90"), ("28\"", "175"), ("32\"", "225"), ("36-40\"", "300")]},
        21: {"name": "Mrigshala (Heavy)", "for": "Bhagwan Parshuram / Shankar ji", "prices": [("24\"", "180"), ("28\"", "200"), ("32\"", "225")]},
        22: {"name": "Kewat Dress", "for": "Kewat Character", "prices": [("20\"", "250"), ("24\"", "300"), ("28\"", "350"), ("32\"", "400"), ("36\"", "450"), ("40\"", "500")]},
        23: {"name": "Joker Dress", "for": "Comedy Character", "prices": [("20\"", "250"), ("24\"", "275"), ("28\"", "300"), ("32\"", "350"), ("36-40\"", "400"), ("Wig", "90"), ("Nose", "15")]}
    }

    for page_obj in data:
        p_num = page_obj.get("page", 0)
        # Skip cover
        if p_num <= 1: continue
        
        # In this catalog, each page is a single item with a single main image
        img_src = f"assets/Ramleela_Dresses_2025/page_{p_num}_full.png"
        
        info = dresses_info.get(p_num)
        if not info: continue
        
        title = info["name"]
        usage = info["for"]
        prices = info["prices"]
        
        rows_html = "".join([f"<tr><td>{p[0]}</td><td class='price'>₹{p[1]}</td></tr>" for p in prices])
        
        html += f"""
        <div class="item-card">
            <div class="img-container">
                <img src="{img_src}" alt="{title}" class="item-image" onerror="this.src='https://placehold.co/400x550?text=Page+{p_num}'" loading="lazy">
            </div>
            <div class="details">
                <h2 class="product-title">{title}</h2>
                <span class="usage">For: {usage}</span>
                <table class="specs-table">
                    <thead><tr><th>Size</th><th>Rate</th></tr></thead>
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
    
    with open("ramleela_dresses_2025_catalog.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Corrected ramleela_dresses_2025_catalog.html")

if __name__ == "__main__":
    render_html()
