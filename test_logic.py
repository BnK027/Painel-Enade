import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from app import load_data, render_filters

data = load_data()
for year in ['2018', '2019', '2021', '2022']:
    df = data.copy()
    if str(df['ANO'].dtype) == 'object':
        df = df[df['ANO'] == str(year)]
    else:
        try: df = df[df['ANO'] == float(year)]
        except: pass
    
    print(f"\nYear {year}: {df.shape[0]} rows")
    if df.shape[0] > 0:
        df_calc = df.copy()
        if 'NOTA_FG' in df_calc.columns and 'NOTA_CE' in df_calc.columns:
            df_calc['NOTA_FG'] = pd.to_numeric(df_calc['NOTA_FG'].astype(str).str.replace(',', '.'), errors='coerce')
            df_calc['NOTA_CE'] = pd.to_numeric(df_calc['NOTA_CE'].astype(str).str.replace(',', '.'), errors='coerce')
            avg_scores = df_calc.groupby('NOME DO CURSO')[['NOTA_FG', 'NOTA_CE']].mean().reset_index().dropna()
            print(f"Courses in Raio-X chart for {year}: {avg_scores['NOME DO CURSO'].tolist()}")
        else:
            print("Missing NOTA_FG or NOTA_CE")
