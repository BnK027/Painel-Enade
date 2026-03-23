import pandas as pd
import json

try:
    xls = pd.ExcelFile('Enade_2022_Ifes.xlsx')
    info = {"sheets": xls.sheet_names}
    for sheet in xls.sheet_names:
        if sheet.startswith("Arq_"):
            df = pd.read_excel(xls, sheet_name=sheet, nrows=2)
            info[sheet] = df.columns.tolist()
            # print sample of first row to understand the data
            if not df.empty:
                print(f"Sheet {sheet} columns: {info[sheet][:10]}")
                print(f"Sheet {sheet} sample: {df.iloc[0].to_dict()}")
except Exception as e:
    print(f"Error: {e}")
