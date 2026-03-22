@echo off
chcp 65001 > nul
title Backup - Painel ENADE

echo =========================================
echo   Salvando as alteracoes no GitHub...
echo =========================================
echo.

:: Vai para a pasta nativa do script
cd /d "%~dp0"

:: Forca o nome da branch inicial como main
git branch -M main 2>nul || echo Inicializando o historico...

:: Adiciona todas as modificacoes atuais
git add .

:: Cria o 'pacote' da modificacao atual com a data/hora local
git commit -m "Backup automatico - %date% %time%"

echo.
echo Enviando para a nuvem...
git push -u origin main

echo.
echo =========================================
echo   Prontinho! Backups salvos com sucesso!
echo =========================================
echo (Da proxima vez, o login ficara salvo automaticamente).
echo.

pause
