import os
import json
import uuid
import platform
import tempfile
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify

# Importar funciones de utilidad
from utils.helpers import get_app_dir, get_user_data_dir, format_currency, load_qualification_label, load_section_title

# Configuración de la aplicación
app = Flask(__name__)
app.secret_key = 'f4d3-d3ducc10n3s-f1sc4l3s'  # Usar una clave fija para evitar problemas al reiniciar
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora de duración
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
app.config['SESSION_USE_SIGNER'] = True

# Si no existe el directorio para la sesión, crearlo
if not os.path.exists(app.config['SESSION_FILE_DIR']):
    os.makedirs(app.config['SESSION_FILE_DIR'])

# Inicializar Flask-Session
from flask_session import Session
Session(app)

# Cargar configuraciones
def load_config(filename):
    try:
        # Obtener la ruta completa al archivo de configuración
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', filename)
        print(f"Cargando configuración: {filename}")
        print(f"Ruta completa: {config_path}")
        print(f"¿El archivo existe? {os.path.exists(config_path)}")
        
        if not os.path.exists(config_path):
            print(f"ADVERTENCIA: El archivo de configuración {filename} no existe")
            return {}
            
        with open(config_path, 'r', encoding='utf-8') as file:
            content = file.read()
            try:
                data = json.loads(content)
                print(f"Configuración {filename} cargada correctamente")
                return data
            except json.JSONDecodeError as e:
                print(f"ERROR: El archivo {filename} no contiene JSON válido: {e}")
                return {}
    except Exception as e:
        print(f"ERROR al cargar configuración {filename}: {e}")
        import traceback
        print(traceback.format_exc())
        return {}

# Rutas de la aplicación
@app.route('/')
def home():
    """Página de inicio principal"""
    return render_template('home.html')

# Rutas para financiación
@app.route('/financing-critical-aspects')
def financing_critical_aspects():
    """Muestra la página de consejos y aspectos críticos para la financiación"""
    return render_template('financing_critical_aspects.html')

# Rutas para la estructura de proyectos
@app.route('/estructura')
def project_structure_home():
    """Página principal de la herramienta de estructura de proyectos"""
    return render_template('project_structure/base_structure.html')

@app.route('/estructura/secciones')
def project_structure_sections():
    """Muestra la guía de secciones para proyectos de I+D+i"""
    # Cargar la información de las secciones del proyecto
    from models.project_structure import ProjectStructureGuide
    guide = ProjectStructureGuide()
    sections = guide.sections.get('sections', [])
    return render_template('project_structure/sections_guide.html', sections=sections)

@app.route('/estructura/metodologia')
def project_structure_methodology():
    """Muestra la guía de metodologías para proyectos de I+D+i"""
    # Cargar la información de metodologías
    from models.project_structure import ProjectStructureGuide
    guide = ProjectStructureGuide()
    methodologies = guide.methodologies.get('methodologies', [])
    return render_template('project_structure/methodology.html', methodologies=methodologies)

@app.route('/estructura/redaccion')
def project_structure_writing():
    """Muestra consejos de redacción para proyectos de I+D+i"""
    # Cargar consejos de redacción
    from models.project_structure import ProjectStructureGuide
    guide = ProjectStructureGuide()
    writing_tips = guide.writing_tips
    return render_template('project_structure/writing_tips.html', writing_tips=writing_tips)

@app.route('/estructura/presupuesto')
def project_structure_budget():
    """Muestra la guía para la planificación presupuestaria"""
    # Cargar información sobre categorías de presupuesto
    from models.project_structure import ProjectStructureGuide
    guide = ProjectStructureGuide()
    budget_categories = guide.budget_categories
    return render_template('project_structure/budget_planning.html', budget_categories=budget_categories)

