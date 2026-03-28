import pandas as pd
import shutil
import os

f = 'Enade_2018_Ifes.xlsx'
tmp_name = f"temp_{f}"
shutil.copy2(f, tmp_name)

try:
    xls = pd.ExcelFile(tmp_name)
    dic_sheet = [s for s in xls.sheet_names if 'DICION' in s.upper()][0]
    df = pd.read_excel(xls, sheet_name=dic_sheet)
    
    # print the first 30 rows showing all columns
    print(df.head(30).to_string())

except Exception as e:
    print(f"Error: {e}")
finally:
    if os.path.exists(tmp_name):
        os.remove(tmp_name)
