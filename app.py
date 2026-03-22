import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Painel - ENADE", layout="wide", initial_sidebar_state="collapsed")

# 2. Premium Global CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');
    
    /* Font enforcement */
    html, body, [class*="st-"], .stMarkdown {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* App background subtle gradient */
    .stApp {
        background: linear-gradient(135deg, #f2f9f4 0%, #ffffff 100%);
    }
    
    /* Home Page Typography */
    .home-inst-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #1a5722;
        margin-top: 1rem;
        line-height: 1.1;
        letter-spacing: -1.2px;
    }
    .home-inst-subtitle {
        font-size: 1.6rem;
        color: #32A041;
        margin-bottom: 1.5rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Glassmorphism Cards */
    .card-panel {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        border-top: 5px solid #32A041;
        backdrop-filter: blur(10px);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card-panel:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    .card-panel-dark {
        border-top: 5px solid #1a5722;
        background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(245,252,246,1) 100%);
    }
    
    /* Info Texts */
    .home-info-title {
        font-size: 0.9rem;
        color: #777;
        text-transform: uppercase;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 0.2rem;
    }
    .home-info-name {
        font-size: 1.6rem;
        font-weight: 600;
        color: #111;
        margin-bottom: 1.8rem;
    }
    .indicadores-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1a5722;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    /* Dashboard Texts */
    .main-title {
        text-align: center;
        background: linear-gradient(to right, #1a5722, #32A041);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 4rem;
        margin-bottom: 5px;
        letter-spacing: -2px;
    }
    
    /* Filter Blocks */
    .filter-header {
        font-size: 0.85rem;
        color: #1a5722;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 8px;
        border-bottom: 2px solid rgba(50, 160, 65, 0.2);
        padding-bottom: 4px;
        letter-spacing: 0.5px;
    }
    
    /* Streamlit Components Overrides */
    .stButton>button {
        border-radius: 10px;
        font-weight: 800;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(50, 160, 65, 0.2);
        letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 15px -3px rgba(50, 160, 65, 0.3);
    }
    
    /* Divider */
    .custom-divider {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, rgba(50,160,65,0.0), rgba(50,160,65,0.4), rgba(50,160,65,0.0));
        margin: 40px 0;
    }
</style>
""", unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data
def load_data():
    files = [
        'Enade_2018_Ifes.xlsx',
        'Enade_2019_Ifes.xlsx',
        'Enade_2021_Ifes.xlsx',
        'Enade_2022_Ifes.xlsx'
    ]
    
    all_dfs = []
    
    for file in files:
        df_enade = pd.read_excel(file, sheet_name='Enade')
        df_cursos = pd.read_excel(file, sheet_name='Cursos')
        
        col_inscritos = next((c for c in df_enade.columns if 'Inscrito' in str(c)), None)
        col_participantes = next((c for c in df_enade.columns if 'Participante' in str(c)), None)
        
        df_merged = pd.merge(
            df_enade, 
            df_cursos[['CO_CURSO', 'CAMPUS']], 
            left_on='Código do Curso', 
            right_on='CO_CURSO', 
            how='left'
        )
        
        rename_dict = {
            'Área de Avaliação': 'NOME DO CURSO',
            'CAMPUS': 'CENTRO',
            'Município do Curso': 'MUNICÍPIO',
            'Município do Curso**': 'MUNICÍPIO',
            'Ano': 'ANO',
            'Conceito Enade (Contínuo)': 'ENADE CONTÍNUO',
            'Conceito Enade (Faixa)': 'ENADE FAIXA',
            'Modalidade de Ensino': 'MODALIDADE',
            'Categoria Administrativa': 'CATEGORIA',
            'Grau Acadêmico': 'PROGRAMA'
        }
        
        if col_inscritos:
            rename_dict[col_inscritos] = 'INSCRITOS'
        if col_participantes:
            rename_dict[col_participantes] = 'PRESENTES'
            
        df_final = df_merged.rename(columns=rename_dict)
        
        cols_to_keep = [
            'NOME DO CURSO', 'CENTRO', 'MUNICÍPIO', 'ANO', 
            'ENADE CONTÍNUO', 'ENADE FAIXA', 'MODALIDADE',
            'INSCRITOS', 'PRESENTES'
        ]
        
        cols_to_keep = [c for c in cols_to_keep if c in df_final.columns]
        
        all_dfs.append(df_final[cols_to_keep])
        
    final_combined = pd.concat(all_dfs, ignore_index=True)
    
    if pd.api.types.is_numeric_dtype(final_combined['ENADE CONTÍNUO']):
        final_combined['ENADE CONTÍNUO'] = final_combined['ENADE CONTÍNUO'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else str(x))
        
    return final_combined

try:
    data = load_data()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

def get_options(df, column):
    options = df[column].dropna().unique().tolist()
    options.sort()
    return ['Todos'] + [str(opt) for opt in options]


# --- TELAS PRINCIPAIS ---

def show_home():
    # Logo and title row
    col_text, col_img = st.columns([3, 1], gap="large")
    with col_text:
        st.markdown('<div class="home-inst-title">Instituto Federal do Espírito Santo</div>', unsafe_allow_html=True)
    with col_img:
        st.image('ifes-horizontal-cor.png', use_container_width=True)
        
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # Info and Buttons row
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
            <div class="indicadores-title">Indicadores Externos</div>
            <p style="color: #555; font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">
                Acesse a plataforma de monitoramento e análise de métricas dos cursos. Identifique rapidamente os resultados institucionais nos exames oficiais.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        # Botão super chamativo
        if st.button("🚀 ACESSAR PAINEL ENADE", use_container_width=True, type="primary"):
            st.session_state.page = 'dashboard'
            st.rerun()

def show_dashboard():
    # Back button com espaçamento
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
            
    # Header Premium Centralizado
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

    # Area de Filtros em um container isolado nativo (se suportado ficará como bloco)
    st.markdown('<div style="margin-top: 2rem; margin-bottom: 1rem;"><span style="background: #32A041; color: white; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.85rem; letter-spacing: 1px;">⚙️ FILTROS DE PESQUISA</span></div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown('<div class="filter-header">Centro</div>', unsafe_allow_html=True)
        centro_options = get_options(data, 'CENTRO')
        selected_centro = st.multiselect("Selecione os Centros", centro_options[1:], placeholder="Todos", label_visibility="collapsed")
        
    with col_b:
        st.markdown('<div class="filter-header">Ano Base</div>', unsafe_allow_html=True)
        selected_ano = st.selectbox("Selecione o Ano", get_options(data, 'ANO'), label_visibility="collapsed")
        
    with col_c:
        st.markdown('<div class="filter-header">Nota Faixa</div>', unsafe_allow_html=True)
        enade_options = get_options(data, 'ENADE FAIXA')
        selected_nota = st.multiselect("Selecione a Nota", enade_options[1:], placeholder="Todas", label_visibility="collapsed")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="filter-header">Curso</div>', unsafe_allow_html=True)
        selected_curso = st.selectbox("Selecione o Curso", get_options(data, 'NOME DO CURSO'), label_visibility="collapsed")

    with col2:
        st.markdown('<div class="filter-header">Modalidade</div>', unsafe_allow_html=True)
        selected_modalidade = st.selectbox("Selecione a Modalidade", get_options(data, 'MODALIDADE'), label_visibility="collapsed")


    # Apply Filters
    filtered_data = data.copy()

    if selected_centro:
        filtered_data = filtered_data[filtered_data['CENTRO'].isin(selected_centro)]

    if selected_ano != 'Todos':
        if str(filtered_data['ANO'].dtype) == 'object':
            filtered_data = filtered_data[filtered_data['ANO'] == selected_ano]
        else:
            try:
                 filtered_data = filtered_data[filtered_data['ANO'] == float(selected_ano)]
            except:
                 pass

    if selected_nota:
        filtered_data = filtered_data[filtered_data['ENADE FAIXA'].astype(str).isin(selected_nota)]

    if selected_curso != 'Todos':
        filtered_data = filtered_data[filtered_data['NOME DO CURSO'] == selected_curso]

    if selected_modalidade != 'Todos':
        filtered_data = filtered_data[filtered_data['MODALIDADE'] == selected_modalidade]


    st.markdown("<br>", unsafe_allow_html=True)

    st.dataframe(
        filtered_data[['NOME DO CURSO', 'CENTRO', 'MUNICÍPIO', 'ANO', 'ENADE CONTÍNUO', 'ENADE FAIXA']],
        width='stretch',
        hide_index=True,
        height=500
    )


    st.caption("""
    <div style="margin-top: 20px; font-size: 0.85rem; color: #888; text-align: center;">
        *SC - Cursos Avaliados mas sem conceito &bull; *ND - Dados não disponíveis &bull; *N/A - Cursos ainda não avaliados.<br>
        <strong>Fonte:</strong> <a href="https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-qualidade-da-educacao-superior" target="_blank" style="color: #32A041; text-decoration: none;">INEP - Indicadores de Qualidade da Educação Superior</a>
    </div>
    """, unsafe_allow_html=True)


# --- ROUTER (GERENCIADOR DE ESTADO) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    show_home()
else:
    show_dashboard()
