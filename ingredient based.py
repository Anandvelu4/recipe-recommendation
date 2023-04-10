import requests


# Define a function to recommend recipes based on input ingredients using Spoonacular API
def recommend_ingredients(input_ingredients):
    # Call the Spoonacular API to get recipe recommendations
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": "7944ff7180bf4e14b50e378e3a1d911b",
        "ingredients": input_ingredients,
        "number": 10,
        "ranking": 1,
        "ignorePantry": True
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    # Parse the JSON response and extract the recipe information
    results = []
    for result in response.json():
        recipe = {
            "id": result["id"],
            "title": result["title"],
            "image": result["image"],
            "missedIngredients": result["missedIngredients"],
            "usedIngredients": result["usedIngredients"]
        }
        results.append(recipe)

    return results
