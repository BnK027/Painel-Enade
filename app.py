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
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    
    .home-inst-title { font-size: 2.8rem; font-weight: 900; color: #1a5722; margin-top: 1rem; line-height: 1.1; letter-spacing: -1.2px; }
    .home-inst-subtitle { font-size: 1.6rem; color: #32A041; margin-bottom: 1.5rem; font-weight: 600; letter-spacing: -0.5px; }
    
    .card-panel {
        background-color: rgba(255, 255, 255, 0.85); padding: 2.5rem; border-radius: 20px;
        box-shadow: 0 10px 30px -5px rgba(0,0,0,0.06), 0 8px 10px -6px rgba(0,0,0,0.02);
        border-top: 5px solid #32A041; border-bottom: 1px solid rgba(50,160,65,0.1); border-left: 1px solid rgba(50,160,65,0.1); border-right: 1px solid rgba(50,160,65,0.1);
        backdrop-filter: blur(12px); height: 100%; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .card-panel:hover { transform: translateY(-6px); box-shadow: 0 20px 40px -5px rgba(0,0,0,0.1), 0 10px 15px -5px rgba(0,0,0,0.04); }
    .card-panel-dark { border-top: 5px solid #1a5722; background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(245,252,246,0.95) 100%); }
    
    .filter-box { background: rgba(255,255,255,0.7); backdrop-filter: blur(16px); padding: 20px; border-radius: 16px; border: 1px solid rgba(50,160,65,0.15); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05); margin-bottom: 25px; }
    
    [data-testid="stPlotlyChart"] {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        padding: 5px;
        border: 1px solid rgba(0,0,0,0.04);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stPlotlyChart"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }

    .kpi-card { background: linear-gradient(145deg, #ffffff, #f0f7f2); border-left: 5px solid #32A041; border-radius: 12px; padding: 15px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); display: inline-block; min-width: 200px; text-align: center; margin: 10px auto; transition: transform 0.3s; }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
    .kpi-title { font-size: 0.85rem; color: #666; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .kpi-value { font-size: 2.2rem; font-weight: 900; color: #1a5722; line-height: 1; }
    .kpi-unit { font-size: 1rem; color: #777; font-weight: 600; margin-left: 4px; }
    
    .home-info-title { font-size: 0.9rem; color: #777; text-transform: uppercase; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 0.2rem; }
    .home-info-name { font-size: 1.6rem; font-weight: 600; color: #111; margin-bottom: 1.8rem; }
    .indicadores-title { font-size: 1.8rem; font-weight: 800; color: #1a5722; margin-bottom: 1rem; letter-spacing: -0.5px; }
    
    .main-title { text-align: center; background: linear-gradient(135deg, #1a5722 0%, #32A041 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 4rem; margin-bottom: 5px; letter-spacing: -2px; }
    .filter-header { font-size: 0.85rem; color: #1a5722; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; border-bottom: 2px solid rgba(50,160,65,0.2); padding-bottom: 4px; letter-spacing: 0.5px; }
    
    .stButton>button { border-radius: 12px; font-weight: 800; padding: 0.7rem 1.4rem; border: none; background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%); border: 1px solid #e0e0e0; color: #333; transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: 0 4px 10px -2px rgba(0,0,0,0.05); letter-spacing: 0.5px; }
    .stButton>button:hover { transform: translateY(-4px) scale(1.02); box-shadow: 0 12px 20px -3px rgba(50,160,65,0.25); border-color: #32A041; color: #1a5722; }
    
    /* Force primary button style strictly based on internal types if possible, but hover effects cover it all */
    
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
    all_sexo, all_idade, all_raca, all_renda, all_evasao = [], [], [], [], []
    all_pai, all_mae, all_trab, all_bolsa, all_cota, all_estudo, all_motiv_c, all_motiv_i, all_arq4 = [], [], [], [], [], [], [], [], []
    
    for file in files:
        try:
            df_cursos = pd.read_excel(file, sheet_name='Cursos')
            df_enade = pd.read_excel(file, sheet_name='Enade')
            xls = pd.ExcelFile(file)
            
            # Map CO_CURSO to their actual Names and Campus
            curso_map = pd.merge(df_cursos[['CO_CURSO', 'CAMPUS']], df_enade[['Código do Curso', 'Área de Avaliação', 'Ano']], left_on='CO_CURSO', right_on='Código do Curso', how='inner')
            curso_map = curso_map.rename(columns={'Área de Avaliação': 'NOME DO CURSO', 'CAMPUS': 'CENTRO', 'Ano': 'ANO'})
            
            # Aba Arq_5 (Sexo)
            if 'Arq_5' in xls.sheet_names:
                df_sexo = pd.merge(pd.read_excel(xls, sheet_name='Arq_5'), curso_map, on='CO_CURSO', how='inner')
                if not df_sexo.empty: all_sexo.append(df_sexo)
            # Aba Arq_6 (Idade)
            if 'Arq_6' in xls.sheet_names:
                df_idade = pd.merge(pd.read_excel(xls, sheet_name='Arq_6'), curso_map, on='CO_CURSO', how='inner')
                if not df_idade.empty: all_idade.append(df_idade)
            # Aba Arq_8 (Cor/Raça - QE_I02)
            if 'Arq_8' in xls.sheet_names:
                df_raca = pd.merge(pd.read_excel(xls, sheet_name='Arq_8'), curso_map, on='CO_CURSO', how='inner')
                if not df_raca.empty: all_raca.append(df_raca)
            # Aba Arq_14 (Renda Familiar - QE_I08)
            if 'Arq_14' in xls.sheet_names:
                df_renda = pd.merge(pd.read_excel(xls, sheet_name='Arq_14'), curso_map, on='CO_CURSO', how='inner')
                if not df_renda.empty: all_renda.append(df_renda)

            for arq, lst in zip(['Arq_10','Arq_11','Arq_16','Arq_17','Arq_21','Arq_29','Arq_31','Arq_32', 'Arq_4'], 
                                [all_pai, all_mae, all_trab, all_bolsa, all_cota, all_estudo, all_motiv_c, all_motiv_i, all_arq4]):
                if arq in xls.sheet_names:
                    df_temp = pd.merge(pd.read_excel(xls, sheet_name=arq), curso_map, on='CO_CURSO', how='inner')
                    if not df_temp.empty: lst.append(df_temp)
                
            # Dataset Integrado de Evasão (Arq_2, Arq_3, Arq_5, Arq_6, Arq_14, Arq_23)
            req_sheets = ['Arq_2', 'Arq_3', 'Arq_5', 'Arq_6', 'Arq_14', 'Arq_23']
            if all(s in xls.sheet_names for s in req_sheets):
                df_a2 = pd.read_excel(xls, sheet_name='Arq_2')[['ANO_FIM_EM']]
                df_a3 = pd.read_excel(xls, sheet_name='Arq_3')[['TP_PRES', 'CO_CURSO']]
                df_a5 = pd.read_excel(xls, sheet_name='Arq_5')[['TP_SEXO']]
                df_a6 = pd.read_excel(xls, sheet_name='Arq_6')[['NU_IDADE']]
                df_a14 = pd.read_excel(xls, sheet_name='Arq_14')[['QE_I08']]
                df_a23 = pd.read_excel(xls, sheet_name='Arq_23')[['QE_I17']]
                
                df_concat = pd.concat([df_a3, df_a2, df_a5, df_a6, df_a14, df_a23], axis=1)
                df_ev = pd.merge(df_concat, curso_map, on='CO_CURSO', how='inner')
                
                # Marcar Evasão: alunos que não têm presença confirmada (diferente de 555 ou 333)
                df_ev['EVADIU'] = df_ev['TP_PRES'].apply(lambda x: True if str(x) not in ['555', '333', '555.0', '333.0'] else False)
                if not df_ev.empty: all_evasao.append(df_ev)
                
        except Exception as e:
            continue
            
    return {
        'sexo': pd.concat(all_sexo, ignore_index=True) if all_sexo else pd.DataFrame(),
        'idade': pd.concat(all_idade, ignore_index=True) if all_idade else pd.DataFrame(),
        'raca': pd.concat(all_raca, ignore_index=True) if all_raca else pd.DataFrame(),
        'renda': pd.concat(all_renda, ignore_index=True) if all_renda else pd.DataFrame(),
        'evasao': pd.concat(all_evasao, ignore_index=True) if all_evasao else pd.DataFrame(),
        'pai': pd.concat(all_pai, ignore_index=True) if all_pai else pd.DataFrame(),
        'mae': pd.concat(all_mae, ignore_index=True) if all_mae else pd.DataFrame(),
        'trab': pd.concat(all_trab, ignore_index=True) if all_trab else pd.DataFrame(),
        'bolsa': pd.concat(all_bolsa, ignore_index=True) if all_bolsa else pd.DataFrame(),
        'cota': pd.concat(all_cota, ignore_index=True) if all_cota else pd.DataFrame(),
        'estudo': pd.concat(all_estudo, ignore_index=True) if all_estudo else pd.DataFrame(),
        'motiv_c': pd.concat(all_motiv_c, ignore_index=True) if all_motiv_c else pd.DataFrame(),
        'motiv_i': pd.concat(all_motiv_i, ignore_index=True) if all_motiv_i else pd.DataFrame(),
        'arq4': pd.concat(all_arq4, ignore_index=True) if all_arq4 else pd.DataFrame()
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
def render_filters(source_data):
    st.markdown('<div class="fade-in" style="margin-top: 1rem; margin-bottom: 1rem;"><span style="background: linear-gradient(135deg, #1a5722, #32A041); color: white; padding: 6px 16px; border-radius: 20px; font-weight: 800; font-size: 0.85rem; letter-spacing: 1px; box-shadow: 0 4px 10px rgba(50,160,65,0.3);">⚙️ FILTROS DE PESQUISA</span></div>', unsafe_allow_html=True)
    
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
        col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
        with col_b1:
            if st.button("🚀 NOTAS", use_container_width=True, type="primary"):
                st.session_state.page = 'dashboard'
                st.rerun()
        with col_b2:
            if st.button("👥 CURSOS", use_container_width=True):
                st.session_state.page = 'cursos'
                st.rerun()
        with col_b3:
            if st.button("🎓 ESTUDANTE", use_container_width=True):
                st.session_state.page = 'estudantes'
                st.rerun()
        with col_b4:
            if st.button("⚠️ EVASÃO", use_container_width=True):
                st.session_state.page = 'evasao'
                st.rerun()
        with col_b5:
            if st.button("📝 QUEST. ESTUDANTE", use_container_width=True):
                st.session_state.page = 'questionario'
                st.rerun()

def show_dashboard():
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True, key='back_bt_dash'):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown("""
        <div class="fade-in" style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
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
        <div class="fade-in" style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
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
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter")
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
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", coloraxis_showscale=False)
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

def show_evasao():
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True, key='back_bt_evs'):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
            <p style="color: #32A041; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;">Cruzamento Demográfico e Abstenção</p>
            <h1 class="main-title" style="font-size: 3rem;">ANÁLISE DE EVASÃO</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider" style="margin: 20px 0;">', unsafe_allow_html=True)

    filtered_data = render_filters(data)
    st.markdown("<br>", unsafe_allow_html=True)
    
    cursos_filtrados = filtered_data['CO_CURSO'].unique().tolist()
    anos_filtrados = filtered_data['ANO'].unique().tolist()
    
    df_ev = microdados['evasao']
    if df_ev.empty:
        st.warning("Sem dados pré-processados de evasão disponíveis para esta visão.")
        return
        
    df_ev = df_ev[(df_ev['CO_CURSO'].isin(cursos_filtrados)) & (df_ev['ANO'].isin(anos_filtrados))]
    
    if df_ev.empty:
        st.info("Nenhum dado de evasão disponível neste filtro.")
        return

    df_taxa_campus = df_ev.groupby('CENTRO')['EVADIU'].mean().reset_index()
    df_taxa_campus['EVADIU'] = (df_taxa_campus['EVADIU'] * 100).round(1)
    df_taxa_campus = df_taxa_campus.sort_values('EVADIU', ascending=False)
    
    df_taxa_curso = df_ev.groupby('NOME DO CURSO')['EVADIU'].mean().reset_index()
    df_taxa_curso['EVADIU'] = (df_taxa_curso['EVADIU'] * 100).round(1)
    df_taxa_curso = df_taxa_curso.sort_values('EVADIU', ascending=False).head(15) # Top 15 maiores evasões

    st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem;">Taxa Global de Evasão (%)</div>', unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2, gap="large")
    
    with col_c1:
        st.markdown('<div style="text-align:center; font-weight:600; margin-bottom: 10px;">Por Campus</div>', unsafe_allow_html=True)
        fig_campus = px.bar(df_taxa_campus, x='CENTRO', y='EVADIU', text='EVADIU', color='EVADIU', color_continuous_scale='Reds')
        fig_campus.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=1.5, marker_line_color='white', opacity=0.95)
        fig_campus.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", coloraxis_showscale=False, yaxis_title="% Evasão", hoverlabel={"bgcolor": "white", "font_size": 13, "font_family": "Inter", "bordercolor": "#d62828"})
        fig_campus.update_yaxes(range=[0, max(df_taxa_campus['EVADIU'] + 5) if not df_taxa_campus.empty else 100])
        st.plotly_chart(fig_campus, use_container_width=True)

    with col_c2:
        st.markdown('<div style="text-align:center; font-weight:600; margin-bottom: 10px;">Por Curso (Top 15 Maiores do Filtro)</div>', unsafe_allow_html=True)
        fig_curso = px.bar(df_taxa_curso, x='NOME DO CURSO', y='EVADIU', text='EVADIU', color_discrete_sequence=['#e63946'])
        fig_curso.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=1.5, marker_line_color='white', opacity=0.95)
        fig_curso.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", yaxis_title="% Evasão", hoverlabel={"bgcolor": "white", "font_size": 13, "font_family": "Inter", "bordercolor": "#e63946"})
        fig_curso.update_yaxes(range=[0, max(df_taxa_curso['EVADIU'] + 5) if not df_taxa_curso.empty else 100])
        st.plotly_chart(fig_curso, use_container_width=True)

    st.markdown("<br><hr class='custom-divider'><br>", unsafe_allow_html=True)
    st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem;">Perfil dos Estudantes Evadidos</div>', unsafe_allow_html=True)
    
    # Filtrar apenas alunos evadidos para os gráficos de perfil
    df_evadidos = df_ev[df_ev['EVADIU'] == True].copy()
    
    if df_evadidos.empty:
        st.success("Não houve nenhum registro de evasão sob este filtro!")
        return

    col_e1, col_e2 = st.columns(2, gap="large")
    
    with col_e1:
        st.markdown('<div style="text-align:center; font-weight:600; margin-bottom: 10px;">Idade dos Alunos (Frequência)</div>', unsafe_allow_html=True)
        df_evadidos['NU_IDADE'] = pd.to_numeric(df_evadidos['NU_IDADE'], errors='coerce')
        idade_clean = df_evadidos.dropna(subset=['NU_IDADE'])
        if not idade_clean.empty:
            media_idade = idade_clean['NU_IDADE'].mean()
            fig_i = px.histogram(idade_clean, x='NU_IDADE', nbins=15, color_discrete_sequence=['#d62828'])
            fig_i.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
            fig_i.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", xaxis_title="Idade", hoverlabel={"bgcolor": "white", "font_size": 13, "font_family": "Inter", "bordercolor": "#d62828"})
            st.plotly_chart(fig_i, use_container_width=True)
            st.markdown(f'<div style="text-align:center;"><div class="kpi-card"><div class="kpi-title">Perfil Etário dos Evadidos</div><div class="kpi-value">{media_idade:.1f}<span class="kpi-unit">anos (Média)</span></div></div></div>', unsafe_allow_html=True)
        else:
            st.info("Sem dados de idade preenchidos.")

    with col_e2:
        st.markdown('<div style="text-align:center; font-weight:600; margin-bottom: 10px;">Situação Financeira (Frequência)</div>', unsafe_allow_html=True)
        dict_renda = {'A': 'Até 1,5 SM', 'B': '1,5 a 3 SM', 'C': '3 a 4,5 SM', 'D': '4,5 a 6 SM', 'E': '6 a 10 SM', 'F': '10 a 30 SM', 'G': 'Acima 30 SM'}
        df_evadidos['Renda'] = df_evadidos['QE_I08'].map(dict_renda)
        renda_counts = df_evadidos['Renda'].value_counts().reset_index()
        renda_counts.columns = ['Renda', 'Qtd']
        
        ordem_renda = ['Acima 30 SM', '10 a 30 SM', '6 a 10 SM', '4,5 a 6 SM', '3 a 4,5 SM', '1,5 a 3 SM', 'Até 1,5 SM']
        renda_counts['Renda'] = pd.Categorical(renda_counts['Renda'], categories=ordem_renda, ordered=True)
        renda_counts = renda_counts.sort_values('Renda')
        
        fig_r = px.bar(renda_counts, x='Qtd', y='Renda', orientation='h', color_discrete_sequence=['#f77f00'])
        fig_r.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
        fig_r.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", xaxis_title="Estudantes", hoverlabel={"bgcolor": "white", "font_size": 13, "font_family": "Inter", "bordercolor": "#f77f00"})
        st.plotly_chart(fig_r, use_container_width=True)

    col_e3, col_e4 = st.columns(2, gap="large")
    
    with col_e3:
        st.markdown('<div style="text-align:center; font-weight:600; margin-bottom: 10px; margin-top:20px;">Tempo desde a conclusão do Ens. Médio</div>', unsafe_allow_html=True)
        df_evadidos['ANO_FIM_EM'] = pd.to_numeric(df_evadidos['ANO_FIM_EM'], errors='coerce')
        df_evadidos['ANO'] = pd.to_numeric(df_evadidos['ANO'], errors='coerce')
        
        df_tempo = df_evadidos.dropna(subset=['ANO_FIM_EM', 'ANO']).copy()
        df_tempo['TEMPO_EM'] = (df_tempo['ANO'] - df_tempo['ANO_FIM_EM']).clip(lower=0)
        
        if not df_tempo.empty:
            media_tempo = df_tempo['TEMPO_EM'].mean()
            fig_t = px.histogram(df_tempo, x='TEMPO_EM', nbins=10, color_discrete_sequence=['#fcbf49'])
            fig_t.update_traces(marker_line_width=1.5, marker_line_color='white', opacity=0.9)
            fig_t.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", xaxis_title="Anos de Diferença", hoverlabel={"bgcolor": "white", "font_size": 13, "font_family": "Inter", "bordercolor": "#fcbf49"})
            st.plotly_chart(fig_t, use_container_width=True)
            st.markdown(f'<div style="text-align:center;"><div class="kpi-card"><div class="kpi-title">Defasagem desde o Ens. Médio</div><div class="kpi-value">{media_tempo:.1f}<span class="kpi-unit">anos</span></div></div></div>', unsafe_allow_html=True)
        else:
            st.info("Sem dados de final de EM preenchidos.")
            
    with col_e4:
        st.markdown('<div style="text-align:center; font-weight:600; margin-bottom: 10px; margin-top:20px;">Tipo de Escola no Ens. Médio</div>', unsafe_allow_html=True)
        dict_tipo = {'A':'Toda em Escola Pública', 'B':'Toda em Escola Privada', 'C':'Toda no exterior', 'D':'Maior parte em Pública', 'E':'Maior parte em Privada', 'F':'Parte no Brasil e exterior'}
        df_evadidos['Tipo_EM'] = df_evadidos['QE_I17'].map(dict_tipo)
        tipo_counts = df_evadidos['Tipo_EM'].value_counts().reset_index()
        tipo_counts.columns = ['Tipo', 'Qtd']
        
        if not tipo_counts.empty:
            fig_tipo = px.pie(tipo_counts, values='Qtd', names='Tipo', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_tipo.update_traces(textposition='inside', textinfo='percent+label', marker={"line": {"color": "white", "width": 2}})
            fig_tipo.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white', font_family="Inter", showlegend=False, hoverlabel={"bgcolor": "white", "font_size": 13, "font_family": "Inter"})
            st.plotly_chart(fig_tipo, use_container_width=True)
        else:
            st.info("Sem dados de tipo de EM preenchidos.")


def show_questionario():
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Voltar ao Início", use_container_width=True, key='back_bt_quest'):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
            <p style="color: #32A041; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;">Avaliação do Processo Formativo</p>
            <h1 class="main-title" style="font-size: 3rem;">QUESTIONÁRIO DO ESTUDANTE</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider" style="margin: 20px 0;">', unsafe_allow_html=True)

    filtered_data = render_filters(data)
    st.markdown("<br>", unsafe_allow_html=True)
    
    cursos_filtrados = filtered_data['CO_CURSO'].unique().tolist()
    anos_filtrados = filtered_data['ANO'].unique().tolist()
    
    df_arq4 = microdados.get('arq4', pd.DataFrame())
    if df_arq4.empty:
        st.warning("Sem dados pré-processados de Arq_4 disponíveis.")
        return
        
    df_arq4 = df_arq4[(df_arq4['CO_CURSO'].isin(cursos_filtrados)) & (df_arq4['ANO'].isin(anos_filtrados))]
    
    if df_arq4.empty:
        st.info("Nenhum dado do questionário disponível neste filtro.")
        return

    # Dicionário Extraído das Imagens fornecidas pelo usuário
    dict_questoes = {
        'QE_I27': 'As disciplinas cursadas contribuíram para sua formação integral, como cidadão e profissional.',
        'QE_I28': 'Os conteúdos abordados nas disciplinas do curso favoreceram sua atuação em estágios ou em atividades de iniciação profissional.',
        'QE_I29': 'As metodologias de ensino utilizadas no curso desafiaram você a aprofundar conhecimentos e desenvolver competências reflexivas e críticas.',
        'QE_I30': 'O curso propiciou experiências de aprendizagem inovadoras.',
        'QE_I31': 'O curso contribuiu para o desenvolvimento da sua consciência ética para o exercício profissional.',
        'QE_I32': 'No curso você teve oportunidade de aprender a trabalhar em equipe.',
        'QE_I33': 'O curso possibilitou aumentar sua capacidade de reflexão e argumentação.',
        'QE_I39': 'Os professores demonstraram domínio dos conteúdos abordados nas disciplinas.',
        'QE_I41': "Os professores utilizaram tecnologias da informação e comunicação (TIC's) como estratégia de ensino..."
    }

    # Discover all QE_I columns available in Arq_4 (Likert scale 1-6)
    qe_cols = [str(c) for c in df_arq4.columns if str(c).startswith('QE_I')]
    qe_cols.sort()
    
    # Montar dropdown customizado
    opcoes = []
    for c in qe_cols:
        texto = dict_questoes.get(c, f"Questão {c.replace('QE_I', '')} (Sem enunciado cadastrado)")
        opcoes.append(f"{c} - {texto}")
        
    st.markdown('<div class="indicadores-title" style="text-align:center; font-size: 1.5rem;">QUESTÕES DO ESTUDANTE</div>', unsafe_allow_html=True)
    selecionada = st.selectbox("Selecione a pergunta para visualizar o detalhamento:", opcoes)
    col_var = selecionada.split(" - ")[0]
    
    # Calcula os KPIs
    inscritos = filtered_data['INSCRITOS'].sum()
    participantes = filtered_data['PRESENTES'].sum()

    col_q1, col_kpi = st.columns([3, 1], gap="large")
    
    with col_q1:
        st.markdown('<div style="background-color: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.04);">', unsafe_allow_html=True)
        st.markdown('<div class="filter-header" style="color: #103d6d; font-size: 1.2rem; border-bottom: 2px solid rgba(16,61,109,0.2);">ENUNCIADO DA QUESTÃO:</div>', unsafe_allow_html=True)
        texto_selecionada = selecionada.split(" - ", 1)[1]
        st.markdown(f'<p style="color: #222; font-size: 1.5rem; font-weight: 600; line-height: 1.4; margin-top: 15px; margin-bottom: 30px;">{texto_selecionada}</p>', unsafe_allow_html=True)
        
        # Mapeamento Likert expandido
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
        
        # Converte nulos, '.' ou espaços em branco para código 9
        df_arq4[col_var] = pd.to_numeric(df_arq4[col_var], errors='coerce').fillna(9)
        # Filtra respostas catalogadas (1 a 9)
        df_resp = df_arq4[df_arq4[col_var].isin([1, 2, 3, 4, 5, 6, 7, 8, 9])].copy()
        
        if df_resp.empty:
            st.info("Sem dados disponíveis para este filtro.")
        else:
            contagem = df_resp[col_var].value_counts().reset_index()
            contagem.columns = ['Resposta', 'Quantidade']
            
            # Garantir opções essenciais: 1 a 6 e 9 (Não respondeu) sempre. 7 e 8 se houver respostas.
            opcoes_exibir = [1, 2, 3, 4, 5, 6, 9]
            for opc in [7, 8]:
                if opc in contagem['Resposta'].values and contagem[contagem['Resposta'] == opc]['Quantidade'].iloc[0] > 0:
                    opcoes_exibir.append(opc)
            opcoes_exibir.sort()
            
            para_plot = pd.DataFrame({'Resposta': opcoes_exibir, 'Resposta_Texto': [dict_likert[i] for i in opcoes_exibir]})
            para_plot = pd.merge(para_plot, contagem[['Resposta', 'Quantidade']], on='Resposta', how='left').fillna(0)
            
            total_alunos = len(df_arq4)
            para_plot['Percentual'] = (para_plot['Quantidade'] / total_alunos) * 100 if total_alunos > 0 else 0
            para_plot['Texto_Eixo'] = para_plot['Resposta_Texto'].str.replace(' ', '<br>')
            para_plot['Rotulo'] = para_plot.apply(lambda row: f"<b>{row['Percentual']:.0f}%</b><br><span style='font-size:11px'>({int(row['Quantidade'])})</span>", axis=1)
            
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
                margin=dict(t=30, b=0, l=0, r=0)
            )
            fig.update_yaxes(showticklabels=False, range=[0, max(para_plot['Percentual'] + 10)], showgrid=False)
            fig.update_xaxes(tickfont=dict(size=12, color='#103d6d', weight='bold'))
            st.plotly_chart(fig, use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_kpi:
        st.markdown(f'''
        <div style="background-color: white; border-radius: 12px; padding: 25px 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.06); margin-bottom: 25px; border-top: 5px solid #103d6d;">
            <div style="font-size: 0.95rem; font-weight: 800; color: #103d6d; text-transform: uppercase;">CONCLUINTES<br>INSCRITOS</div>
            <div style="font-size: 3.5rem; font-weight: 900; color: #103d6d; line-height: 1.2;">{int(inscritos)}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
        <div style="background-color: white; border-radius: 12px; padding: 25px 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.06); border-top: 5px solid #103d6d;">
            <div style="font-size: 0.95rem; font-weight: 800; color: #103d6d; text-transform: uppercase;">CONCLUINTES<br>PARTICIPANTES</div>
            <div style="font-size: 3.5rem; font-weight: 900; color: #103d6d; line-height: 1.2;">{int(participantes)}</div>
        </div>
        ''', unsafe_allow_html=True)

# --- ROUTER (GERENCIADOR DE ESTADO) ---

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'dashboard':
    show_dashboard()
elif st.session_state.page == 'cursos':
    show_cursos()
elif st.session_state.page == 'estudantes':
    show_estudantes()
elif st.session_state.page == 'evasao':
    show_evasao()
elif st.session_state.page == 'questionario':
    show_questionario()
