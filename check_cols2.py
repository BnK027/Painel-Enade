import pandas as pd
import glob

files = glob.glob("Enade_*_Ifes.xlsx")
for file in files:
    print(f"--- {file} ---")
    df_e = pd.read_excel(file, sheet_name='Enade', nrows=0)
    print("Enade cols:", list(df_e.columns))
