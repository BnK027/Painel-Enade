import pandas as pd

file = 'Enade_2022_Ifes_temp.xlsx'
try:
    xls = pd.ExcelFile(file)
    print("Sheets:", xls.sheet_names)

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
        for col in df.columns:
            col_str = str(col).lower()
            if 'professores' in col_str or 'tecnologias' in col_str:
                print(f"[{sheet}] header match: {col}")
            
            if len(df) > 0:
                val = str(df[col].iloc[0]).lower()
                val2 = str(df[col].iloc[1]).lower() if len(df) > 1 else ""
                
                if 'professores' in val or 'tecnologias' in val:
                    print(f"[{sheet}] row0 match: {col} -> {df[col].iloc[0]}")
                if 'professores' in val2 or 'tecnologias' in val2:
                    print(f"[{sheet}] row1 match: {col} -> {df[col].iloc[1]}")
                    
except Exception as e:
    print(f"Error: {e}")
