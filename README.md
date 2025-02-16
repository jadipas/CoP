# Costumer over Product (CoP)

This is a Flask web application that demonstrates a product recommendation system using the Amazon Reviews 2023 dataset. The application allows users to browse products from different categories and view product recommendations.

## Features

-   Browse products from 28 different Amazon categories
-   Random category selection on startup
-   Category switching via dropdown menu
-   Detailed product pages with images and descriptions
-   Product recommendations (currently using random sampling, ready for ML model integration)
-   Responsive design that works on both desktop and mobile devices

## Installation

1. Clone this repository:

```bash
git clone <your-repository-url>
cd <repository-folder>
```

2. (Optional) Create and activate a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Project Structure

```
CoP/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── templates/         # HTML templates
    ├── base.html      # Base template with common elements
    ├── home.html      # Homepage template
    └── product.html   # Product detail page template
```

## Running the Application

1. Make sure your virtual environment is activated

2. Run the Flask application:

```bash
python app.py
```

For testing:

```bash
export FLASK_ENV=testing
python app.py
```

3. Open your web browser and navigate to:

```
http://localhost:5000
```

## Usage

-   The homepage will display a 4x5 grid of random products from a randomly selected category
-   Use the category dropdown in the header to switch between different product categories
-   Click on any product to view its details and recommendations
-   Click the house icon (🏠) in the header to return to the homepage

## Direct Category Access

You can directly access a specific category by using the category parameter in the URL:

```
http://localhost:5000/?category=Books
```

Available categories:

-   All_Beauty
-   Appliances
-   Arts_Crafts_and_Sewing
-   Automotive
-   Books
-   CDs_and_Vinyl
-   Cell_Phones_and_Accessories
-   Clothing_Shoes_and_Jewelry
-   Digital_Music
-   Electronics
-   Gift_Cards
-   Grocery_and_Gourmet_Food
-   Home_and_Kitchen
-   Industrial_and_Scientific
-   Kindle_Store
-   Luxury_Beauty
-   Magazine_Subscriptions
-   Movies_and_TV
-   Musical_Instruments
-   Office_Products
-   Patio_Lawn_and_Garden
-   Pet_Supplies
-   Prime_Pantry
-   Software
-   Sports_and_Outdoors
-   Tools_and_Home_Improvement
-   Toys_and_Games
-   Video_Games

## Integrating Your Recommendation Model

To integrate your own recommendation model, modify the `product()` route in `app.py`. Look for the following section:

```python
# Get random recommendations from the same category
recommendations = random.sample(
    [p for p in products if p['parent_asin'] != parent_asin],
    min(10, len(products)-1)
)
```

Replace this with your model's recommendation logic.

## Troubleshooting

1. If you encounter memory issues when loading large categories:

    - Reduce the `maxsize` parameter in the `@lru_cache` decorator
    - Consider implementing pagination for the product grid

2. If a category fails to load:
    - The application will automatically fall back to the "All_Beauty" category
    - Check your internet connection
    - Ensure you have enough disk space for dataset caching

## Dataset Information

This project uses the Amazon Reviews 2023 dataset from the McAuley Lab, hosted on Hugging Face. The dataset contains product metadata and reviews across multiple categories.

Dataset Link: [McAuley-Lab/Amazon-Reviews-2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023)

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT
