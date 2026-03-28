import pandas as pd

file = 'Enade_2022_Ifes_temp.xlsx'
try:
    xls = pd.ExcelFile(file)
    dic_sheet = [s for s in xls.sheet_names if 'DICION' in s][0]
    df = pd.read_excel(xls, sheet_name=dic_sheet)
    
    with open('dicionario_completo.txt', 'w', encoding='utf-8') as f:
        for i, row in df.iterrows():
            row_str = ' | '.join([str(x).replace('\n', ' ') for x in row if pd.notna(x)])
            f.write(row_str + '\n')
            
except Exception as e:
    print(e)
