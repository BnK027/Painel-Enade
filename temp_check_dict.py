import pandas as pd

file = 'Enade_2021_Ifes.xlsx'
try:
    xls = pd.ExcelFile(file)
    dict_sheet = xls.sheet_names[-2]
    df = pd.read_excel(xls, sheet_name=dict_sheet)
    with open('dict_utf8.txt', 'w', encoding='utf-8') as f:
        for index, row in df.iterrows():
            row_str = " | ".join([f"{col}: {val}" for col, val in zip(df.columns, row.values) if pd.notna(val)])
            f.write(row_str + '\n')
except Exception as e:
    print("Error:", e)
