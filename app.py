import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import re

# --- Caminho base e imagens pré-carregadas ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _img_b64(filename):
    path = os.path.join(BASE_DIR, filename)
    try:
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ''

IMG_VERTICAL_B64 = _img_b64('ifes-vertical-cor.png')
IMG_HORIZONTAL_B64 = _img_b64('ifes-horizontal-cor.png')

# 1. Page Configuration
st.set_page_config(page_title="Painel - ENADE", layout="wide", initial_sidebar_state="collapsed")

# 2. Premium Global CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');
    
    /* Aplica a fonte Inter apenas em textos, evitando quebrar os ícones nativos da UI (como o expander) */
    .stMarkdown, .card-panel, .kpi-card, .home-inst-title, .indicadores-title, .filter-header, h1, h2, h3, h4, p, span.st-emotion-cache-10trblm { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #f4f7f6 0%, #ffffff 100%); }
    
    /* Animations */
    @keyframes fadeInScale {
        from { opacity: 0; transform: translateY(20px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    .fade-in { animation: fadeInScale 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    
    /* Typography */
    .home-inst-title { font-size: 3.2rem; font-weight: 800; color: #0f2c16; margin-top: 1rem; line-height: 1.1; letter-spacing: -1.5px; }
    .home-inst-subtitle { font-size: 1.5rem; color: #2c8c44; margin-bottom: 2rem; font-weight: 600; letter-spacing: -0.5px; }
    .indicadores-title { font-size: 2rem; font-weight: 800; color: #103d6d; margin-bottom: 1.5rem; letter-spacing: -1px; text-transform: uppercase; }
    .filter-header { font-size: 0.9rem; color: #103d6d; font-weight: 800; text-transform: uppercase; margin-bottom: 10px; border-bottom: 2px solid rgba(16, 61, 109, 0.15); padding-bottom: 6px; letter-spacing: 0.5px; }
    
    /* Premium Cards & Glassmorphism */
    .card-panel {
        background-color: rgba(255, 255, 255, 0.75); padding: 2.5rem; border-radius: 24px;
        box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05), 0 8px 16px -6px rgba(0,0,0,0.02);
        border: 1px solid rgba(255,255,255,0.6); border-top: 6px solid #2c8c44;
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        height: 100%; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .card-panel:hover { transform: translateY(-8px); box-shadow: 0 30px 60px -12px rgba(44, 140, 68, 0.15); }
    .card-panel-dark { border-top: 6px solid #103d6d; background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(240,244,248,0.95) 100%); }
    .card-panel-dark:hover { box-shadow: 0 30px 60px -12px rgba(16, 61, 109, 0.15); }

    /* Streamlit Input Overrides (Fixing White Bars & Placeholder Color) */
    div[data-baseweb="select"] > div {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e0e6ed;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        font-weight: 500;
        color: #103d6d;
        transition: all 0.3s ease;
    }
    div[data-baseweb="select"] * { line-height: 1.6; }
    div[data-baseweb="select"] div, div[data-baseweb="select"] span {
        color: #103d6d !important;
        opacity: 1 !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #103d6d; box-shadow: 0 6px 16px rgba(16,61,109,0.1);
    }
    
    /* Plotly Charts Premium Look */
    [data-testid="stPlotlyChart"] {
        background-color: rgba(255,255,255,0.9);
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        padding: 10px;
        border: 1px solid rgba(0,0,0,0.03);
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
    }
    [data-testid="stPlotlyChart"]:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 12px 32px rgba(0,0,0,0.08);
    }

    /* KPI Cards */
    .kpi-card { background: linear-gradient(135deg, #ffffff, #fdfdfd); border-left: 6px solid #103d6d; border-radius: 16px; padding: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.04); text-align: center; margin: 10px auto; transition: transform 0.3s; border-right: 1px solid #f0f0f0; border-top: 1px solid #f0f0f0; border-bottom: 1px solid #f0f0f0; }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(16,61,109,0.12); }
    .kpi-title { font-size: 0.85rem; color: #888; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }
    .kpi-value { font-size: 2.8rem; font-weight: 800; color: #103d6d; line-height: 1; letter-spacing: -1px; }

    /* Button Styling */
    .stButton>button { border-radius: 14px; font-weight: 700; padding: 0.8rem 1.5rem; border: none; background: #ffffff; color: #103d6d; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e8e8e8; }
    .stButton>button:hover { transform: translateY(-3px) scale(1.03); box-shadow: 0 12px 24px rgba(16,61,109,0.15); background: #103d6d; color: #ffffff; border-color: #103d6d; }
    
    /* Responsive & Questionnaire Section */
    @media (max-width: 1024px) { 
        .kpi-value { font-size: 2.2rem; } 
        .card-panel { padding: 1.5rem; }
    }
    @media (max-width: 768px) { 
        .home-inst-title { font-size: 2rem; } 
        .kpi-value { font-size: 1.8rem; }
        .qe-section { padding: 1rem; }
    }
    .qe-section { background: #f8fafc; border-radius: 20px; padding: 2rem; border-left: 8px solid #2c8c44; margin-top: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .qe-label { font-size: 1.1rem; font-weight: 700; color: #0f2c16; margin-bottom: 0.5rem; display: block; border-bottom: 1px solid #e2e8f0; padding-bottom: 5px; }
    .qe-value-tag { display: inline-block; background: #e2e8f0; padding: 4px 12px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; color: #334155; margin-top: 5px; }
""", unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data
def load_data():
    files = ['Enade_2017_Ifes.xlsx', 'Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']
    all_dfs = []
    
    for file in files:
        df_enade = pd.read_excel(file, sheet_name='Enade')
        df_cursos = pd.read_excel(file, sheet_name='Cursos')
        
        col_inscritos = next((c for c in df_enade.columns if 'Inscrito' in str(c)), None)
        col_participantes = next((c for c in df_enade.columns if 'Participante' in str(c)), None)
        col_nota_fg = next((c for c in df_enade.columns if 'Bruta' in str(c) and 'FG' in str(c)), None)
        col_nota_ce = next((c for c in df_enade.columns if 'Bruta' in str(c) and 'CE' in str(c)), None)
        
        df_enade['Código do Curso'] = df_enade['Código do Curso'].astype(str).str.replace(r'\.0$', '', regex=True)
        df_cursos['CO_CURSO'] = df_cursos['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
        
        df_merged = pd.merge(df_enade, df_cursos[['CO_CURSO', 'CAMPUS']], left_on='Código do Curso', right_on='CO_CURSO', how='left')
        
        rename_dict = {
            'Área de Avaliação': 'NOME DO CURSO', 'CAMPUS': 'CAMPUS',
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
        if 'ANO' in df_final.columns:
            df_final['ANO'] = df_final['ANO'].astype(str).str.replace(r'\.0$', '', regex=True)
            
        cols_to_keep = ['NOME DO CURSO', 'CAMPUS', 'MUNICÍPIO', 'ANO', 'ENADE CONTÍNUO', 'ENADE FAIXA', 'MODALIDADE', 'INSCRITOS', 'PRESENTES', 'NOTA_FG', 'NOTA_CE', 'CO_CURSO']
        cols_to_keep = [c for c in cols_to_keep if c in df_final.columns]
        all_dfs.append(df_final[cols_to_keep])
        
    final_combined = pd.concat(all_dfs, ignore_index=True)
    if pd.api.types.is_numeric_dtype(final_combined['ENADE CONTÍNUO']):
        final_combined['ENADE CONTÍNUO'] = final_combined['ENADE CONTÍNUO'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else str(x))
    return final_combined

@st.cache_data
def load_microdata():
    files = ['Enade_2017_Ifes.xlsx', 'Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']
    all_sexo, all_idade, all_raca, all_renda = [], [], [], []
    all_pai, all_mae, all_trab, all_bolsa, all_cota, all_estudo, all_motiv_c, all_motiv_i, all_arq4, all_arq43 = [], [], [], [], [], [], [], [], [], []
    all_ce_respostas, all_ce_gabarito = [], []
    
    for file in files:
        try:
            df_cursos = pd.read_excel(file, sheet_name='Cursos')
            df_cursos['CO_CURSO'] = df_cursos['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
            
            if 'CAMPUS' not in df_cursos.columns:
                df_cursos['CAMPUS'] = 'Desconhecido'

            curso_map = df_cursos[['CO_CURSO', 'CAMPUS']].copy()
            # Adiciona a coluna ANO vinda do nome do arquivo
            ano_match = re.search(r'20\d{2}', file)
            file_ano = ano_match.group(0) if ano_match else ''
            curso_map['ANO'] = str(file_ano)
            df_enade = pd.read_excel(file, sheet_name='Enade')
            xls = pd.ExcelFile(file)
            
            df_enade['Código do Curso'] = df_enade['Código do Curso'].astype(str).str.replace(r'\.0$', '', regex=True)
            
            # Map CO_CURSO to their actual Names and Campus
            curso_map = pd.merge(curso_map, df_enade[['Código do Curso', 'Área de Avaliação']], left_on='CO_CURSO', right_on='Código do Curso', how='inner')
            curso_map = curso_map.rename(columns={'Área de Avaliação': 'NOME DO CURSO'})
            
            # Aba Arq_5 (Sexo)
            if 'Arq_5' in xls.sheet_names:
                df_temp = pd.read_excel(xls, sheet_name='Arq_5')
                df_temp['CO_CURSO'] = df_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
                if 'ANO' in df_temp.columns: df_temp = df_temp.drop(columns=['ANO'])
                df_sexo = pd.merge(df_temp, curso_map, on='CO_CURSO', how='inner')
                if not df_sexo.empty: all_sexo.append(df_sexo)
            # Aba Arq_6 (Idade)
            if 'Arq_6' in xls.sheet_names:
                df_temp = pd.read_excel(xls, sheet_name='Arq_6')
                df_temp['CO_CURSO'] = df_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
                if 'ANO' in df_temp.columns: df_temp = df_temp.drop(columns=['ANO'])
                df_idade = pd.merge(df_temp, curso_map, on='CO_CURSO', how='inner')
                if not df_idade.empty: all_idade.append(df_idade)
            # Aba Arq_8 (Cor/Raça - QE_I02)
            if 'Arq_8' in xls.sheet_names:
                df_temp = pd.read_excel(xls, sheet_name='Arq_8')
                df_temp['CO_CURSO'] = df_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
                if 'ANO' in df_temp.columns: df_temp = df_temp.drop(columns=['ANO'])
                df_raca = pd.merge(df_temp, curso_map, on='CO_CURSO', how='inner')
                if not df_raca.empty: all_raca.append(df_raca)
            # Aba Arq_14 (Renda Familiar - QE_I08)
            if 'Arq_14' in xls.sheet_names:
                df_temp = pd.read_excel(xls, sheet_name='Arq_14')
                df_temp['CO_CURSO'] = df_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
                if 'ANO' in df_temp.columns: df_temp = df_temp.drop(columns=['ANO'])
                df_renda = pd.merge(df_temp, curso_map, on='CO_CURSO', how='inner')
                if not df_renda.empty: all_renda.append(df_renda)

            for arq, lst in zip(['Arq_10','Arq_11','Arq_16','Arq_17','Arq_21','Arq_29','Arq_31','Arq_32', 'Arq_4', 'Arq_43'], 
                                [all_pai, all_mae, all_trab, all_bolsa, all_cota, all_estudo, all_motiv_c, all_motiv_i, all_arq4, all_arq43]):
                if arq in xls.sheet_names:
                    df_arq_temp = pd.read_excel(xls, sheet_name=arq)
                    df_arq_temp['CO_CURSO'] = df_arq_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
                    if 'ANO' in df_arq_temp.columns: df_arq_temp = df_arq_temp.drop(columns=['ANO'])
                    df_temp = pd.merge(df_arq_temp, curso_map, on='CO_CURSO', how='inner')
                    if not df_temp.empty: lst.append(df_temp)

            # Arq_3B: respostas por questão do CE (CE1..CE27) + gabarito por aluno
            if 'Arq_3B' in xls.sheet_names:
                df_temp = pd.read_excel(xls, sheet_name='Arq_3B')
                df_temp['CO_CURSO'] = df_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
                if 'ANO' in df_temp.columns: df_temp = df_temp.drop(columns=['ANO'])
                df_3b = pd.merge(df_temp, curso_map, on='CO_CURSO', how='inner')
                if not df_3b.empty: all_ce_respostas.append(df_3b)
            # Arq_3: gabarito final (DS_VT_GAB_OCE_FIN) por aluno
            if 'Arq_3' in xls.sheet_names:
                df_temp = pd.read_excel(xls, sheet_name='Arq_3')
                df_temp['CO_CURSO'] = df_temp['CO_CURSO'].astype(str).str.replace(r'\.0$', '', regex=True)
                if 'ANO' in df_temp.columns: df_temp = df_temp.drop(columns=['ANO'])
                df_3 = pd.merge(df_temp, curso_map, on='CO_CURSO', how='inner')
                if not df_3.empty: all_ce_gabarito.append(df_3)
                
        except Exception as e:
            print(f"Erro no load_microdata para {file}: {e}")
            continue
            
    return {
        'sexo': pd.concat(all_sexo, ignore_index=True) if all_sexo else pd.DataFrame(),
        'idade': pd.concat(all_idade, ignore_index=True) if all_idade else pd.DataFrame(),
        'raca': pd.concat(all_raca, ignore_index=True) if all_raca else pd.DataFrame(),
        'renda': pd.concat(all_renda, ignore_index=True) if all_renda else pd.DataFrame(),
        'pai': pd.concat(all_pai, ignore_index=True) if all_pai else pd.DataFrame(),
        'mae': pd.concat(all_mae, ignore_index=True) if all_mae else pd.DataFrame(),
        'trab': pd.concat(all_trab, ignore_index=True) if all_trab else pd.DataFrame(),
        'bolsa': pd.concat(all_bolsa, ignore_index=True) if all_bolsa else pd.DataFrame(),
        'cota': pd.concat(all_cota, ignore_index=True) if all_cota else pd.DataFrame(),
        'estudo': pd.concat(all_estudo, ignore_index=True) if all_estudo else pd.DataFrame(),
        'motiv_c': pd.concat(all_motiv_c, ignore_index=True) if all_motiv_c else pd.DataFrame(),
        'motiv_i': pd.concat(all_motiv_i, ignore_index=True) if all_motiv_i else pd.DataFrame(),
        'arq4': pd.concat(all_arq4, ignore_index=True) if all_arq4 else pd.DataFrame(),
        'arq43': pd.concat(all_arq43, ignore_index=True) if all_arq43 else pd.DataFrame(),
        'ce_respostas': pd.concat(all_ce_respostas, ignore_index=True) if all_ce_respostas else pd.DataFrame(),
        'ce_gabarito': pd.concat(all_ce_gabarito, ignore_index=True) if all_ce_gabarito else pd.DataFrame(),
    }

try:
    data = load_data()
    microdados = load_microdata()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

def get_options(df, column):
    options = df[column].dropna().unique().tolist()
    options.sort()
    return ['Todos'] + [str(opt) for opt in options]

# --- Helper de Filtros Global ---
def render_filters(source_data, ano_fixo=None):
    st.markdown('<div class="fade-in" style="margin-top: 1rem; margin-bottom: 1rem;"><span style="background: linear-gradient(135deg, #1a5722, #32A041); color: white; padding: 6px 16px; border-radius: 20px; font-weight: 800; font-size: 0.85rem; letter-spacing: 1px; box-shadow: 0 4px 10px rgba(50,160,65,0.3);">⚙️ FILTROS DE PESQUISA</span></div>', unsafe_allow_html=True)
    
    curr_campus = st.session_state.get('filtro_campus', [])
    curr_curso = st.session_state.get('filtro_curso', 'Todos')

    def get_filtered_for(exclude_key):
        df = source_data.copy()
        
        # Filtro de Ano OBRIGATÓRIO (invisível)
        if ano_fixo:
            # Força a conversão para string removendo possíveis decimais para garantir o match
            df['ANO_STR_TEMP'] = df['ANO'].astype(str).str.replace('.0', '', regex=False)
            df = df[df['ANO_STR_TEMP'] == str(ano_fixo)]
            df = df.drop(columns=['ANO_STR_TEMP'])
                
        if exclude_key != 'CAMPUS' and curr_campus:
            df = df[df['CAMPUS'].isin(curr_campus)]
        if exclude_key != 'NOME DO CURSO' and curr_curso != 'Todos':
            df = df[df['NOME DO CURSO'] == curr_curso]
        return df

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="filter-header">Campus</div>', unsafe_allow_html=True)
        campus_options = get_options(get_filtered_for('CAMPUS'), 'CAMPUS')
        valid_campi = [c for c in curr_campus if c in campus_options]
        if valid_campi != curr_campus: st.session_state['filtro_campus'] = valid_campi
        selected_campus = st.multiselect("Selecione os Campi", campus_options[1:], placeholder="Todos", label_visibility="collapsed", key='filtro_campus')
        
    with col_b:
        st.markdown('<div class="filter-header">Curso</div>', unsafe_allow_html=True)
        curso_options = get_options(get_filtered_for('NOME DO CURSO'), 'NOME DO CURSO')
        if curr_curso not in curso_options: st.session_state['filtro_curso'] = 'Todos'
        selected_curso = st.selectbox("Selecione o Curso", curso_options, label_visibility="collapsed", key='filtro_curso')

    return get_filtered_for(None)

# --- Header das Views com logo IFES no canto direito ---
def render_page_header(ano, back_key):
    col_back, col_title, col_logo = st.columns([1.5, 5, 1.5])
    with col_back:
        st.markdown("<div style='padding-top: 8px;'>", unsafe_allow_html=True)
        if st.button('⬅ Voltar ao Início', use_container_width=True, key=back_key):
            st.session_state.page = 'home'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_title:
        st.markdown(f'''
            <div class="fade-in" style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
                <p style="color: #32A041; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;">Painel Analítico</p>
                <h1 style="font-size: 3rem; font-weight: 900; color: #103d6d;">ENADE {ano}</h1>
            </div>
        ''', unsafe_allow_html=True)
    with col_logo:
        if IMG_VERTICAL_B64:
            st.markdown(
                f'<img src="data:image/png;base64,{IMG_VERTICAL_B64}" '
                f'style="width:120px; display:block; margin-left:auto; margin-top:4px;"/>',
                unsafe_allow_html=True
            )

def show_home():
    col_text, col_img = st.columns([3, 1], gap="large")
    with col_text:
        st.markdown('<div class="home-inst-title">INSTITUTO FEDERAL DO ESPÍRITO SANTO - IFES</div>', unsafe_allow_html=True)
    with col_img:
        if IMG_HORIZONTAL_B64:
            st.markdown(f'<img src="data:image/png;base64,{IMG_HORIZONTAL_B64}" style="width:100%; max-width:300px;"/>', unsafe_allow_html=True)
        
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1], gap="large")
    with col_left:
        st.markdown('''<div class="card-panel" style="padding: 2rem;">
<div style="display: flex; align-items: center; margin-bottom: 1.5rem; padding: 10px; border-radius: 12px; transition: all 0.3s; background: linear-gradient(to right, rgba(16, 61, 109, 0.03), transparent);">
<div style="width: 54px; height: 54px; border-radius: 50%; background: linear-gradient(135deg, #103d6d, #205c9e); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 800; margin-right: 15px; box-shadow: 0 4px 10px rgba(16,61,109,0.2);">W</div>
<div>
<p style="margin: 0; font-size: 0.75rem; color: #103d6d; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px;">Orientador</p>
<p style="margin: 0; font-size: 1.15rem; color: #111; font-weight: 800; letter-spacing: -0.5px;">Prof. Wagner Teixeira da Costa</p>
</div>
</div>
<div style="display: flex; align-items: center; padding: 10px; border-radius: 12px; transition: all 0.3s; background: linear-gradient(to right, rgba(44, 140, 68, 0.03), transparent);">
<div style="width: 54px; height: 54px; border-radius: 50%; background: linear-gradient(135deg, #2c8c44, #3bb358); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 800; margin-right: 15px; box-shadow: 0 4px 10px rgba(44,140,68,0.2);">M</div>
<div>
<p style="margin: 0; font-size: 0.75rem; color: #2c8c44; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px;">Aluno Desenvolvedor</p>
<p style="margin: 0; font-size: 1.15rem; color: #111; font-weight: 800; letter-spacing: -0.5px;">Matheus Ferreira Tissianel Benincá</p>
</div>
</div>
</div>''', unsafe_allow_html=True)
        
        # --- Indicadores Globais no Espaço Vazio ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="indicadores-title" style="font-size: 1.2rem; margin-bottom: 0.8rem; letter-spacing: 0;">📊 Destaques Institucionais (Total)</div>', unsafe_allow_html=True)
        
        # Cálculos globais
        total_alunos = data['PRESENTES'].sum()
        total_cursos = data['NOME DO CURSO'].nunique()
        total_campi = data['CAMPUS'].nunique()
        
        # Card 1: Alunos
        st.markdown(f'''<div class="kpi-card" style="padding: 15px; margin-bottom: 15px;">
            <p class="kpi-title" style="font-size: 0.75rem; margin-bottom: 5px;">Total de Alunos Avaliados</p>
            <p class="kpi-value" style="font-size: 2.2rem;">{int(total_alunos):,}</p>
        </div>'''.replace(',', '.'), unsafe_allow_html=True)
        
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.markdown(f'''<div class="kpi-card" style="padding: 15px; border-left-color: #2c8c44;">
                <p class="kpi-title" style="font-size: 0.75rem; margin-bottom: 5px;">Cursos</p>
                <p class="kpi-value" style="font-size: 2rem;">{total_cursos}</p>
            </div>''', unsafe_allow_html=True)
        with col_k2:
            st.markdown(f'''<div class="kpi-card" style="padding: 15px; border-left-color: #f39c12;">
                <p class="kpi-title" style="font-size: 0.75rem; margin-bottom: 5px;">Campi</p>
                <p class="kpi-value" style="font-size: 2rem;">{total_campi}</p>
            </div>''', unsafe_allow_html=True)
        
    with col_right:
        st.markdown('''
        <div class="card-panel card-panel-dark">
            <div class="indicadores-title">Plataformas Analíticas</div>
            <p style="color: #555; font-size: 1.05rem; line-height: 1.5; margin-bottom: 1rem;">
                Utilize os filtros abaixo para escolher seu Campus e/ou Curso. Os anos disponíveis para o ENADE aparecerão logo abaixo!
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Renderiza os filtros globais na tela inicial
        filtered_data = render_filters(data, ano_fixo=None)
        
        # Descobre quais anos estão disponíveis no dataset filtrado
        anos_disponiveis = filtered_data['ANO'].dropna().astype(str).str.replace('.0', '', regex=False).unique().tolist()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.2rem;">Anos Disponíveis para sua Busca</div>', unsafe_allow_html=True)
        if len(anos_disponiveis) == 0:
            st.warning("Nenhum dado de ENADE encontrado para os filtros selecionados.")
        else:
            # Ordena os anos para ficarem em ordem cronológica
            anos_disponiveis.sort()
            cols = st.columns(len(anos_disponiveis))
            
            for idx, ano in enumerate(anos_disponiveis):
                with cols[idx]:
                    if st.button(f"📅 {ano}", use_container_width=True, type="primary"):
                        st.session_state.ano_selecionado = ano
                        st.session_state.page = f'visao_{ano}'
                        st.rerun()
                        
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Consultar Tabela Geral: Todos os Cursos e Anos Disponíveis", expanded=False):
        st.markdown("Confira abaixo a lista completa de todos os cursos da base de dados e os anos em que realizaram o Enade:")
        df_table = data.groupby(['CAMPUS', 'NOME DO CURSO'])['ANO'].apply(
            lambda x: sorted(list(set(x.dropna().astype(str).str.replace('.0', '', regex=False))))
        ).reset_index()
        df_table['Anos Avaliados'] = df_table['ANO'].apply(lambda x: ', '.join(x))
        df_table = df_table.drop(columns=['ANO'])
        df_table.columns = ['Campus', 'Curso', 'Anos Avaliados']
        st.dataframe(df_table, hide_index=True, use_container_width=True)

# --- ROUTER (GERENCIADOR DE ESTADO) ---

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = None

# --- Tela de transição: fundo branco, logo IFES + nome do ano ---
def show_splash(ano):
    import time
    # Só exibe o splash uma vez por navegação (evita re-exibir em reruns por filtros)
    if st.session_state.splash_shown == ano:
        return

    st.session_state.splash_shown = ano

    # Espaço vertical para centralizar
    st.markdown('<div style="height: 20vh;"></div>', unsafe_allow_html=True)

    # Logo horizontal IFES centralizado
    _, col_img, _ = st.columns([1, 2, 1])
    with col_img:
        for candidate in [
            os.path.join(BASE_DIR, 'ifes-horizontal-cor.png'),
            'ifes-horizontal-cor.png',
            os.path.join(os.getcwd(), 'ifes-horizontal-cor.png'),
        ]:
            if os.path.exists(candidate):
                st.image(candidate, use_container_width=True)
                break

    # Texto centralizado abaixo do logo
    st.markdown(f'''
        <div style="text-align:center; margin-top: 2.5rem;">
            <p style="color:#2c8c44; font-weight:800; letter-spacing:3px;
                       text-transform:uppercase; margin-bottom:0.5rem;
                       font-family:Inter,sans-serif; font-size:1.1rem;">
                PAINEL ANALÍTICO
            </p>
            <h1 style="color:#103d6d; font-size:3.8rem; font-weight:900;
                        margin:0; letter-spacing:-2px; font-family:Inter,sans-serif;">
                ENADE {ano}
            </h1>
        </div>
    ''', unsafe_allow_html=True)

    time.sleep(1.5)
    st.rerun()

if st.session_state.page == 'home':
    st.session_state.splash_shown = None   # reseta ao voltar para home
    show_home()
elif st.session_state.page == 'visao_2017':
    show_splash('2017')
    from views.visao_2017 import render_visao_2017
    render_visao_2017(data, microdados, render_filters, render_page_header)
elif st.session_state.page == 'visao_2018':
    show_splash('2018')
    from views.visao_2018 import render_visao_2018
    render_visao_2018(data, microdados, render_filters, render_page_header)
elif st.session_state.page == 'visao_2019':
    show_splash('2019')
    from views.visao_2019 import render_visao_2019
    render_visao_2019(data, microdados, render_filters, render_page_header)
elif st.session_state.page == 'visao_2021':
    show_splash('2021')
    from views.visao_2021 import render_visao_2021
    render_visao_2021(data, microdados, render_filters, render_page_header)
elif st.session_state.page == 'visao_2022':
    show_splash('2022')
    from views.visao_2022 import render_visao_2022
    render_visao_2022(data, microdados, render_filters, render_page_header)
