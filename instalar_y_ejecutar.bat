@echo off
echo Herramienta de Evaluacion de Deducciones Fiscales I+D+i
echo ======================================================
echo.

REM Cambiar al directorio donde se encuentra este script
cd /d "%~dp0"

REM Mostrar el directorio actual para debug
echo Directorio actual: %CD%
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python no está instalado o no se encuentra en el PATH.
    echo Por favor, instale Python 3.7 o superior desde https://www.python.org/downloads/
    echo Asegúrese de marcar la opción "Add Python to PATH" durante la instalación.
    echo.
    pause
    exit /b 1
)

REM Verificar si el entorno virtual existe y eliminarlo si es necesario
if exist venv\ (
    echo Eliminando entorno virtual anterior para evitar conflictos...
    rmdir /s /q venv
)

echo Creando nuevo entorno virtual...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo crear el entorno virtual.
    echo Por favor, asegúrese de tener instalado el módulo venv.
    echo Puede instalarlo con: python -m pip install --user virtualenv
    pause
    exit /b 1
)

REM Activar el entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar que existe el archivo requirements.txt
if not exist requirements.txt (
    echo ERROR: No se encuentra el archivo requirements.txt
    echo Directorio actual: %CD%
    echo Contenido del directorio:
    dir
    pause
    exit /b 1
)

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
pip install requests
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

REM Ejecutar la aplicación
echo.
echo Iniciando la aplicación...
python run.py

REM Desactivar el entorno virtual cuando se cierre la aplicación
call venv\Scripts\deactivate.bat

pause
