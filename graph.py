import pandas as pd
import networkx as nx
from pyvis.network import Network

print("Loading data...")
edges_df = pd.read_csv('network_edges_final.csv')
centrality_df = pd.read_csv('centrality_metrics.csv')

years = [2023, 2024, 2025]

for year in years:
    print(f"Generating interactive graph for {year}...")
    
    # Filter data for the specific year
    year_edges = edges_df[edges_df['Year'] == year]
    year_nodes = centrality_df[centrality_df['Year'] == year]
    
    # Initialize a NetworkX graph
    G = nx.Graph()
    
    # 1. Add Nodes (Size based on Degree Centrality)
    for _, row in year_nodes.iterrows():
        item = row['Item']
        degree = row['Degree_Centrality']
        
        # Scale the size so it looks good on screen (min size 15, scaling up by centrality)
        visual_size = 15 + (degree * 150) 
        
        G.add_node(
            item, 
            size=visual_size, 
            title=f"{item}<br>Degree: {degree:.4f}", # Hover text
            color="#4CAF50" if year == 2025 else "#2196F3" # Different colors per year!
        )
        
    # 2. Add Edges (Thickness based on Weight_Count)
    for _, row in year_edges.iterrows():
        G.add_edge(
            row['Item_A'], 
            row['Item_B'], 
            value=row['Weight_Count'], # PyVis uses 'value' to make lines thicker
            title=f"Correlated in {row['Weight_Count']} cities" # Hover text
        )
        
    # 3. Create the PyVis Network
    # Using a dark theme which looks amazing for presentations
    net = Network(height='800px', width='100%', bgcolor='#222222', font_color='white')
    
    # Read the NetworkX graph into PyVis
    net.from_nx(G)
    
    # Add the interactive physics control panel for your YouTube video!
    net.show_buttons(filter_=['physics'])
    
    # Save the HTML file
    filename = f'CPI_Network_{year}.html'
    net.save_graph(filename)
    print(f"Saved {filename}!")

print("All graphs generated successfully. Open the HTML files in your web browser!")
