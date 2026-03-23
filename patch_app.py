import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update lists initialization
content = content.replace(
    "all_sexo, all_idade, all_raca, all_renda, all_evasao = [], [], [], [], []",
    "all_sexo, all_idade, all_raca, all_renda, all_evasao = [], [], [], [], []\n    all_pai, all_mae, all_trab, all_bolsa, all_cota, all_estudo, all_motiv_c, all_motiv_i = [], [], [], [], [], [], [], []"
)

# 2. Extract new arcs
arq14_block = """            if 'Arq_14' in xls.sheet_names:
                df_renda = pd.merge(pd.read_excel(xls, sheet_name='Arq_14'), curso_map, on='CO_CURSO', how='inner')
                if not df_renda.empty: all_renda.append(df_renda)"""
new_arcs_block = """            if 'Arq_14' in xls.sheet_names:
                df_renda = pd.merge(pd.read_excel(xls, sheet_name='Arq_14'), curso_map, on='CO_CURSO', how='inner')
                if not df_renda.empty: all_renda.append(df_renda)

            for arq, lst in zip(['Arq_10','Arq_11','Arq_16','Arq_17','Arq_21','Arq_29','Arq_31','Arq_32'], 
                                [all_pai, all_mae, all_trab, all_bolsa, all_cota, all_estudo, all_motiv_c, all_motiv_i]):
                if arq in xls.sheet_names:
                    df_temp = pd.merge(pd.read_excel(xls, sheet_name=arq), curso_map, on='CO_CURSO', how='inner')
                    if not df_temp.empty: lst.append(df_temp)"""
content = content.replace(arq14_block, new_arcs_block)

# 3. Update return schema
return_block = """        'renda': pd.concat(all_renda, ignore_index=True) if all_renda else pd.DataFrame(),
        'evasao': pd.concat(all_evasao, ignore_index=True) if all_evasao else pd.DataFrame()
    }"""
new_return_block = """        'renda': pd.concat(all_renda, ignore_index=True) if all_renda else pd.DataFrame(),
        'evasao': pd.concat(all_evasao, ignore_index=True) if all_evasao else pd.DataFrame(),
        'pai': pd.concat(all_pai, ignore_index=True) if all_pai else pd.DataFrame(),
        'mae': pd.concat(all_mae, ignore_index=True) if all_mae else pd.DataFrame(),
        'trab': pd.concat(all_trab, ignore_index=True) if all_trab else pd.DataFrame(),
        'bolsa': pd.concat(all_bolsa, ignore_index=True) if all_bolsa else pd.DataFrame(),
        'cota': pd.concat(all_cota, ignore_index=True) if all_cota else pd.DataFrame(),
        'estudo': pd.concat(all_estudo, ignore_index=True) if all_estudo else pd.DataFrame(),
        'motiv_c': pd.concat(all_motiv_c, ignore_index=True) if all_motiv_c else pd.DataFrame(),
        'motiv_i': pd.concat(all_motiv_i, ignore_index=True) if all_motiv_i else pd.DataFrame()
    }"""
content = content.replace(return_block, new_return_block)

