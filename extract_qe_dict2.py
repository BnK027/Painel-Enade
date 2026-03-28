import pandas as pd
import json

file = 'Enade_2022_Ifes_temp.xlsx'
try:
    xls = pd.ExcelFile(file)
    dic_sheet = [s for s in xls.sheet_names if 'DICION' in s][0]
    df = pd.read_excel(xls, sheet_name=dic_sheet)

    questions = {}
    for i, row in df.iterrows():
        vals = [str(x).replace('\n',' ').replace('\r',' ').strip() for x in row if pd.notna(x)]
        
        for val in vals:
            if val.startswith('QE_I') and len(val) <= 6:
                var_name = val
                desc_candidates = [v for v in vals if v != var_name and len(v) > 15]
                if desc_candidates:
                    desc = max(desc_candidates, key=len)
                    questions[var_name] = desc
                break

    with open('qe_dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)
    print(f"Extracted {len(questions)} questions.")

except Exception as e:
    print(f"Error: {e}")
