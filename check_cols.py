import pandas as pd
import glob

files = glob.glob("Enade_*_Ifes.xlsx")
for file in files:
    print(f"--- {file} ---")
    try:
        df_e = pd.read_excel(file, sheet_name='Enade')
        df_c = pd.read_excel(file, sheet_name='Cursos')
        print("Enade cols:", [c for c in df_e.columns if "Código" in c or "Munic" in c or "Conceito" in c or "Ano" in c])
        print("Cursos cols:", [c for c in df_c.columns if "CO_CURSO" in c or "CAMPUS" in c])
    except Exception as e:
        print("Error:", e)
