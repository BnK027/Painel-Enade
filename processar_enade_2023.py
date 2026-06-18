import pandas as pd
import numpy as np
import sys
import os
import re

def main():
    ano = 2023
    raw_file = "temp_2023.xlsm" # Lendo do temp por permissao
    out_file = f"Enade_{ano}_Ifes.xlsx"

    print(f"\n{'='*50}")
    print(f" INICIANDO ETL DO ENADE {ano}")
    print(f"{'='*50}\n")
    
    # 1. Carregar EMEC para cruzamento de nomes
    try:
        df_emec = pd.read_excel('Dados Cursos EMEC finalizado.xlsx')
        if 'Código' in df_emec.columns:
            df_emec = df_emec.rename(columns={'Código': 'CO_CURSO', 'Curso': 'NOME DO CURSO', 'Município': 'CAMPUS'})
        df_emec['CO_CURSO'] = pd.to_numeric(df_emec['CO_CURSO'], errors='coerce')
    except Exception as e:
        print(f" Aviso: Erro ao ler EMEC: {e}")
        df_emec = pd.DataFrame(columns=['CO_CURSO', 'NOME DO CURSO', 'CAMPUS'])

    # 2. Ler arquivo Bruto
    print(f"\n[2/5] Lendo arquivo bruto: {raw_file}...")
    try:
        xls_raw = pd.ExcelFile(raw_file)
        abas_brutas = xls_raw.sheet_names
        print(f"      OK! Arquivo lido. Abas encontradas: {len(abas_brutas)}")
    except Exception as e:
        print(f" Erro ao ler arquivo bruto: {e}")
        sys.exit(1)

    print("\n[3/5] Identificando cursos do IFES via arq1...")
    df_arq1 = pd.DataFrame()
    if 'microdados2023_arq1' in abas_brutas:
        df_arq1 = pd.read_excel(xls_raw, sheet_name='microdados2023_arq1')
        df_arq1 = df_arq1[df_arq1['CO_IES'] == 1808]
    ifes_cursos = df_arq1['CO_CURSO'].dropna().unique() if not df_arq1.empty else []
    print(f"      Encontrados {len(ifes_cursos)} cursos do IFES.")

    print("\n[4/5] Processando abas e gerando arquivo final...")
    with pd.ExcelWriter(out_file, engine='openpyxl') as writer:
        
        # Gerar Aba Cursos e Enade sintetica
        df_cursos = pd.DataFrame({'CO_CURSO': ifes_cursos})
        df_cursos = pd.merge(df_cursos, df_emec[['CO_CURSO', 'NOME DO CURSO', 'CAMPUS']], on='CO_CURSO', how='left')
        df_cursos['NOME DO CURSO'] = df_cursos['NOME DO CURSO'].fillna('Desconhecido')
        df_cursos['CAMPUS'] = df_cursos['CAMPUS'].fillna('Desconhecido')
        df_cursos.to_excel(writer, sheet_name='Cursos', index=False)

        df_enade = pd.DataFrame()
        df_enade['Código do Curso'] = df_cursos['CO_CURSO']
        df_enade['Área de Avaliação'] = df_cursos['NOME DO CURSO']
        df_enade['Município do Curso'] = df_cursos['CAMPUS']
        df_enade['Ano'] = ano
        df_enade['Conceito Enade (Contínuo)'] = np.nan
        df_enade['Conceito Enade (Faixa)'] = np.nan
        df_enade['Inscritos'] = np.nan
        df_enade['Participantes'] = np.nan
        df_enade.to_excel(writer, sheet_name='Enade', index=False)
        print("      Abas Cursos e Enade geradas.")

        # Processar Abas de Microdados (Arq_X)
        abas_arq = [s for s in abas_brutas if 'arq' in s.lower()]
        
        df_arq3 = None
        for aba in abas_arq:
            df_temp = pd.read_excel(xls_raw, sheet_name=aba)
            
            if 'CO_CURSO' in df_temp.columns:
                df_temp = df_temp[df_temp['CO_CURSO'].isin(ifes_cursos)].copy()
            
            if len(df_temp) == 0:
                continue
                
            match = re.search(r'arq_?(\d+)', aba.lower())
            nome_aba_saida = f"Arq_{match.group(1)}" if match else aba
            
            if 'ANO' in df_temp.columns:
                df_temp = df_temp.drop(columns=['ANO'])
            
            print(f"      -> {aba} convertido para {nome_aba_saida} ({len(df_temp)} registros).")
            
            if nome_aba_saida == 'Arq_3':
                df_arq3 = df_temp.copy()
            
            df_temp.to_excel(writer, sheet_name=nome_aba_saida, index=False)

        # Construir Arq_3B (Desempenho Componente Específico)
        if df_arq3 is not None:
            print("\n[5/5] Reconstruindo a aba Arq_3B (Desmembramento Questão por Questão)...")
            df_arq3b = pd.DataFrame()
            df_arq3b['CO_CURSO'] = df_arq3['CO_CURSO']
            
            for col in ['DS_VT_GAB_OFG_FIN', 'DS_VT_GAB_OCE_FIN', 'DS_VT_ESC_OFG', 'DS_VT_ESC_OCE']:
                if col in df_arq3.columns:
                    df_arq3b[col] = df_arq3[col]
            
            if 'DS_VT_ACE_OCE' in df_arq3.columns:
                s_oce = df_arq3['DS_VT_ACE_OCE'].astype(str).str.replace(r'\.0$', '', regex=True)
                s_oce = s_oce.apply(lambda x: x if x != 'nan' else '')
                for i in range(27):
                    df_arq3b[f'CE{i+1}'] = pd.to_numeric(s_oce.str[i:i+1], errors='coerce')
                
                df_arq3b.to_excel(writer, sheet_name='Arq_3B', index=False)
                print("      -> Arq_3B gerado com sucesso!")
            else:
                print("       Aviso: Coluna DS_VT_ACE_OCE não encontrada em Arq_3.")

    print(f"\n{'='*50}")
    print(f" SUCESSO! Base do ENADE {ano} salva em: {out_file}")
    
    view_path = f"views/visao_{ano}.py"
    if not os.path.exists(view_path):
        with open('views/visao_2022.py', 'r', encoding='utf-8') as f:
            code = f.read()
        code = code.replace('2022', str(ano))
        with open(view_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f" Arquivo do dashboard criado: {view_path}")

if __name__ == '__main__':
    main()
