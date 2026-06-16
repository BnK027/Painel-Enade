import pandas as pd
import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Uso: python processar_novo_enade_txt.py <ano> <caminho_arquivo_bruto_txt_csv>")
        print("Exemplo: python processar_novo_enade_txt.py 2023 \"MICRODADOS_ENADE_2023.txt\"")
        sys.exit(1)

    ano = sys.argv[1]
    raw_file = sys.argv[2]
    out_file = f"Enade_{ano}_Ifes.xlsx"

    print(f"\n{'='*50}")
    print(f"🚀 INICIANDO ETL DO ENADE {ano} (VIA ARQUIVO TXT/CSV)")
    print(f"{'='*50}\n")
    
    print("[1/4] Carregando dicionário oficial de cursos do IFES...")
    try:
        df_cursos_oficial = pd.read_excel('Dados Cursos EMEC finalizado.xlsx')
        ifes_cursos = df_cursos_oficial['CO_CURSO'].dropna().unique()
    except Exception as e:
        print(f"❌ Erro ao ler 'Dados Cursos EMEC finalizado.xlsx': {e}")
        sys.exit(1)

    print(f"\n[2/4] Lendo arquivo bruto de microdados: {raw_file}...")
    try:
        # Lê o TXT/CSV em blocos (chunks) para economizar RAM caso o arquivo seja gigante (Brasil todo).
        # Assume que o separador do INEP seja ponto e vírgula ';'
        chunksize = 10 ** 5
        chunks = []
        for chunk in pd.read_csv(raw_file, sep=';', encoding='latin1', chunksize=chunksize, low_memory=False):
            # Filtra apenas os cursos do IFES instantaneamente
            if 'CO_CURSO' in chunk.columns:
                chunk_filtered = chunk[chunk['CO_CURSO'].isin(ifes_cursos)]
                chunks.append(chunk_filtered)
            else:
                print("❌ Coluna CO_CURSO não encontrada no arquivo. Verifique se o separador é ;")
                sys.exit(1)
        
        df_microdados = pd.concat(chunks, ignore_index=True)
        print(f"      OK! Extraídos {len(df_microdados)} registros de estudantes pertencentes ao IFES.")
        
        if len(df_microdados) == 0:
            print("      ⚠️ Aviso: Nenhum registro encontrado para o IFES neste arquivo.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Erro ao ler arquivo bruto txt/csv: {e}")
        sys.exit(1)

    print("\n[3/4] Traduzindo o padrão do INEP para a arquitetura de Abas (Arq_X) do Painel IFES...")
    
    # O arquivo texto do INEP junta todas as colunas. A dashboard espera elas separadas.
    # Fazemos a tradução (Mapeamento Reverso) aqui:
    mapeamento_abas = {
        'Arq_5': ['CO_CURSO', 'TP_SEXO'],
        'Arq_6': ['CO_CURSO', 'NU_IDADE'],
        'Arq_8': ['CO_CURSO', 'QE_I02'],
        'Arq_10': ['CO_CURSO', 'QE_I04'],
        'Arq_11': ['CO_CURSO', 'QE_I05'],
        'Arq_14': ['CO_CURSO', 'QE_I08'],
        'Arq_16': ['CO_CURSO', 'QE_I10'],
        'Arq_17': ['CO_CURSO', 'QE_I11'],
        'Arq_21': ['CO_CURSO', 'QE_I15'],
        'Arq_29': ['CO_CURSO', 'QE_I23'],
        'Arq_31': ['CO_CURSO', 'QE_I25'],
        'Arq_32': ['CO_CURSO', 'QE_I26']
    }

    with pd.ExcelWriter(out_file, engine='openpyxl') as writer:
        # Aba de Cursos (Necessária para cruzamentos do app.py)
        df_cursos_oficial.to_excel(writer, sheet_name='Cursos', index=False)
        
        # Gerar abas Demográficas
        for aba, colunas in mapeamento_abas.items():
            cols_disponiveis = [c for c in colunas if c in df_microdados.columns]
            if len(cols_disponiveis) == len(colunas):
                df_aba = df_microdados[cols_disponiveis].copy()
                df_aba.to_excel(writer, sheet_name=aba, index=False)
                print(f"      -> Aba {aba} sintetizada com sucesso.")
            else:
                print(f"      ⚠️ Aviso: Faltaram as colunas {colunas} para montar {aba}.")

        # Gerar aba Arq_4 (Questionário Completo do Estudante)
        cols_qe = [c for c in df_microdados.columns if c.startswith('QE_I') or c == 'CO_CURSO']
        if len(cols_qe) > 1:
            df_arq4 = df_microdados[cols_qe].copy()
            df_arq4.to_excel(writer, sheet_name='Arq_4', index=False)
            print(f"      -> Aba Arq_4 montada com {len(cols_qe)-1} questões do estudante.")
            
        # Gerar aba Arq_3 (Gabaritos Oficiais)
        cols_arq3_esperadas = ['CO_CURSO', 'DS_VT_GAB_OFG_FIN', 'DS_VT_GAB_OCE_FIN', 'DS_VT_ESC_OFG', 'DS_VT_ESC_OCE', 'DS_VT_ACE_OFG', 'DS_VT_ACE_OCE']
        cols_arq3 = [c for c in cols_arq3_esperadas if c in df_microdados.columns]
        if len(cols_arq3) > 1:
            df_arq3 = df_microdados[cols_arq3].copy()
            df_arq3.to_excel(writer, sheet_name='Arq_3', index=False)
            print("      -> Aba Arq_3 montada com os dados de prova.")
            
            # Gerar aba Arq_3B (Análise Questão por Questão)
            print("\n[4/4] Construindo Arq_3B (Desmembramento Automático do Componente Específico)...")
            df_arq3b = df_arq3.copy()
            
            if 'DS_VT_ACE_OCE' in df_arq3b.columns:
                s_oce = df_arq3b['DS_VT_ACE_OCE'].astype(str).str.replace(r'\.0$', '', regex=True)
                s_oce = s_oce.apply(lambda x: x if x != 'nan' else '')
                for i in range(27):
                    # Quebra a string em CE1, CE2, CE3...
                    df_arq3b[f'CE{i+1}'] = pd.to_numeric(s_oce.str[i:i+1], errors='coerce')
                
                df_arq3b.to_excel(writer, sheet_name='Arq_3B', index=False)
                print("      -> Aba Arq_3B gerada com sucesso!")
        else:
            print("      ⚠️ Aviso: Colunas de desempenho na prova não encontradas. Arq_3 pulado.")

    print(f"\n{'='*50}")
    print(f"✅ CONVERSÃO CONCLUÍDA! Base do ENADE {ano} salva em formato Dashboard: {out_file}")
    
    # Automação de Clone Visual
    view_path = f"views/visao_{ano}.py"
    if not os.path.exists(view_path):
        with open('views/visao_2022.py', 'r', encoding='utf-8') as f:
            code = f.read()
        code = code.replace('2022', str(ano))
        with open(view_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"📄 Arquivo do dashboard gráfico criado: {view_path}")
    else:
        print(f"📄 Arquivo de visualização {view_path} já existe.")

    print("\n⚠️ IMPORTANTE: COMO TRATAR A ABA 'Enade' (NOTAS INSTITUCIONAIS)")
    print("Os arquivos TXT de microdados do estudante NÃO trazem a nota geral da faculdade (Enade Contínuo e Faixa).")
    print(f"Para a tela de '🚀 NOTAS' funcionar, abra o arquivo {out_file} gerado, crie uma aba chamada 'Enade'")
    print("e cole a tabela do 'Conceito Enade' lá dentro.")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    main()
