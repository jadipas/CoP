# app.py

from flask import Flask, render_template, redirect, url_for, request
from datasets import load_dataset
import pandas as pd
import random
import os
import json
from pathlib import Path
from functools import lru_cache
from util.handlers import Product

app = Flask(__name__)

# Configuration
DATA_DIR = Path("cached_data")
SAMPLE_SIZE = 1000  # Number of records to use in testing mode
IS_TESTING = os.getenv("FLASK_ENV") == "testing"

# List of available categories
CATEGORIES = [
    "Movies_and_TV",
]

# CATEGORIES = [
#     "All_Beauty",
#     "Toys_and_Games",
#     "Cell_Phones_and_Accessories",
#     "Industrial_and_Scientific",
#     "Gift_Cards",
#     "Musical_Instruments",
#     "Electronics",
#     "Arts_Crafts_and_Sewing",
#     "Office_Products",
#     "Digital_Music",
#     "Grocery_and_Gourmet_Food",
#     "Sports_and_Outdoors",
#     "Home_and_Kitchen",
#     "Tools_and_Home_Improvement",
#     "Pet_Supplies",
#     "Video_Games",
#     "Kindle_Store",
#     "Clothing_Shoes_and_Jewelry",
#     "Patio_Lawn_and_Garden",
#     "Books",
#     "Automotive",
#     "CDs_and_Vinyl",
#     "Magazine_Subscriptions",
#     "Software",
#     "Movies_and_TV",
# ]

def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(exist_ok=True)


def get_cache_path(category):
    """Get path for cached category data."""
    return DATA_DIR / f"{category}.parquet"


def save_to_cache(df, category):
    """Save DataFrame to parquet file."""
    ensure_data_dir()
    cache_path = get_cache_path(category)
    df.to_parquet(cache_path)


def load_from_cache(category):
    """Load DataFrame from parquet file if it exists."""
    cache_path = get_cache_path(category)
    if cache_path.exists():
        return pd.read_parquet(cache_path)
    return None


@lru_cache(maxsize=3)
def load_amazon_data(category="All_Beauty", split="full"):
    """Load Amazon Reviews dataset for a specific category with caching."""
    try:
        # First try to load from local cache
        df = load_from_cache(category)

        if df is None:
            # If not in cache, load from HuggingFace and cache it
            meta_dataset = load_dataset(
                "McAuley-Lab/Amazon-Reviews-2023",
                f"raw_meta_{category}",
                split=split,
                trust_remote_code=True,
            )
            df = pd.DataFrame(meta_dataset)

            # Cache the full dataset
            save_to_cache(df, category)

        # If in testing mode, return a sample
        if IS_TESTING:
            return df.sample(min(SAMPLE_SIZE, len(df)))

        return df

    except Exception as e:
        print(f"Error loading category {category}: {str(e)}")
        return None


# Store the current category in memory
current_category = None


@app.route("/")
def home():
    global current_category

    # Get category from query parameter or use random
    category = request.args.get("category")
    if category and category in CATEGORIES:
        current_category = category
    elif not current_category:
        current_category = random.choice(CATEGORIES)

    # Load data for the selected category
    products_df = load_amazon_data(current_category)

    # If loading fails, try with All_Beauty as fallback
    if products_df is None:
        current_category = "All_Beauty"
        products_df = load_amazon_data(current_category)

    # If even fallback fails, show error
    if products_df is None:
        return "Error loading dataset. Please try again later.", 500

    products = products_df.to_dict("records")
    random_products = random.sample(products, min(20, len(products)))
    random_products = [Product(p) for p in random_products]
    
    return render_template(
        "home.html",
        products=random_products,
        current_category=current_category,
        categories=CATEGORIES,
    )


@app.route("/product/<parent_asin>")
def product(parent_asin):
    global current_category

    # Load current category data
    products_df = load_amazon_data(current_category)

    if products_df is None:
        return redirect(url_for("home"))

    products = products_df.to_dict("records")

    # Find the product with matching ASIN
    product = next((p for p in products if p["parent_asin"] == parent_asin), None)
    if not product:
        return redirect(url_for("home"))

    # Get random recommendations from the same category
    recommendations = random.sample(
        [p for p in products if p["parent_asin"] != parent_asin],
        min(10, len(products) - 1),
    )

    return render_template(
        "product.html",
        product=product,
        recommendations=recommendations,
        current_category=current_category,
        categories=CATEGORIES,
    )


@app.route("/change_category/<category>")
def change_category(category):
    if category in CATEGORIES:
        return redirect(url_for("home", category=category))
    return redirect(url_for("home"))


if __name__ == "__main__":
    ensure_data_dir()
    app.run(debug=True)
