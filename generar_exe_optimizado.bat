@echo off
echo ===============================================================
echo Generador de Ejecutable Optimizado - Deducciones Fiscales I+D+i
echo ===============================================================
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

REM Ejecutar script de generación optimizado
echo.
echo Generando ejecutable optimizado...
python optimized_build_exe.py

REM Desactivar el entorno virtual
call venv\Scripts\deactivate.bat

echo.
echo Si no hay errores, el ejecutable y los archivos de distribución se encuentran en la carpeta "dist"
echo.
echo Para distribuir la aplicación, simplemente copie todo el contenido de la carpeta "dist"
echo a una memoria USB o a los ordenadores destino.
echo.
pause
