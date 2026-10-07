import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Load dataset
df = pd.read_csv('All_Diets.csv')

# Clean missing values
numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# 2. Average macronutrients
avg_macros = df.groupby('Diet_type')[numeric_cols].mean()
print("=== Average Macronutrients by Diet Type ===")
print(avg_macros)

# 3. Top 5 protein-rich recipes
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print("\n=== Top Protein-Rich Recipes ===")
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']])

# 4. Highest protein diet type
highest_protein = avg_macros['Protein(g)'].idxmax()
print(f"\nHighest Protein Diet Type: {highest_protein}")

# 5. Ratios
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / (df['Carbs(g)'] + 0.001)
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / (df['Fat(g)'] + 0.001)

# Visualizations output folder
os.makedirs('static', exist_ok=True)

# Plot 1: Bar Chart
plt.figure(figsize=(8, 5))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'], palette='viridis')
plt.title('Average Protein by Diet Type')
plt.ylabel('Average Protein (g)')
plt.savefig('static/bar_chart.png')
plt.close()

# Plot 2: Heatmap
plt.figure(figsize=(8, 5))
sns.heatmap(avg_macros, annot=True, cmap='YlGnBu', fmt=".1f")
plt.title('Macronutrient Heatmap by Diet Type')
plt.savefig('static/heatmap.png')
plt.close()

# Plot 3: Scatter Plot
plt.figure(figsize=(8, 5))
sns.scatterplot(data=top_protein, x='Cuisine_type', y='Protein(g)', hue='Diet_type', s=100)
plt.title('Top Protein Recipes Across Cuisines')
plt.xticks(rotation=45)
plt.savefig('static/scatter_plot.png')
plt.close()

print("\nTask 1 complete. Plots saved in 'static/' directory.")
