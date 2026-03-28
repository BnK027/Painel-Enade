import pandas as pd
import json

file = 'Enade_2022_Ifes_temp.xlsx'
try:
    xls = pd.ExcelFile(file)
    # The sheet name had weird encoding characters. Let's find it.
    dic_sheet = [s for s in xls.sheet_names if 'DICION' in s][0]
    df = pd.read_excel(xls, sheet_name=dic_sheet)
    
    out = []
    for i, row in df.iterrows():
        row_str = ' | '.join([str(x) for x in row if pd.notna(x)])
        if 'QE_I' in row_str and ('tecnologia' in row_str.lower() or 'professor' in row_str.lower() or 'conte' in row_str.lower()):
            out.append(row_str)
            print(row_str)
            
    with open('qe_questions.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
        
except Exception as e:
    print(f"Error: {e}")
