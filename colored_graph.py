import pandas as pd
from pyvis.network import Network

# 1. Load the data and filter for 2025
edges_df = pd.read_csv('network_edges_final.csv')
edges_2025 = edges_df[edges_df['Year'] == 2025]

# 2. Your exact category mapping
category_map = {
    'Wheat Flour Bag': 'Food & Beverages', 'Rice Basmati Broken (Average Quality)': 'Food & Beverages',
    'Beef with Bone (Average Quality)': 'Food & Beverages', 'Mutton (Average Quality)': 'Food & Beverages',
    'Milk fresh (Un-boiled)': 'Food & Beverages', 'Curd (Dahi) Loose': 'Food & Beverages',
    'Cooking Oil DALDA or Other Similar Brand (SN), 5 Litre Tin': 'Food & Beverages',
    'Vegetable Ghee DALDA/HABIB 2.5 kg Tin': 'Food & Beverages',
    'Vegetable Ghee DALDA/HABIB or Other superior Quality 1 kg Pouch': 'Food & Beverages',
    'Pulse Masoor (Washed)': 'Food & Beverages', 'Pulse Moong (Washed)': 'Food & Beverages',
    'Cooked Beef at Average Hotel': 'Food & Beverages', 'Cooked Daal at Average Hotel': 'Food & Beverages',
    'Chilies Powder NATIONAL 200 gm Packet': 'Food & Beverages',
    'Long Cloth 57" Gul Ahmed/Al Karam': 'Apparel & Footwear', 'Shirting (Average Quality)': 'Apparel & Footwear',
    'Georgette (Average Quality)': 'Apparel & Footwear', 'Gents Sandal Bata': 'Apparel & Footwear',
    'Gents Sponge Chappal Bata': 'Apparel & Footwear', 'Ladies Sandal Bata': 'Apparel & Footwear',
    'Petrol Super': 'Transport & Communication', 'Hi-Speed Diesel': 'Transport & Communication',
    'Toilet Soap LIFEBUOY 115 gm': 'Personal Care', 'Sufi Washing Soap 250 gm Cake': 'Personal Care'
}

# 3. Assign a specific color to each category
color_palette = {
    'Food & Beverages': '#2ca02c',       # Green
    'Apparel & Footwear': '#1f77b4',     # Blue
    'Transport & Communication': '#d62728', # Red
    'Personal Care': '#9467bd'           # Purple (just in case)
}

# 4. Initialize PyVis Network
net = Network(height='700px', width='100%', bgcolor='#222222', font_color='white')

# 5. Extract unique nodes for 2025 and add them with colors
nodes_2025 = set(edges_2025['Item_A']).union(set(edges_2025['Item_B']))

for node in nodes_2025:
    # Find the category, default to 'Food & Beverages' if slight name mismatch
    category = category_map.get(node, 'Food & Beverages') 
    node_color = color_palette.get(category, '#ffffff')
    
    net.add_node(node, label=node, color=node_color, title=category)

# 6. Add the edges
for _, row in edges_2025.iterrows():
    net.add_edge(row['Item_A'], row['Item_B'])

# 7. Apply physics and save
net.set_options("""
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -3000,
      "centralGravity": 0.3,
      "springLength": 150
    }
  }
}
""")

net.show('Category_Network_2025.html', notebook=False)
print("Saved Category_Network_2025.html!")
