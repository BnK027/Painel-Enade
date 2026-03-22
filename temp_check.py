import pandas as pd

try:
    xls = pd.ExcelFile('Enade_2022_Ifes.xlsx')
    print('Sheets:', xls.sheet_names)
    has_demo = False
    for s in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=s)
        demo_cols = [c for c in df.columns if any(w in str(c).lower() for w in ['idade', 'sexo', 'masculin', 'femini', 'cor', 'raça'])]
        if demo_cols:
            print(f"Sheet '{s}' has demo cols: {demo_cols}")
            print(df[demo_cols].head())
            has_demo = True
            
    if not has_demo:
        print("NO DEMOGRAPHIC DATA FOUND IN ANY SHEET.")

except Exception as e:
    print(f"Error: {e}")
