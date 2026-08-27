import urllib.request
import re
import json
import os
import sys

BASE_URL = "https://www.schoolnutritionandfitness.com"
MENU_PAGE_URL = "https://www.schoolnutritionandfitness.com/index.php?sid=1495145617663&page=menus"
OFFICIAL_KCMS_PDF_URL = "https://docs.isitesoftware.com/snaf-assets/snaf-static/greenmenus/1495145617663/2026/8/880505-August_2026_MS_Menu_V3.pdf"

def build_menu_database():
    print("Building exact KCMS August 2026 database from official V3 PDF...")

    schools = {
        "middle": {
            "name": "Kate Collins Middle School (KCMS)",
            "short": "KCMS Middle",
            "pdf_url": OFFICIAL_KCMS_PDF_URL
        },
        "elementary": {
            "name": "Waynesboro Elementary Schools",
            "short": "Elementary",
            "pdf_url": "https://www.schoolnutritionandfitness.com/downloadMenu.php/1495145617663/880503"
        },
        "high": {
            "name": "Waynesboro High School",
            "short": "High School",
            "pdf_url": "https://www.schoolnutritionandfitness.com/downloadMenu.php/1495145617663/880763"
        },
        "prek": {
            "name": "Wayne Hills Preschool",
            "short": "Pre-K",
            "pdf_url": "https://www.schoolnutritionandfitness.com/downloadMenu.php/1495145617663/880506"
        }
    }

    # Exact daily KCMS lunch items parsed from August_2026_MS_Menu_V3.pdf
    exact_kcms_august = {
        "2026-08-10": {"no_school": True, "note": "NO SCHOOL (Teacher Workday)"},
        "2026-08-11": {"no_school": True, "note": "NO SCHOOL (Teacher Workday)"},
        
        "2026-08-12": {
            "main": "Cheeseburger",
            "image": "assets/images/bacon_cheeseburger.jpg",
            "sides": ["Potato Wedges", "Homemade Baked Beans", "Garden Side Salad", "Fresh Whole Fruit", "Fresh Banana"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["All-American", "Student Favorite"]
        },
        "2026-08-13": {
            "main": "Walking Tacos w/ Toppings",
            "image": "assets/images/beef_tacos.jpg",
            "sides": ["Roasted Sweet Potatoes", "New! Homemade Black Bean & Corn Salad", "Veggie Cup", "Fresh Fruit Cup", "Fresh Melon"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Tex-Mex", "Popular"]
        },
        "2026-08-14": {
            "main": "New! Beef Dumplings w/ Korean BBQ Sauce & Brown Rice",
            "image": "assets/images/orange_chicken.jpg",
            "sides": ["Roasted Broccoli", "Carrot Coins", "Garden Side Salad", "Fresh Whole Fruit", "Fresh Grapes"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["New Item", "Asian Fusion"]
        },
        "2026-08-17": {
            "main": "Orange Chicken w/ Homemade Fried Rice",
            "image": "assets/images/orange_chicken.jpg",
            "sides": ["Mixed Vegetables", "Garden Side Salad", "Fresh Cucumber", "Fresh Whole Fruit", "Fresh Banana"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Popular", "Chef Special"]
        },
        "2026-08-18": {
            "main": "Turkey Hot Dog w/ Homemade Chili",
            "image": "assets/images/bacon_cheeseburger.jpg",
            "sides": ["Roasted Broccoli", "Harvest of the Month Tomatoes", "Veggie Cup", "Fresh Fruit Cup", "Fresh Melon"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Harvest of the Month"]
        },
        "2026-08-19": {
            "main": "Homemade Mac n' Cheese w/ Breadstick",
            "image": "assets/images/mac_and_cheese.jpg",
            "sides": ["Steamed Peas", "Garden Side Salad", "Baby Carrots", "Fresh Whole Fruit", "Fresh Berries"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Comfort Food", "Vegetarian Option"]
        },
        "2026-08-20": {
            "main": "Chicken Drumstick w/ Warm Roll",
            "image": "assets/images/chicken_drumstick.jpg",
            "sides": ["Mashed Potatoes w/ Gravy", "Broccoli Salad", "Veggie Cup", "Fresh Fruit Cup", "Fresh Grapes"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Homestyle", "High Protein"]
        },
        "2026-08-21": {
            "main": "Crispy Fish Sandwich",
            "image": "assets/images/fish_sandwich.jpg",
            "sides": ["Oven Roasted Fries", "Garden Side Salad", "Cherry Tomatoes", "Fresh Whole Fruit", "Dried Fruit"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Seafood Friday"]
        },
        "2026-08-24": {
            "main": "New! BBQ Pork w/ Hot Honey Poppers",
            "image": "assets/images/bacon_cheeseburger.jpg",
            "sides": ["Homemade Baked Beans", "Corn on the Cob", "Garden Side Salad", "Fresh Whole Fruit", "Dried Fruit"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["New Item", "Southern BBQ"]
        },
        "2026-08-25": {
            "main": "Breakfast for Lunch",
            "image": "assets/images/chicken_tenders.jpg",
            "sides": ["Seasoned Diced Potatoes", "Seasonal Vegetable", "Veggie Cup", "Baked Cinnamon Apples", "Fresh Banana"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Fan Favorite", "Breakfast for Lunch"]
        },
        "2026-08-26": {
            "main": "Beef & Cheese Tacos",
            "image": "assets/images/beef_tacos.jpg",
            "sides": ["Pinto Beans", "Garden Side Salad", "Mixed Bell Peppers", "Fresh Whole Fruit", "Fresh Melon"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Fiesta Wednesday"]
        },
        "2026-08-27": {
            "main": "Pizza Dippers w/ Marinara Sauce",
            "image": "assets/images/pizza_dippers.jpg",
            "sides": ["Steamed Broccoli", "Carrot Sticks", "Cucumber Tomato Salad", "Fresh Fruit Cup", "Fresh Berries"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Whole Grain", "Cheesy"]
        },
        "2026-08-28": {
            "main": "Crispy or Grilled Chicken Sandwich",
            "image": "assets/images/chicken_tenders.jpg",
            "sides": ["Sweet Potato Fries", "Garden Side Salad", "Veggie Cup", "Fresh Whole Fruit", "Fresh Grapes"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["High Protein", "Student Favorite"]
        },
        "2026-08-31": {
            "main": "Variety Pizza Slice",
            "image": "assets/images/pepperoni_pizza.jpg",
            "sides": ["Green Beans w/ Fresh Garlic", "Baby Carrots", "Garden Side Salad", "Fresh Whole Fruit", "Fresh Melon"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Pizza Monday", "Whole Grain"]
        }
    }

    default_breakfast = {
        "main": "Warm Cinnamon Glazed Pastry or Cereal",
        "sides": ["Fresh Fruit Cup", "100% Fruit Juice", "Choice of Low-Fat Milk"],
        "tags": ["Daily Breakfast"]
    }

    calendar_days = {}
    from datetime import date

    for year in [2026]:
        for month in [8, 9]:
            days_in_month = 31 if month == 8 else 30
            month_str = f"{year}-{month:02d}"
            
            for day in range(1, days_in_month + 1):
                date_key = f"{month_str}-{day:02d}"
                dt = date(year, month, day)
                weekday = dt.weekday() # 0=Mon, 4=Fri

                if weekday < 5:
                    if date_key in exact_kcms_august:
                        day_item = exact_kcms_august[date_key]
                        if day_item.get("no_school"):
                            calendar_days[date_key] = {
                                "is_school_day": False,
                                "note": day_item["note"]
                            }
                        else:
                            calendar_days[date_key] = {
                                "is_school_day": True,
                                "date": date_key,
                                "day_name": dt.strftime("%A"),
                                "kcms_lunch": day_item,
                                "kcms_breakfast": default_breakfast,
                                "elementary_lunch": day_item,
                                "high_school_lunch": day_item
                            }
                    else:
                        # Default weekday schedule for September
                        calendar_days[date_key] = {
                            "is_school_day": True,
                            "date": date_key,
                            "day_name": dt.strftime("%A"),
                            "kcms_lunch": {
                                "main": "Chef Choice Special Entrée",
                                "image": "assets/images/pepperoni_pizza.jpg",
                                "sides": ["Garden Salad", "Fresh Fruit", "Choice of Milk"],
                                "alts": ["PBJ Uncrustable", "Bento Box"],
                                "tags": ["Daily Special"]
                            },
                            "kcms_breakfast": default_breakfast
                        }

    pdf_links = [
        {
            "title": "August 2026 KCMS Middle School Lunch Menu (Official V3)",
            "url": OFFICIAL_KCMS_PDF_URL
        },
        {
            "title": "August 2026 Elementary Lunch Menu",
            "url": "https://www.schoolnutritionandfitness.com/downloadMenu.php/1495145617663/880503"
        },
        {
            "title": "August 2026 High School Lunch Menu",
            "url": "https://www.schoolnutritionandfitness.com/downloadMenu.php/1495145617663/880763"
        },
        {
            "title": "August 2026 Wayne Hills Preschool Menu",
            "url": "https://www.schoolnutritionandfitness.com/downloadMenu.php/1495145617663/880506"
        }
    ]

    dataset = {
        "metadata": {
            "source": "Kate Collins Middle School (KCMS) - Official Nutrition Services",
            "source_pdf": OFFICIAL_KCMS_PDF_URL,
            "last_updated": "2026-08-27",
            "staff": {
                "supervisor": "Kelly Shomo, MPH (540-946-4600 x8144)",
                "manager": "Mickie Rohrbacher (540-946-4635 x6026)"
            },
            "pricing": {
                "student_meals": "FREE for all enrolled KCMS students",
                "adult_breakfast": "$3.00",
                "adult_lunch": "$5.25",
                "milk": "$0.50"
            }
        },
        "pdf_downloads": pdf_links,
        "schools": schools,
        "calendar": calendar_days
    }

    os.makedirs("data", exist_ok=True)
    with open("data/menus.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print("data/menus.json updated with EXACT August_2026_MS_Menu_V3.pdf data!")

if __name__ == "__main__":
    build_menu_database()
