"""Helper para ranking Top 3 positivas/negativas do Questionário do Estudante."""

import streamlit as st
import pandas as pd


def _set_source(ano, new_source):
    """Callback para rastrear qual selectbox foi usado por último e limpar os inativos."""
    source_key = f'quest_source_{ano}'
    st.session_state[source_key] = new_source
    
    # Limpa a seleção visual dos outros campos para garantir que o usuário
    # possa re-selecionar opções sem sofrer com a inércia de estado do Streamlit.
    if new_source == 'all':
        st.session_state[f'quest_pos_{ano}'] = None
        st.session_state[f'quest_neg_{ano}'] = None
    elif new_source == 'top_pos':
        st.session_state[f'quest_neg_{ano}'] = None
    elif new_source == 'top_neg':
        st.session_state[f'quest_pos_{ano}'] = None


def render_question_selectors(df_arq4, df_arq43, qe_cols, dict_questoes, ano):
    """
    Calcula rankings positivo/negativo de todas as questões QE_I,
    renderiza 3 selectboxes (Todas, Top 3 Positivas, Top 3 Negativas)
    e retorna (col_var, texto_selecionada).
    """
    source_key = f'quest_source_{ano}'
    if source_key not in st.session_state:
        st.session_state[source_key] = 'all'

    # --- Monta opções do selectbox principal (todas) ---
    opcoes = []
    for c in qe_cols:
        texto = dict_questoes.get(c, f"Questão {c.replace('QE_I', '')} (Sem enunciado cadastrado)")
        opcoes.append(f"{c} - {texto}")

    if not opcoes:
        return None, None

    # --- Calcula % positivo e % negativo para cada questão ---
    rankings = []
    for col in qe_cols:
        series = None
        df_source = None
        if col in df_arq4.columns and not df_arq4.empty and not df_arq4[col].dropna().empty:
            series = pd.to_numeric(df_arq4[col], errors='coerce')
            df_source = df_arq4
        elif col in df_arq43.columns and not df_arq43.empty and not df_arq43[col].dropna().empty:
            series = pd.to_numeric(df_arq43[col], errors='coerce')
            df_source = df_arq43

        if series is None or df_source is None:
            continue

        total = len(df_source)
        if total == 0:
            continue

        series_filled = series.fillna(9)
        pos_count = len(series_filled[series_filled.isin([4, 5, 6])])
        neg_count = len(series_filled[series_filled.isin([1, 2, 3])])

        pos_pct = (pos_count / total) * 100
        neg_pct = (neg_count / total) * 100

        label = dict_questoes.get(col, f"Questão {col.replace('QE_I', '')}")
        rankings.append({'col': col, 'label': label, 'pos_pct': pos_pct, 'neg_pct': neg_pct})

    # --- Selectbox 1: Todas as questões ---
    selecionada_all = st.selectbox(
        "Selecione a pergunta para visualizar o detalhamento:",
        opcoes,
        key=f'quest_all_{ano}',
        on_change=_set_source, args=(ano, 'all')
    )

    # --- Top 3 Positivas e Negativas ---
    if rankings:
        df_rank = pd.DataFrame(rankings)
        top_pos = df_rank.nlargest(3, 'pos_pct')
        top_neg = df_rank.nlargest(3, 'neg_pct')

        pos_opts = [f"{r['col']} - {r['label']} ({r['pos_pct']:.0f}% concordam)" for _, r in top_pos.iterrows()]
        neg_opts = [f"{r['col']} - {r['label']} ({r['neg_pct']:.0f}% discordam)" for _, r in top_neg.iterrows()]

        col1, col2 = st.columns(2)
        with col1:
            sel_pos = st.selectbox(
                "🏆 Top 3 Avaliações Mais Positivas:",
                pos_opts,
                index=None,
                placeholder=pos_opts[0],
                key=f'quest_pos_{ano}',
                on_change=_set_source, args=(ano, 'top_pos')
            )
        with col2:
            sel_neg = st.selectbox(
                "⚠️ Top 3 Avaliações Mais Negativas:",
                neg_opts,
                index=None,
                placeholder=neg_opts[0],
                key=f'quest_neg_{ano}',
                on_change=_set_source, args=(ano, 'top_neg')
            )
    else:
        sel_pos = None
        sel_neg = None

    # --- Determina qual questão exibir ---
    source = st.session_state.get(source_key, 'all')

    if source == 'top_pos' and sel_pos:
        col_var = sel_pos.split(" - ")[0]
        texto = sel_pos.split(" - ", 1)[1]
    elif source == 'top_neg' and sel_neg:
        col_var = sel_neg.split(" - ")[0]
        texto = sel_neg.split(" - ", 1)[1]
    else:
        col_var = selecionada_all.split(" - ")[0]
        texto = selecionada_all.split(" - ", 1)[1]

    # Remove sufixo de percentual se existir (ex: "... (45% concordam)")
    if texto.endswith('%)'):
        texto = texto.rsplit(' (', 1)[0]

    return col_var, texto