@app.route('/estructura/checklist')
def project_structure_checklist():
    """Muestra la lista de verificación para proyectos de I+D+i"""
    # Cargar la lista de verificación desde el archivo JSON
    try:
        print("\n===== CARGANDO LISTA DE VERIFICACIÓN =====")
        
        # Cargar la lista de verificación directamente desde la lista predeterminada
        from models.project_structure import ProjectStructureGuide
        guide = ProjectStructureGuide()
        
        print("Cargando directamente la lista predeterminada para evitar problemas...")
        checklist_data = guide._default_checklist()  # Usamos directamente la lista predeterminada
        print(f"Tipo de datos recibidos: {type(checklist_data)}")
        
        # Asegurar que todas las secciones usen 'checklist_items' en lugar de 'items'
        if isinstance(checklist_data, dict) and 'sections' in checklist_data:
            sections = checklist_data['sections']
            for section in sections:
                if isinstance(section, dict) and 'items' in section:
                    section['checklist_items'] = section.pop('items')
        
        if checklist_data and isinstance(checklist_data, dict) and 'sections' in checklist_data:
            sections = checklist_data['sections']
            print(f"Secciones cargadas correctamente: {len(sections)}")
            
            # Si detectamos que hay un problema con las secciones (están vacías o no tienen items),
            # intentemos cargar la lista por defecto directamente
            section_items_count = 0
            for section in sections:
                if isinstance(section, dict):
                    if 'checklist_items' in section and isinstance(section['checklist_items'], list):
                        section_items_count += len(section['checklist_items'])
                    elif 'items' in section and isinstance(section['items'], list):
                        section_items_count += len(section['items'])
            
            print(f"Total de elementos en todas las secciones: {section_items_count}")
            
            if section_items_count == 0:
                print("ADVERTENCIA: No hay elementos en ninguna sección, intentando cargar lista por defecto")
                # Intentar cargar la lista predeterminada directamente
                sections = guide._default_checklist()['sections']
                print(f"Cargada lista por defecto con {len(sections)} secciones")
                
                # Convertir 'items' a 'checklist_items' si es necesario
                for section in sections:
                    if isinstance(section, dict) and 'items' in section:
                        section['checklist_items'] = section.pop('items')
                
                # Verificar elementos nuevamente
                default_items_count = 0
                for section in sections:
                    if isinstance(section, dict):
                        if 'checklist_items' in section and isinstance(section['checklist_items'], list):
                            default_items_count += len(section['checklist_items'])
                        elif 'items' in section and isinstance(section['items'], list):
                            default_items_count += len(section['items'])
                print(f"Total de elementos en la lista por defecto: {default_items_count}")
            
            # Verificar la estructura de datos de cada sección
            for i, section in enumerate(sections):
                print(f"Analizando sección {i+1}/{len(sections)}")
                if not isinstance(section, dict):
                    print(f"ADVERTENCIA: La sección no es un diccionario: {type(section)}")
                    # Reemplazar con una sección vacía válida
                    sections[i] = {
                        'id': f'section_{i}',
                        'title': f'Sección {i+1}',
                        'items': []
                    }
                    continue
                    
                # Asegurarse de que la sección tenga ID y título
                if 'id' not in section or not section['id']:
                    section['id'] = f'section_{i}'
                    print(f"  Añadido ID a la sección: {section['id']}")
                if 'title' not in section or not section['title']:
                    section['title'] = f'Sección {i+1}'
                    print(f"  Añadido título a la sección: {section['title']}")
                    
                section_id = section.get('id')
                print(f"Sección {section_id}:")
                print(f"  Título: {section.get('title')}")
                
                # Asegurarse de que la sección tenga una lista de elementos
                if 'checklist_items' not in section and 'items' not in section:
                    print(f"  ADVERTENCIA: La sección {section_id} no tiene elementos")
                    section['checklist_items'] = []  # Añadir lista vacía para evitar errores en la plantilla
                elif 'items' in section and not isinstance(section['items'], list):
                    print(f"  ERROR: 'items' no es una lista en la sección {section_id}: {type(section['items'])}")
                    section['checklist_items'] = []  # Corregir para evitar errores
                elif 'checklist_items' in section and not isinstance(section['checklist_items'], list):
                    print(f"  ERROR: 'checklist_items' no es una lista en la sección {section_id}: {type(section['checklist_items'])}")
                    section['checklist_items'] = []  # Corregir para evitar errores
                
                print(f"  Número de elementos: {len(section['checklist_items'] if 'checklist_items' in section else section.get('items', []))}")
                
                # Verificar estructura de cada elemento
                fixed_items = []
                items_list = section['checklist_items'] if 'checklist_items' in section else section.get('items', [])
                for j, item in enumerate(items_list):
                    if not isinstance(item, dict):
                        print(f"  ADVERTENCIA: Elemento {j} no es un diccionario: {type(item)}")
                        continue
                        
                    # Verificar y asegurar que cada item tenga los campos necesarios
                    if 'id' not in item or not item['id']:
                        item_id = f"{section_id}_{j}"
                        print(f"  ADVERTENCIA: Añadido ID '{item_id}' al elemento {j}")
                        item['id'] = item_id
                    
                    if 'text' not in item or not item['text']:
                        item_text = f"Elemento {j+1} de la sección {section_id}"
                        print(f"  ADVERTENCIA: Añadido texto al elemento {j}")
                        item['text'] = item_text
                    
                    if 'recommendation' not in item:
                        print(f"  ADVERTENCIA: Añadida recomendación vacía al elemento {j}")
                        item['recommendation'] = "Sin recomendación disponible"
                    
                    fixed_items.append(item)
                    print(f"  Procesado elemento {j}: ID={item['id']}, texto={item['text'][:20]}...")
                    
                # Reemplazar la lista de items con la lista corregida
                item_count = len(section['checklist_items'] if 'checklist_items' in section else section.get('items', []))
                print(f"  Reemplazando {item_count} elementos originales con {len(fixed_items)} elementos procesados")
                section['checklist_items'] = fixed_items
        else:
            print("ERROR: No se encontraron secciones válidas en la lista de verificación")
            if not checklist_data:
                print("  checklist_data es None o evaluado como False")
            elif not isinstance(checklist_data, dict):
                print(f"  checklist_data no es un diccionario: {type(checklist_data)}")
            elif 'sections' not in checklist_data:
                print(f"  No se encontró la clave 'sections' en checklist_data. Claves disponibles: {checklist_data.keys()}")
            
            # Crear una lista de verificación vacía para evitar errores en la plantilla
            print("Intentando cargar lista predeterminada...")
            sections = guide._default_checklist()['sections']
            
            # Convertir 'items' a 'checklist_items' si es necesario
            for section in sections:
                if isinstance(section, dict) and 'items' in section:
                    section['checklist_items'] = section.pop('items')
                    
            flash('Se ha cargado la lista de verificación predeterminada.', 'warning')
    except Exception as e:
        print(f"ERROR al cargar la lista de verificación: {e}")
        import traceback
        print(f"Traza de error:\n{traceback.format_exc()}")
        # Si hay un error, intentar usar la lista predeterminada
        try:
            print("Intentando cargar lista predeterminada debido al error...")
            from models.project_structure import ProjectStructureGuide
            guide = ProjectStructureGuide()
            sections = guide._default_checklist()['sections']
            
            # Convertir 'items' a 'checklist_items' si es necesario
            for section in sections:
                if isinstance(section, dict) and 'items' in section:
                    section['checklist_items'] = section.pop('items')
                    
            flash('Se ha cargado la lista de verificación predeterminada debido a un error.', 'warning')
        except Exception as default_error:
            print(f"ERROR al cargar la lista predeterminada: {default_error}")
            # Si falla incluso la lista predeterminada, usar una lista vacía
            sections = []
            flash('Ocurrió un error al cargar la lista de verificación. Por favor, contacta con el soporte técnico.', 'danger')
    
    # Comprobar antes de renderizar para seguridad adicional
    if not isinstance(sections, list):
        print(f"ADVERTENCIA: La variable 'sections' no es una lista: {type(sections)}")
        sections = []
        
    print(f"Renderizando plantilla con {len(sections)} secciones")
    
    # Renombrar 'items' a 'checklist_items' para evitar conflictos con el método 'items()' de los diccionarios
    for section in sections:
        if isinstance(section, dict) and 'items' in section:
            section['checklist_items'] = section.pop('items')
            
    return render_template('project_structure/simple_checklist.html', sections=sections)

