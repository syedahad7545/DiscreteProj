import pandas as pd
import os
import re
import numpy as np

# Mapping dictionary for the 51 items to 7 categories
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

# The 17 cities requested
cities_to_keep = [
    'Islam-abad', 'Rawal-pindi', 'Gujran-wala', 'Sialkot', 'Lahore', 
    'Faisal-abad', 'Sar-godha', 'Multan', 'Baha-walpur', 'Karachi', 
    'Hyder-abad', 'Sukkur', 'Larkana', 'Pesha-war', 'Bannu', 
    'Quetta', 'Khuz-dar'
]

month_map = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

def clean_price(val):
    """
    Cleans the price value by removing spaces and commas.
    Only returns a value if it is purely numeric.
    """
    if pd.isna(val):
        return np.nan
    
    # Convert to string and remove spaces/commas
    s = str(val).replace(' ', '').replace(',', '')
    
    # Try to convert to float
    try:
        f = float(s)
        return f
    except ValueError:
        # If conversion fails, it likely contains text (e.g. 'ket60.00' or 'te 1.79')
        # We discard these to ensure data integrity
        return np.nan

folder_path = './Data/xlsx_files/'
all_dfs = []

for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(folder_path, filename)
        
        # Rule 4: Extract Month and Year
        match = re.match(r'([a-zA-Z]+)_(\d{4})\.xlsx', filename)
        if match:
            month_name = match.group(1)
            year = match.group(2)
            month = month_map.get(month_name, month_name)
        else:
            continue
            
        try:
            # Read first 10 rows to find "Description"
            header_search = pd.read_excel(file_path, header=None, nrows=10)
            desc_row = header_search.apply(lambda x: x.astype(str).str.contains('Description', case=False)).any(axis=1).idxmax()
            
            # Read with identified header row
            df = pd.read_excel(file_path, header=desc_row)
            df.columns = [str(c).replace('\n', '').strip() for c in df.columns]
            
            # Special handling for June_2025.xlsx which has MIN/AVG/MAX
            if 'MIN' in df.columns and 'AVG' in df.columns:
                header_above = pd.read_excel(file_path, header=None, nrows=desc_row + 1).iloc[desc_row - 1]
                new_cols = []
                for col in df.columns:
                    if col == 'AVG':
                        idx = df.columns.get_loc(col)
                        city_candidate = header_above.iloc[idx - 1] if not pd.isna(header_above.iloc[idx - 1]) else header_above.iloc[idx]
                        new_cols.append(str(city_candidate))
                    else:
                        new_cols.append(col)
                df.columns = new_cols

            # Rename Description to Item
            desc_col = [c for c in df.columns if 'Description' in c or 'DESCRIPTION' in c][0]
            df = df.rename(columns={desc_col: 'Item'})
            
            # Filter cities
            final_cols = ['Item']
            city_rename_map = {}
            for col in df.columns:
                col_norm = col.replace('-', '').replace(' ', '').lower()
                for target_city in cities_to_keep:
                    target_norm = target_city.replace('-', '').replace(' ', '').lower()
                    if target_norm in col_norm:
                        final_cols.append(col)
                        city_rename_map[col] = target_city
                        break
            
            df = df[final_cols].rename(columns=city_rename_map)
            
            # Melt
            df_melted = df.melt(id_vars=['Item'], var_name='City', value_name='Price')
            
            # Clean Price values
            df_melted['Price'] = df_melted['Price'].apply(clean_price)
            
            # Add Month, Year
            df_melted['Month'] = month
            df_melted['Year'] = year
            
            # Map Category
            df_melted['Item'] = df_melted['Item'].astype(str).str.strip()
            df_melted['Category'] = df_melted['Item'].map(category_map)
            
            if df_melted['Category'].isnull().any():
                for item_name, cat in category_map.items():
                    df_melted.loc[df_melted['Category'].isnull() & df_melted['Item'].str.startswith(item_name[:20]), 'Category'] = cat

            # Rule 6: Drop NaN prices or missing categories
            df_melted = df_melted.dropna(subset=['Price', 'Category'])
            
            # Rule 7: Remove hyphens from City
            df_melted['City'] = df_melted['City'].str.replace('-', '')
            
            all_dfs.append(df_melted)
            print(f"Processed {filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Save
if all_dfs:
    master_df = pd.concat(all_dfs, ignore_index=True)
    master_df.to_csv('master_cpi_data.csv', index=False)
    print(f"Successfully saved {len(master_df)} rows to master_cpi_data.csv")
else:
    print("No data processed.")
