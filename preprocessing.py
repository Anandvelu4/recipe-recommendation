import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('C:\\Users\\Anand\\Desktop\\FINAL data set.csv',encoding='iso-8859-1')

# Drop duplicate rows
df = df.drop_duplicates()

# Replace missing values with NaN
df.replace('', np.nan, inplace=True)

# Drop rows with missing values
df = df.dropna()

# Convert ingredients column to list
df['Ingredients'] = df['Ingredients'].apply(lambda x: x.split(','))

# Convert cooking time and total time columns to integers
df['CookTimeInMins'] = df['CookTimeInMins'].astype(int)
df['TotalTimeInMins'] = df['TotalTimeInMins'].astype(int)

# Convert servings column to float
df['Servings'] = df['Servings'].astype(float)

# Convert cuisine, course, and diet columns to categorical variables
df['Cuisine'] = df['Cuisine'].astype('category')
df['Course'] = df['Course'].astype('category')
df['Diet'] = df['Diet'].astype('category')

# Reset the index
df.reset_index(drop=True, inplace=True)

# Save the preprocessed dataset
df.to_csv('preprocessed_recipes_dataset.csv', index=False)
