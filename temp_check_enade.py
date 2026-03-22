import pandas as pd
import json

file = 'Enade_2021_Ifes.xlsx'
try:
    xls = pd.ExcelFile(file)
    print("Sheets:", xls.sheet_names)
    
    for sheet in xls.sheet_names:
        if sheet.startswith('Arq_'):
            df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
            print(f"--- {sheet} ---")
            print(df.columns.tolist())
            # print some values from the question column (usually QE_Ixx)
            for col in df.columns:
                if col.startswith('QE_'):
                    vals = df[col].dropna().unique()
                    print(f"  {col}: {vals}")
except Exception as e:
    print("Error:", e)
