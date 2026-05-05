import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import itertools

def perform_sensitivity_analysis():
    # 1. Load price_vectors.csv
    df = pd.read_csv('price_vectors.csv')
    
    # Define vector columns (Month_2 to Month_12)
    vector_cols = [c for c in df.columns if c.startswith('Month_')]
    
    # 2. Define test scenarios
    scenarios = [
        {'Name': 'Baseline', 'tau': 0.85, 'K': 5},
        {'Name': 'Strict', 'tau': 0.90, 'K': 8},
        {'Name': 'Loose', 'tau': 0.80, 'K': 3}
    ]
    
    # 3. List to store results
    summary_results = []
    
    years = [2023, 2024, 2025]
    
    # Cache city-item-vectors for each year to avoid repeated lookups
    year_cache = {}
    for year in years:
        year_df = df[df['Year'] == year]
        unique_items = sorted(year_df['Item'].unique())
        unique_cities = sorted(year_df['City'].unique())
        
        city_item_vectors = {}
        for city in unique_cities:
            city_data = year_df[year_df['City'] == city].set_index('Item')
            # Reindex ensures all items exist for each city, filled with 0s if missing
            vectors = city_data.reindex(unique_items)[vector_cols].fillna(0.0).values
            # Compute similarity matrix for this city
            sim_matrix = cosine_similarity(vectors)
            city_item_vectors[city] = np.nan_to_num(sim_matrix, nan=0.0)
            
        year_cache[year] = {
            'items': unique_items,
            'cities': unique_cities,
            'city_sims': city_item_vectors
        }

    # 4. Loop through each scenario
    for scenario in scenarios:
        tau = scenario['tau']
        K = scenario['K']
        name = scenario['Name']
        
        for year in years:
            data = year_cache[year]
            items = data['items']
            cities = data['cities']
            city_sims = data['city_sims']
            
            num_items = len(items)
            # Initialize a matrix to count how many cities pass the threshold
            pass_count_matrix = np.zeros((num_items, num_items))
            
            for city in cities:
                # Add 1 where similarity >= tau
                pass_count_matrix += (city_sims[city] >= tau).astype(int)
            
            # A valid edge is where pass_count >= K
            # Since it's an undirected graph, we only look at the upper triangle (excluding diagonal)
            upper_tri_indices = np.triu_indices(num_items, k=1)
            valid_edges_mask = pass_count_matrix[upper_tri_indices] >= K
            total_edges = np.sum(valid_edges_mask)
            
            # 5. Append results
            summary_results.append({
                'Scenario': name,
                'Year': year,
                'Tau': tau,
                'K': K,
                'Total_Edges': int(total_edges)
            })

    # 10. Convert to dataframe and print
    results_df = pd.DataFrame(summary_results)
    
    print("\n" + "="*70)
    print("THRESHOLD SENSITIVITY ANALYSIS RESULTS")
    print("="*70)
    print(results_df.to_string(index=False))
    print("="*70)
    
    # 11. Save as sensitivity_analysis.csv
    results_df.to_csv('sensitivity_analysis.csv', index=False)
    print("Successfully saved results to sensitivity_analysis.csv")

if __name__ == "__main__":
    perform_sensitivity_analysis()
