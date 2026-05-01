import pandas as pd

# 1. Load master_cpi_data.csv
df = pd.read_csv('master_cpi_data.csv')

# 2. Sort the dataframe strictly by ['Year', 'City', 'Item', 'Month']
df = df.sort_values(by=['Year', 'City', 'Item', 'Month'])

# 3. Group by ['Year', 'City', 'Item'] and calculate .diff() on 'Price'
df['Price_Change'] = df.groupby(['Year', 'City', 'Item'])['Price'].transform(lambda x: x.diff())

# 4. Drop all rows where Month == 1
# The vector is strictly from Month 2 to 12.
df_filtered = df[df['Month'] != 1].copy()

# 5. Use pd.pivot_table() to reshape the data
# Index: ['Year', 'City', 'Category', 'Item'], Columns: Month, Values: Price_Change
pivot_df = pd.pivot_table(
    df_filtered, 
    index=['Year', 'City', 'Category', 'Item'], 
    columns='Month', 
    values='Price_Change'
)

# 6. Fill any missing values (NaN) with 0.0
pivot_df = pivot_df.fillna(0.0)

# 7. Flatten the column headers and rename to 'Month_2', ..., 'Month_12'
pivot_df.columns = [f'Month_{int(m)}' for m in pivot_df.columns]

# 8. Reset the index and save
result_df = pivot_df.reset_index()
result_df.to_csv('price_vectors.csv', index=False)

print(f"Successfully saved {len(result_df)} vectors to price_vectors.csv")
print("Vector dimensions (columns 4 onwards):", result_df.columns[4:].tolist())
