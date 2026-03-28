import pandas as pd
import shutil
import os

tmp_name = "temp_Enade_2018_Ifes.xlsx"
shutil.copy2('Enade_2018_Ifes.xlsx', tmp_name)

try:
    xls = pd.ExcelFile(tmp_name)
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        for i, row in df.iterrows():
            row_str = str(row.to_list())
            if 'QE_I27' in row_str or 'QE_I68' in row_str:
                print(f"[{sheet}] Row {i}: A='{row.iloc[0]}' | D='{row.iloc[3] if len(row) > 3 else 'N/A'}'")
except Exception as e:
    print(f"Error: {e}")
finally:
    if os.path.exists(tmp_name):
        try:
            xls.close()
            os.remove(tmp_name)
        except:
            pass
