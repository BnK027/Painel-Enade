import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Painel - ENADE", layout="wide")

# 2. Global CSS
st.markdown("""
<style>
    .header-container {
        display: flex;
        align-items: center;
        border-bottom: 2px solid #32A041;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .header-logo {
        height: 60px;
        margin-right: 20px;
    }
    .main-title {
        text-align: center;
        color: #277A32;
        font-weight: 900;
        font-size: 3rem;
        margin-bottom: 30px;
        text-transform: uppercase;
    }
    .filter-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .filter-header {
        background-color: #32A041;
        color: white;
        padding: 5px 10px;
        font-weight: bold;
        border-radius: 3px;
        margin-bottom: 10px;
    }
    /* Home page specific styles */
    .home-inst-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #277A32;
        margin-top: 1rem;
    }
    .home-inst-subtitle {
        font-size: 1.4rem;
        color: #32A041;
        margin-bottom: 2rem;
    }
    .home-info-title {
        font-size: 1.2rem;
        color: #666;
        font-style: italic;
        margin-bottom: 0px;
    }
    .home-info-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
    }
    .indicadores-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #277A32;
        margin-bottom: 1rem;
        border-bottom: 2px solid #32A041;
        padding-bottom: 10px;
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

# Load data globally to make it available to all pages with high performance
try:
    data = load_data()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# Helper function
def get_options(df, column):
    options = df[column].dropna().unique().tolist()
    options.sort()
    return ['Todos'] + [str(opt) for opt in options]


# --- TELAS PRINCIPAIS ---

def show_home():
    # Logo and title row
    col_text, col_img = st.columns([3, 1])
    with col_text:
        st.markdown('<div class="home-inst-title">INSTITUTO FEDERAL DO ESPÍRITO SANTO</div>', unsafe_allow_html=True)
        st.markdown('<div class="home-inst-subtitle">Campus Vitória</div>', unsafe_allow_html=True)
    with col_img:
        st.image('ifes-horizontal-cor.png', use_container_width=True)
        
    st.markdown('<hr style="border: 1px solid #32A041; margin-top: 10px; margin-bottom: 40px;">', unsafe_allow_html=True)
    
    # Info and Buttons row
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown('<p class="home-info-title">Orientador</p>', unsafe_allow_html=True)
        st.markdown('<p class="home-info-name">Wagner Teixeira da Costa</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="home-info-title">Aluno</p>', unsafe_allow_html=True)
        st.markdown('<p class="home-info-name">Matheus Ferreira Tissianel Benincá</p>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown('<div class="indicadores-title">Indicadores Externos</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botao para ingressar no painel
        if st.button("📈 Exame Nacional de Desempenho dos Estudantes - ENADE", use_container_width=True, type="primary"):
            st.session_state.page = 'dashboard'
            st.rerun()

def show_dashboard():
    # Back button
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar à Página Inicial", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
            
    # Header Section
    col_logo, col_text = st.columns([1, 4])
    with col_logo:
        st.image('ifes-horizontal-cor.png', use_container_width=True)

    with col_text:
        st.markdown("""
        <div style="font-family: sans-serif; color: #32A041; padding-top: 15px;">
            <h2 style="margin: 0; font-size: 1.5rem; font-weight: bold;">INSTITUTO FEDERAL DO ESPÍRITO SANTO</h2>
            <p style="margin: 0; font-size: 1.2rem;">Pró-Reitoria de Ensino - PROEN</p>
            <p style="margin: 0; font-size: 1.2rem;">Avaliação Institucional</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr style="border: 1px solid #32A041; margin-top: 15px; margin-bottom: 20px;">', unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">PAINEL - ENADE</h1>', unsafe_allow_html=True)

    # Filters
    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown('<div class="filter-header">CENTRO</div>', unsafe_allow_html=True)
        centro_options = get_options(data, 'CENTRO')
        selected_centro = st.multiselect("Selecione os Centros", centro_options[1:], placeholder="Selecione... (Vazio = Todos)", label_visibility="collapsed")
        
    with col_b:
        st.markdown('<div class="filter-header">ANO</div>', unsafe_allow_html=True)
        selected_ano = st.selectbox("Selecione o Ano", get_options(data, 'ANO'), label_visibility="collapsed")
        
    with col_c:
        st.markdown('<div class="filter-header">Nota ENADE</div>', unsafe_allow_html=True)
        enade_options = get_options(data, 'ENADE FAIXA')
        selected_nota = st.multiselect("Selecione a Nota", enade_options[1:], placeholder="Selecione... (Vazio = Todos)", label_visibility="collapsed")


    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="filter-header">CURSO</div>', unsafe_allow_html=True)
        selected_curso = st.selectbox("Selecione o Curso", get_options(data, 'NOME DO CURSO'), label_visibility="collapsed")

    with col2:
        st.markdown('<div class="filter-header">MODALIDADE</div>', unsafe_allow_html=True)
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
        height=400
    )


    st.caption("""
    ---
    *SC - Cursos Avaliados mas sem conceito. *ND - Dados não disponíveis nos relatórios oficiais. *N/A - Não Avaliado. Nesse caso se refere a cursos que ainda serão avaliados.

    **Fonte:** https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-qualidade-da-educacao-superior
    """)


# --- ROUTER (GERENCIADOR DE ESTADO) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    show_home()
else:
    show_dashboard()
