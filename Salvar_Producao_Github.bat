@echo off
echo ===================================================
echo   SALVAR APENAS DADOS DE PRODUCAO NO GITHUB
echo ===================================================
echo Este script adiciona APENAS os arquivos necessarios
echo para o Painel Enade rodar no Streamlit.
echo.

:: Remove do index arquivos deletados
git add -u

:: Adiciona explicitamente os arquivos essenciais
git add app.py
git add views/
git add .streamlit/
git add requirements.txt
git add qe_dictionary.py
git add "Dados Cursos EMEC finalizado.xlsx"
git add ifes-horizontal-cor.png
git add Enade_2017_Ifes.xlsx
git add Enade_2018_Ifes.xlsx
git add Enade_2019_Ifes.xlsx
git add Enade_2021_Ifes.xlsx
git add Enade_2022_Ifes.xlsx
git add .gitignore
git add Iniciar_Painel_ENADE.bat
git add Salvar_No_Github.bat
git add Salvar_Producao_Github.bat

echo.
set /p comment="Digite uma mensagem para o backup (ou pressione Enter para data atual): "
if "%comment%"=="" (
    for /f "tokens=1-4 delims=/ " %%i in ("%date%") do set d=%%i/%%j/%%k
    for /f "tokens=1-3 delims=:," %%i in ("%time%") do set t=%%i:%%j:%%k
    set comment=Atualizacao Producao - %d% %t%
)

git commit -m "%comment%"

echo.
echo Enviando para a nuvem (GitHub)...
git push

echo ===================================================
echo   Prontinho! Painel salvo com sucesso!
echo ===================================================
pause
