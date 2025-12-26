import requests


def fetch_ingredients(barcode):
    """Fetches ingredients from Open Food Facts API."""
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            # Returns the raw ingredients text from the database
            return data["product"].get("ingredients_text", "Ingredients not listed.")
    return None