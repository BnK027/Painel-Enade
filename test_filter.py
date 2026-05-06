import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from app import load_data, render_filters
# We need to mock st.session_state
import streamlit as st
st.session_state = {'ano_selecionado': '2018', 'filtro_campus': [], 'filtro_nota': [], 'filtro_curso': 'Todos', 'filtro_mod': 'Todos'}

data = load_data()
print('Total data shape:', data.shape)
print('ANO dtype:', data['ANO'].dtype)
print('Unique ANOs in data:', data['ANO'].unique())

filtered = data.copy()
ano_fixo = '2018'
if str(filtered['ANO'].dtype) == 'object':
    filtered = filtered[filtered['ANO'] == str(ano_fixo)]
else:
    try: filtered = filtered[filtered['ANO'] == float(ano_fixo)]
    except Exception as e: print('Error', e)

print('Filtered data shape for 2018:', filtered.shape)
print('Unique ANOs in filtered:', filtered['ANO'].unique())
print('Unique courses in filtered:', filtered['NOME DO CURSO'].unique())
