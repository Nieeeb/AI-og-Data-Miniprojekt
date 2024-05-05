import pandas as pd
import matplotlib.pyplot as plt

# Indlæser data i dataframe.
raw_data = pd.read_csv(r"Data\recipeData.csv", sep=',', index_col='BeerID', encoding='latin-1')
print(raw_data)

# Fjerner alle rækker med manglende værdier
print(f"Before dropping: {len(raw_data)}")
dropped = raw_data.dropna()
print(f"After dropping: {len(dropped)}")

# Indlæser pokemon data i et dataframe
raw_pokemon = pd.read_csv(r"Data\pokemon.csv", sep=',', index_col='#')
print(raw_pokemon)

# Fjerner rækker med manglende værdier
cleaned_pokemon = raw_pokemon.dropna()
print(cleaned_pokemon)

# Opretter plt objekt
fig = plt.figure()
# Plotter histogram over HP feature
axis = cleaned_pokemon["HP"].plot.hist()
plt.show()
