$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath('Desktop')
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\Painel ENADE.lnk")
$Shortcut.TargetPath = "C:\Users\professor\Desktop\IC - Análise dos Indicadores Educacionais do Ifes - Wagner\Antigravity\Iniciar_Painel_ENADE.bat"
$Shortcut.WorkingDirectory = "C:\Users\professor\Desktop\IC - Análise dos Indicadores Educacionais do Ifes - Wagner\Antigravity"
$Shortcut.IconLocation = "C:\Users\professor\Desktop\IC - Análise dos Indicadores Educacionais do Ifes - Wagner\Antigravity\ifes-horizontal-cor.png"
$Shortcut.Save()
