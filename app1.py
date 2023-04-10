import streamlit as st
import requests
import pandas as pd

# Set the page title and favicon
st.set_page_config(page_title='Cooking Recipes', page_icon=':spaghetti:')
# Header
st.header("Christy Recipe BOT")

# Subheader
st.subheader("Love for Cooking ")
# Display Images

# import Image from pillow to open images
from PIL import Image
img = Image.open("C:\\Users\\Anand\\Pictures\\CM.jpeg")

# display image using streamlit
# width is used to set the width of an image
st.image(img, width=300)





# Read the preprocessed dataset
df = pd.read_csv('preprocessed_recipes_dataset.csv')

# Define a function to recommend recipes based on user input
def recommend_recipe(input_recipe, cuisine=None, course=None, diet=None):
    # Filter the dataset based on user input
    filtered_df = df[df['RecipeName'].str.contains(input_recipe, case=False)]
    if cuisine and cuisine != 'All':
        filtered_df = filtered_df[filtered_df['Cuisine'] == cuisine]
    if course and course != 'All':
        filtered_df = filtered_df[filtered_df['Course'] == course]
    if diet and diet != 'All':
        filtered_df = filtered_df[filtered_df['Diet'] == diet]
    # Return the recommended recipes
    return filtered_df.reset_index(drop=True)

# Define the Streamlit app
def app():
    # Set the app title and header
    st.title('Cooking Recipes')
    st.header('Find your perfect recipe')

    # Define the user input components
    input_recipe = st.text_input('Enter a recipe name:')

    # Automatically select the other attributes based on the preprocessed dataset
    if input_recipe:
        recipe = df[df['RecipeName'].str.contains(input_recipe, case=False)].iloc[0]
        cuisine = recipe['Cuisine']
        course = recipe['Course']
        diet = recipe['Diet']
    else:
        cuisine = 'All'
        course = 'All'
        diet = 'All'

    cuisine_options = ['All'] + df['Cuisine'].unique().tolist()
    course_options = ['All'] + df['Course'].unique().tolist()
    diet_options = ['All'] + df['Diet'].unique().tolist()

    cuisine = st.selectbox('Select a cuisine:', cuisine_options, index=cuisine_options.index(cuisine))
    course = st.selectbox('Select a course:', course_options, index=course_options.index(course))
    diet = st.selectbox('Select a diet:', diet_options, index=diet_options.index(diet))

    # Generate the recommendations based on user input
    if st.button('Get Recommendations'):
        if not input_recipe:
            st.warning('Please enter a recipe name.')
        else:
            filtered_df = recommend_recipe(input_recipe, cuisine, course, diet)

            if filtered_df.empty:
                st.warning('No recipes found. Please try again.')
            else:
                st.success(f"{len(filtered_df)} recipes found!")
                for index, row in filtered_df.iterrows():
                    st.write(f"{index + 1}. Recipe Name: {row['RecipeName']}")
                    st.write(f"   Ingredients: {row['Ingredients']}")
                    st.write(f"   Prep Time: {row['PrepTimeInMins']} mins")
                    st.write(f"   Cook Time: {row['CookTimeInMins']} mins")
                    st.write(f"   Total Time: {row['TotalTimeInMins']} mins")
                    st.write(f"   Servings: {row['Servings']}")
                    st.write(f"   Cuisine: {row['Cuisine']}")
                    st.write(f"   Course: {row['Course']}")
                    st.write(f"   Diet: {row['Diet']}")
                    st.write(f"   Instructions: {row['Instructions']}")

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

# Create a Streamlit app
st.title("Recipe Recommender")
input_ingredients = st.text_input("Enter ingredients (comma-separated):")
if input_ingredients:
    ingredients_list = [i.strip() for i in input_ingredients.split(",")]
    results = recommend_ingredients(ingredients_list)
    if results:
        st.subheader("Results")
        for result in results:
            st.write(f"{result['title']} ({len(result['usedIngredients'])} out of {len(result['usedIngredients'])+len(result['missedIngredients'])} ingredients)")
            st.image(result['image'], use_column_width=True)
            st.write("Missing ingredients:", ", ".join([ing['name'] for ing in result['missedIngredients']]))
            st.write("---")
    else:
        st.write("Sorry, no results found.")

api_key = "7944ff7180bf4e14b50e378e3a1d911b"


# define a function to search for recipes based on nutrient values
def search_by_nutrients(nutrient_name, min_value, max_value):
    # create the URL for the API request
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&addRecipeInformation=true&fillIngredients=true&sort=popularity&min{nutrient_name}={min_value}&max{nutrient_name}={max_value}"

    # send the API request and get the response
    response = requests.get(url)

    # parse the response JSON data
    data = response.json()

    # return the results
    return data["results"]


# create a Streamlit app to search for recipes by nutrient values
st.title("Recipe Search by Nutrients")
nutrient_name = st.text_input("Enter the nutrient name (e.g. calories):")
min_value = st.number_input("Enter the minimum value:")
max_value = st.number_input("Enter the maximum value:")
if st.button("Search"):
    results = search_by_nutrients(nutrient_name, min_value, max_value)
    for result in results:
        st.write(result["title"])
        st.write(result["sourceUrl"])
        st.write("------")

if __name__ == '__main__':
    app()