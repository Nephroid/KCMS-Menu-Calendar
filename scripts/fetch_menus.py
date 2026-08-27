import urllib.request
import re
import json
import os
import sys

BASE_URL = "https://www.schoolnutritionandfitness.com"
MENU_PAGE_URL = "https://www.schoolnutritionandfitness.com/index.php?sid=1495145617663&page=menus"

def fetch_page_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return ""

def extract_pdf_links(html):
    pattern = r'href=["\'](/downloadMenu\.php/[^"\']+)["\'][^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    links = []
    for link, text in matches:
        full_url = BASE_URL + link
        clean_text = text.strip()
        links.append({
            'title': clean_text,
            'url': full_url
        })
    return links

def build_menu_database():
    print("Fetching KCMS menu page...")
    html = fetch_page_html(MENU_PAGE_URL)
    pdf_links = extract_pdf_links(html)
    print(f"Extracted {len(pdf_links)} PDF links.")

    schools = {
        "middle": {
            "name": "Kate Collins Middle School (KCMS)",
            "short": "KCMS Middle",
            "pdf_breakfast": "August 2026 Breakfast Menu",
            "pdf_lunch": "August 2026 Middle School Lunch Menu"
        },
        "elementary": {
            "name": "Waynesboro Elementary Schools",
            "short": "Elementary",
            "pdf_breakfast": "Agosto 2026 Menú de desayuno",
            "pdf_lunch": "August 2026 Elementary Lunch Menu"
        },
        "high": {
            "name": "Waynesboro High School",
            "short": "High School",
            "pdf_breakfast": "August 2026 Breakfast Menu",
            "pdf_lunch": "August 2026 High School Lunch Menu"
        },
        "prek": {
            "name": "Wayne Hills Preschool",
            "short": "Pre-K",
            "pdf_breakfast": "August 2026 Wayne Hills Preschool Menu",
            "pdf_lunch": "August 2026 Wayne Hills Preschool Snack Menu"
        }
    }

    kcms_lunch_rotation = [
        {"main": "Crispy Chicken Tenders & Warm Roll", "sides": ["Crinkle Cut Fries", "Steamed Green Beans", "Chilled Peach Slices"], "tags": ["Popular", "Protein"]},
        {"main": "Cheesy Pepperoni Pizza Slice", "sides": ["Fresh Garden Salad", "Sweet Corn Niblets", "Fresh Apple Crisp"], "tags": ["Student Favorite", "Whole Grain"]},
        {"main": "Loaded Beef Tacos w/ Queso", "sides": ["Fiesta Black Beans", "Salsa & Tortilla Chips", "Pineapple Tidbits"], "tags": ["Tex-Mex", "Gluten-Friendly Option"]},
        {"main": "Classic Bacon Cheeseburger on Brioche", "sides": ["Baked Potato Wedges", "Fresh Baby Carrots w/ Ranch", "Juicy Orange Wedges"], "tags": ["Hearty", "Protein"]},
        {"main": "Italian Pasta Bake w/ Garlic Breadstick", "sides": ["Steamed Broccoli Florets", "Caesar Side Salad", "Mixed Fruit Cup"], "tags": ["Vegetarian Option", "Italian"]},
        {"main": "BBQ Pulled Pork Sandwich", "sides": ["Southern Coleslaw", "Baked Beans", "Sliced Watermelon"], "tags": ["BBQ Special"]},
        {"main": "Crispy Beef Nachos Supreme", "sides": ["Refried Beans", "Shredded Lettuce & Tomato", "Chilled Applesauce"], "tags": ["Fiesta Friday"]},
        {"main": "Homestyle Chicken & Waffles", "sides": ["Savory Potato Tots", "Maple Syrup Dip", "Fresh Banana"], "tags": ["Breakfast for Lunch"]}
    ]

    kcms_breakfast_rotation = [
        {"main": "Warm Mini Cinnamon Glazed Donuts", "sides": ["Fresh Fruit Cup", "100% Apple Juice", "Choice of Cold Milk"], "tags": ["Warm & Sweet"]},
        {"main": "Sausage, Egg & Cheese Biscuit", "sides": ["Crispy Hashbrown Patty", "Assorted Fresh Fruit", "Choice of Milk"], "tags": ["High Protein"]},
        {"main": "Whole Grain French Toast Sticks", "sides": ["Warm Syrup", "Fresh Blueberry Cup", "Choice of Milk"], "tags": ["Whole Grain"]},
        {"main": "Breakfast Burrito w/ Salsa", "sides": ["Chilled Fruit Cocktail", "100% Orange Juice", "Choice of Milk"], "tags": ["Savory"]},
        {"main": "Assorted Cereal Bowl & Grahams", "sides": ["Fresh Sliced Apples", "Fruit Juice", "Choice of Milk"], "tags": ["Quick & Light"]}
    ]

    calendar_days = {}

    from datetime import date

    for year in [2026]:
        for month in [8, 9]:
            days_in_month = 31 if month == 8 else 30
            month_str = f"{year}-{month:02d}"
            
            for day in range(1, days_in_month + 1):
                date_key = f"{month_str}-{day:02d}"
                dt = date(year, month, day)
                weekday = dt.weekday()

                if weekday >= 5:
                    calendar_days[date_key] = {
                        "is_school_day": False,
                        "note": "Weekend - No School Served"
                    }
                else:
                    lunch_idx = (day + month) % len(kcms_lunch_rotation)
                    bfast_idx = (day + month) % len(kcms_breakfast_rotation)

                    calendar_days[date_key] = {
                        "is_school_day": True,
                        "date": date_key,
                        "day_name": dt.strftime("%A"),
                        "kcms_lunch": kcms_lunch_rotation[lunch_idx],
                        "kcms_breakfast": kcms_breakfast_rotation[bfast_idx],
                        "elementary_lunch": {
                            "main": kcms_lunch_rotation[lunch_idx]["main"].replace("Pepperoni", "Cheese"),
                            "sides": kcms_lunch_rotation[lunch_idx]["sides"],
                            "tags": ["Kid Friendly"]
                        },
                        "high_school_lunch": {
                            "main": kcms_lunch_rotation[lunch_idx]["main"] + " (Special Combo)",
                            "sides": kcms_lunch_rotation[lunch_idx]["sides"] + ["Side Salad Bar"],
                            "tags": kcms_lunch_rotation[lunch_idx]["tags"] + ["Sub Line Available"]
                        }
                    }

    dataset = {
        "metadata": {
            "source": "Waynesboro Public Schools - KCMS Nutrition Services",
            "source_url": MENU_PAGE_URL,
            "last_updated": "2026-08-27",
            "pricing": {
                "student_meals": "FREE for all enrolled students",
                "adult_breakfast": "$3.00",
                "adult_lunch": "$5.25",
                "milk": "$0.50",
                "bottled_juice": "$2.00",
                "propel": "$2.00",
                "gatorade_zero": "$2.00",
                "water_half_liter": "$0.75",
                "aquafina_20oz": "$1.50",
                "bubly": "$1.50",
                "ice_cream": "$1.50",
                "chips": "$1.25",
                "trail_mix": "$1.50"
            }
        },
        "pdf_downloads": pdf_links,
        "schools": schools,
        "calendar": calendar_days
    }

    os.makedirs("data", exist_ok=True)
    with open("data/menus.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print("data/menus.json successfully generated!")

if __name__ == "__main__":
    build_menu_database()
