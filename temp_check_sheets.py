import pandas as pd
import os

files = ['Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']
target_sheets = ['Arq_2', 'Arq_3', 'Arq_6', 'Arq_14', 'Arq_23']

for f in files:
    try:
        xls = pd.ExcelFile(f)
        sheets = xls.sheet_names
        missing = [s for s in target_sheets if s not in sheets]
        print(f"{f}: Missing {missing}")
    except Exception as e:
        print(f"Error {f}: {e}")
