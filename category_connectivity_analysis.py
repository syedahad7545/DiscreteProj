import pandas as pd

# 1. Copy the exact category_map dictionary
category_map = {
    'Wheat Flour Bag': 'Food & Beverages',
    'Rice Basmati Broken (Average Quality)': 'Food & Beverages',
    'Rice Basmati Broken (Average Qualit': 'Food & Beverages',
    'Rice IRRI-6/9 (Sindh/Punjab)': 'Food & Beverages',
    'Bread plain (Small Size)': 'Food & Beverages',
    'Beef with Bone (Average Quality)': 'Food & Beverages',
    'Mutton (Average Quality)': 'Food & Beverages',
    'Chicken Farm Broiler (Live)': 'Food & Beverages',
    'Milk fresh (Un-boiled)': 'Food & Beverages',
    'Curd (Dahi) Loose': 'Food & Beverages',
    'Powdered Milk NIDO 390 gm Polybag': 'Food & Beverages',
    'Eggs Hen (Farm)': 'Food & Beverages',
    'Mustard Oil (Average Quality)': 'Food & Beverages',
    'Cooking Oil DALDA or Other Similar Brand': 'Food & Beverages',
    'Cooking Oil DALDA or Other Similar B': 'Food & Beverages',
    'Vegetable Ghee DALDA/HABIB 2.5 kg': 'Food & Beverages',
    'Vegetable Ghee DALDA/HABIB or Other': 'Food & Beverages',
    'Vegetable Ghee DALDA/HABIB or Oth': 'Food & Beverages',
    'Bananas (Kela) Local': 'Food & Beverages',
    'Pulse Masoor (Washed)': 'Food & Beverages',
    'Pulse Moong (Washed)': 'Food & Beverages',
    'Pulse Mash (Washed)': 'Food & Beverages',
    'Pulse Gram': 'Food & Beverages',
    'Potatoes': 'Food & Beverages',
    'Onions': 'Food & Beverages',
    'Tomatoes': 'Food & Beverages',
    'Sugar Refined': 'Food & Beverages',
    'Gur (Average Quality)': 'Food & Beverages',
    'Salt Powdered (NATIONAL/SHAN) 800 gm': 'Food & Beverages',
    'Salt Powdered (NATIONAL/SHAN) 80': 'Food & Beverages',
    'Chilies Powder NATIONAL 200 gm Packet': 'Food & Beverages',
    'Chilies Powder NATIONAL 200 gm Pa': 'Food & Beverages',
    'Garlic (Lehsun)': 'Food & Beverages',
    'Tea Lipton Yellow Label 190 gm Pack': 'Food & Beverages',
    'Cooked Beef at Average Hotel': 'Food & Beverages',
    'Cooked Daal at Average Hotel': 'Food & Beverages',
    'Tea Prepared Ordinary': 'Food & Beverages',
    'Cigarettes Capstan 20\'S Packet': 'Miscellaneous',
    'Long Cloth 57" Gul Ahmed/Al Karam': 'Apparel & Footwear',
    'Shirting (Average Quality)': 'Apparel & Footwear',
    'Lawn Printed Gul Ahmed/Al Karam': 'Apparel & Footwear',
    'Georgette (Average Quality)': 'Apparel & Footwear',
    'Gents Sandal Bata': 'Apparel & Footwear',
    'Gents Sponge Chappal Bata': 'Apparel & Footwear',
    'Ladies Sandal Bata': 'Apparel & Footwear',
    'Electricity Charges upto 50 Units': 'Housing Water & Energy',
    'Gas Charges upto 3.3719 MMBTU': 'Housing Water & Energy',
    'Gas Charges for Q1': 'Housing Water & Energy',
    'Firewood Whole': 'Housing Water & Energy',
    'LPG 11.67 kg Cylinder': 'Housing Water & Energy',
    'Petrol Super': 'Transport & Communication',
    'Hi-Speed Diesel': 'Transport & Communication',
    'Telephone Call Charges': 'Transport & Communication',
    'Sufi Washing Soap 250 gm Cake': 'Personal Care',
    'Toilet Soap LIFEBUOY 115 gm': 'Personal Care',
    'Energy Saver Philips 14 Watt': 'Household Equipment',
    'Match Box': 'Household Equipment'
}

def analyze_connectivity():
    # 2. Load network_edges_final.csv
    df = pd.read_csv('network_edges_final.csv')
    
    # Pre-clean item names to handle partial matches from the original mapping logic
    def map_category(item_name):
        item_name = str(item_name).strip()
        # Direct match
        if item_name in category_map:
            return category_map[item_name]
        # Partial match (like the logic in consolidate_data.py)
        for key, value in category_map.items():
            if item_name.startswith(key[:20]):
                return value
        return "Unknown"

    # 3. Create new columns Category_A and Category_B
    df['Category_A'] = df['Item_A'].apply(map_category)
    df['Category_B'] = df['Item_B'].apply(map_category)
    
    # 4. Create Connection_Type (alphabetized and hyphenated)
    def get_connection_type(row):
        cats = sorted([row['Category_A'], row['Category_B']])
        return f"{cats[0]} - {cats[1]}"
    
    df['Connection_Type'] = df.apply(get_connection_type, axis=1)
    
    # 5. Group by Year and Connection_Type
    report_df = df.groupby(['Year', 'Connection_Type']).size().reset_index(name='Edge_Count')
    
    # 6. Print formatted report
    print("="*60)
    print("CATEGORY CONNECTIVITY BREAKDOWN REPORT")
    print("="*60)
    
    for year in sorted(report_df['Year'].unique()):
        print(f"\nYEAR: {year}")
        print("-" * 30)
        year_data = report_df[report_df['Year'] == year].sort_values(by='Edge_Count', ascending=False)
        for _, row in year_data.iterrows():
            print(f"{row['Connection_Type']:<45} : {row['Edge_Count']}")
            
    # 7. Save to category_connectivity_report.csv
    report_df.to_csv('category_connectivity_report.csv', index=False)
    print("\n" + "="*60)
    print("Successfully saved report to category_connectivity_report.csv")

if __name__ == "__main__":
    analyze_connectivity()
