import pandas as pd
import warnings
warnings.filterwarnings('ignore')

files = ['Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']
for file in files:
    df_enade = pd.read_excel(file, sheet_name='Enade')
    col_nota_fg = next((c for c in df_enade.columns if 'Bruta' in str(c) and 'FG' in str(c)), None)
    col_nota_ce = next((c for c in df_enade.columns if 'Bruta' in str(c) and 'CE' in str(c)), None)
    print(file, '-> FG:', col_nota_fg, 'CE:', col_nota_ce)
