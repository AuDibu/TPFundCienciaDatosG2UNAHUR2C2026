@echo off
setlocal
title TP Fundamentos - Ejecucion
cd /d "%~dp0" || exit /b 1

echo [run.bat] Inicio del lanzador
echo [run.bat] Directorio del proyecto: %cd%

if not exist ".venv\Scripts\python.exe" (
    echo [run.bat] Creando entorno virtual en .venv
    python -m venv .venv
    if errorlevel 1 exit /b 1
) else (
    echo [run.bat] Entorno virtual existente detectado en .venv
)

echo [run.bat] Activando entorno virtual
call ".venv\Scripts\activate.bat"
if errorlevel 1 exit /b 1

echo [run.bat] Instalando dependencias desde requirements.txt
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo [run.bat] Lanzando main.py
python main.py
echo [run.bat] Proceso finalizado
exit /b %errorlevel%
