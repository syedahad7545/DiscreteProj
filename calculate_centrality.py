import pandas as pd
import networkx as nx

# 1. Load network_edges_final.csv
edges_df = pd.read_csv('network_edges_final.csv')

# 2. Create an empty list to store the centrality results
centrality_results = []

# 3. Loop through each unique Year
years = sorted(edges_df['Year'].unique())

for year in years:
    # 4. Initialize an undirected, unweighted graph
    G = nx.Graph()
    
    # 5. Add all edges for that specific year
    year_edges = edges_df[edges_df['Year'] == year]
    for _, row in year_edges.iterrows():
        G.add_edge(row['Item_A'], row['Item_B'])
    
    # 6. Calculate centrality metrics
    degree_cent = nx.degree_centrality(G)
    closeness_cent = nx.closeness_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    
    # 7. Loop through every node and store results
    for node in G.nodes():
        centrality_results.append({
            'Year': year,
            'Item': node,
            'Degree_Centrality': degree_cent[node],
            'Closeness_Centrality': closeness_cent[node],
            'Betweenness_Centrality': betweenness_cent[node]
        })

# 8. Convert the results list into a pandas dataframe
results_df = pd.DataFrame(centrality_results)

# 9. Sort the dataframe primarily by Year and secondarily by Degree_Centrality (descending)
results_df = results_df.sort_values(by=['Year', 'Degree_Centrality'], ascending=[True, False])

# 10. Save as centrality_metrics.csv
results_df.to_csv('centrality_metrics.csv', index=False)

print(f"Successfully calculated centrality metrics for {len(results_df)} nodes across years {years}.")
print(f"Results saved to centrality_metrics.csv")
