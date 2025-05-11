# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/Users/calebjorgensen/Documents/CSE310/Videogame-Sales/data/video_games_sales.csv')

# 1. Data Cleaning
# Check for missing values in the 'year' and 'publisher' columns
print("Missing values before cleaning:\n", df.isnull().sum())

# Fill missing values in 'year' with the most common year (mode)
most_common_year = df['year'].mode()[0]  # Get the most common year
df['year'].fillna(most_common_year, inplace=True)  # Fill missing 'year' values

# Fill missing values in 'publisher' with 'Unknown'
df['publisher'].fillna('Unknown', inplace=True)  # Fill missing 'publisher' values

# Check again for missing values after cleaning
print("\nMissing values after cleaning:\n", df.isnull().sum())

# 2. Best Games by Year
# Group by 'year' and find the game with the highest global sales in each year
top_games_by_year = df.loc[df.groupby('year')['global_sales'].idxmax()][['year', 'name', 'global_sales']]

# Sort the result by 'year' in descending order. 
top_games_by_year = top_games_by_year.sort_values('year', ascending=False)

# Print the top games by year
print("\nTop Games by Year:")
print(top_games_by_year.head())  # Displaying first few rows

# 3. Best Games by Decade
# Create a new column 'decade' by dividing 'year' by 10 and multiplying by 10
df['decade'] = (df['year'] // 10) * 10

# Group by 'decade' and find the game with the highest global sales in each decade
top_games_by_decade = df.loc[df.groupby('decade')['global_sales'].idxmax()][['decade', 'name', 'global_sales']]

# Sort the result by 'decade' for better readability
top_games_by_decade = top_games_by_decade.sort_values('decade')

# Print the top games by decade
print("\nTop Games by Decade:")
print(top_games_by_decade.head())  # Displaying first few rows

# 4. Visualization: Top 10 Games by Global Sales (in years)
# Group by 'year' and calculate total global sales per year
top_sales_by_year = df.groupby('year')['global_sales'].sum().sort_values(ascending=False).head(10)

# Plot the data
plt.figure(figsize=(10, 6))

# Create a color map for publishers based on top-selling games in 'top_sales_by_year'
bar_colors = []
for year in top_sales_by_year.index:
    # Get the publisher for the top-selling game in that year
    publisher = df[df['year'] == year].iloc[0]['publisher']
    
    # Create a color map for each publisher
    publisher_colors = {publisher: plt.cm.tab20(i / len(df['publisher'].unique())) for i, publisher in enumerate(df['publisher'].unique())}

    # Add the color corresponding to the publisher
    bar_colors.append(publisher_colors.get(publisher, 'gray'))  # Default to 'gray' if publisher not found in color map

# Plot the bar chart with the specific colors
ax = top_sales_by_year.plot(kind='bar', color=bar_colors)
plt.title('Top 10 Games by Global Sales (by Year)')
plt.xlabel('Year')
plt.ylabel('Total Global Sales (in millions)')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to avoid label cut-off

# Annotate the bars with game names, rotating the text vertically
for idx, value in enumerate(top_sales_by_year):
    # Get the name of the game for the corresponding year
    game_name = df[df['year'] == top_sales_by_year.index[idx]].iloc[0]['name']
    ax.text(idx, value + 1, game_name, ha='center', va='bottom', fontsize=10)

plt.show()