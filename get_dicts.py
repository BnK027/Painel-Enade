import pandas as pd

try:
    xls = pd.ExcelFile('Enade_2022_Ifes.xlsx')
    sheets_and_cols = [
        ('Arq_10', 'QE_I04'),
        ('Arq_11', 'QE_I05'),
        ('Arq_16', 'QE_I10'),
        ('Arq_17', 'QE_I11'),
        ('Arq_21', 'QE_I15'),
        ('Arq_29', 'QE_I23'),
        ('Arq_31', 'QE_I25'),
        ('Arq_32', 'QE_I26')
    ]
    
    for sheet, col in sheets_and_cols:
        if sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            if col in df.columns:
                print(f"--- {col} ({sheet}) ---")
                print(df[col].value_counts().head(10))
                print()
except Exception as e:
    print(f"Error: {e}")
