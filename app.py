import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Painel - ENADE", layout="wide")

# 2. Custom CSS to match the requested visual
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
    .header-text {
        font-family: sans-serif;
        color: #32A041;
    }
    .header-text h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .header-text p {
        margin: 0;
        font-size: 1.2rem;
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
</style>
""", unsafe_allow_html=True)

# Header Section (Simulating the logo and title)
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

# 3. Data Loading and Processing
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
        # Load specific sheets
        df_enade = pd.read_excel(file, sheet_name='Enade')
        df_cursos = pd.read_excel(file, sheet_name='Cursos')
        
        # Encontra colunas de inscritos e participantes dinamicamente (ignora espaços extras/modificações)
        col_inscritos = next((c for c in df_enade.columns if 'Inscrito' in str(c)), None)
        col_participantes = next((c for c in df_enade.columns if 'Participante' in str(c)), None)
        
        # Merge Enade and Cursos to get Campus information
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
            
        # Rename columns to match the requested output
        df_final = df_merged.rename(columns=rename_dict)
        
        # Select only relevant columns for display and filtering
        cols_to_keep = [
            'NOME DO CURSO', 'CENTRO', 'MUNICÍPIO', 'ANO', 
            'ENADE CONTÍNUO', 'ENADE FAIXA', 'MODALIDADE',
            'INSCRITOS', 'PRESENTES'
        ]
        
        # Keep only the columns that actually exist (to be safe)
        cols_to_keep = [c for c in cols_to_keep if c in df_final.columns]
        
        all_dfs.append(df_final[cols_to_keep])
        
    final_combined = pd.concat(all_dfs, ignore_index=True)
    
    # Format ENADE CONTÍNUO to string with 4 decimal places if it's numeric, to look nicer
    if pd.api.types.is_numeric_dtype(final_combined['ENADE CONTÍNUO']):
        final_combined['ENADE CONTÍNUO'] = final_combined['ENADE CONTÍNUO'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else str(x))
        
    return final_combined

try:
    data = load_data()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# --- MARQUEE DE AUSENTES ---
if 'INSCRITOS' in data.columns and 'PRESENTES' in data.columns:
    # Converter para numérico para somar com segurança
    data['INSCRITOS_NUM'] = pd.to_numeric(data['INSCRITOS'], errors='coerce')
    data['PRESENTES_NUM'] = pd.to_numeric(data['PRESENTES'], errors='coerce')
    
    # Agrupar por ano e calcular ausentes (inscritos - presentes)
    abs_data = data.groupby('ANO').agg({'INSCRITOS_NUM': 'sum', 'PRESENTES_NUM': 'sum'}).reset_index()
    abs_data = abs_data.dropna(subset=['ANO'])
    
    # Ordenar por ano propriamente
    try:
        abs_data['ANO_SORT'] = abs_data['ANO'].astype(str).str.extract(r'(\d{4})').astype(float)
        abs_data = abs_data.sort_values('ANO_SORT')
    except:
        abs_data = abs_data.sort_values('ANO')
        
    marquee_items = []
    for _, row in abs_data.iterrows():
        insc = row['INSCRITOS_NUM']
        pres = row['PRESENTES_NUM']
        if pd.notnull(insc) and pd.notnull(pres) and insc > 0:
            tx = (1 - (pres / insc)) * 100
            ano_formatado = str(row['ANO']).replace('.0', '')
            marquee_items.append(f"👨‍🎓 <b>ENADE {ano_formatado}</b>: {tx:.1f}% de Ausentes")
            
    if marquee_items:
        marquee_html = f"""
        <div style="background-color: #ffeaea; border-left: 5px solid #e12d39; padding: 10px; border-radius: 4px; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="font-size: 0.85rem; color: #e12d39; margin-bottom: 5px; font-weight: bold; text-transform: uppercase;">📊 Taxa de Abstenção por Ano:</div>
            <marquee behavior="scroll" direction="left" scrollamount="6" style="font-size: 1.2rem; color: #333; font-weight: 500; font-family: sans-serif;">
                {' &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; '.join(marquee_items)}
            </marquee>
        </div>
        """
        st.markdown(marquee_html, unsafe_allow_html=True)

# Helper function to get unique sorted values including 'Todos'
def get_options(df, column):
    options = df[column].dropna().unique().tolist()
    options.sort()
    return ['Todos'] + [str(opt) for opt in options]

# 4. Filter Layout Setup (All in main body to prevent sidebar from resizing the header)
st.markdown("<br>", unsafe_allow_html=True)

# First row of filters
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


# Second row of filters
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="filter-header">CURSO</div>', unsafe_allow_html=True)
    selected_curso = st.selectbox("Selecione o Curso", get_options(data, 'NOME DO CURSO'), label_visibility="collapsed")

with col2:
    st.markdown('<div class="filter-header">MODALIDADE</div>', unsafe_allow_html=True)
    selected_modalidade = st.selectbox("Selecione a Modalidade", get_options(data, 'MODALIDADE'), label_visibility="collapsed")


# 5. Apply Filters
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
    # Handle numbers/strings mixing
    filtered_data = filtered_data[filtered_data['ENADE FAIXA'].astype(str).isin(selected_nota)]

if selected_curso != 'Todos':
    filtered_data = filtered_data[filtered_data['NOME DO CURSO'] == selected_curso]

if selected_modalidade != 'Todos':
    filtered_data = filtered_data[filtered_data['MODALIDADE'] == selected_modalidade]




# 6. Display DataFrame
st.markdown("<br>", unsafe_allow_html=True)

# Custom Styling for DataFrame headers isn't perfectly replicable in Streamlit native dataframe,
# but we can display the table using st.dataframe and it looks clean.
st.dataframe(
    filtered_data[['NOME DO CURSO', 'CENTRO', 'MUNICÍPIO', 'ANO', 'ENADE CONTÍNUO', 'ENADE FAIXA']],
    width='stretch',
    hide_index=True,
    height=400
)

# 7. Footer notes
st.caption("""
---
*SC - Cursos Avaliados mas sem conceito. *ND - Dados não disponíveis nos relatórios oficiais. *N/A - Não Avaliado. Nesse caso se refere a cursos que ainda serão avaliados.

**Fonte:** https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-qualidade-da-educacao-superior
""")
