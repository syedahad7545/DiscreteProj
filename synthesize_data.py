import pandas as pd
import glob
import os

# Paths
folder_path = 'Data/xlsx_files/'
files_2023 = glob.glob(os.path.join(folder_path, '*2023.xlsx'))

# Target cities and their PBS names with newlines
city_map_rev = {
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

cities = list(city_map_rev.keys())
all_dfs = []

print(f"Found {len(files_2023)} files for 2023.")

for f in files_2023:
    # Rule 2: No skiprows
    df = pd.read_excel(f)
    
    # Rule 3: Standardize column names
    df.columns = [str(c).replace('\n', '').replace(' ', '').replace('-', '') for c in df.columns]
    
    # Map the messy PBS names to clean names for internal processing
    rename_map = {}
    for col in df.columns:
        for target in cities:
            if target.lower() in col.lower():
                rename_map[col] = target
                break
        if 'description' in col.lower():
            rename_map[col] = 'Description'
            
    df = df.rename(columns=rename_map)
    
    # Rule 4: Keep ONLY 'Description' and the 17 cities
    available_cols = [c for c in ['Description'] + cities if c in df.columns]
    all_dfs.append(df[available_cols])

# Rule 5: Concatenate, group by 'Description', and calculate mean
combined = pd.concat(all_dfs, ignore_index=True)
# Ensure numeric columns only for mean
for city in cities:
    if city in combined.columns:
        combined[city] = pd.to_numeric(combined[city], errors='coerce')

synthesis = combined.groupby('Description').mean(numeric_only=True).reset_index()

# Rule 6: Add dummy 'S.No.' and 'Unit'
synthesis.insert(0, 'S.No.', range(1, len(synthesis) + 1))
synthesis.insert(2, 'Unit', '1 Kg')

# Rule 7: Reorder and add dummy summary columns
# Total 25 columns
summary_cols = ['Average Prices', 'NaN_1', 'NaN_2', '%change', 'NaN_3']
for sc in summary_cols:
    synthesis[sc] = ""

# Final column order
final_col_order = ['S.No.', 'Description', 'Unit'] + cities + summary_cols
synthesis = synthesis[final_col_order]

# Rule 8: Add \n back into header names
final_rename = {
    'S.No.': 'S.\nNo.',
    'Description': 'Description',
    'Unit': 'Unit',
    'Average Prices': 'Average Prices',
    'NaN_1': 'NaN',
    'NaN_2': 'NaN',
    '%change': '%change',
    'NaN_3': 'NaN'
}
final_rename.update(city_map_rev)
synthesis = synthesis.rename(columns=final_rename)

# Rule 9: Export to Excel twice
synthesis.to_excel(os.path.join(folder_path, 'January_2023.xlsx'), index=False)
synthesis.to_excel(os.path.join(folder_path, 'February_2023.xlsx'), index=False)

print("Synthesized January_2023.xlsx and February_2023.xlsx successfully.")
