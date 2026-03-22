import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Painel - ENADE", layout="wide", initial_sidebar_state="collapsed")

# 2. Premium Global CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');
    
    html, body, [class*="st-"], .stMarkdown { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #f2f9f4 0%, #ffffff 100%); }
    
    .home-inst-title { font-size: 2.8rem; font-weight: 900; color: #1a5722; margin-top: 1rem; line-height: 1.1; letter-spacing: -1.2px; }
    .home-inst-subtitle { font-size: 1.6rem; color: #32A041; margin-bottom: 1.5rem; font-weight: 600; letter-spacing: -0.5px; }
    
    .card-panel {
        background-color: rgba(255, 255, 255, 0.9); padding: 2.5rem; border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05), 0 8px 10px -6px rgba(0,0,0,0.01);
        border-top: 5px solid #32A041; backdrop-filter: blur(10px); height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card-panel:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04); }
    .card-panel-dark { border-top: 5px solid #1a5722; background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(245,252,246,1) 100%); }
    
    .home-info-title { font-size: 0.9rem; color: #777; text-transform: uppercase; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 0.2rem; }
    .home-info-name { font-size: 1.6rem; font-weight: 600; color: #111; margin-bottom: 1.8rem; }
    .indicadores-title { font-size: 1.8rem; font-weight: 800; color: #1a5722; margin-bottom: 1rem; letter-spacing: -0.5px; }
    
    .main-title { text-align: center; background: linear-gradient(to right, #1a5722, #32A041); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 4rem; margin-bottom: 5px; letter-spacing: -2px; }
    .filter-header { font-size: 0.85rem; color: #1a5722; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; border-bottom: 2px solid rgba(50,160,65,0.2); padding-bottom: 4px; letter-spacing: 0.5px; }
    
    .stButton>button { border-radius: 10px; font-weight: 800; padding: 0.6rem 1.2rem; transition: all 0.3s cubic-bezier(0.4,0,0.2,1); box-shadow: 0 4px 6px -1px rgba(50,160,65,0.2); letter-spacing: 0.5px; }
    .stButton>button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 15px -3px rgba(50,160,65,0.3); }
    
    .custom-divider { border: 0; height: 1px; background: linear-gradient(to right, rgba(50,160,65,0.0), rgba(50,160,65,0.4), rgba(50,160,65,0.0)); margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data
def load_data():
    files = ['Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']
    all_dfs = []
    
    for file in files:
        df_enade = pd.read_excel(file, sheet_name='Enade')
        df_cursos = pd.read_excel(file, sheet_name='Cursos')
        
        col_inscritos = next((c for c in df_enade.columns if 'Inscrito' in str(c)), None)
        col_participantes = next((c for c in df_enade.columns if 'Participante' in str(c)), None)
        col_nota_fg = next((c for c in df_enade.columns if 'Bruta' in str(c) and 'FG' in str(c)), None)
        col_nota_ce = next((c for c in df_enade.columns if 'Bruta' in str(c) and 'CE' in str(c)), None)
        
        df_merged = pd.merge(df_enade, df_cursos[['CO_CURSO', 'CAMPUS']], left_on='Código do Curso', right_on='CO_CURSO', how='left')
        
        rename_dict = {
            'Área de Avaliação': 'NOME DO CURSO', 'CAMPUS': 'CENTRO',
            'Município do Curso': 'MUNICÍPIO', 'Município do Curso**': 'MUNICÍPIO',
            'Ano': 'ANO', 'Conceito Enade (Contínuo)': 'ENADE CONTÍNUO',
            'Conceito Enade (Faixa)': 'ENADE FAIXA', 'Modalidade de Ensino': 'MODALIDADE',
            'Categoria Administrativa': 'CATEGORIA', 'Grau Acadêmico': 'PROGRAMA'
        }
        
        if col_inscritos: rename_dict[col_inscritos] = 'INSCRITOS'
        if col_participantes: rename_dict[col_participantes] = 'PRESENTES'
        if col_nota_fg: rename_dict[col_nota_fg] = 'NOTA_FG'
        if col_nota_ce: rename_dict[col_nota_ce] = 'NOTA_CE'
            
        df_final = df_merged.rename(columns=rename_dict)
        cols_to_keep = ['NOME DO CURSO', 'CENTRO', 'MUNICÍPIO', 'ANO', 'ENADE CONTÍNUO', 'ENADE FAIXA', 'MODALIDADE', 'INSCRITOS', 'PRESENTES', 'NOTA_FG', 'NOTA_CE', 'CO_CURSO']
        cols_to_keep = [c for c in cols_to_keep if c in df_final.columns]
        all_dfs.append(df_final[cols_to_keep])
        
    final_combined = pd.concat(all_dfs, ignore_index=True)
    if pd.api.types.is_numeric_dtype(final_combined['ENADE CONTÍNUO']):
        final_combined['ENADE CONTÍNUO'] = final_combined['ENADE CONTÍNUO'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else str(x))
    return final_combined

@st.cache_data
def load_microdata():
    files = ['Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']
    all_sexo = []
    all_idade = []
    
    for file in files:
        try:
            df_cursos = pd.read_excel(file, sheet_name='Cursos')
            df_enade = pd.read_excel(file, sheet_name='Enade')
            df_sexo_raw = pd.read_excel(file, sheet_name='Arq_5')
            df_idade_raw = pd.read_excel(file, sheet_name='Arq_6')
            
            # Map CO_CURSO to their actual Names and Campus
            curso_map = pd.merge(df_cursos[['CO_CURSO', 'CAMPUS']], df_enade[['Código do Curso', 'Área de Avaliação', 'Ano']], left_on='CO_CURSO', right_on='Código do Curso', how='inner')
            curso_map = curso_map.rename(columns={'Área de Avaliação': 'NOME DO CURSO', 'CAMPUS': 'CENTRO', 'Ano': 'ANO'})
            
            df_sexo = pd.merge(df_sexo_raw, curso_map, on='CO_CURSO', how='inner')
            if not df_sexo.empty: all_sexo.append(df_sexo)
                
            df_idade = pd.merge(df_idade_raw, curso_map, on='CO_CURSO', how='inner')
            if not df_idade.empty: all_idade.append(df_idade)
                
        except Exception as e:
            continue
            
    df_sexo_final = pd.concat(all_sexo, ignore_index=True) if all_sexo else pd.DataFrame()
    df_idade_final = pd.concat(all_idade, ignore_index=True) if all_idade else pd.DataFrame()
    return df_sexo_final, df_idade_final

try:
    data = load_data()
    df_sexo_global, df_idade_global = load_microdata()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

def get_options(df, column):
    options = df[column].dropna().unique().tolist()
    options.sort()
    return ['Todos'] + [str(opt) for opt in options]

# --- Helper de Filtros Global ---
def render_filters(source_data):
    st.markdown('<div style="margin-top: 2rem; margin-bottom: 1rem;"><span style="background: #32A041; color: white; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.85rem; letter-spacing: 1px;">⚙️ FILTROS DE PESQUISA</span></div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="filter-header">Centro</div>', unsafe_allow_html=True)
        centro_options = get_options(source_data, 'CENTRO')
        selected_centro = st.multiselect("Selecione os Centros", centro_options[1:], placeholder="Todos", label_visibility="collapsed", key='filtro_centro')
        
    with col_b:
        st.markdown('<div class="filter-header">Ano Base</div>', unsafe_allow_html=True)
        selected_ano = st.selectbox("Selecione o Ano", get_options(source_data, 'ANO'), label_visibility="collapsed", key='filtro_ano')
        
    with col_c:
        st.markdown('<div class="filter-header">Nota Faixa</div>', unsafe_allow_html=True)
        enade_options = get_options(source_data, 'ENADE FAIXA')
        selected_nota = st.multiselect("Selecione a Nota", enade_options[1:], placeholder="Todas", label_visibility="collapsed", key='filtro_nota')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="filter-header">Curso</div>', unsafe_allow_html=True)
        selected_curso = st.selectbox("Selecione o Curso", get_options(source_data, 'NOME DO CURSO'), label_visibility="collapsed", key='filtro_curso')

    with col2:
        st.markdown('<div class="filter-header">Modalidade</div>', unsafe_allow_html=True)
        selected_modalidade = st.selectbox("Selecione a Modalidade", get_options(source_data, 'MODALIDADE'), label_visibility="collapsed", key='filtro_mod')

    filtered_data = source_data.copy()

    if selected_centro:
        filtered_data = filtered_data[filtered_data['CENTRO'].isin(selected_centro)]
    if selected_ano != 'Todos':
        if str(filtered_data['ANO'].dtype) == 'object':
            filtered_data = filtered_data[filtered_data['ANO'] == selected_ano]
        else:
            try: filtered_data = filtered_data[filtered_data['ANO'] == float(selected_ano)]
            except: pass
    if selected_nota:
        filtered_data = filtered_data[filtered_data['ENADE FAIXA'].astype(str).isin(selected_nota)]
    if selected_curso != 'Todos':
        filtered_data = filtered_data[filtered_data['NOME DO CURSO'] == selected_curso]
    if selected_modalidade != 'Todos':
        filtered_data = filtered_data[filtered_data['MODALIDADE'] == selected_modalidade]

    return filtered_data


# --- TELAS PRINCIPAIS ---

def show_home():
    col_text, col_img = st.columns([3, 1], gap="large")
    with col_text:
        st.markdown('<div class="home-inst-title">INSTITUTO FEDERAL DO ESPÍRITO SANTO - IFES</div>', unsafe_allow_html=True)
    with col_img:
        st.image('ifes-horizontal-cor.png', use_container_width=True)
        
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1], gap="large")
    with col_left:
        st.markdown("""
        <div class="card-panel">
            <p class="home-info-title">Orientador</p>
            <p class="home-info-name">Wagner Teixeira da Costa</p>
            <p class="home-info-title">Aluno</p>
            <p class="home-info-name" style="margin-bottom: 0;">Matheus Ferreira Tissianel Benincá</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div class="card-panel card-panel-dark">
            <div class="indicadores-title">Plataformas Analíticas</div>
            <p style="color: #555; font-size: 1.05rem; line-height: 1.5; margin-bottom: 1rem;">
                Acesse abaixo os módulos isolados de métricas institucionais, desempenho padronizado e a nova base de microdados demográficos coletados do INEP.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            if st.button("🚀 NOTAS ENADE", use_container_width=True, type="primary"):
                st.session_state.page = 'dashboard'
                st.rerun()
        with col_b2:
            if st.button("👥 DADOS DOS CURSOS", use_container_width=True):
                st.session_state.page = 'cursos'
                st.rerun()
        with col_b3:
            if st.button("🎓 INFORMAÇÕES DO ESTUDANTE", use_container_width=True):
                st.session_state.page = 'estudantes'
                st.rerun()

def show_dashboard():
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True, key='back_bt_dash'):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
            <p style="color: #32A041; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;">Avaliação Institucional</p>
            <h1 class="main-title">NOTAS ENADE</h1>
            <p style="color: #666; font-size: 1.15rem; margin: 0 auto; font-weight: 400; max-width: 600px;">
                Cruzamento de dados contínuos e métricas de desempenho dos estudantes do <span style="color:#1a5722; font-weight:600;">IFES</span>
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider" style="margin: 20px 0;">', unsafe_allow_html=True)

    filtered_data = render_filters(data)

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(filtered_data[['NOME DO CURSO', 'CENTRO', 'MUNICÍPIO', 'ANO', 'ENADE CONTÍNUO', 'ENADE FAIXA']], width='stretch', hide_index=True, height=500)

def show_cursos():
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True, key='back_bt_cursos'):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
            <p style="color: #32A041; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;">Análise de Provas e Evasão</p>
            <h1 class="main-title" style="font-size: 3rem;">DADOS DOS CURSOS</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider" style="margin: 20px 0;">', unsafe_allow_html=True)

    filtered_data = render_filters(data)
    st.markdown("<br>", unsafe_allow_html=True)
    
    df_calc = filtered_data.copy()
    
    st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem; margin-top: 1rem;">Raio-X da Prova: Formação Geral vs Específica</div>', unsafe_allow_html=True)
    if 'NOTA_FG' in df_calc.columns and 'NOTA_CE' in df_calc.columns:
        df_calc['NOTA_FG'] = pd.to_numeric(df_calc['NOTA_FG'].astype(str).str.replace(',', '.'), errors='coerce')
        df_calc['NOTA_CE'] = pd.to_numeric(df_calc['NOTA_CE'].astype(str).str.replace(',', '.'), errors='coerce')
        avg_scores = df_calc.groupby('NOME DO CURSO')[['NOTA_FG', 'NOTA_CE']].mean().reset_index().dropna()
        if not avg_scores.empty:
            melted = avg_scores.melt(id_vars='NOME DO CURSO', value_vars=['NOTA_FG', 'NOTA_CE'], var_name='Tipo de Prova', value_name='Nota Média')
            fig1 = px.bar(melted, x='NOME DO CURSO', y='Nota Média', color='Tipo de Prova', barmode='group', color_discrete_sequence=['#1a5722', '#58c769'])
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Inter")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Sem dados de notas isoladas suficientes no filtro.")
            
    st.markdown("<br><hr class='custom-divider'><br>", unsafe_allow_html=True)
    st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem;">Taxa de Abstenção por Campus (Evasão no Exame)</div>', unsafe_allow_html=True)
    if 'INSCRITOS' in df_calc.columns and 'PRESENTES' in df_calc.columns:
        df_calc['INSCRITOS'] = pd.to_numeric(df_calc['INSCRITOS'], errors='coerce')
        df_calc['PRESENTES'] = pd.to_numeric(df_calc['PRESENTES'], errors='coerce')
        abs_data = df_calc.groupby('CENTRO').agg({'INSCRITOS':'sum', 'PRESENTES':'sum'}).reset_index()
        abs_data = abs_data[abs_data['INSCRITOS'] > 0]
        try: abs_data['Taxa de Abstenção (%)'] = ((1 - abs_data['PRESENTES'] / abs_data['INSCRITOS']) * 100).round(1)
        except: pass
        abs_data = abs_data.dropna()
        if not abs_data.empty:
            abs_data = abs_data.sort_values('Taxa de Abstenção (%)', ascending=False)
            fig2 = px.bar(abs_data, x='CENTRO', y='Taxa de Abstenção (%)', color='Taxa de Abstenção (%)', color_continuous_scale='Reds', text='Taxa de Abstenção (%)')
            fig2.update_traces(texttemplate='%{text}%', textposition='outside')
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Inter", coloraxis_showscale=False)
            fig2.update_yaxes(range=[0, max(abs_data['Taxa de Abstenção (%)']) * 1.25])
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Sem dados de abstenção suficientes no filtro.")

def show_estudantes():
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True, key='back_bt_estd'):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
            <p style="color: #32A041; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;">Microdados Sociodemográficos INEP</p>
            <h1 class="main-title" style="font-size: 3rem;">INFORMAÇÕES DO ESTUDANTE</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider" style="margin: 20px 0;">', unsafe_allow_html=True)

    # 1. Obter o dataframe base das aplicacoes de filtros e descobrir o escopo
    filtered_data = render_filters(data)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Extrair os identificadores dos cursos exatos que restaram no filtro
    cursos_filtrados = filtered_data['CO_CURSO'].unique().tolist()
    anos_filtrados = filtered_data['ANO'].unique().tolist()
    
    if df_sexo_global.empty or df_idade_global.empty:
        st.warning("Aviso: Falha ao cruzar as abas ocultas `Arq_5` e `Arq_6` dos microdados do INEP nas planilhas de base.")
        st.stop()
        
    # Aplicar o espelhamento de Filtros nos Dataframes de Microdados usando Chave Estrangeira CO_CURSO
    df_sexo = df_sexo_global[(df_sexo_global['CO_CURSO'].isin(cursos_filtrados)) & (df_sexo_global['ANO'].isin(anos_filtrados))]
    df_idade = df_idade_global[(df_idade_global['CO_CURSO'].isin(cursos_filtrados)) & (df_idade_global['ANO'].isin(anos_filtrados))]

    col_g1, col_g2 = st.columns(2, gap="large")
    
    with col_g1:
        st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Distribuição de Idade dos Estudantes</div>', unsafe_allow_html=True)
        if not df_idade.empty and 'NU_IDADE' in df_idade.columns:
            df_idade['NU_IDADE'] = pd.to_numeric(df_idade['NU_IDADE'], errors='coerce')
            df_idade = df_idade.dropna(subset=['NU_IDADE'])
            
            fig_idade = px.histogram(df_idade, x='NU_IDADE', nbins=15, 
                                   color_discrete_sequence=['#32A041'],
                                   labels={'NU_IDADE': 'Faixa Etária (Anos)'})
            fig_idade.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Inter",
                                    yaxis_title="Qtd de Estudantes")
            st.plotly_chart(fig_idade, use_container_width=True)
            
            # Sub-dados rápidos
            media = df_idade['NU_IDADE'].mean()
            if pd.notna(media):
                st.markdown(f"<div style='text-align:center; color:#555;'>Média de Idade: <b>{media:.1f} anos</b></div>", unsafe_allow_html=True)
        else:
            st.info("Sem dados etários nesse filtro.")
            
    with col_g2:
        st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.3rem;">Distribuição de Gênero Declarado</div>', unsafe_allow_html=True)
        if not df_sexo.empty and 'TP_SEXO' in df_sexo.columns:
            # Aggregate to create Pie Chart
            sexo_counts = df_sexo['TP_SEXO'].value_counts().reset_index()
            sexo_counts.columns = ['Gênero', 'Quantidade']
            # Mapear para PT-BR
            sexo_counts['Gênero'] = sexo_counts['Gênero'].map({'F': 'Feminino', 'M': 'Masculino'}).fillna(sexo_counts['Gênero'])
            
            fig_sexo = px.pie(sexo_counts, values='Quantidade', names='Gênero', hole=0.4,
                              color='Gênero', color_discrete_map={'Feminino': '#d45070', 'Masculino': '#2d539e'})
            fig_sexo.update_traces(textposition='inside', textinfo='percent+label')
            fig_sexo.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Inter", showlegend=False)
            st.plotly_chart(fig_sexo, use_container_width=True)
        else:
            st.info("Sem dados demográficos de sexo nesse filtro.")


# --- ROUTER (GERENCIADOR DE ESTADO) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'dashboard':
    show_dashboard()
elif st.session_state.page == 'cursos':  # Corrigido label routing
    show_cursos()
elif st.session_state.page == 'estudantes':
    show_estudantes()
