import pandas as pd
import shutil
import os
import re

files = ['Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']
all_dicts = {}

for f in files:
    tmp_name = f"temp_{f}"
    shutil.copy2(f, tmp_name)
    try:
        xls = pd.ExcelFile(tmp_name)
        df = pd.read_excel(xls, sheet_name='Microdados', header=None)
        
        qe_dict = {}
        for idx, row in df.iterrows():
            col_a = str(row.iloc[0]).strip()
            if col_a.startswith('QE_I') and len(col_a) >= 6:
                if len(row) > 3:
                    col_d = str(row.iloc[3]).strip()
                    if col_d and str(col_d).lower() != 'nan':
                        qe_dict[col_a] = col_d
                
        all_dicts[f] = qe_dict
        xls.close()
    except Exception as e:
        print(f"Error on {f}: {e}")
    finally:
        os.remove(tmp_name)

# Let's save the dictionary to a JSON file to inspect
import json
with open('extracted_missing_qe.json', 'w', encoding='utf-8') as fh:
    json.dump(all_dicts, fh, indent=2, ensure_ascii=False)

print("Extraction completed. Found questions:")
for f in files:
    print(f"[{f}]: {len(all_dicts.get(f, {}))} questions missing (QE_I27+)")

