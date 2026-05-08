import streamlit as st
import pandas as pd
import plotly.express as px

def render_visao_2019(data, microdados, render_filters):
    ano = '2019'
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button('⬅ Voltar ao Início', use_container_width=True, key='back_bt_visao_2019'):
            st.session_state.page = 'home'
            st.rerun()

    with st.container():    
        st.markdown(f'''
            <div class="fade-in" style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
                <p style="color: #32A041; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;">Painel Analítico</p>
                <h1 style="font-size: 3rem; font-weight: 900; color: #103d6d;">ENADE {ano}</h1>
            </div>
        ''', unsafe_allow_html=True)

    # Renderiza os filtros fixando o ano
    filtered_data = render_filters(data, ano_fixo=ano)
    
    # KPIs de Participação (Inscritos, Presentes, Faltantes)
    inscritos = filtered_data['INSCRITOS'].sum()
    participantes = filtered_data['PRESENTES'].sum()
    faltantes = inscritos - participantes
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f'''<div class="kpi-card"><p class="kpi-title">Inscritos</p><p class="kpi-value">{int(inscritos)}</p></div>''', unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f'''<div class="kpi-card"><p class="kpi-title">Fizeram a Prova</p><p class="kpi-value">{int(participantes)}</p></div>''', unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f'''<div class="kpi-card" style="border-left-color: #d9534f;"><p class="kpi-title">Faltaram</p><p class="kpi-value" style="color: #d9534f;">{int(faltantes)}</p></div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    t_notas, t_cursos, t_estudantes, t_quest = st.tabs(["🚀 NOTAS", "👥 CURSOS", "🎓 ESTUDANTE", "📝 QUEST. ESTUDANTE"])
    
    with t_notas:
        st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem; margin-top: 1rem;">Avaliação Institucional</div>', unsafe_allow_html=True)
        st.dataframe(filtered_data[['NOME DO CURSO', 'CAMPUS', 'MUNICÍPIO', 'ANO', 'ENADE CONTÍNUO', 'ENADE FAIXA']], width='stretch', hide_index=True, height=500)
        
    with t_cursos:
        st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem; margin-top: 1rem;">Raio-X da Prova: Formação Geral vs Específica</div>', unsafe_allow_html=True)
        df_calc = filtered_data.copy()
        if 'NOTA_FG' in df_calc.columns and 'NOTA_CE' in df_calc.columns:
            df_calc['NOTA_FG'] = pd.to_numeric(df_calc['NOTA_FG'].astype(str).str.replace(',', '.'), errors='coerce')
            df_calc['NOTA_CE'] = pd.to_numeric(df_calc['NOTA_CE'].astype(str).str.replace(',', '.'), errors='coerce')
            avg_scores = df_calc.groupby('NOME DO CURSO')[['NOTA_FG', 'NOTA_CE']].mean().reset_index().dropna()
            if not avg_scores.empty:
                import plotly.express as px
                melted = avg_scores.melt(id_vars='NOME DO CURSO', value_vars=['NOTA_FG', 'NOTA_CE'], var_name='Tipo de Prova', value_name='Nota Média')
                fig1 = px.bar(melted, x='NOME DO CURSO', y='Nota Média', color='Tipo de Prova', barmode='group', color_discrete_sequence=['#1a5722', '#58c769'])
                fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter")
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Sem dados de notas isoladas suficientes no filtro.")
                
    with t_estudantes:
        st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem; margin-top: 1rem;">Microdados Sociodemográficos INEP</div>', unsafe_allow_html=True)
        
        cursos_filtrados = filtered_data['CO_CURSO'].unique().tolist()
        anos_filtrados = filtered_data['ANO'].unique().tolist()
        
        # Como o Streamlit não permite st.tabs aninhados, usaremos st.radio horizontal
        sub_tab = st.radio(
            "Selecione a categoria de dados:",
            ["📊 Demografia Básica", "💼 Perfil Socioeconômico", "🏛️ Acesso e Permanência", "📚 Rotina de Estudos"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        import plotly.express as px
        
        if sub_tab == "📊 Demografia Básica":
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

        elif sub_tab == "💼 Perfil Socioeconômico":
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

        elif sub_tab == "🏛️ Acesso e Permanência":
            df_cota = microdados['cota'][microdados['cota']['CO_CURSO'].isin(cursos_filtrados) & microdados['cota']['ANO'].isin(anos_filtrados)]
            df_bolsa = microdados['bolsa'][microdados['bolsa']['CO_CURSO'].isin(cursos_filtrados) & microdados['bolsa']['ANO'].isin(anos_filtrados)]
            
            col_a1, col_a2 = st.columns(2, gap="large")
            with col_a1:
                st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Admissão por Políticas Sociais (Cotas)</div>', unsafe_allow_html=True)
                dict_cota = {'A': 'Ampla Concorrência (Não)', 'B': 'Étnico-Racial', 'C': 'Critério de Renda', 'D': 'Escola Pública', 'E': 'Dois ou mais critérios', 'F': 'Outros'}
                if not df_cota.empty:
                    cota_c = df_cota['QE_I15'].map(lambda x: dict_cota.get(x, 'Outros')).value_counts().reset_index()
                    cota_c.columns = ['Critério', 'Total']
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

        elif sub_tab == "📚 Rotina de Estudos":
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

    with t_quest:
        st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem; margin-top: 1rem;">Avaliação do Processo Formativo</div>', unsafe_allow_html=True)
        
        cursos_filtrados = filtered_data['CO_CURSO'].unique().tolist()
        anos_filtrados = filtered_data['ANO'].unique().tolist()
        
        df_arq4 = microdados.get('arq4', pd.DataFrame())
        df_arq43 = microdados.get('arq43', pd.DataFrame())
        
        if df_arq4.empty and df_arq43.empty:
            st.warning("Sem dados pré-processados de Arq_4 ou Arq_43 disponíveis.")
        else:
            df_arq4 = df_arq4[(df_arq4['CO_CURSO'].isin(cursos_filtrados)) & (df_arq4['ANO'].isin(anos_filtrados))]
            df_arq43 = df_arq43[(df_arq43['CO_CURSO'].isin(cursos_filtrados)) & (df_arq43['ANO'].isin(anos_filtrados))]
            
            if df_arq4.empty and df_arq43.empty:
                st.info("Nenhum dado do questionário disponível neste filtro.")
            else:
                try:
                    from qe_dictionary import qe_dict as dict_questoes
                except ImportError:
                    dict_questoes = {}

                qe_cols = []
                if not df_arq4.empty:
                    qe_cols.extend([str(c) for c in df_arq4.columns.tolist() if str(c).startswith('QE_I') and not df_arq4[c].dropna().empty])
                if not df_arq43.empty:
                    qe_cols.extend([str(c) for c in df_arq43.columns.tolist() if str(c).startswith('QE_I') and not df_arq43[c].dropna().empty])
                
                qe_cols = list(set(qe_cols))
                qe_cols.sort()
                
                opcoes = []
                for c in qe_cols:
                    texto = dict_questoes.get(c, f"Questão {c.replace('QE_I', '')} (Sem enunciado cadastrado)")
                    opcoes.append(f"{c} - {texto}")
                    
                selecionada = st.selectbox("Selecione a pergunta para visualizar o detalhamento:", opcoes)
                col_var = selecionada.split(" - ")[0]
                
                inscritos = filtered_data['INSCRITOS'].sum()
                participantes = filtered_data['PRESENTES'].sum()

                col_q1, col_kpi = st.columns([3, 1], gap="large")
                
                with col_q1:
                    texto_selecionada = selecionada.split(" - ", 1)[1]
                    st.markdown(f'''
                    <div style="background-color: white; border-radius: 16px; padding: 25px; box-shadow: 0 8px 24px rgba(0,0,0,0.04); margin-bottom: 25px; border: 1px solid rgba(0,0,0,0.03);">
                        <div class="filter-header" style="color: #103d6d; font-size: 1.1rem; border-bottom: 2px solid rgba(16,61,109,0.1); padding-bottom: 10px; margin-bottom: 15px;">ENUNCIADO DA QUESTÃO:</div>
                        <div style="color: #111; font-size: 1.4rem; font-weight: 600; line-height: 1.5;">{texto_selecionada}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    dict_likert = {
                        1: 'DISCORDO TOTALMENTE',
                        2: 'DISCORDO',
                        3: 'DISCORDO PARCIALMENTE',
                        4: 'CONCORDO PARCIALMENTE',
                        5: 'CONCORDO',
                        6: 'CONCORDO TOTALMENTE',
                        7: 'NÃO SEI RESPONDER',
                        8: 'NÃO SE APLICA',
                        9: 'NÃO RESPONDEU'
                    }
                    
                    if col_var in df_arq4.columns and not df_arq4.empty and not df_arq4[col_var].dropna().empty:
                        df_target = df_arq4.copy()
                    elif col_var in df_arq43.columns and not df_arq43.empty and not df_arq43[col_var].dropna().empty:
                        df_target = df_arq43.copy()
                    else:
                        df_target = pd.DataFrame(columns=[col_var])
                        
                    df_target[col_var] = pd.to_numeric(df_target[col_var], errors='coerce').fillna(9)
                    df_resp = df_target[df_target[col_var].isin([1, 2, 3, 4, 5, 6, 7, 8, 9])].copy()
                    
                    if df_resp.empty:
                        st.info("Sem dados disponíveis para este filtro.")
                    else:
                        contagem = df_resp[col_var].value_counts().reset_index()
                        contagem.columns = ['Resposta', 'Quantidade']
                        
                        opcoes_exibir = [1, 2, 3, 4, 5, 6, 9]
                        for opc in [7, 8]:
                            if opc in contagem['Resposta'].values and contagem[contagem['Resposta'] == opc]['Quantidade'].iloc[0] > 0:
                                opcoes_exibir.append(opc)
                        opcoes_exibir.sort()
                        
                        para_plot = pd.DataFrame({'Resposta': opcoes_exibir, 'Resposta_Texto': [dict_likert[i] for i in opcoes_exibir]})
                        para_plot = pd.merge(para_plot, contagem[['Resposta', 'Quantidade']], on='Resposta', how='left').fillna(0)
                        
                        total_alunos = len(df_target)
                        para_plot['Percentual'] = (para_plot['Quantidade'] / total_alunos) * 100 if total_alunos > 0 else 0
                        para_plot['Texto_Eixo'] = para_plot['Resposta_Texto']
                        para_plot['Rotulo'] = para_plot.apply(lambda row: f"<b>{row['Percentual']:.0f}%</b><br><span style='font-size:11px'>({int(row['Quantidade'])})</span>", axis=1)
                        
                        import plotly.express as px
                        fig = px.bar(para_plot, x='Texto_Eixo', y='Percentual', text='Rotulo')
                        fig.update_traces(
                            marker_color='#103d6d',
                            textposition='outside',
                            textfont_size=13,
                            textfont_color='#103d6d',
                            hovertemplate="<b>%{x}</b><br>Quantidade: %{customdata[0]}<br>Percentual: %{y:.1f}%<extra></extra>",
                            customdata=para_plot[['Quantidade']]
                        )
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_family="Inter",
                            yaxis_title=None,
                            xaxis_title=None,
                            showlegend=False,
                            margin=dict(t=30, b=100, l=0, r=0),
                            height=500
                        )
                        fig.update_yaxes(showticklabels=False, range=[0, max(para_plot['Percentual'] + 10)], showgrid=False)
                        fig.update_xaxes(tickfont=dict(size=11, color='#103d6d', weight='bold'), tickangle=-90, automargin=True)
                        st.plotly_chart(fig, use_container_width=True)
                        
                # Removido col_kpi lateral para dar mais espaço ao gráfico no mobile
                pass
