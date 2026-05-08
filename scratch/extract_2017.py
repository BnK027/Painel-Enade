import pandas as pd
import os

base_path = 'microdados_Enade_2017_LGPD/2.DADOS'
output_file = 'Enade_2017_Ifes.xlsx'

print("Lendo arq1 para filtrar IFES (1808)...")
arq1 = pd.read_csv(os.path.join(base_path, 'microdados2017_arq1.txt'), sep=';')
ifes_mask = arq1['CO_IES'] == 1808
df_ifes = arq1[ifes_mask].copy()

# Files to process
files_to_process = {
    'microdados2017_arq3.txt': ['NT_GER', 'NT_FG', 'NT_CE', 'TP_PRES'],
    'microdados2017_arq4.txt': [f'QE_I{i}' for i in range(27, 69)],
    'microdados2017_arq5.txt': ['TP_SEXO'],
    'microdados2017_arq6.txt': ['NU_IDADE'],
}
for i in range(1, 27):
    files_to_process[f'microdados2017_arq{i+6}.txt'] = [f'QE_I{i:02d}']

for filename, cols in files_to_process.items():
    print(f"Processando {filename}...")
    df_temp = pd.read_csv(os.path.join(base_path, filename), sep=';')
    df_filtered = df_temp[ifes_mask][cols]
    df_ifes = pd.concat([df_ifes.reset_index(drop=True), df_filtered.reset_index(drop=True)], axis=1)

# Robust mapping from 2021
curso_map = {}
campus_map = {}
try:
    df_21 = pd.read_excel('Enade_2021_Ifes.xlsx', sheet_name='Cursos')
    # Try different name columns
    name_col = 'CURSO' if 'CURSO' in df_21.columns else ('NOME_CURSO' if 'NOME_CURSO' in df_21.columns else 'NOME DO CURSO')
    curso_map = dict(zip(df_21['CO_CURSO'], df_21[name_col]))
    campus_map = dict(zip(df_21['CO_CURSO'], df_21['CAMPUS']))
except Exception as e:
    print(f"Erro ao carregar mapa 2021: {e}")

df_ifes['NOME DO CURSO'] = df_ifes['CO_CURSO'].apply(lambda x: curso_map.get(x, f"Curso {x}"))
df_ifes['CAMPUS'] = df_ifes['CO_CURSO'].apply(lambda x: campus_map.get(x, "IFES (Sede)"))
df_ifes['Ano'] = 2017

with pd.ExcelWriter(output_file) as writer:
    df_ifes.to_excel(writer, sheet_name='Microdados', index=False)
    
    enade_resumo = df_ifes.groupby('CO_CURSO').agg({
        'NOME DO CURSO': 'first',
        'CAMPUS': 'first',
        'Ano': 'first',
        'CO_IES': 'count',
        'TP_PRES': lambda x: (x == 555).sum(),
        'NT_GER': 'mean',
        'NT_FG': 'mean',
        'NT_CE': 'mean'
    }).reset_index()
    
    enade_resumo.columns = ['Código do Curso', 'Área de Avaliação', 'CAMPUS', 'Ano', 'Inscritos', 'Participantes', 'Nota Bruta Geral', 'Nota Bruta FG', 'Nota Bruta CE']
    enade_resumo['Conceito Enade (Contínuo)'] = 0.0
    enade_resumo['Conceito Enade (Faixa)'] = 'N/A'
    enade_resumo['Município do Curso'] = 'ES'
    
    enade_resumo.to_excel(writer, sheet_name='Enade', index=False)
    
    cursos_df = df_ifes[['CO_CURSO', 'NOME DO CURSO', 'CAMPUS']].drop_duplicates()
    cursos_df.columns = ['CO_CURSO', 'NOME_CURSO', 'CAMPUS']
    cursos_df.to_excel(writer, sheet_name='Cursos', index=False)
    
    # Extra sheets
    df_ifes[['CO_CURSO', 'TP_SEXO']].to_excel(writer, sheet_name='Arq_5', index=False)
    df_ifes[['CO_CURSO', 'NU_IDADE', 'Ano']].rename(columns={'Ano':'ANO'}).to_excel(writer, sheet_name='Arq_6', index=False)
    df_ifes[['CO_CURSO', 'QE_I02', 'Ano']].rename(columns={'Ano':'ANO'}).to_excel(writer, sheet_name='Arq_8', index=False)
    df_ifes[['CO_CURSO', 'QE_I08', 'Ano']].rename(columns={'Ano':'ANO'}).to_excel(writer, sheet_name='Arq_14', index=False)
    df_ifes[['CO_CURSO'] + [f'QE_I{i}' for i in range(27, 69)] + ['Ano']].rename(columns={'Ano':'ANO'}).to_excel(writer, sheet_name='Arq_4', index=False)
    
    sheets_map = {10:'Arq_10', 11:'Arq_11', 16:'Arq_16', 17:'Arq_17', 21:'Arq_21', 29:'Arq_29', 31:'Arq_31', 32:'Arq_32'}
    for i, sheet in sheets_map.items():
        col = f'QE_I{i:02d}'
        df_ifes[['CO_CURSO', col, 'Ano']].rename(columns={'Ano':'ANO'}).to_excel(writer, sheet_name=sheet, index=False)

print("Arquivo Enade_2017_Ifes.xlsx finalizado.")