show_estudantes_new = """def show_estudantes():
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True, key='back_bt_estd'):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown('''
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
            <p style="color: #32A041; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;">Microdados Sociodemográficos INEP</p>
            <h1 class="main-title" style="font-size: 3rem;">INFORMAÇÕES DO ESTUDANTE</h1>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider" style="margin: 20px 0;">', unsafe_allow_html=True)

    filtered_data = render_filters(data)
    st.markdown("<br>", unsafe_allow_html=True)
    
    cursos_filtrados = filtered_data['CO_CURSO'].unique().tolist()
    anos_filtrados = filtered_data['ANO'].unique().tolist()
    
    t1, t2, t3, t4 = st.tabs(["📊 Demografia Básica", "💼 Perfil Socioeconômico", "🏛️ Acesso e Permanência", "📚 Rotina de Estudos"])
    
    with t1:
        df_sexo = microdados['sexo'][microdados['sexo']['CO_CURSO'].isin(cursos_filtrados) & microdados['sexo']['ANO'].isin(anos_filtrados)]
        df_idade = microdados['idade'][microdados['idade']['CO_CURSO'].isin(cursos_filtrados) & microdados['idade']['ANO'].isin(anos_filtrados)]
        df_raca = microdados['raca'][microdados['raca']['CO_CURSO'].isin(cursos_filtrados) & microdados['raca']['ANO'].isin(anos_filtrados)]
        df_renda = microdados['renda'][microdados['renda']['CO_CURSO'].isin(cursos_filtrados) & microdados['renda']['ANO'].isin(anos_filtrados)]
        
        col_g1, col_g2 = st.columns(2, gap="large")
        with col_g1:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Distribuição de Idade</div>', unsafe_allow_html=True)
            if not df_idade.empty and 'NU_IDADE' in df_idade.columns:
                df_idade['NU_IDADE'] = pd.to_numeric(df_idade['NU_IDADE'], errors='coerce')
                df_idade = df_idade.dropna(subset=['NU_IDADE'])
                fig_idade = px.histogram(df_idade, x='NU_IDADE', nbins=15, color_discrete_sequence=['#32A041'], labels={'NU_IDADE': 'Faixa Etária (Anos)'})
                fig_idade.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
                fig_idade.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", yaxis_title="Qtd de Estudantes")
                st.plotly_chart(fig_idade, use_container_width=True)
        with col_g2:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Distribuição de Gênero</div>', unsafe_allow_html=True)
            if not df_sexo.empty and 'TP_SEXO' in df_sexo.columns:
                sexo_counts = df_sexo['TP_SEXO'].value_counts().reset_index()
                sexo_counts.columns = ['Gênero', 'Quantidade']
                sexo_counts['Gênero'] = sexo_counts['Gênero'].map({'F': 'Feminino', 'M': 'Masculino'}).fillna(sexo_counts['Gênero'])
                fig_sexo = px.pie(sexo_counts, values='Quantidade', names='Gênero', hole=0.4, color_discrete_map={'Feminino': '#d45070', 'Masculino': '#2d539e'})
                fig_sexo.update_traces(textposition='inside', textinfo='percent+label', marker={"line": {"color": "white", "width": 2}})
                fig_sexo.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", showlegend=False)
                st.plotly_chart(fig_sexo, use_container_width=True)

        col_g3, col_g4 = st.columns(2, gap="large")
        with col_g3:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Distribuição Cor/Raça</div>', unsafe_allow_html=True)
            dict_raca = {'A': 'Branca', 'B': 'Preta', 'C': 'Amarela', 'D': 'Parda', 'E': 'Indígena', 'F': 'Não declarado'}
            if not df_raca.empty and 'QE_I02' in df_raca.columns:
                raca_counts = df_raca['QE_I02'].map(dict_raca).value_counts().reset_index()
                raca_counts.columns = ['Cor/Raça', 'Quantidade']
                raca_counts = raca_counts.sort_values(by='Quantidade', ascending=True)
                fig_raca = px.bar(raca_counts, y='Cor/Raça', x='Quantidade', orientation='h', color_discrete_sequence=['#1a5722'])
                fig_raca.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
                fig_raca.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", xaxis_title="Estudantes")
                st.plotly_chart(fig_raca, use_container_width=True)
        with col_g4:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Perfil de Renda Familiar</div>', unsafe_allow_html=True)
            dict_renda = {'A': 'Até 1,5 SM', 'B': '1,5 a 3 SM', 'C': '3 a 4,5 SM', 'D': '4,5 a 6 SM', 'E': '6 a 10 SM', 'F': '10 a 30 SM', 'G': 'Acima 30 SM'}
            if not df_renda.empty and 'QE_I08' in df_renda.columns:
                renda_counts = df_renda['QE_I08'].map(dict_renda).value_counts().reset_index()
                renda_counts.columns = ['Renda', 'Quantidade']
                ordem_renda = ['Acima 30 SM', '10 a 30 SM', '6 a 10 SM', '4,5 a 6 SM', '3 a 4,5 SM', '1,5 a 3 SM', 'Até 1,5 SM']
                renda_counts['Renda'] = pd.Categorical(renda_counts['Renda'], categories=ordem_renda, ordered=True)
                renda_counts = renda_counts.sort_values('Renda')
                fig_renda = px.bar(renda_counts, y='Renda', x='Quantidade', orientation='h', color_discrete_sequence=['#32A041'])
                fig_renda.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
                fig_renda.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", xaxis_title="Estudantes")
                st.plotly_chart(fig_renda, use_container_width=True)

    with t2:
        df_pai = microdados['pai'][microdados['pai']['CO_CURSO'].isin(cursos_filtrados) & microdados['pai']['ANO'].isin(anos_filtrados)]
        df_mae = microdados['mae'][microdados['mae']['CO_CURSO'].isin(cursos_filtrados) & microdados['mae']['ANO'].isin(anos_filtrados)]
        df_trab = microdados['trab'][microdados['trab']['CO_CURSO'].isin(cursos_filtrados) & microdados['trab']['ANO'].isin(anos_filtrados)]

        col_s1, col_s2 = st.columns(2, gap="large")
        with col_s1:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Escolaridade Média dos Pais</div>', unsafe_allow_html=True)
            dict_escolaridade = {'A': 'Nenhuma', 'B': 'Ens. Fundamental I', 'C': 'Ens. Fundamental II', 'D': 'Ensino Médio', 'E': 'Ensino Superior', 'F': 'Pós-graduação'}
            if not df_pai.empty and not df_mae.empty:
                pai_c = df_pai['QE_I04'].map(dict_escolaridade).value_counts()
                mae_c = df_mae['QE_I05'].map(dict_escolaridade).value_counts()
                df_esc = pd.DataFrame({'Pai': pai_c, 'Mãe': mae_c}).fillna(0).reset_index()
                df_esc.columns = ['Nível', 'Pai', 'Mãe']
                ordem_esc = ['Nenhuma', 'Ens. Fundamental I', 'Ens. Fundamental II', 'Ensino Médio', 'Ensino Superior', 'Pós-graduação']
                df_esc['Nível'] = pd.Categorical(df_esc['Nível'], categories=ordem_esc, ordered=True)
                df_esc = df_esc.sort_values('Nível')
                melted = df_esc.melt(id_vars='Nível', value_vars=['Pai', 'Mãe'], var_name='Parente', value_name='Qtd')
                fig_esc = px.bar(melted, x='Qtd', y='Nível', color='Parente', barmode='group', orientation='h', color_discrete_sequence=['#1a5722', '#58c769'])
                fig_esc.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
                fig_esc.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", yaxis_title=None)
                st.plotly_chart(fig_esc, use_container_width=True)
        
        with col_s2:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Situação de Trabalho Atual</div>', unsafe_allow_html=True)
            dict_trab = {'A': 'Não trabalha', 'B': 'Trabalha eventualmente', 'C': 'Até 20h/semana', 'D': '21-39h/semana', 'E': '40h ou mais/semana'}
            if not df_trab.empty:
                trab_c = df_trab['QE_I10'].map(dict_trab).value_counts().reset_index()
                trab_c.columns = ['Situação', 'Quantidade']
                fig_trab = px.pie(trab_c, values='Quantidade', names='Situação', hole=0.5, color_discrete_sequence=px.colors.sequential.Teal)
                fig_trab.update_traces(textposition='inside', textinfo='percent+label', marker={"line": {"color": "white", "width": 2}})
                fig_trab.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", showlegend=False)
                st.plotly_chart(fig_trab, use_container_width=True)

    with t3:
        df_cota = microdados['cota'][microdados['cota']['CO_CURSO'].isin(cursos_filtrados) & microdados['cota']['ANO'].isin(anos_filtrados)]
        df_bolsa = microdados['bolsa'][microdados['bolsa']['CO_CURSO'].isin(cursos_filtrados) & microdados['bolsa']['ANO'].isin(anos_filtrados)]
        
        col_a1, col_a2 = st.columns(2, gap="large")
        with col_a1:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Admissão por Políticas Sociais (Cotas)</div>', unsafe_allow_html=True)
            dict_cota = {'A': 'Ampla Concorrência (Não)', 'B': 'Étnico-Racial', 'C': 'Critério de Renda', 'D': 'Escola Pública', 'E': 'Dois ou mais critérios', 'F': 'Outros'}
            if not df_cota.empty:
                cota_c = df_cota['QE_I15'].map(lambda x: dict_cota.get(x, 'Outros')).value_counts().reset_index()
                cota_c.columns = ['Critério', 'Total']
                fig_cota = px.bar(cota_c, x='Relevância', y='Critério', orientation='h', color='Total', color_continuous_scale='Greens')
                cota_c = cota_c.sort_values('Total', ascending=True)
                fig_cota = px.bar(cota_c, y='Critério', x='Total', orientation='h', color_discrete_sequence=['#32A041'])
                fig_cota.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
                fig_cota.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", yaxis_title=None)
                st.plotly_chart(fig_cota, use_container_width=True)
                
        with col_a2:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Bolsas e Auxílios Financeiros</div>', unsafe_allow_html=True)
            dict_bolsa = {'A': 'Nenhum', 'B': 'FIES', 'C': 'ProUni', 'D': 'Entidade Externa', 'E': 'Programa IFES', 'F': 'Outros'}
            if not df_bolsa.empty:
                bolsa_c = df_bolsa['QE_I11'].map(lambda x: dict_bolsa.get(x, 'Outros') if isinstance(x, str) else 'Outros').value_counts().reset_index()
                bolsa_c.columns = ['Tipo', 'Total']
                fig_bolsa = px.pie(bolsa_c, values='Total', names='Tipo', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_bolsa.update_traces(textposition='inside', textinfo='percent+label', marker={"line": {"color": "white", "width": 2}})
                fig_bolsa.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", showlegend=False)
                st.plotly_chart(fig_bolsa, use_container_width=True)

    with t4:
        df_estudo = microdados['estudo'][microdados['estudo']['CO_CURSO'].isin(cursos_filtrados) & microdados['estudo']['ANO'].isin(anos_filtrados)]
        df_motiv_c = microdados['motiv_c'][microdados['motiv_c']['CO_CURSO'].isin(cursos_filtrados) & microdados['motiv_c']['ANO'].isin(anos_filtrados)]
        df_motiv_i = microdados['motiv_i'][microdados['motiv_i']['CO_CURSO'].isin(cursos_filtrados) & microdados['motiv_i']['ANO'].isin(anos_filtrados)]

        col_r1, col_r2 = st.columns(2, gap="large")
        with col_r1:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Horas de Estudo (Extra-classe) por Semana</div>', unsafe_allow_html=True)
            dict_estudo = {'A': 'Nenhuma', 'B': '1 a 3 horas', 'C': '4 a 7 horas', 'D': '8 a 12 horas', 'E': 'Mais de 12 horas'}
            if not df_estudo.empty:
                estudo_c = df_estudo['QE_I23'].map(dict_estudo).value_counts().reset_index()
                estudo_c.columns = ['Horas', 'Qtd']
                ordem_e = [' Mais de 12 horas', '8 a 12 horas', '4 a 7 horas', '1 a 3 horas', 'Nenhuma']
                fig_est = px.bar(estudo_c, y='Horas', x='Qtd', orientation='h', color_discrete_sequence=['#ffca3a'])
                fig_est.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
                fig_est.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter")
                st.plotly_chart(fig_est, use_container_width=True)

        with col_r2:
            st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Motivação Principal de Escolha do Curso</div>', unsafe_allow_html=True)
            dict_motiv = {'A': 'Inserção no mercado', 'B': 'Influência familiar', 'C': 'Valorização Profissional', 'D': 'Contribuição Social', 'E': 'Vocação', 'F': 'Oferecido na cidade', 'G': 'Flexibilidade', 'H': 'Outro'}
            if not df_motiv_c.empty:
                m_c = df_motiv_c['QE_I25'].map(lambda x: dict_motiv.get(x, 'Outro')).value_counts().reset_index()
                m_c.columns = ['Motivo', 'Qtd']
                m_c = m_c.sort_values('Qtd', ascending=True)
                fig_m = px.bar(m_c, y='Motivo', x='Qtd', orientation='h', color_discrete_sequence=['#8ac926'])
                fig_m.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
                fig_m.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", yaxis_title=None)
                st.plotly_chart(fig_m, use_container_width=True)
                
# Keep evasao as is
"""

import re
# We need to replace everything from "def show_estudantes():" down to "def show_evasao():"
pattern = re.compile(r"def show_estudantes\(\):.*?def show_evasao\(\):", re.DOTALL)
content = pattern.sub(f"{show_estudantes_new}\ndef show_evasao():", content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied to app.py successfully!")
