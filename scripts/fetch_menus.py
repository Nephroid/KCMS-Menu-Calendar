import json
import os
from datetime import date

OFFICIAL_KCMS_SEP_LUNCH_PDF = "https://www.schoolnutritionandfitness.com/downloadMenu.php/1495145617663/888538"
OFFICIAL_KCMS_SEP_BFAST_PDF = "https://www.schoolnutritionandfitness.com/downloadMenu.php/1495145617663/893592"
OFFICIAL_KCMS_AUG_LUNCH_PDF = "https://docs.isitesoftware.com/snaf-assets/snaf-static/greenmenus/1495145617663/2026/8/880505-August_2026_MS_Menu_V3.pdf"
OFFICIAL_KCMS_AUG_BFAST_PDF = "https://docs.isitesoftware.com/snaf-assets/snaf-static/greenmenus/1495145617663/2026/8/880509-August_2026_Breakfast_Menu_V2.pdf"

def build_menu_database():
    print("Building KCMS August + September 2026 menu database...")

    schools = {
        "middle": {
            "name": "Kate Collins Middle School (KCMS)",
            "short": "KCMS Middle",
        }
    }

    # ── AUGUST 2026 LUNCH (from Lunch V3 PDF) ──────────────────────────────
    august_lunch = {
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
            "sides": ["Roasted Sweet Potatoes", "Homemade Black Bean & Corn Salad", "Veggie Cup", "Fresh Fruit Cup", "Fresh Melon"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Tex-Mex", "Popular"]
        },
        "2026-08-14": {
            "main": "Beef Dumplings w/ Korean BBQ Sauce & Brown Rice",
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
            "main": "BBQ Pork w/ Hot Honey Poppers",
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
        },
    }

    # ── AUGUST 2026 BREAKFAST (from Breakfast V2 PDF) ──────────────────────
    august_bfast = {
        "2026-08-12": {"main": "Egg & Cheese Croissant", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Hot Breakfast"]},
        "2026-08-13": {"main": "Homemade Breakfast Pizza", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Fruit & Yogurt Parfait", "Fresh Banana", "Dried Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["New Item"]},
        "2026-08-14": {"main": "Bagel Bites w/ Cream Cheese", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["New Item"]},
        "2026-08-17": {"main": "Breakfast Chicken Biscuit", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Apple", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["High Protein"]},
        "2026-08-18": {"main": "Breakfast Stacker", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Fruit & Yogurt Parfait", "Fresh Orange", "Canned or Frozen Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Popular"]},
        "2026-08-19": {"main": "Homemade Smoothie w/ Muffin", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Homemade"]},
        "2026-08-20": {"main": "Homemade Energy Bites", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Fruit & Yogurt Parfait", "Fresh Banana", "Dried Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Energy Boost"]},
        "2026-08-21": {"main": "Western Frittata", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Egg Special"]},
        "2026-08-24": {"main": "Dutch Waffle", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Apple", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["New Item"]},
        "2026-08-25": {"main": "Egg Bite w/ Baby Cakes", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Fruit & Yogurt Parfait", "Fresh Orange", "Canned or Frozen Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["New Item"]},
        "2026-08-26": {"main": "Egg & Cheese Croissant", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-08-27": {"main": "Homemade Breakfast Pizza", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Fruit & Yogurt Parfait", "Fresh Banana", "Dried Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-08-28": {"main": "Bagel Bites w/ Cream Cheese", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-08-31": {"main": "Breakfast Chicken Biscuit", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Apple", "100% Fruit Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["High Protein"]},
    }

    # ── SEPTEMBER 2026 LUNCH (from official portal PDF #888538) ────────────
    september_lunch = {
        "2026-09-01": {
            "main": "Homemade Mac n' Cheese w/ Roll",
            "image": "assets/images/mac_and_cheese.jpg",
            "sides": ["Steamed Peas", "HOM or Seasonal Vegetable", "Veggie Cup", "Fresh Fruit Cup", "Berries"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Comfort Food", "Vegetarian"]
        },
        "2026-09-02": {
            "main": "Beef Dumpling w/ Teriyaki Sauce & Brown Rice",
            "image": "assets/images/orange_chicken.jpg",
            "sides": ["Roasted Broccoli", "Carrot Coins", "Garden Side Salad", "Fresh Whole Fruit", "Fresh Grapes"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Asian Fusion", "Chef Special"]
        },
        "2026-09-03": {
            "main": "Walking Tacos w/ Toppings",
            "image": "assets/images/beef_tacos.jpg",
            "sides": ["Roasted Sweet Potatoes", "Black Bean & Corn Salad", "Veggie Cup", "Fresh Fruit Cup", "Dried Fruit"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Tex-Mex", "Popular"]
        },
        "2026-09-04": {
            "main": "Cheeseburger",
            "image": "assets/images/bacon_cheeseburger.jpg",
            "sides": ["Potato Wedges", "Homemade Baked Beans", "Garden Side Salad", "Fresh Whole Fruit", "Fresh Banana"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["All-American", "Student Favorite"]
        },
        "2026-09-07": {"no_school": True, "note": "HAPPY LABOR DAY! – NO SCHOOL"},
        "2026-09-08": {
            "main": "Turkey Hot Dog w/ Homemade Chili",
            "image": "assets/images/bacon_cheeseburger.jpg",
            "sides": ["Roasted Broccoli", "HOM or Seasonal Vegetable", "Veggie Cup", "Fresh Fruit Cup", "Fresh Melon"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Harvest of the Month"]
        },
        "2026-09-09": {
            "main": "Chicken Drumstick w/ Roll",
            "image": "assets/images/chicken_drumstick.jpg",
            "sides": ["Mashed Potatoes", "Homemade Broccoli Salad", "Veggie Cup", "Fresh Fruit Cup", "Fresh Grapes"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Homestyle", "High Protein"]
        },
        "2026-09-10": {
            "main": "Homemade Fajita Chicken Baked Pasta w/ Breadstick",
            "image": "assets/images/italian_pasta.jpg",
            "sides": ["Steamed Peas", "Garden Side Salad", "Baby Carrots", "Fresh Whole Fruit", "Fresh Berries"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Homemade", "Chef Special"]
        },
        "2026-09-11": {
            "main": "Crispy Fish Sticks w/ Roll",
            "image": "assets/images/fish_sandwich.jpg",
            "sides": ["Oven Roasted Fries", "Garden Side Salad", "Cherry Tomatoes", "Fresh Whole Fruit", "Dried Fruit"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Seafood Friday"]
        },
        "2026-09-14": {
            "main": "BBQ Pork w/ Hot Honey Poppers",
            "image": "assets/images/bacon_cheeseburger.jpg",
            "sides": ["Homemade Baked Beans", "Corn on the Cob", "Garden Side Salad", "Fresh Whole Fruit", "Dried Fruit"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Southern BBQ"]
        },
        "2026-09-15": {
            "main": "Breakfast for Lunch",
            "image": "assets/images/breakfast_pizza.jpg",
            "sides": ["Seasoned Diced Potatoes", "HOM or Seasonal Vegetable", "Veggie Cup", "Baked Cinnamon Apples", "Fresh Banana"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Fan Favorite", "Breakfast for Lunch"]
        },
        "2026-09-16": {
            "main": "Pizza Dippers w/ Marinara",
            "image": "assets/images/pizza_dippers.jpg",
            "sides": ["Steamed Broccoli", "Carrot Sticks", "Cucumber Tomato Salad", "Fresh Fruit Cup", "Fresh Berries"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Whole Grain", "Cheesy"]
        },
        "2026-09-17": {
            "main": "Homemade Beef & Cheese Tacos",
            "image": "assets/images/beef_tacos.jpg",
            "sides": ["Pinto Beans", "Garden Side Salad", "Mixed Bell Peppers", "Fresh Whole Fruit", "Fresh Melon"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Fiesta Thursday"]
        },
        "2026-09-18": {
            "main": "Crispy or Grilled Chicken Sandwich",
            "image": "assets/images/chicken_tenders.jpg",
            "sides": ["Sweet Potato Fries", "Garden Side Salad", "Veggie Cup", "Fresh Whole Fruit", "Fresh Grapes"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["High Protein", "Student Favorite"]
        },
        "2026-09-21": {"no_school": True, "note": "NO SCHOOL"},
        "2026-09-22": {
            "main": "Homemade Mac n' Cheese w/ Roll",
            "image": "assets/images/mac_and_cheese.jpg",
            "sides": ["Steamed Peas", "HOM or Seasonal Vegetable", "Veggie Cup", "Fresh Fruit Cup", "Berries"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Comfort Food", "Vegetarian"]
        },
        "2026-09-23": {
            "main": "Beef Dumpling w/ Teriyaki Sauce & Brown Rice",
            "image": "assets/images/orange_chicken.jpg",
            "sides": ["Roasted Broccoli", "Carrot Coins", "Garden Side Salad", "Fresh Whole Fruit", "Fresh Grapes"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Asian Fusion"]
        },
        "2026-09-24": {
            "main": "Walking Tacos w/ Toppings",
            "image": "assets/images/beef_tacos.jpg",
            "sides": ["Roasted Sweet Potatoes", "Black Bean & Corn Salad", "Veggie Cup", "Fresh Fruit Cup", "Dried Fruit"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Tex-Mex", "Popular"]
        },
        "2026-09-25": {
            "main": "Cheeseburger",
            "image": "assets/images/bacon_cheeseburger.jpg",
            "sides": ["Potato Wedges", "Homemade Baked Beans", "Garden Side Salad", "Fresh Whole Fruit", "Fresh Banana"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["All-American", "Student Favorite"]
        },
        "2026-09-28": {
            "main": "Orange Chicken w/ Homemade Fried Rice",
            "image": "assets/images/orange_chicken.jpg",
            "sides": ["Mixed Vegetables", "Garden Side Salad", "Fresh Cucumber", "Fresh Whole Fruit", "Fresh Banana"],
            "alts": ["PBJ Uncrustable", "Bento Box"],
            "tags": ["Popular", "Chef Special"]
        },
        "2026-09-29": {
            "main": "Turkey Hot Dog w/ Homemade Chili",
            "image": "assets/images/bacon_cheeseburger.jpg",
            "sides": ["Roasted Broccoli", "HOM or Seasonal Vegetable", "Veggie Cup", "Fresh Fruit Cup", "Fresh Melon"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Harvest of the Month"]
        },
        "2026-09-30": {
            "main": "Chicken Drumstick w/ Roll",
            "image": "assets/images/chicken_drumstick.jpg",
            "sides": ["Mashed Potatoes", "Homemade Broccoli Salad", "Veggie Cup", "Fresh Fruit Cup", "Fresh Grapes"],
            "alts": ["PBJ Uncrustable", "Entrée Salad"],
            "tags": ["Homestyle", "High Protein"]
        },
    }

    # ── SEPTEMBER 2026 BREAKFAST (from official portal PDF #893592) ────────
    september_bfast = {
        "2026-09-01": {"main": "Breakfast Stacker", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Fresh Orange", "Canned or Frozen Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Popular"]},
        "2026-09-02": {"main": "Homemade Smoothie w/ Muffin", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Homemade"]},
        "2026-09-03": {"main": "Homemade Energy Bites", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Yogurt Parfait", "Fresh Banana", "Dried Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Energy Boost"]},
        "2026-09-04": {"main": "Western Frittata", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Egg Special"]},
        "2026-09-07": None,  # No school
        "2026-09-08": {"main": "Egg Bite w/ Baby Cakes", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Fresh Orange", "Canned or Frozen Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-09": {"main": "Egg & Cheese Croissant", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-10": {"main": "Homemade Breakfast Pizza", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Yogurt Parfait", "Fresh Banana", "Dried Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-11": {"main": "Bagel Bites", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-14": {"main": "Breakfast Chicken Biscuit", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Apple", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["High Protein"]},
        "2026-09-15": {"main": "Apple Bites & Berry Trio Parfait", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Fresh Orange", "Canned or Frozen Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Harvest of Month"]},
        "2026-09-16": {"main": "Homemade Smoothie w/ Muffin", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Homemade"]},
        "2026-09-17": {"main": "New! Homemade Apple Cinnamon Breakfast Bar", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Yogurt Parfait", "Fresh Banana", "Dried Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["New Item"]},
        "2026-09-18": {"main": "Western Frittata", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["Egg Special"]},
        "2026-09-21": None,  # No school
        "2026-09-22": {"main": "Egg Bite w/ Baby Cakes & Berry Trio Parfait", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Fresh Orange", "Canned or Frozen Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-23": {"main": "Egg & Cheese Croissant", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-24": {"main": "Homemade Breakfast Pizza", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Seasonal Yogurt Parfait", "Fresh Banana", "Dried Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-25": {"main": "Bagel Bites w/ Cream Cheese", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-28": {"main": "Breakfast Chicken Biscuit", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Apple", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": ["High Protein"]},
        "2026-09-29": {"main": "Breakfast Stacker & Berry Trio Parfait", "image": "assets/images/breakfast_pizza.jpg", "sides": ["Fresh Orange", "Canned or Frozen Fruit", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
        "2026-09-30": {"main": "Homemade Smoothie w/ Muffin", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal Bowl", "Grahams w/ Yogurt"], "tags": []},
    }

    # Combine all months
    all_lunch = {**august_lunch, **september_lunch}
    all_bfast = {**august_bfast, **september_bfast}

    calendar_days = {}

    for year in [2026]:
        for month in [8, 9]:
            days_in_month = 31 if month == 8 else 30
            month_str = f"{year}-{month:02d}"

            for day in range(1, days_in_month + 1):
                date_key = f"{month_str}-{day:02d}"
                dt = date(year, month, day)
                weekday = dt.weekday()  # 0=Mon, 4=Fri

                if weekday >= 5:
                    continue  # Skip weekends

                lunch = all_lunch.get(date_key)
                bfast = all_bfast.get(date_key)

                # Before first day of school
                if year == 2026 and month == 8 and day < 12:
                    calendar_days[date_key] = {"is_school_day": False, "note": "Summer Recess (1st Day: Aug 12)"}
                    continue

                if lunch and lunch.get("no_school"):
                    calendar_days[date_key] = {"is_school_day": False, "note": lunch["note"]}
                    continue

                calendar_days[date_key] = {
                    "is_school_day": True,
                    "date": date_key,
                    "day_name": dt.strftime("%A"),
                    "kcms_lunch": lunch or {"main": "Chef Choice Special Entrée", "image": "assets/images/pepperoni_pizza.jpg", "sides": ["Garden Salad", "Fresh Fruit", "Choice of Milk"], "alts": ["PBJ Uncrustable", "Bento Box"], "tags": ["Daily Special"]},
                    "kcms_breakfast": bfast or {"main": "Warm Pastry or Cereal", "image": "assets/images/croissant_bfast.jpg", "sides": ["Fresh Fruit", "100% Juice", "Choice of Milk"], "daily_alts": ["Breakfast Bar", "Cereal", "Grahams"], "tags": []}
                }

    pdf_downloads = [
        {"title": "Official KCMS September 2026 Lunch Menu", "url": OFFICIAL_KCMS_SEP_LUNCH_PDF},
        {"title": "Official KCMS September 2026 Breakfast Menu", "url": OFFICIAL_KCMS_SEP_BFAST_PDF},
        {"title": "Official KCMS August 2026 Lunch Menu (V3)", "url": OFFICIAL_KCMS_AUG_LUNCH_PDF},
        {"title": "Official KCMS August 2026 Breakfast Menu (V2)", "url": OFFICIAL_KCMS_AUG_BFAST_PDF},
    ]

    dataset = {
        "metadata": {
            "source": "Kate Collins Middle School (KCMS) - Official Nutrition Services",
            "last_updated": "2026-09-01",
            "harvest_of_month": {
                "august": {"item": "Fresh Local Tomatoes", "emoji": "🍅"},
                "september": {"item": "Fresh Local Apples", "emoji": "🍎"}
            },
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
        "pdf_downloads": pdf_downloads,
        "schools": schools,
        "calendar": calendar_days
    }

    os.makedirs("data", exist_ok=True)
    with open("data/menus.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ data/menus.json updated with August + September 2026 data!")
    print(f"   August school days: {sum(1 for k,v in calendar_days.items() if k.startswith('2026-08') and v.get('is_school_day'))}")
    print(f"   September school days: {sum(1 for k,v in calendar_days.items() if k.startswith('2026-09') and v.get('is_school_day'))}")

if __name__ == "__main__":
    build_menu_database()
