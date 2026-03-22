import pandas as pd
file = 'Enade_2021_Ifes.xlsx'
try:
    df = pd.read_excel(file, sheet_name='Arq_3')
    print("TP_PRES values:", df['TP_PRES'].value_counts(dropna=False))
except Exception as e:
    print("Error:", e)
