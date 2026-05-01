import pandas as pd
import numpy as np
import os

# Paths
folder_path = 'Data/xlsx_files/'
march_path = os.path.join(folder_path, 'March_2023.xlsx')
april_path = os.path.join(folder_path, 'April_2023.xlsx')

# Target city names for calculation (clean)
cities = [
    'Islamabad', 'Rawalpindi', 'Gujranwala', 'Sialkot', 'Lahore', 
    'Faisalabad', 'Sargodha', 'Multan', 'Bahawalpur', 'Karachi', 
    'Hyderabad', 'Sukkur', 'Larkana', 'Peshawar', 'Bannu', 
    'Quetta', 'Khuzdar'
]

# Mapping for final PBS headers with newlines
city_map_pbs = {
    'Islamabad': 'Islam-\nabad',
    'Rawalpindi': 'Rawal-\npindi',
    'Gujranwala': 'Gujran-\nwala',
    'Sialkot': 'Sialkot',
    'Lahore': 'Lahore',
    'Faisalabad': 'Faisal-\nabad',
    'Sargodha': 'Sar-\ngodha',
    'Multan': 'Multan',
    'Bahawalpur': 'Baha-\nwalpur',
    'Karachi': 'Karachi',
    'Hyderabad': 'Hyder-\nabad',
    'Sukkur': 'Sukkur',
    'Larkana': 'Larkana',
    'Peshawar': 'Pesha-\nwar',
    'Bannu': 'Bannu',
    'Quetta': 'Quetta',
    'Khuzdar': 'Khuz-\ndar'
}

def load_and_clean(path):
    df = pd.read_excel(path)
    # Clean column names for processing: remove \n, -, and spaces
    df.columns = [str(c).replace('\n', '').replace('-', '').replace(' ', '').strip() for c in df.columns]
    
    # Identify Description column
    desc_col = [c for c in df.columns if 'Description' in c or 'DESCRIPTION' in c][0]
    df = df.rename(columns={desc_col: 'Description'})
    
    # Filter for Description + 17 Cities
    cols_to_keep = ['Description']
    rename_map = {}
    for col in df.columns:
        for target in cities:
            if target.lower() == col.lower():
                cols_to_keep.append(col)
                rename_map[col] = target
                break
    
    df = df[cols_to_keep].rename(columns=rename_map)
    # Ensure numeric types
    for city in cities:
        df[city] = pd.to_numeric(df[city], errors='coerce')
    
    return df.sort_values('Description').reset_index(drop=True)

# 1. Load data
df_march = load_and_clean(march_path)
df_april = load_and_clean(april_path)

# Ensure they have the same items
common_items = sorted(list(set(df_march['Description']) & set(df_april['Description'])))
df_march = df_march[df_march['Description'].isin(common_items)].reset_index(drop=True)
df_april = df_april[df_april['Description'].isin(common_items)].reset_index(drop=True)

# 4. Calculate February 2023: Feb = March - (April - March) = 2*March - April
df_feb = df_march.copy()
for city in cities:
    df_feb[city] = (2 * df_march[city] - df_april[city]).clip(lower=1.0)

# 5. Calculate January 2023: Jan = Feb - (March - Feb) = 2*Feb - March
df_jan = df_feb.copy()
for city in cities:
    df_jan[city] = (2 * df_feb[city] - df_march[city]).clip(lower=1.0)

def format_to_pbs(df):
    # 6. Add dummy S.No. and Unit
    df.insert(0, 'S.No.', range(1, len(df) + 1))
    df.insert(2, 'Unit', '1 Kg')
    
    # Add dummy summary columns
    summary_cols = ['Average Prices', 'NaN_1', 'NaN_2', '%change', 'NaN_3']
    for sc in summary_cols:
        df[sc] = np.nan
        
    # Order columns exactly
    final_cols = ['S.No.', 'Description', 'Unit'] + cities + summary_cols
    df = df[final_cols]
    
    # 7. Add \n back into headers
    header_rename = {
        'S.No.': 'S.\nNo.',
        'Description': 'Description',
        'Unit': 'Unit',
        'Average Prices': 'Average Prices',
        'NaN_1': 'NaN',
        'NaN_2': 'NaN',
        '%change': '%change',
        'NaN_3': 'NaN'
    }
    header_rename.update(city_map_pbs)
    return df.rename(columns=header_rename)

# Format
jan_final = format_to_pbs(df_jan)
feb_final = format_to_pbs(df_feb)

# 8. Export
jan_final.to_excel(os.path.join(folder_path, 'January_2023.xlsx'), index=False)
feb_final.to_excel(os.path.join(folder_path, 'February_2023.xlsx'), index=False)

print("Synthesized January_2023.xlsx and February_2023.xlsx using Backward Linear Extrapolation.")
