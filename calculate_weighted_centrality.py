import pandas as pd
import networkx as nx

def calculate_centrality():
    # 1. Load network_edges_final.csv
    df = pd.read_csv('network_edges_final.csv')
    
    # 2. Create an empty list to store results
    results = []
    
    # 3. Loop through the years: 2023, 2024, 2025
    years = [2023, 2024, 2025]
    
    for year in years:
        # Filter data for the specific year
        year_df = df[df['Year'] == year]
        
        # 4. Initialize an undirected graph using networkx.Graph()
        G = nx.Graph()
        
        # 5. Loop through the edges for that year
        for _, row in year_df.iterrows():
            weight = row['Weight_Avg_Sim']
            # Avoid division by zero if weight is 0
            distance = 1.0 / weight if weight > 0 else float('inf')
            G.add_edge(row['Item_A'], row['Item_B'], weight=weight, distance=distance)
            
        # 6. Calculate Weighted Degree (Strength)
        weighted_degree = dict(G.degree(weight='weight'))
        
        # 7. Calculate Weighted Closeness (using distance)
        weighted_closeness = nx.closeness_centrality(G, distance='distance')
        
        # 8. Calculate Weighted Betweenness (using distance)
        weighted_betweenness = nx.betweenness_centrality(G, weight='distance')
        
        # 9. Append results for every node in the graph
        for node in G.nodes():
            results.append({
                'Year': year,
                'Item': node,
                'Weighted_Degree': weighted_degree.get(node, 0),
                'Weighted_Closeness': weighted_closeness.get(node, 0),
                'Weighted_Betweenness': weighted_betweenness.get(node, 0)
            })
            
    # 10. Convert to a dataframe, sort by Year and then Weighted_Degree descending
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by=['Year', 'Weighted_Degree'], ascending=[True, False])
    
    # 11. Save as weighted_centrality_metrics.csv
    results_df.to_csv('weighted_centrality_metrics.csv', index=False)
    print("Successfully saved metrics to weighted_centrality_metrics.csv")

if __name__ == "__main__":
    calculate_centrality()
