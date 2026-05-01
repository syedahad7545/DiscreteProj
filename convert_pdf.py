import pdfplumber
import pandas as pd
import os

pdf_path = 'Data/xlsx_files/March_2023.pdf'
xlsx_path = 'Data/xlsx_files/March_2023.xlsx'

all_data = []
try:
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                all_data.extend(table)
    
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel(xlsx_path, index=False, header=False)
        print(f"Successfully converted {pdf_path} to {xlsx_path}")
    else:
        print("No tables found in PDF.")
except Exception as e:
    print(f"Error: {e}")