@app.route('/estructura/checklist/generar-informe', methods=['POST'])
def generate_checklist_report():
    """Genera un informe PDF de la lista de verificación"""
    try:
        # Recibir los datos de verificación del formulario
        form_data = request.form.get('checklist_data')
        if not form_data:
            flash('No hay datos de verificación para generar el informe', 'danger')
            return redirect(url_for('project_structure_checklist'))
        
        print("\n===== GENERANDO INFORME DE VERIFICACIÓN =====")
        print(f"Datos recibidos del formulario: {form_data[:100]}...")  # Mostrar los primeros 100 caracteres
        
        # Convertir los datos de JSON a un diccionario Python
        try:
            usuario_checklist_data = json.loads(form_data)
            print(f"Datos de verificación del usuario parseados correctamente. Elementos: {len(usuario_checklist_data)}")
        except json.JSONDecodeError as e:
            print(f"ERROR: No se pudieron parsear los datos del formulario: {e}")
            flash('Error al procesar los datos del formulario', 'danger')
            return redirect(url_for('project_structure_checklist'))
        
        # Obtener las secciones de la lista de verificación desde el archivo JSON
        try:
            print("Cargando lista de verificación completa desde archivo JSON...")
            from models.project_structure import ProjectStructureGuide
            guide = ProjectStructureGuide()
            checklist_template = guide.checklist
            
            if not checklist_template or not isinstance(checklist_template, dict) or 'sections' not in checklist_template:
                print(f"ERROR: La plantilla de verificación no es válida. Tipo: {type(checklist_template)}")
                if isinstance(checklist_template, dict):
                    print(f"Claves disponibles: {checklist_template.keys()}")
                flash('Error al cargar la plantilla de verificación', 'danger')
                return redirect(url_for('project_structure_checklist'))
                
            sections = checklist_template['sections']
            print(f"Plantilla cargada correctamente con {len(sections)} secciones")
            
            # Verificar la estructura y simplificar para el informe
            for section in sections:
                if not isinstance(section, dict) or 'id' not in section or 'checklist_items' not in section:
                    print(f"ADVERTENCIA: Sección con formato incorrecto: {section}")
                    continue
                    
                section_id = section['id']
                if not isinstance(section['checklist_items'], list):
                    print(f"ADVERTENCIA: checklist_items no es una lista en sección {section_id}")
                    section['items'] = []
                    continue
                    
                # Simplificar los checklist_items para el informe, solo necesitamos id y text
                section['checklist_items'] = [
                    {'id': item.get('id', 'sin_id'), 'text': item.get('text', 'Sin texto')} 
                    for item in section['checklist_items'] 
                    if isinstance(item, dict) and 'id' in item and 'text' in item
                ]
                print(f"Sección {section_id}: {len(section['checklist_items'])} elementos procesados")
        except Exception as e:
            print(f"ERROR al cargar la lista de verificación para el informe: {e}")
            import traceback
            print(f"Traza de error:\n{traceback.format_exc()}")
            flash('Error al procesar la lista de verificación', 'danger')
            return redirect(url_for('project_structure_checklist'))
            
        # Asegurarse de que tenemos una lista válida para el informe
        if not isinstance(sections, list) or len(sections) == 0:
            print("ADVERTENCIA: No hay secciones válidas para el informe")
            flash('No hay elementos válidos para generar el informe', 'danger')
            return redirect(url_for('project_structure_checklist'))
            
        # Guardar los datos procesados para ser utilizados en el resto de la función
        checklist_data = usuario_checklist_data  # Datos de verificación del usuario
        
        # Crear un HTML con los resultados
        html_content = '<h1>Informe de Verificación de Proyecto I+D+i</h1>'
        html_content += f'<p>Fecha: {datetime.now().strftime("%d/%m/%Y")}</p>'
        html_content += '<p>Este informe muestra el estado de cumplimiento de los diferentes aspectos de su proyecto de I+D+i.</p>'
        
        # Contador de elementos completados y totales
        total_items = 0
        completed_items = 0
        
        # Para cada sección, añadir los elementos y su estado
        for section in sections:
            section_id = section['id']
            section_completed = 0
            section_total = len(section['checklist_items'])
            total_items += section_total
            
            html_content += f'<h2>{section["title"]}</h2>'
            html_content += '<ul>'
            for item in section['checklist_items']:
                item_key = f"{section_id}_{item['id']}"
                checked = item_key in checklist_data and checklist_data[item_key]
                if checked:
                    section_completed += 1
                    completed_items += 1
                check_mark = '✓' if checked else '✗'  # Símbolo de check o cruz
                color = 'green' if checked else 'red'
                html_content += f'<li style="color: {color}">{check_mark} {item["text"]}</li>'
            html_content += '</ul>'
            
            # Mostrar el porcentaje de completitud de la sección
            percentage = int((section_completed / section_total) * 100) if section_total > 0 else 0
            html_content += f'<p>Completado: {section_completed}/{section_total} ({percentage}%)</p>'
            html_content += '<hr>'
        
        # Mostrar resumen general
        total_percentage = int((completed_items / total_items) * 100) if total_items > 0 else 0
        html_content += f'<h2>Resumen General</h2>'
        html_content += f'<p>Total completado: {completed_items}/{total_items} ({total_percentage}%)</p>'
        
        # Añadir recomendaciones generales según el porcentaje de completitud
        html_content += '<h2>Recomendaciones</h2>'
        if total_percentage < 25:
            html_content += '<p>Su proyecto está en una fase inicial de estructuración. Dedique tiempo a completar los aspectos fundamentales antes de avanzar.</p>'
        elif total_percentage < 50:
            html_content += '<p>Su proyecto está parcialmente estructurado pero requiere mayor detalle en varios aspectos clave. Revise especialmente las secciones con menor porcentaje de completitud.</p>'
        elif total_percentage < 75:
            html_content += '<p>Su proyecto tiene una buena estructura básica, pero aún puede mejorarse en algunos aspectos para maximizar sus posibilidades de éxito y aplicación de deducciones fiscales.</p>'
        elif total_percentage < 100:
            html_content += '<p>Su proyecto está bien estructurado en general. Complete los pocos aspectos restantes para asegurar una estructura óptima.</p>'
        else:
            html_content += '<p>¡Felicitaciones! Su proyecto cumple con todos los aspectos recomendados para una estructura óptima de proyecto de I+D+i.</p>'
        
        # Generar PDF usando una utilidad existente o una nueva
        from utils.helpers import get_user_data_dir
        import tempfile
        
        # Crear directorio temporal para el PDF
        temp_dir = os.path.join(get_user_data_dir(), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        # Ruta del archivo PDF
        pdf_path = os.path.join(temp_dir, f'verificacion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        
        # Crear un archivo HTML temporal
        _, html_path = tempfile.mkstemp(suffix='.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; }
                    h1 { color: #2c3e50; text-align: center; }
                    h2 { color: #3498db; margin-top: 20px; }
                    ul { margin-bottom: 20px; }
                    li { margin-bottom: 5px; }
                    .footer { text-align: center; margin-top: 50px; font-size: 12px; color: #7f8c8d; }
                </style>
            </head>
            <body>
                """+html_content+"""
                <div class="footer">
                    Generado por la herramienta de Deducciones Fiscales I+D+i
                </div>
            </body>
            </html>""")
        
        # Generar PDF (usando pdfkit u otra biblioteca)
        try:
            import pdfkit
            pdfkit.from_file(html_path, pdf_path)
        except Exception as pdf_error:
            print(f"Error al generar PDF con pdfkit: {pdf_error}")
            # Alternativa si pdfkit falla
            # Aquí se podría implementar otra forma de generar el PDF
            flash('Error al generar el PDF. Contacte con el soporte.', 'danger')
            return redirect(url_for('project_structure_checklist'))
            
        # Eliminar el archivo HTML temporal
        os.unlink(html_path)
        
        # Devolver el archivo PDF
        return send_file(pdf_path, as_attachment=True, download_name='Verificacion_Proyecto_IDi.pdf')
        
    except Exception as e:
        print(f"Error al generar informe de verificación: {e}")
        flash('Ha ocurrido un error al generar el informe. Inténtelo de nuevo.', 'danger')
        return redirect(url_for('project_structure_checklist'))

@app.route('/herramientas')
def tools_guide():
    """Muestra la guía rápida de herramientas"""
    return render_template('tools_guide.html')

@app.route('/welcome')
def welcome():
    """Página de bienvenida y disclaimer para el simulador de deducciones"""
    return render_template('welcome.html')

@app.route('/not-implemented/<page>')
def not_implemented(page):
    """Página para mostrar características no implementadas aún"""
    page_titles = {
        'estructura': 'Estructuración de proyectos'
    }
    page_descriptions = {
        'estructura': 'cómo estructurar tus proyectos de innovación'
    }
    
    return render_template('not_implemented.html', 
                          page=page,
                          page_title=page_titles.get(page, 'Función'),
                          page_description=page_descriptions.get(page, 'esta funcionalidad'))

@app.route('/financing-questionnaire', methods=['GET', 'POST'])
def financing_questionnaire():
    """Muestra el cuestionario para el asesor de financiación"""
    if request.method == 'POST':
        try:
            # Procesar la información del formulario
            # Cuidado con las comillas en strings en json - usar json.dumps para seguridad
            company_info = {
                'nombre': request.form.get('company_name', ''),
                'tamaño': request.form.get('company_size', ''),
                'antiguedad': request.form.get('company_age', ''),
                'sector': request.form.get('company_sector', ''),
                'ubicacion': request.form.get('company_location', ''),
                'financiacion_previa': request.form.get('previous_funding', '')
            }
            
            project_info = {
                'titulo': request.form.get('project_title', ''),
                'descripcion': request.form.get('project_description', ''),
                'tipo': request.form.get('project_type', ''),
                'nivel_tecnologico': request.form.get('technology_level', ''),
                'presupuesto': request.form.get('project_budget', ''),
                'duracion': request.form.get('project_duration', ''),
                'objetivos': request.form.getlist('project_goals'),
                'colaboracion': request.form.get('collaboration', ''),
                'tipo_colaboracion': request.form.getlist('collaboration_type') if request.form.get('collaboration') == 'yes' else [],
                'info_adicional': request.form.get('additional_info', '')
            }
            
            # Importar el asesor de financiación
            from utils.ai.financing_advisor import FinancingAdvisor
            advisor = FinancingAdvisor()
            
            # Obtener recomendaciones
            result = advisor.get_financing_advice(company_info, project_info)
            
            if result['status'] == 'success':
                # Renderizar la página de resultados
                structured_data = result.get('structured_data')
                full_response = result.get('full_response', '')
                
                # Eliminar cualquier posible bloque de código JSON de la respuesta completa
                # para evitar duplicación (ya que se muestra estructurado arriba)
                if structured_data and full_response:
                    full_response = re.sub(r'```json\s*[\s\S]*?\s*```', '', full_response)
                
                return render_template('financing_results.html', 
                                       structured_data=structured_data,
                                       full_response=full_response)
            else:
                # Mostrar error
                flash(f"Ha ocurrido un error: {result.get('message', 'Error desconocido')}", 'danger')
                return render_template('financing_questionnaire.html')
                
        except Exception as e:
            print(f"Error al procesar el formulario de financiación: {e}")
            flash(f"Ha ocurrido un error al procesar su solicitud: {str(e)}", 'danger')
            return render_template('financing_questionnaire.html')
    
    # Si es GET, mostrar el formulario
    return render_template('financing_questionnaire.html')

@app.route('/questionnaire/<section>', methods=['GET', 'POST'])
def questionnaire(section):
    """Maneja las diferentes secciones del cuestionario"""
    # Cargar preguntas
    questions = load_config('questions.json')
    
    # Verificar que la sección exista
    if section not in questions:
        return redirect(url_for('home'))
    
    # Si es POST, guardar respuestas en la sesión
    if request.method == 'POST':
        try:
            # Inicializar la evaluación si no existe en la sesión
            if 'assessment' not in session:
                session['assessment'] = {
                    'id': str(uuid.uuid4()),
                    'timestamp': datetime.now().isoformat(),
                    'responses': {}
                }
            elif 'responses' not in session['assessment']:
                session['assessment']['responses'] = {}
            
            # Guardar respuestas de la sección actual
            form_data = request.form.to_dict()
            print(f"\nGuardando datos de la sección '{section}': {form_data}")
            
            session['assessment']['responses'][section] = form_data
            
            # Asegurarnos de que la sesión se guarde
            session.modified = True
            
            # Log de verificación
            print(f"Secciones guardadas hasta ahora: {list(session['assessment']['responses'].keys())}")
            
            # Determinar la siguiente sección
            sections = list(questions.keys())
            current_index = sections.index(section)
            
            # Si es la última sección, redirigir a resultados
            if current_index == len(sections) - 1:
                session.modified = True  # Asegurar que se guarda la sesión antes de redirigir
                return redirect(url_for('calculate_results'))
            else:
                # Redirigir a la siguiente sección
                next_section = sections[current_index + 1]
                session.modified = True  # Asegurar que se guarda la sesión antes de redirigir
                return redirect(url_for('questionnaire', section=next_section))
        except Exception as e:
            print(f"Error al guardar respuestas: {e}")
            # En caso de error, seguir adelante con lo que tenemos
            pass
    
    # Si es GET, mostrar las preguntas de la sección
    
    # Determinar secciones para la barra de progreso
    sections = list(questions.keys())
    current_index = sections.index(section)
    progress = int((current_index / len(sections)) * 100)
    
    # Determinar URL anterior
    if current_index > 0:
        prev_url = url_for('questionnaire', section=sections[current_index - 1])
    else:
        prev_url = url_for('welcome') # Mantener la navegación desde welcome
    
    # Obtener título de la sección
    section_title = load_section_title(section)
    
    # Obtener respuestas previas si existen
    previous_responses = {}
    if 'assessment' in session and 'responses' in session['assessment'] and section in session['assessment']['responses']:
        previous_responses = session['assessment']['responses'][section]
    
    return render_template('questionnaire.html', 
                          section=section, 
                          section_title=section_title, 
                          questions=questions[section], 
                          progress=progress, 
                          prev_url=prev_url, 
                          previous_responses=previous_responses)

@app.route('/calculate')
def calculate_results():
    """Calcula los resultados basados en las respuestas"""
    # Verificar que exista una evaluación en la sesión
    if 'assessment' not in session:
        return redirect(url_for('welcome'))
    
    try:
        # Imprimir información de depuración
        print("\nCalculando resultados...")
        print(f"Secciones disponibles: {list(session['assessment']['responses'].keys())}")
        
        if 'expenses' in session['assessment']['responses']:
            print(f"Gastos: {session['assessment']['responses']['expenses']}")
        else:
            print("No hay datos de gastos")
        
        # Importar los módulos para cálculos
        from models.calculator import calculate_deduction, qualify_project, generate_recommendations
        
        # Calificar el proyecto (I+D o IT)
        qualification = qualify_project(session['assessment']['responses'])
        print(f"Calificación obtenida: {qualification}")
        
        # Calcular deducción fiscal
        tax_rates = load_config('tax_rates.json')
        expenses = session['assessment']['responses'].get('expenses', {})
        deduction = calculate_deduction(qualification, expenses, tax_rates)
        print(f"Deducción calculada: {deduction}")
        
        # Generar recomendaciones
        recommendations = generate_recommendations(qualification, deduction, session['assessment']['responses'])
        print(f"Recomendaciones generadas: {len(recommendations)}")
        
        # Guardar resultados en la sesión
        session['assessment']['results'] = {
            'qualification': qualification,
            'deduction': deduction,
            'recommendations': recommendations
        }
        
        # Guardar la sesión explícitamente
        session.modified = True
        
        print("Cálculo completado con éxito.\n")
        
        return redirect(url_for('results'))
    
    except Exception as e:
        print(f"Error en el cálculo de resultados: {e}")
        # Asegurar que haya al menos algunos resultados mínimos
        session['assessment']['results'] = {
            'qualification': 'NOT_QUALIFIED',
            'deduction': {
                'total': 0,
                'eligible_expenses': {'total': 0}
            },
            'recommendations': [
                "Se produjo un error al calcular los resultados.",
                "Por favor, inténtelo de nuevo o contacte con el soporte técnico."
            ]
        }
        session.modified = True
        return redirect(url_for('results'))

@app.route('/results')
def results():
    """Muestra los resultados de la evaluación"""
    # Verificar que exista una evaluación con resultados en la sesión
    if 'assessment' not in session or 'results' not in session['assessment']:
        return redirect(url_for('welcome'))
    
    # Nombre de archivo por defecto para guardar
    company_name = ''
    if 'responses' in session['assessment'] and 'basic_info' in session['assessment']['responses'] and 'company_name' in session['assessment']['responses']['basic_info']:
        company_name = session['assessment']['responses']['basic_info']['company_name']
    
    from utils.helpers import generate_filename
    default_filename = generate_filename(company_name)
    
    # Pasar funciones de formato y etiquetas a la plantilla
    return render_template('results.html', 
                          assessment=session['assessment'],
                          format_currency=format_currency,
                          get_qualification_label=load_qualification_label,
                          default_filename=default_filename,
                          now=datetime.now())

@app.route('/report')
def generate_report():
    """Genera un informe PDF con los resultados"""
    # Verificar que exista una evaluación con resultados en la sesión
    if 'assessment' not in session or 'results' not in session['assessment']:
        return redirect(url_for('welcome'))
    
    # Generar el PDF
    try:
        print("\nGenerando informe PDF...")
        from utils.pdf_generator import generate_pdf
        pdf_path = generate_pdf(session['assessment'], app)
        print(f"PDF generado en: {pdf_path}")
        
        # Generar nombre de archivo para descarga
        company_name = ''
        if 'responses' in session['assessment'] and 'basic_info' in session['assessment']['responses'] and 'company_name' in session['assessment']['responses']['basic_info']:
            company_name = session['assessment']['responses']['basic_info']['company_name']
    
        # Limpiar el nombre para el archivo
        if company_name:
            company_name = ''.join(c for c in company_name if c.isalnum() or c in ' _-').strip().replace(' ', '_')
            filename = f"Deduccion_ID_IT_{company_name}.pdf"
        else:
            filename = "Deduccion_ID_IT_Informe.pdf"
        
        # Enviar el archivo al usuario (compatibilidad con Flask 2.3+)
        return send_file(pdf_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        flash('Ha ocurrido un error al generar el PDF. Inténtelo de nuevo.', 'danger')
        return redirect(url_for('results'))

@app.route('/save_assessment', methods=['POST'])
def save_assessment():
    """Guarda una evaluación en un archivo JSON"""
    # Verificar que exista una evaluación en la sesión
    if 'assessment' not in session:
        flash('No hay una evaluación activa para guardar', 'danger')
        return redirect(url_for('welcome'))
    
    # Obtener el nombre de archivo del formulario o usar uno por defecto
    filename = request.form.get('filename', '')
    if not filename:
        from utils.helpers import generate_filename
        company_name = ''
        if 'responses' in session['assessment'] and 'basic_info' in session['assessment']['responses'] and 'company_name' in session['assessment']['responses']['basic_info']:
            company_name = session['assessment']['responses']['basic_info']['company_name']
        filename = generate_filename(company_name)
    
    # Asegurar que el archivo tenga extensión .json
    if not filename.lower().endswith('.json'):
        filename += '.json'
    
    # Obtener el directorio para guardar las evaluaciones
    from utils.helpers import get_saved_assessments_dir
    save_dir = get_saved_assessments_dir()
    
    # Ruta completa del archivo
    file_path = os.path.join(save_dir, filename)
    
    try:
        # Guardar la evaluación en el archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(session['assessment'], f, ensure_ascii=False, indent=2)
        
        flash(f'Evaluación guardada exitosamente como {filename}', 'success')
        
    except Exception as e:
        flash(f'Error al guardar la evaluación: {str(e)}', 'danger')
    
    return redirect(url_for('results'))

@app.route('/reset')
def reset():
    """Reinicia la evaluación"""
    session.pop('assessment', None)
    return redirect(url_for('home'))

@app.route('/info/imv')
def info_imv():
    """Muestra información sobre el Informe Motivado Vinculante (IMV)"""
    return render_template('info/imv.html')

# Función para ejecutar la aplicación
# Jinja context processor para variables globales
@app.context_processor
def inject_globals():
    """Inyecta variables globales en todas las plantillas"""
    from utils.helpers import get_version
    return {
        'version': get_version(),
        'now': datetime.now()
    }

# Filtro para formato de texto a HTML
@app.template_filter('nl2br')
def nl2br(value):
    """Convierte los saltos de línea en etiquetas <br>"""
    if value:
        return value.replace('\n', '<br>')
    return value

# Manejador de errores 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', 
                          error_code=404,
                          error_message="Página no encontrada"), 404

# Manejador de errores 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', 
                          error_code=500,
                          error_message="Error interno del servidor"), 500

def run_app():
    """Función para iniciar la aplicación"""
    import webbrowser
    import threading
    import socket
    import sys
    
    try:
        # Encontrar un puerto disponible
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()
        
        # Iniciar el navegador después de que Flask haya iniciado
        def open_browser():
            try:
                webbrowser.open(f'http://localhost:{port}')
            except Exception as e:
                print(f"Error al abrir el navegador: {e}")
                print(f"Por favor, abra manualmente la siguiente URL en su navegador: http://localhost:{port}")
        
        threading.Timer(1.5, open_browser).start()
        
        print(f"\nIniciando Herramienta de Evaluación de Deducciones Fiscales I+D+i en el puerto {port}...")
        print(f"Acceda a la aplicación en: http://localhost:{port}")
        print(f"Presione Ctrl+C para detener la aplicación\n")
        
        # Iniciar Flask
        app.run(host='localhost', port=port, debug=False)
        
    except Exception as e:
        print(f"\nError al iniciar la aplicación: {e}")
        print("Por favor, asegúrese de que no hay otras aplicaciones usando el mismo puerto.")
        sys.exit(1)

# Si se ejecuta directamente el script
if __name__ == '__main__':
    run_app()