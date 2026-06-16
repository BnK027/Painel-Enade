import pandas as pd
import numpy as np
import sys
import os
import re

def main():
    if len(sys.argv) < 3:
        print("Uso: python processar_novo_enade.py <ano> <caminho_arquivo_bruto>")
        print("Exemplo: python processar_novo_enade.py 2023 \"Enade 2023.xlsm\"")
        sys.exit(1)

    ano = sys.argv[1]
    raw_file = sys.argv[2]
    out_file = f"Enade_{ano}_Ifes.xlsx"

    print(f"\n{'='*50}")
    print(f"🚀 INICIANDO ETL DO ENADE {ano}")
    print(f"{'='*50}\n")
    
    # 1. Carregar Cursos IFES
    print("[1/5] Carregando dicionário oficial de cursos do IFES...")
    try:
        df_cursos_oficial = pd.read_excel('Dados Cursos EMEC finalizado.xlsx')
        ifes_cursos = df_cursos_oficial['CO_CURSO'].dropna().unique()
        print(f"      OK! {len(ifes_cursos)} cursos válidos mapeados.")
    except Exception as e:
        print(f"❌ Erro ao ler 'Dados Cursos EMEC finalizado.xlsx': {e}")
        sys.exit(1)

    # 2. Ler arquivo Bruto
    print(f"\n[2/5] Lendo arquivo bruto: {raw_file} (Isso pode demorar vários minutos)...")
    try:
        xls_raw = pd.ExcelFile(raw_file)
        print(f"      OK! Arquivo lido. Abas encontradas: {len(xls_raw.sheet_names)}")
    except Exception as e:
        print(f"❌ Erro ao ler arquivo bruto: {e}")
        sys.exit(1)

    print("\n[3/5] Iniciando processamento e limpeza (gravando em arquivo temporário)...")
    with pd.ExcelWriter(out_file, engine='openpyxl') as writer:
        
        # Copiar aba Cursos
        df_cursos_oficial.to_excel(writer, sheet_name='Cursos', index=False)

        # Processar Aba Enade (Notas e Metadados)
        enade_sheet = next((s for s in xls_raw.sheet_names if 'enade' in s.lower() and 'microdados' not in s.lower()), None)
        if enade_sheet:
            print(f"      -> Filtrando Aba principal Institucional ({enade_sheet})...")
            df_enade = pd.read_excel(xls_raw, sheet_name=enade_sheet)
            # Filtro para manter apenas IFES
            if 'Código da IES' in df_enade.columns:
                df_enade = df_enade[df_enade['Código da IES'] == 1808]
            elif 'CO_IES' in df_enade.columns:
                df_enade = df_enade[df_enade['CO_IES'] == 1808]
            df_enade.to_excel(writer, sheet_name='Enade', index=False)
        else:
            print("      ⚠️ Aviso: Aba principal do Enade não encontrada.")

        # Processar Abas de Microdados (Arq_X)
        print("\n[4/5] Processando abas de Microdados de Estudantes (Filtro por CO_CURSO)...")
        abas_arq = [s for s in xls_raw.sheet_names if 'arq' in s.lower()]
        
        df_arq3 = None
        for aba in abas_arq:
            df_temp = pd.read_excel(xls_raw, sheet_name=aba)
            
            if 'CO_CURSO' in df_temp.columns:
                df_temp = df_temp[df_temp['CO_CURSO'].isin(ifes_cursos)].copy()
            
            if len(df_temp) == 0:
                continue
                
            # Extrair número do arquivo para padronização (Ex: microdados2017_arq5 -> Arq_5)
            match = re.search(r'arq_?(\d+)', aba.lower())
            nome_aba_saida = f"Arq_{match.group(1)}" if match else aba
            
            # O sistema antigo causou um bug com a coluna ANO, então garantimos que não haja lixo aqui.
            if 'ANO' in df_temp.columns:
                df_temp = df_temp.drop(columns=['ANO'])
            
            print(f"      -> {aba} limpo e convertido para {nome_aba_saida} ({len(df_temp)} registros).")
            
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
                    # Extrai o caractere individual e converte para numérico
                    df_arq3b[f'CE{i+1}'] = pd.to_numeric(s_oce.str[i:i+1], errors='coerce')
                
                df_arq3b.to_excel(writer, sheet_name='Arq_3B', index=False)
                print("      -> Arq_3B gerado com sucesso!")
            else:
                print("      ⚠️ Aviso: Coluna DS_VT_ACE_OCE não encontrada em Arq_3. Impossível desmembrar.")
        else:
            print("\n[5/5] ⚠️ Aviso: Aba de gabaritos (Arq_3) não estava no arquivo bruto. Arq_3B pulado.")

    print(f"\n{'='*50}")
    print(f"✅ SUCESSO! Base do ENADE {ano} salva em: {out_file}")
    
    # Gerar a View Clonada
    view_path = f"views/visao_{ano}.py"
    if not os.path.exists(view_path):
        with open('views/visao_2022.py', 'r', encoding='utf-8') as f:
            code = f.read()
        code = code.replace('2022', str(ano))
        with open(view_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"📄 Arquivo do dashboard criado automaticamente: {view_path}")
    else:
        print(f"📄 O arquivo {view_path} já existe.")

    print("\n🚀 PRÓXIMOS PASSOS OBRIGATÓRIOS PARA ATIVAR NO PAINEL:")
    print(f"   1. Abra o arquivo app.py")
    print(f"   2. Na função load_data(), adicione '{out_file}' na lista `files`")
    print(f"   3. Na função load_microdata(), adicione '{out_file}' na lista `files`")
    print(f"   4. No final do app.py, adicione as 4 linhas de roteamento para a nova view.")
    print(f"   (Leia o MANUAL_ETL_NOVO_ENADE.md para copiar e colar o código certinho).")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    main()
