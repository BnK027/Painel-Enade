import pandas as pd
import numpy as np
import sys
import os
import re

def main():
    if len(sys.argv) < 3:
        print("Uso: python processar_enade_diretorio.py <ano> <caminho_pasta_bruta>")
        sys.exit(1)

    ano = sys.argv[1]
    raw_dir = sys.argv[2]
    out_file = f"Enade_{ano}_Ifes.xlsx"

    print(f"\n{'='*50}")
    print(f"INICIANDO ETL DO ENADE {ano} (VIA DIRETÓRIO DE TXTs)")
    print(f"{'='*50}\n")
    
    print("[1/4] Carregando dicionário oficial de cursos do IFES...")
    try:
        df_cursos_oficial = pd.read_excel('Dados Cursos EMEC finalizado.xlsx')
        if 'Código' in df_cursos_oficial.columns:
            df_cursos_oficial = df_cursos_oficial.rename(columns={'Código': 'CO_CURSO'})
        if 'Município' in df_cursos_oficial.columns and 'CAMPUS' not in df_cursos_oficial.columns:
            df_cursos_oficial['CAMPUS'] = df_cursos_oficial['Município']
        ifes_cursos = df_cursos_oficial['CO_CURSO'].dropna().astype(str).str.replace(r'\.0$', '', regex=True).unique()
    except Exception as e:
        print(f"Erro ao ler Dados Cursos EMEC finalizado.xlsx: {e}")
        sys.exit(1)

    # Verifica subpasta 2.DADOS
    dados_dir = os.path.join(raw_dir, '2.DADOS')
    if not os.path.exists(dados_dir):
        dados_dir = raw_dir # Se não tiver subpasta, usa a raiz
        
    txt_files = [f for f in os.listdir(dados_dir) if f.endswith('.txt') or f.endswith('.csv')]
    if not txt_files:
        print(f"Nenhum arquivo .txt encontrado em {dados_dir}")
        sys.exit(1)
        
    print(f"\n[2/4] Lendo {len(txt_files)} arquivos de microdados no diretório...")

    with pd.ExcelWriter(out_file, engine='openpyxl') as writer:
        df_cursos_oficial.to_excel(writer, sheet_name='Cursos', index=False)
        
        df_arq3 = None
        for file in txt_files:
            aba_bruta = file.split('.')[0]
            
            # Filtra apenas se for arq
            if 'arq' not in aba_bruta.lower():
                continue
                
            match = re.search(r'arq_?(\d+)', aba_bruta.lower())
            nome_aba_saida = f"Arq_{match.group(1)}" if match else aba_bruta
            
            file_path = os.path.join(dados_dir, file)
            # Tentar utf-8 e latin1
            try:
                df_temp = pd.read_csv(file_path, sep=';', encoding='latin1', low_memory=False)
            except:
                df_temp = pd.read_csv(file_path, sep=',', encoding='utf-8', low_memory=False)
                
            if 'CO_CURSO' in df_temp.columns:
                # Trata a tipagem da coluna CO_CURSO no TXT
                df_temp['CO_CURSO_STR'] = df_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
                df_temp = df_temp[df_temp['CO_CURSO_STR'].isin(ifes_cursos)].copy()
                df_temp = df_temp.drop(columns=['CO_CURSO_STR'])
                
            if len(df_temp) == 0:
                continue
                
            if 'ANO' in df_temp.columns:
                df_temp = df_temp.drop(columns=['ANO'])
                
            if nome_aba_saida == 'Arq_3':
                df_arq3 = df_temp.copy()
                
            df_temp.to_excel(writer, sheet_name=nome_aba_saida, index=False)
            print(f"      -> {nome_aba_saida} filtrado e salvo com {len(df_temp)} registros.")

        # Gerar Arq_3B
        if df_arq3 is not None:
            print("\n[3/4] Construindo Arq_3B (Desmembramento do Componente Específico)...")
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
        
        # Gerar Aba "Enade" placeholder para evitar quebra no painel
        print("\n[4/4] Gerando aba institucional...")
        # Cria uma aba Enade fake usando a base de cursos para ter Área de Avaliação e Código
        df_enade = pd.DataFrame()
        df_enade['Código do Curso'] = df_cursos_oficial['CO_CURSO']
        df_enade['Área de Avaliação'] = df_cursos_oficial['Curso'] if 'Curso' in df_cursos_oficial.columns else 'Curso IFES'
        df_enade['Ano'] = ano
        df_enade.to_excel(writer, sheet_name='Enade', index=False)
        print("      -> Aba Enade injetada com placeholders.")

    print(f"\n{'='*50}")
    print(f"SUCESSO! Base do ENADE {ano} convertida do diretório para: {out_file}")
    
    # Gerar a View Clonada
    view_path = f"views/visao_{ano}.py"
    if not os.path.exists(view_path):
        with open('views/visao_2022.py', 'r', encoding='utf-8') as f:
            code = f.read()
        code = code.replace('2022', str(ano))
        with open(view_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"Arquivo do dashboard criado automaticamente: {view_path}")

if __name__ == '__main__':
    main()
