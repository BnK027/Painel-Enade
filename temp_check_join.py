import pandas as pd

file = 'Enade_2021_Ifes.xlsx'
try:
    df_pres = pd.read_excel(file, sheet_name='Arq_3')
    df_idade = pd.read_excel(file, sheet_name='Arq_6')
    df_renda = pd.read_excel(file, sheet_name='Arq_14')
    
    print("Arq_3 shape:", df_pres.shape)
    print("Arq_6 shape:", df_idade.shape)
    print("Arq_14 shape:", df_renda.shape)
    
    # Check if we can safely concatenate horizontally
    df_merged = pd.concat([df_pres['TP_PRES'], df_idade['NU_IDADE'], df_renda['QE_I08'], df_pres['CO_CURSO']], axis=1)
    print(df_merged.head())
    
    # Calculate evasao
    df_merged['EVADIU'] = df_merged['TP_PRES'].apply(lambda x: 1 if x == 222 else 0)
    print("Evasao total:", df_merged['EVADIU'].sum())
    
except Exception as e:
    print("Error:", e)
