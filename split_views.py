import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Extrair a funcao show_visao_ano
match = re.search(r'def show_visao_ano\(\):(.*?)(?=\n# --- ROUTER \(GERENCIADOR DE ESTADO\) ---)', app_content, re.DOTALL)
if match:
    body = match.group(1)
    
    # Adicionar os imports necessarios e a assinatura da funcao
    header = '''import streamlit as st
import pandas as pd
import plotly.express as px

def render_visao_{ano}(data, microdados, render_filters):
    ano = '{ano}'
'''
    
    # Substituir ano dinamico pelo fixo no corpo e ajustar indentação
    # O body já está indentado em 4 espaços. A assinatura usa 4 espaços também,
    # mas o corpo original começava com a linha:
    #     ano = st.session_state.get('ano_selecionado', '2018')
    # que substituimos no header.
    
    # Remove as primeiras linhas do body (ano e col_back) ate col_back:
    body = re.sub(r'^\n    ano = st.session_state\.get.*?st\.rerun\(\)\n            ', '', body, flags=re.DOTALL)
    
    # Vamos recriar o botao de voltar
    btn_back = '''
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True, key='back_bt_visao_{ano}'):
            st.session_state.page = 'home'
            st.rerun()
'''
    
    for ano in ['2018', '2019', '2021', '2022']:
        content = header.format(ano=ano) + btn_back.format(ano=ano) + body
        with open(f'views/visao_{ano}.py', 'w', encoding='utf-8') as out_f:
            out_f.write(content)
        print(f"Created views/visao_{ano}.py")
else:
    print("Could not find show_visao_ano")
