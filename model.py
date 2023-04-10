import pandas as pd

# Read the preprocessed dataset
df = pd.read_csv('preprocessed_recipes_dataset.csv')

def recommend_recipe(input_recipe, cuisine=None, course=None, diet=None, cooking_time=None, num_ingredients=None):
    '''
    Recommend recipes based on user input.

    Parameters:
    input_recipe (str): name or keywords of the recipe.
    cuisine (str): cuisine type of the recipe.
    course (str): course type of the recipe.
    diet (str): diet type of the recipe.
    cooking_time (int): maximum cooking time of the recipe.
    num_ingredients (int): minimum number of ingredients required for the recipe.

    Returns:
    pd.DataFrame: recommended recipes with details such as recipe name, cuisine, course, diet, cooking time, and number of ingredients.
    '''
    # Filter the dataset based on user input
    filtered_df = df[df['RecipeName'].str.contains(input_recipe, case=False)]
    if cuisine:
        filtered_df = filtered_df[filtered_df['Cuisine'] == cuisine]
    if course:
        filtered_df = filtered_df[filtered_df['Course'] == course]
    if diet:
        filtered_df = filtered_df[filtered_df['Diet'] == diet]
    if cooking_time:
        filtered_df = filtered_df[filtered_df['CookTimeInMins'] <= cooking_time]
    if num_ingredients:
        filtered_df = filtered_df[filtered_df['NumIngredients'] >= num_ingredients]

    # Return the recommended recipes
    return filtered_df[['RecipeName', 'Cuisine', 'Course', 'Diet', 'CookTimeInMins', 'NumIngredients']]

# Example usage
recommend_recipe('Masala Karela Recipe', cuisine='Indian', course='Side Dish', diet='Diabetic Friendly', cooking_time=60, num_ingredients=6)
