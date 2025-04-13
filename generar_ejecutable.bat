@echo off
echo Generador de Ejecutable - Herramienta de Deducciones Fiscales I+D+i
echo ================================================================
echo.

REM Cambiar al directorio donde se encuentra este script
cd /d "%~dp0"

REM Mostrar el directorio actual para debug
echo Directorio actual: %CD%
echo.

REM Verificar si el entorno virtual existe
if not exist venv\ (
    echo ERROR: No se encuentra el entorno virtual.
    echo Por favor, ejecute primero "instalar_y_ejecutar.bat"
    pause
    exit /b 1
)

REM Activar el entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar si PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Instalando PyInstaller...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: No se pudo instalar PyInstaller.
        pause
        exit /b 1
    )
)

REM Ejecutar script de generación
echo.
echo Generando ejecutable...
python build_exe.py

REM Desactivar el entorno virtual
call venv\Scripts\deactivate.bat

echo.
echo Si no hay errores, el ejecutable se encuentra en la carpeta "dist"
echo.
pause
