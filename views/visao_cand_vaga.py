import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_visao_cand_vaga():
    # Back button
    if st.button("⬅️ Voltar ao Início"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<div class="home-inst-title">Análise de Candidato x Vaga</div>', unsafe_allow_html=True)
    st.markdown('<div class="home-inst-subtitle">Processo Seletivo - IFES</div>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Load Data
    @st.cache_data
    def load_cv_data():
        file_path = r'c:\Users\mathe\OneDrive\Área de Trabalho\CV\Cand_Vaga_Unico.xlsx'
        df = pd.read_excel(file_path)
        # Ensure Semestre is a string and clean it if it's a timestamp
        if pd.api.types.is_datetime64_any_dtype(df['Semestre']):
            df['Semestre'] = df['Semestre'].dt.strftime('%Y-%m')
        return df

    try:
        df = load_cv_data()
    except Exception as e:
        st.error(f"Erro ao carregar os dados de Candidato x Vaga: {e}")
        return

    # Filters Section
    st.markdown('<div class="fade-in" style="margin-top: 1rem; margin-bottom: 1rem;"><span style="background: linear-gradient(135deg, #103d6d, #205c9e); color: white; padding: 6px 16px; border-radius: 20px; font-weight: 800; font-size: 0.85rem; letter-spacing: 1px; box-shadow: 0 4px 10px rgba(16,61,109,0.3);">⚙️ FILTROS DE PESQUISA</span></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    with col1:
        st.markdown('<div class="filter-header">Semestre</div>', unsafe_allow_html=True)
        semestres = sorted(df['Semestre'].unique().tolist(), reverse=True)
        sel_semestre = st.multiselect("Filtrar por Semestre", semestres, placeholder="Todos", label_visibility="collapsed")

    with col2:
        st.markdown('<div class="filter-header">Campus</div>', unsafe_allow_html=True)
        campi = sorted(df['Campus'].unique().tolist())
        sel_campus = st.multiselect("Filtrar por Campus", campi, placeholder="Todos", label_visibility="collapsed")

    with col3:
        st.markdown('<div class="filter-header">Modalidade</div>', unsafe_allow_html=True)
        modalidades = sorted(df['Modalidade'].unique().tolist())
        sel_modalidade = st.multiselect("Filtrar por Modalidade", modalidades, placeholder="Todos", label_visibility="collapsed")

    with col4:
        st.markdown('<div class="filter-header">Turno</div>', unsafe_allow_html=True)
        turnos = sorted(df['Turno'].unique().tolist())
        sel_turno = st.multiselect("Filtrar por Turno", turnos, placeholder="Todos", label_visibility="collapsed")

    with col5:
        st.markdown('<div class="filter-header">Curso</div>', unsafe_allow_html=True)
        cursos = sorted(df['Curso'].unique().tolist())
        sel_curso = st.multiselect("Filtrar por Curso", cursos, placeholder="Todos", label_visibility="collapsed")

    # Apply Filters
    df_filtered = df.copy()
    if sel_semestre:
        df_filtered = df_filtered[df_filtered['Semestre'].isin(sel_semestre)]
    if sel_campus:
        df_filtered = df_filtered[df_filtered['Campus'].isin(sel_campus)]
    if sel_modalidade:
        df_filtered = df_filtered[df_filtered['Modalidade'].isin(sel_modalidade)]
    if sel_turno:
        df_filtered = df_filtered[df_filtered['Turno'].isin(sel_turno)]
    if sel_curso:
        df_filtered = df_filtered[df_filtered['Curso'].isin(sel_curso)]

    if df_filtered.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # KPIs
    total_inscritos = df_filtered['Inscritos'].sum()
    total_vagas = df_filtered['Vagas'].sum()
    media_cand_vaga = df_filtered['Inscritos'].sum() / df_filtered['Vagas'].sum() if total_vagas > 0 else 0

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f'''<div class="kpi-card">
            <p class="kpi-title">Total de Inscritos</p>
            <p class="kpi-value">{int(total_inscritos):,}</p>
        </div>'''.replace(',', '.'), unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f'''<div class="kpi-card" style="border-left-color: #2c8c44;">
            <p class="kpi-title">Total de Vagas</p>
            <p class="kpi-value">{int(total_vagas):,}</p>
        </div>'''.replace(',', '.'), unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f'''<div class="kpi-card" style="border-left-color: #f39c12;">
            <p class="kpi-title">Média Cand/Vaga</p>
            <p class="kpi-value">{media_cand_vaga:.2f}</p>
        </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.markdown('<div class="indicadores-title" style="font-size: 1.2rem;">Top 15 Cursos por Concorrência (Cand x Vaga)</div>', unsafe_allow_html=True)
        # Group by Curso to handle cases where same curso is in multiple campuses/semesters
        df_top = df_filtered.groupby('Curso').agg({'Inscritos': 'sum', 'Vagas': 'sum'}).reset_index()
        df_top['Concorrência'] = df_top['Inscritos'] / df_top['Vagas']
        df_top = df_top.sort_values('Concorrência', ascending=False).head(15)
        
        fig_bar = px.bar(
            df_top, 
            x='Concorrência', 
            y='Curso', 
            orientation='h',
            text='Concorrência',
            color='Concorrência',
            color_continuous_scale='Viridis',
            labels={'Concorrência': 'Candidatos por Vaga'}
        )
        fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_bar.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            margin=dict(l=20, r=20, t=20, b=20),
            height=500,
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.markdown('<div class="indicadores-title" style="font-size: 1.2rem;">Distribuição por Modalidade</div>', unsafe_allow_html=True)
        df_mod = df_filtered.groupby('Modalidade')['Inscritos'].sum().reset_index()
        fig_pie = px.pie(
            df_mod, 
            values='Inscritos', 
            names='Modalidade', 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=500)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.markdown('<div class="indicadores-title" style="font-size: 1.2rem;">Inscritos vs Vagas por Campus</div>', unsafe_allow_html=True)
        df_campus = df_filtered.groupby('Campus').agg({'Inscritos': 'sum', 'Vagas': 'sum'}).reset_index()
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name='Inscritos', x=df_campus['Campus'], y=df_campus['Inscritos'], marker_color='#103d6d'))
        fig_comp.add_trace(go.Bar(name='Vagas', x=df_campus['Campus'], y=df_campus['Vagas'], marker_color='#2c8c44'))
        fig_comp.update_layout(barmode='group', margin=dict(l=20, r=20, t=20, b=20), height=400)
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_chart4:
        st.markdown('<div class="indicadores-title" style="font-size: 1.2rem;">Evolução da Concorrência por Semestre</div>', unsafe_allow_html=True)
        df_ev = df_filtered.groupby('Semestre').agg({'Inscritos': 'sum', 'Vagas': 'sum'}).reset_index()
        df_ev['Concorrência'] = df_ev['Inscritos'] / df_ev['Vagas']
        df_ev = df_ev.sort_values('Semestre')
        
        fig_line = px.line(
            df_ev, 
            x='Semestre', 
            y='Concorrência', 
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#103d6d']
        )
        fig_line.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=400)
        st.plotly_chart(fig_line, use_container_width=True)

    # Detailed Table
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Ver Tabela de Dados Detalhada", expanded=False):
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
