import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import itertools

# 1. Load price_vectors.csv and filter years
df = pd.read_csv('price_vectors.csv')
years = [2023, 2024, 2025]
df = df[df['Year'].isin(years)]

# 11-month vector columns
vector_cols = [f'Month_{i}' for i in range(2, 13)]

# Thresholds
tau = 0.85
K = 5

edges = []

# Loop through each unique Year
for year in years:
    year_df = df[df['Year'] == year]
    
    # Get unique items and cities
    items = sorted(year_df['Item'].unique())
    cities = sorted(year_df['City'].unique())
    
    # Pre-calculate similarity matrices for each city
    # city_sims[city] = matrix of shape (num_items, num_items)
    city_sims = {}
    
    for city in cities:
        city_data = year_df[year_df['City'] == city].set_index('Item')
        # Reindex to ensure item order is consistent
        city_vectors = city_data.reindex(items)[vector_cols].fillna(0.0).values
        
        # Calculate cosine similarity matrix
        # Handling zero vectors: sklearn returns 0 for pairs involving zero vectors
        sim_matrix = cosine_similarity(city_vectors)
        # Explicitly handle NaNs if any (though sklearn usually avoids them)
        sim_matrix = np.nan_to_num(sim_matrix, nan=0.0)
        
        city_sims[city] = sim_matrix

    # Generate every unique pair of items (indices)
    num_items = len(items)
    for i, j in itertools.combinations(range(num_items), 2):
        item_a = items[i]
        item_b = items[j]
        
        # Track similarities across cities
        pair_sims = []
        count_above_tau = 0
        
        for city in cities:
            sim = city_sims[city][i, j]
            pair_sims.append(sim)
            if sim >= tau:
                count_above_tau += 1
        
        # If Item A / Item B pair has N_y >= 5, they form a valid edge
        if count_above_tau >= K:
            avg_sim = np.mean(pair_sims)
            edges.append({
                'Year': year,
                'Item_A': item_a,
                'Item_B': item_b,
                'Weight_Count': count_above_tau,
                'Weight_Avg_Sim': avg_sim
            })

    print(f"Processed year {year}: Found {len([e for e in edges if e['Year'] == year])} edges.")

# Convert the edge list to a dataframe and save
edges_df = pd.DataFrame(edges)
edges_df.to_csv('network_edges_final.csv', index=False)

print(f"\nSuccessfully saved {len(edges_df)} edges to network_edges_final.csv")
