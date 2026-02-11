import json
import os

def render_html():
    json_path = "ramleela_accesories_2025_data.json"
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
    <title>Ramleela Accessories Collection</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        :root { --primary: #c62828; --secondary: #ff8f00; --bg: #fffbf1; --card-bg: #ffffff; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); margin: 0; padding: 40px 20px; color: #333; }
        header { text-align: center; margin-bottom: 50px; }
        h1 { color: var(--primary); font-size: 3em; margin: 0; }
        .subtitle { color: #666; font-size: 1.2em; }
        .catalog { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; max-width: 1400px; margin: 0 auto; }
        .item-card { background: var(--card-bg); border-radius: 15px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: transform 0.3s ease; display: flex; flex-direction: column; }
        .item-card:hover { transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,0.15); }
        .img-container { width: 100%; padding-bottom: 125%; position: relative; background: #fff; display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .item-image { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 15px; }
        .details { padding: 20px; border-top: 1px solid #eee; flex-grow: 1; text-align: center; }
        .product-title { color: var(--primary); font-size: 1.4em; font-weight: 700; margin: 0 0 5px 0; }
        .price { font-size: 1.5em; font-weight: 700; color: var(--secondary); margin-top: 10px; }
        .nav-back { text-align: center; margin-top: 50px; }
        .btn { display: inline-block; padding: 14px 35px; background: var(--primary); color: white; text-decoration: none; border-radius: 50px; font-weight: 600; transition: all 0.3s; }
        .btn:hover { background: #8e0000; transform: scale(1.05); }
    </style>
</head>
<body>
    <header>
        <h1>Ramleela Accessories</h1>
        <div class="subtitle">Complete Collection of Props and Accessories</div>
    </header>
    <div class="catalog">
"""

    accessory_names = {
        2: ["Jatau", "Jamvant", "Heeran", "Tiger", "Face (Rubber)"],
        3: ["Hanuman ji", "Crow", "Kaali Mata", "Ganesh Ji", "Face (Rubber)"],
        4: ["Lion", "Bear", "Joker", "Cow", "Face (Rubber)"],
        5: ["Hanuman ji face (Fiber)"],
        6: ["Ganeshji face (Fiber)"],
        7: ["Hanuman ji mouth"],
        8: ["Ravana face"],
        9: ["Narsingh Face"],
        10: ["Ganesh Soond"],
        11: ["Kaali Face"],
        12: ["Peetal Mukut"],
        13: ["Bhoot Face"],
        14: ["Bhoot Face"],
        15: ["Mund"],
        16: ["Plastic Mund"],
        17: ["Mundmala (125)"],
        18: ["Mundmala (180)"],
        19: ["Mundmala (240)"],
        20: ["PanjaMala (325)"],
        21: ["Mundmala (350)"],
        22: ["Mundmala (1000)"],
        23: ["Hand Leg"],
        24: ["Chester (180)"],
        25: ["Chester (250)"],
        26: ["Raja Rob (180)"],
        27: ["Raja Rob (300)"],
        28: ["Talwar Plastic (75)"],
        29: ["Talwar Plastic (80)"],
        30: ["Talwar Plastic (90)"],
        31: ["Shastra"],
        32: ["Axe"],
        33: ["Hammer"],
        34: ["Talwar (Medium)"],
        35: ["Talwar (Large)"],
        36: ["Dhanush (Mixed Sizes)"],
        37: ["Dhanush (Small to Large)"],
        38: ["Dhanush Folding (Small)"],
        39: ["Dhanush Folding (Big)"],
        40: ["Tarkash"],
        41: ["Hanuman ji tail"],
        42: ["Folding Gada Plastic"],
        43: ["Gada"],
        44: ["Peetal Gada"],
        45: ["Trishul Plastic"],
        46: ["Trishul Fal"],
        47: ["Bhale"],
        48: ["Folding Trishul"],
        49: ["Farsa"],
        50: ["Khanda"],
        51: ["Chakra"],
        52: ["Rudrakshmala"],
        53: ["Rudraksh Bajuband"],
        54: ["Kundal"],
        55: ["Golden Kundal"],
        56: ["Kundal"],
        57: ["Ram Mala set"],
        58: ["Teer Pkt"],
        59: ["Golden Kanthe"],
        60: ["Khadtal"],
        61: ["Handmala (Small)"],
        62: ["Handmala (Big)"],
        63: ["Cobra"],
        64: ["Sadhu teki"],
        65: ["Veena"],
        66: ["Khadau"],
        67: ["Bhuja set"],
        68: ["Damru"],
        69: ["Beard Black (Bandhne wali)"],
        70: ["Beard White (Bandhne wali)"],
        71: ["Beard Orange"],
        72: ["Pancake (Makeup)"]
    }

    price_map = {
        2: "190", 3: "190", 4: "190", 5: "55", 6: "225 - 275", 7: "45-50", 8: "210", 9: "500", 10: "450",
        11: "1200", 12: "1500", 13: "190", 14: "240", 15: "250", 16: "190", 17: "125", 18: "180", 19: "240",
        20: "325", 21: "350", 22: "1000", 23: "190", 24: "180", 25: "250", 26: "180", 27: "300", 28: "75",
        29: "80", 30: "90", 31: "100", 32: "140", 33: "200", 34: "210", 35: "225", 36: "90-290", 37: "100-120",
        38: "75", 39: "150", 40: "60-90", 41: "540-720", 42: "85-150", 43: "180-350", 44: "1250/kg",
        45: "75", 46: "45-120", 47: "45-120", 48: "1050", 49: "180", 50: "270", 51: "150", 52: "396",
        53: "300", 54: "132", 55: "132", 56: "72", 57: "140", 58: "250", 59: "210", 60: "85-115",
        61: "350", 62: "600", 63: "275", 64: "190", 65: "165-350", 66: "75", 67: "390", 68: "45-90",
        69: "45-75", 70: "45-75", 71: "70", 72: "500"
    }

    for page_obj in data:
        p_num = page_obj.get("page", 0)
        if p_num == 0: continue
        
        img_src = f"assets/Ramleela_Accesories_2025/page_{p_num}_full.png"
        
        names_for_page = accessory_names.get(p_num, [])
        price = price_map.get(p_num, "")

        title = " / ".join(names_for_page) if names_for_page else f"Accessory Page {p_num}"

        html += f"""
        <div class="item-card">
            <div class="img-container">
                <img src="{img_src}" alt="{title}" class="item-image" onerror="this.src='https://placehold.co/400x500?text=Image+Missing'" loading="lazy">
            </div>
            <div class="details">
                <h2 class="product-title">{title}</h2>
                <div class="price">₹{price}</div>
            </div>
        </div>
"""

    html += """
    </div>
    <div class="nav-back">
        <a href="index.html" class="btn">← Back to Dashboard</a>
    </div>
</body>
</html>
"""
    
    with open("ramleela_accesories_2025_catalog.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Corrected ramleela_accesories_2025_catalog.html")

if __name__ == "__main__":
    render_html()
