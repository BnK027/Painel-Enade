import pandas as pd
import numpy as np
import sys
import os
import re
import shutil

def main():
    ano = 2023
    original_file = "Enade 2023.xlsm"
    raw_file = "temp_2023.xlsm"
    out_file = f"Enade_{ano}_Ifes.xlsx"

    print(f"\n{'='*50}")
    print(f" INICIANDO ETL DO ENADE {ano}")
    print(f"{'='*50}\n")
    
    try:
        shutil.copy2(original_file, raw_file)
        print(f"[1/6] Cópia temporária {raw_file} criada para evitar locks.")
    except Exception as e:
        print(f"Erro ao copiar {original_file}: {e}")
        sys.exit(1)
        
    # 2. Carregar EMEC para cruzamento de nomes
    try:
        df_emec = pd.read_excel('Dados Cursos EMEC finalizado.xlsx')
        if 'Código' in df_emec.columns:
            df_emec = df_emec.rename(columns={'Código': 'CO_CURSO', 'Curso': 'NOME DO CURSO', 'Município': 'CAMPUS'})
        df_emec['CO_CURSO'] = pd.to_numeric(df_emec['CO_CURSO'], errors='coerce')
    except Exception as e:
        print(f" Aviso: Erro ao ler EMEC: {e}")
        df_emec = pd.DataFrame(columns=['CO_CURSO', 'NOME DO CURSO', 'CAMPUS'])

    # 3. Ler arquivo Bruto
    print(f"\n[2/6] Lendo arquivo bruto: {raw_file}...")
    try:
        xls_raw = pd.ExcelFile(raw_file)
        abas_brutas = xls_raw.sheet_names
        print(f"      OK! Arquivo lido. Abas encontradas: {len(abas_brutas)}")
    except Exception as e:
        print(f" Erro ao ler arquivo bruto: {e}")
        sys.exit(1)

    print("\n[3/6] Identificando cursos do IFES via arq1...")
    df_arq1 = pd.DataFrame()
    if 'microdados2023_arq1' in abas_brutas:
        df_arq1 = pd.read_excel(xls_raw, sheet_name='microdados2023_arq1')
        df_arq1 = df_arq1[df_arq1['CO_IES'] == 1808]
    ifes_cursos = df_arq1['CO_CURSO'].dropna().unique() if not df_arq1.empty else []
    print(f"      Encontrados {len(ifes_cursos)} cursos do IFES.")

    print("\n[4/6] Processando abas e gerando arquivo final...")
    with pd.ExcelWriter(out_file, engine='openpyxl') as writer:
        
        # Gerar Aba Cursos
        df_cursos = pd.DataFrame({'CO_CURSO': ifes_cursos})
        df_cursos = pd.merge(df_cursos, df_emec[['CO_CURSO', 'NOME DO CURSO', 'CAMPUS']], on='CO_CURSO', how='left')
        df_cursos['NOME DO CURSO'] = df_cursos['NOME DO CURSO'].fillna('Desconhecido')
        df_cursos['CAMPUS'] = df_cursos['CAMPUS'].fillna('Desconhecido')
        df_cursos.to_excel(writer, sheet_name='Cursos', index=False)
        print("      Aba Cursos gerada.")

        # Processar Aba PLANILHA_ENADE para gerar a aba 'Enade' oficial
        if 'PLANILHA_ENADE' in abas_brutas:
            df_planilha = pd.read_excel(xls_raw, sheet_name='PLANILHA_ENADE')
            df_enade = df_planilha[df_planilha['Código do Curso'].isin(ifes_cursos)].copy()
            df_enade.to_excel(writer, sheet_name='Enade', index=False)
            print(f"      Aba Enade extraída com sucesso da PLANILHA_ENADE ({len(df_enade)} registros).")
        else:
            print("      Aviso: PLANILHA_ENADE não encontrada. A aba Enade não foi gerada corretamente.")

        # Processar Abas de Microdados (Arq_X)
        abas_arq = [s for s in abas_brutas if 'arq' in s.lower()]
        
        df_arq3 = None
        for aba in abas_arq:
            # Força a leitura de Arq_3 como string para evitar que o Pandas converta zeros à esquerda em notação científica (1.0e+25)
            if aba.lower() == 'microdados2023_arq3':
                df_temp = pd.read_excel(xls_raw, sheet_name=aba, dtype=str)
            else:
                df_temp = pd.read_excel(xls_raw, sheet_name=aba)
            
            if 'CO_CURSO' in df_temp.columns:
                df_temp = df_temp[df_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True).isin(ifes_cursos.astype(str))].copy()
            
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
            print("\n[5/6] Reconstruindo a aba Arq_3B (Desmembramento Questão por Questão)...")
            df_arq3b = pd.DataFrame()
            df_arq3b['CO_CURSO'] = df_arq3['CO_CURSO']
            
            for col in ['DS_VT_GAB_OFG_FIN', 'DS_VT_GAB_OCE_FIN', 'DS_VT_ESC_OFG', 'DS_VT_ESC_OCE']:
                if col in df_arq3.columns:
                    df_arq3b[col] = df_arq3[col]
            
            if 'DS_VT_ACE_OCE' in df_arq3.columns:
                # O gabarito de 2023 tem 29 questões de Componente Específico em vez de 27.
                # Converte para string com segurança
                s_oce = df_arq3['DS_VT_ACE_OCE'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)
                s_oce = s_oce.str.replace('nan', '', case=False).str.replace('NaN', '', case=False)
                
                # Preenche com zeros à esquerda caso o Pandas tenha removido ao ler como número inicialmente
                s_oce = s_oce.apply(lambda x: str(x).zfill(29) if len(str(x)) > 0 and len(str(x)) < 29 else str(x))
                
                for i in range(29):
                    df_arq3b[f'CE{i+1}'] = pd.to_numeric(s_oce.str[i:i+1], errors='coerce')
                
                df_arq3b.to_excel(writer, sheet_name='Arq_3B', index=False)
                print("      -> Arq_3B gerado com sucesso!")
            else:
                print("       Aviso: Coluna DS_VT_ACE_OCE não encontrada em Arq_3.")

    print(f"\n[6/6] Limpeza...")
    if os.path.exists(raw_file):
        os.remove(raw_file)

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
