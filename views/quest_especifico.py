import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_tab_quest_especifico(microdados, filtered_data):
    """
    Renderiza a aba de Questionário Específico (CE) - acertos e erros por questão,
    isolado por curso selecionado.
    """
    st.markdown(
        '<div class="indicadores-title" style="text-align:center; font-size: 1.5rem; margin-top: 1rem;">'
        '🎯 Desempenho por Questão — Componente Específico (CE)'
        '</div>',
        unsafe_allow_html=True
    )

    cursos_filtrados = filtered_data['CO_CURSO'].unique().tolist()
    anos_filtrados = filtered_data['ANO'].unique().tolist()

    df_ce = microdados.get('ce_respostas', pd.DataFrame())

    if df_ce.empty:
        st.warning("Dados de desempenho por questão não disponíveis para este ano/filtro.")
        return

    # Filtra pelo curso/ano selecionado
    df_ce = df_ce[df_ce['CO_CURSO'].isin(cursos_filtrados) & df_ce['ANO'].isin(anos_filtrados)]

    if df_ce.empty:
        st.info("Nenhum dado de questões CE disponível para o filtro selecionado.")
        return

    # --- Colunas de questões CE (Somente as que existem nos arquivos originais) ---
    ce_cols_all = [c for c in df_ce.columns if str(c).startswith('CE') and str(c)[2:].isdigit()]
    ce_cols_all.sort(key=lambda x: int(x[2:]))

    if not ce_cols_all:
        st.warning("Colunas de questões CE não encontradas nos dados.")
        return

    # --- Selector de Curso (obrigatório para CE não misturar cursos) ---
    cursos_disponiveis = df_ce[['CO_CURSO', 'NOME DO CURSO']].drop_duplicates()
    opcoes_curso = {
        f"{row['NOME DO CURSO']} (Código {row['CO_CURSO']})": row['CO_CURSO']
        for _, row in cursos_disponiveis.iterrows()
    }

    if len(opcoes_curso) > 1:
        st.info(
            "⚠️ Cada curso possui seu próprio Componente Específico. "
            "Selecione um curso para visualizar as questões corretas para ele."
        )
        curso_selecionado_label = st.selectbox(
            "Selecione o Curso para análise:",
            options=list(opcoes_curso.keys()),
            key="ce_curso_select"
        )
        curso_co = opcoes_curso[curso_selecionado_label]
    elif len(opcoes_curso) == 1:
        curso_co = list(opcoes_curso.values())[0]
        curso_selecionado_label = list(opcoes_curso.keys())[0]
    else:
        st.warning("Nenhum curso encontrado para o filtro atual.")
        return

    df_curso = df_ce[df_ce['CO_CURSO'] == curso_co].copy()
    nome_curso = curso_selecionado_label.split(" (Código")[0]
    total_alunos = len(df_curso)

    # Oculta colunas CE que são inteiramente NaN/nulas para este curso/ano
    # (Ex: CE28 e CE29 não devem aparecer em 2022)
    ce_cols = [q for q in ce_cols_all if df_curso[q].notna().any() and not (df_curso[q].astype(str).str.strip() == '').all()]

    if not ce_cols:
        st.info("Nenhuma resposta válida para o Componente Específico encontrada.")
        return

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f7f1, #e8f5ea); border-radius: 16px;
         padding: 1rem 1.5rem; border-left: 6px solid #2c8c44; margin-bottom: 1.5rem;">
      <span style="font-size: 0.8rem; color: #2c8c44; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">Curso Analisado</span><br>
      <span style="font-size: 1.3rem; font-weight: 700; color: #0f2c16;">{nome_curso}</span>
      <span style="float: right; background: #103d6d; color: white; padding: 4px 14px; border-radius: 20px;
           font-weight: 700; font-size: 0.9rem;">{total_alunos} alunos</span>
    </div>
    """, unsafe_allow_html=True)

    # --- Cálculo de acertos/erros por questão ---
    resultados = []
    for q in ce_cols:
        col_vals = df_curso[q]
        # Valores válidos: 1 = acerto, 0 = erro, X = anulada, 9 = ausente/branco, B = em branco, M = marcação múltipla
        total = len(col_vals)
        # Converte para comparable
        vals_str = col_vals.astype(str).str.strip().str.upper()
        anuladas = (vals_str == 'X').sum()
        ausentes = ((vals_str == '9') | (vals_str == 'B')).sum()
        multipla = (vals_str == 'M').sum()

        # Converte para numérico somente as respostas válidas (0 ou 1)
        vals_num = pd.to_numeric(col_vals, errors='coerce')
        validas = vals_num.isin([0, 1])
        acertos = (vals_num[validas] == 1).sum()
        erros = (vals_num[validas] == 0).sum()
        validos_count = validas.sum()

        pct_acerto = (acertos / validos_count * 100) if validos_count > 0 else 0
        pct_erro = (erros / validos_count * 100) if validos_count > 0 else 0

        resultados.append({
            'Questão': q,
            'Acertos': int(acertos),
            'Erros': int(erros),
            'Anuladas': int(anuladas),
            'Ausentes': int(ausentes),
            '% Acerto': round(pct_acerto, 1),
            '% Erro': round(pct_erro, 1),
            'Total Válido': int(validos_count)
        })

    df_res = pd.DataFrame(resultados)

    # ─── KPIs resumo ───
    if not df_res.empty:
        media_acerto = df_res['% Acerto'].mean()
        q_mais_acertada = df_res.loc[df_res['Acertos'].idxmax(), 'Questão']
        q_mais_errada = df_res.loc[df_res['Erros'].idxmax(), 'Questão']

        kc1, kc2, kc3 = st.columns(3)
        with kc1:
            st.markdown(f'''<div class="kpi-card">
                <p class="kpi-title">Média de Acertos</p>
                <p class="kpi-value">{media_acerto:.0f}%</p>
            </div>''', unsafe_allow_html=True)
        with kc2:
            st.markdown(f'''<div class="kpi-card" style="border-left-color: #2c8c44;">
                <p class="kpi-title">Questão Mais Acertada</p>
                <p class="kpi-value">{q_mais_acertada}</p>
            </div>''', unsafe_allow_html=True)
        with kc3:
            st.markdown(f'''<div class="kpi-card" style="border-left-color: #d9534f;">
                <p class="kpi-title">Questão Mais Errada</p>
                <p class="kpi-value" style="color: #d9534f;">{q_mais_errada}</p>
            </div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ─── Gráfico de Acertos vs Erros ───
        df_plot = df_res.melt(
            id_vars='Questão',
            value_vars=['Acertos', 'Erros'],
            var_name='Resultado',
            value_name='Quantidade'
        )
        df_plot['% Total'] = df_plot.apply(
            lambda row: df_res.loc[df_res['Questão'] == row['Questão'], f"% {'Acerto' if row['Resultado'] == 'Acertos' else 'Erro'}"].values[0],
            axis=1
        )
        df_plot['Rótulo'] = df_plot.apply(
            lambda row: f"<b>{row['% Total']:.0f}%</b><br><span style='font-size:10px'>({int(row['Quantidade'])})</span>",
            axis=1
        )

        fig = px.bar(
            df_plot,
            x='Questão',
            y='Quantidade',
            color='Resultado',
            barmode='group',
            text='Rótulo',
            color_discrete_map={'Acertos': '#2c8c44', 'Erros': '#d9534f'},
            labels={'Quantidade': 'Nº de Alunos', 'Questão': 'Questão CE'},
            category_orders={'Questão': ce_cols}
        )
        fig.update_traces(
            textposition='outside',
            textfont_size=11,
            cliponaxis=False
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Inter',
            legend_title_text='',
            margin=dict(t=50, b=80, l=0, r=0),
            height=520,
            xaxis=dict(tickangle=-45, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)')
        )
        st.plotly_chart(fig, use_container_width=True)

        # ─── Heatmap de % de acerto ───
        st.markdown(
            '<div class="indicadores-title" style="text-align:center; font-size: 1.2rem; margin-top: 1rem;">'
            '🗺️ Mapa de Calor — % de Acerto por Questão'
            '</div>',
            unsafe_allow_html=True
        )

        heatmap_vals = df_res.set_index('Questão')['% Acerto'].to_dict()
        z_vals = [[heatmap_vals[q] for q in ce_cols]]
        x_labels = ce_cols

        fig_heat = go.Figure(data=go.Heatmap(
            z=z_vals,
            x=x_labels,
            y=[nome_curso[:30]],
            colorscale=[
                [0.0, '#d9534f'],
                [0.5, '#f0ad4e'],
                [1.0, '#2c8c44']
            ],
            zmin=0,
            zmax=100,
            text=[[f"{heatmap_vals[q]:.0f}%" for q in ce_cols]],
            texttemplate='%{text}',
            showscale=True,
            colorbar=dict(title='% Acerto')
        ))
        fig_heat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Inter',
            height=200,
            margin=dict(t=20, b=60, l=0, r=80),
            xaxis=dict(tickangle=-45, tickfont=dict(size=11)),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        # ─── Tabela Detalhada ───
        with st.expander("📋 Ver tabela completa de resultados por questão"):
            df_display = df_res[['Questão', 'Acertos', '% Acerto', 'Erros', '% Erro', 'Anuladas', 'Ausentes', 'Total Válido']].copy()
            df_display['% Acerto'] = df_display['% Acerto'].map(lambda x: f"{x:.1f}%")
            df_display['% Erro'] = df_display['% Erro'].map(lambda x: f"{x:.1f}%")
            st.dataframe(df_display, hide_index=True, use_container_width=True)
