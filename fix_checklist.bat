@echo off
echo ========================================================
echo Herramienta de corrección para la lista de verificación
echo ========================================================
echo.

echo Creando copia de seguridad de los archivos originales...
copy app.py app.py.bak
copy templates\project_structure\simple_checklist.html templates\project_structure\simple_checklist.html.bak

echo.
echo Modificando plantilla simple_checklist.html...
echo Reemplazando referencias a "items" por "checklist_items"...

powershell -Command "(Get-Content templates\project_structure\simple_checklist.html) -replace 'section.items', 'section.checklist_items' | Set-Content templates\project_structure\simple_checklist.html"
powershell -Command "(Get-Content templates\project_structure\simple_checklist.html) -replace 'section.items\|length', 'section.checklist_items\|length' | Set-Content templates\project_structure\simple_checklist.html"

echo.
echo Modificando app.py...
echo Añadiendo código para renombrar items a checklist_items...

echo Código para añadir antes de renderizar:
echo     # Renombrar 'items' a 'checklist_items' para evitar conflictos
echo     for section in sections:
echo         if isinstance(section, dict) and 'items' in section:
echo             section['checklist_items'] = section.pop('items')

echo.
echo Corrección completada. Por favor, edita manualmente app.py
echo y añade este código justo antes de renderizar la plantilla (cerca de la línea 250)
echo.
echo También asegúrate de usar guide._default_checklist() en lugar de guide.checklist
echo para cargar directamente la lista predeterminada.
echo.
echo Puedes ver un ejemplo simplificado del código en app.py.mini
echo.
pause
