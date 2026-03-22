@echo off
title Painel ENADE - Servidor Streamlit
echo =======================================================
echo Iniciando o servidor local do Painel ENADE...
echo Por favor, nao feche esta janela negra enquanto estiver 
echo utilizando o painel no seu navegador.
echo =======================================================
cd /d "%~dp0"
py -m streamlit run app.py
pause
