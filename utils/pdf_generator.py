"""
Módulo para generar informes PDF de las evaluaciones
"""

import os
import tempfile
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

# --- INICIO: NUEVA FUNCIÓN DE FORMATO ---
def format_number_spanish(value):
    """
    Formatea un número al estilo español (ej: 1.234,56) para el PDF,
    manejando None y posibles errores.
    """
    if value is None or value == '':
        return "0,00"
    try:
        # Asegurarse de que es un float para el formato
        num_float = float(value)
        # Formato inicial a string con 2 decimales (usando punto)
        s = f"{num_float:.2f}"
        # Separar parte entera y decimal
        parts = s.split('.')
        integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else "00"

        # Añadir separadores de miles (puntos) a la parte entera
        integer_part_with_sep = ""
        n = len(integer_part)
        # Manejar signo negativo
        start_index = 0
        if integer_part.startswith('-'):
            integer_part_with_sep += '-'
            start_index = 1
            n -= 1 # Ajustar longitud para cálculo de separadores

        # Bucle para añadir separadores
        for i, digit in enumerate(integer_part[start_index:]):
            integer_part_with_sep += digit
            # Añadir punto si es necesario: (longitud_restante - 1) es divisible por 3 y no es el último dígito
            if (n - 1 - i) % 3 == 0 and i != n - 1:
                integer_part_with_sep += "."

        # Asegurar que la parte decimal tenga dos dígitos
        decimal_part = decimal_part.ljust(2, '0')[:2]

        # Unir con coma decimal
        return f"{integer_part_with_sep},{decimal_part}"
    except (ValueError, TypeError):
        # Si la conversión a float falla o hay otro problema
        return "0,00" # O un valor por defecto/error que prefieras
# --- FIN: NUEVA FUNCIÓN DE FORMATO ---

def generate_pdf(assessment, app=None):
    """
    Genera un informe PDF a partir de una evaluación

    Args:
        assessment (dict): Datos de la evaluación
        app (Flask): Aplicación Flask para el contexto de renderizado

    Returns:
        str: Ruta del archivo PDF generado
    """
    try:
        print("\nGenerando PDF con los siguientes datos:")
        print(f"Secciones disponibles: {list(assessment.keys())}")
        if 'responses' in assessment:
            print(f"Respuestas disponibles: {list(assessment['responses'].keys())}")
        if 'results' in assessment:
            print(f"Resultados disponibles: {list(assessment['results'].keys())}")

        # Crear un archivo temporal para el PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()

        # Configurar el documento
        doc = SimpleDocTemplate(
            temp_file.name,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # Estilos
        styles = getSampleStyleSheet()
        
        # No redefinir estilos existentes, crear variantes personalizadas
        custom_styles = {
            'CustomTitle': ParagraphStyle(
                name='CustomTitle',
                parent=styles['Title'],
                fontSize=18,
                spaceAfter=12,
                alignment=1  # Centro
            ),
            'CustomHeading2': ParagraphStyle(
                name='CustomHeading2',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=6,
                spaceBefore=12
            ),
            'CustomNormal': ParagraphStyle(
                name='CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6
            ),
            'Disclaimer': ParagraphStyle(
                name='Disclaimer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.red,
                alignment=1  # Centro
            ),
            'WarningSubsidy': ParagraphStyle(
                name='WarningSubsidy',
                parent=styles['Normal'],
                textColor=colors.red,
                fontSize=9,
                spaceAfter=6
            ),
            'MixedDistribution': ParagraphStyle(
                name='MixedDistribution',
                parent=styles['Normal'],
                fontSize=9,
                fontStyle='italic'
            )
        }

        # Elementos del documento
        elements = []

        # Título
        elements.append(Paragraph('Informe de Evaluación Preliminar de Deducciones Fiscales I+D+i', custom_styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*cm))

        # Fecha
        date_str = datetime.now().strftime('%d/%m/%Y %H:%M')
        elements.append(Paragraph(f'Fecha: {date_str}', custom_styles['CustomNormal']))
        elements.append(Spacer(1, 0.3*cm))

        # Disclaimer
        elements.append(Paragraph(
            'AVISO IMPORTANTE: Este informe proporciona una orientación preliminar y no vinculante. '
            'No constituye asesoramiento fiscal profesional. '
            'Consulte con un experto en deducciones fiscales por I+D+i para obtener una evaluación completa.',
            custom_styles['Disclaimer']
        ))
        elements.append(Spacer(1, 0.7*cm))

        # Información básica
        if 'responses' in assessment and 'basic_info' in assessment['responses']:
            elements.append(Paragraph('Información de la Empresa', custom_styles['CustomHeading2']))

            basic_info = assessment['responses']['basic_info']
            company_name = basic_info.get('company_name', 'No especificado')
            company_size = basic_info.get('company_size', 'No especificado')
            sector = basic_info.get('sector', 'No especificado')

            data = [
                ['Nombre de la empresa:', company_name],
                ['Tamaño de la empresa:', company_size],
                ['Sector de actividad:', sector]
            ]

            table = Table(data, colWidths=[5*cm, 10*cm])
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT')
            ]))

            elements.append(table)
            elements.append(Spacer(1, 0.5*cm)) # Separador añadido después de la tabla

        # Información del proyecto y Aviso Subvenciones (Movido aquí para consistencia)
        project_info = {}
        if 'responses' in assessment and 'project_identification' in assessment['responses']:
            project_info = assessment['responses']['project_identification'] # Guardamos para usar después

            elements.append(Paragraph('Información del Proyecto', custom_styles['CustomHeading2']))

            project_name = project_info.get('project_name', 'No especificado')
            project_year = project_info.get('project_year', 'No especificado')
            subsidy = project_info.get('subsidy_received', 'No')

            data_project = [
                ['Nombre del proyecto:', project_name],
                ['Año fiscal:', project_year],
                ['Subvenciones recibidas:', subsidy]
            ]

            table_project = Table(data_project, colWidths=[5*cm, 10*cm])
            table_project.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT')
            ]))

            elements.append(table_project)

            if 'project_description' in project_info and project_info['project_description']:
                elements.append(Spacer(1, 0.3*cm))
                elements.append(Paragraph('Descripción:', custom_styles['CustomNormal']))
                # Usar Paragraph para manejar saltos de línea en la descripción
                elements.append(Paragraph(project_info['project_description'].replace('\n', '<br/>'), custom_styles['CustomNormal']))

            # Aviso de subvenciones (va DESPUÉS de la tabla de proyecto)
            if project_info.get('subsidy_received') == 'Sí':
                elements.append(Spacer(1, 0.3*cm))
                elements.append(Paragraph(
                    'AVISO IMPORTANTE SOBRE SUBVENCIONES: Ha indicado que este proyecto ha recibido subvenciones. '
                    'La parte subvencionada del proyecto NO puede aplicar para deducciones fiscales, ya que esos '
                    'gastos ya han sido cubiertos por financiación pública. Las cantidades mostradas deben ajustarse restando '
                    'el importe subvencionado.',
                    custom_styles['WarningSubsidy']
                ))

            elements.append(Spacer(1, 0.5*cm))


        # Calificación del proyecto
        if 'results' in assessment and 'qualification' in assessment['results']:
            elements.append(Paragraph('Calificación Preliminar', custom_styles['CustomHeading2']))

            qualification = assessment['results']['qualification']
            qualification_text = {
                'ID': 'Investigación y Desarrollo (I+D)',
                'IT': 'Innovación Tecnológica (IT)',
                'MIXED': 'Mixto: I+D e IT',
                'POTENTIAL': 'Potencial I+D/IT (Requiere análisis detallado)',
                'NOT_QUALIFIED': 'No califica directamente (Consultar con experto)'
            }.get(qualification, 'No determinado')

            elements.append(Paragraph(f'Calificación: {qualification_text}', custom_styles['CustomNormal']))

            # Descripción de la calificación
            qualification_desc = {
                'ID': 'Su proyecto muestra características significativas de Investigación y Desarrollo (I+D), lo que le permitiría acceder a deducciones fiscales del 25% sobre los gastos elegibles.',
                'IT': 'Su proyecto muestra características de Innovación Tecnológica (IT), lo que le permitiría acceder a deducciones fiscales del 12% sobre los gastos elegibles.',
                'MIXED': 'Su proyecto presenta características tanto de Investigación y Desarrollo (I+D) como de Innovación Tecnológica (IT). Este tipo de proyectos puede beneficiarse de deducciones diferentes para cada componente: 25% para la parte calificada como I+D y 12% para la parte calificada como IT.',
                'POTENTIAL': 'Su proyecto muestra algunas características de I+D y/o IT, pero la calificación no es definitiva. Se ha estimado una distribución orientativa para el cálculo de la deducción, pero se recomienda un análisis más detallado.',
                'NOT_QUALIFIED': 'Según las respuestas, el proyecto no parece calificar directamente para deducciones de I+D o IT. Consulte con un experto para confirmar.'
            }.get(qualification, '')

            if qualification_desc:
                 elements.append(Paragraph(qualification_desc, custom_styles['CustomNormal']))

            # Para proyectos MIXED o POTENTIAL, informar sobre la distribución
            if qualification in ['MIXED', 'POTENTIAL']:
                elements.append(Spacer(1, 0.3*cm))
                elements.append(Paragraph(
                    'Nota sobre la distribución: Para este informe se ha estimado una distribución del 60% para actividades '
                    'de I+D y un 40% para actividades de IT. Esta distribución es meramente orientativa y su finalidad es '
                    'exclusivamente ilustrativa para el cálculo de la simulación. Una evaluación profesional podría determinar '
                    'porcentajes diferentes basados en un análisis detallado del proyecto.',
                    custom_styles['MixedDistribution']
                ))

            elements.append(Spacer(1, 0.5*cm))

        # Resumen financiero
        if 'results' in assessment and 'deduction' in assessment['results']:
            deduction = assessment['results']['deduction']
            expenses = deduction.get('eligible_expenses', {})

            # Tabla de gastos elegibles (Solo si hay gastos)
            if expenses and expenses.get('total', 0) > 0:
                elements.append(Paragraph('Gastos Elegibles', custom_styles['CustomHeading2']))

                # --- INICIO: MODIFICACIÓN FORMATO GASTOS ---
                data_expenses = [
                    ['Categoría', 'Importe (€)']
                ]
                # Añadir filas solo si el valor es mayor que cero
                if expenses.get('personnel', 0) > 0:
                    data_expenses.append(['Personal', format_number_spanish(expenses.get('personnel', 0))])

                if expenses.get('exclusive_personnel', 0) > 0:
                    data_expenses.append(['- Del cual, personal exclusivo I+D', format_number_spanish(expenses.get('exclusive_personnel', 0))])

                if expenses.get('external', 0) > 0:
                    data_expenses.append(['Colaboraciones externas', format_number_spanish(expenses.get('external', 0))])

                if expenses.get('equipment', 0) > 0:
                    data_expenses.append(['Equipamiento (amortización)', format_number_spanish(expenses.get('equipment', 0))])

                if expenses.get('materials', 0) > 0:
                    data_expenses.append(['Materiales', format_number_spanish(expenses.get('materials', 0))])

                if expenses.get('general', 0) > 0:
                    data_expenses.append(['Gastos generales', format_number_spanish(expenses.get('general', 0))])

                # Agregamos filas de distribución para proyectos MIXED o POTENTIAL
                if assessment['results']['qualification'] in ['MIXED', 'POTENTIAL']:
                    # Estimamos 60% I+D y 40% IT por defecto
                    id_portion = 0.6 
                    it_portion = 0.4
                    total = expenses.get('total', 0)
                    
                    data_expenses.append(['', ''])  # Separador
                    data_expenses.append(['Asignados a I+D (según distribución)', format_number_spanish(total * id_portion)])
                    data_expenses.append(['Asignados a IT (según distribución)', format_number_spanish(total * it_portion)])

                # Fila de Total
                data_expenses.append(['TOTAL GASTOS ELEGIBLES', format_number_spanish(expenses.get('total', 0))])
                # --- FIN: MODIFICACIÓN FORMATO GASTOS ---

                table_expenses = Table(data_expenses, colWidths=[10*cm, 5*cm])
                
                # Estilos básicos de la tabla
                table_style = [
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),        # Header row
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),     # Footer row (Total)
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),                      # Align numbers right
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),          # Bold header
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),        # Bold footer
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),                   # Padding header
                    ('TOPPADDING', (0, -1), (-1, -1), 10)                     # Padding footer
                ]
                
                # Agregar estilos para filas de distribución si aplica
                if assessment['results']['qualification'] in ['MIXED', 'POTENTIAL']:
                    # Calcular el índice de la primera fila de distribución
                    dist_start_idx = len(data_expenses) - 3  # -3 porque hay 2 filas de distribución + fila total
                    if dist_start_idx >= 0:
                        table_style.append(('BACKGROUND', (0, dist_start_idx), (-1, dist_start_idx+1), colors.lavender))
                
                table_expenses.setStyle(TableStyle(table_style))
                elements.append(table_expenses)
                elements.append(Spacer(1, 0.5*cm))

            # Tabla de deducciones (Solo si la deducción total es mayor que cero)
            if deduction.get('total', 0) > 0:
                elements.append(Paragraph('Deducción Fiscal Estimada', custom_styles['CustomHeading2']))

                # --- INICIO: MODIFICACIÓN FORMATO DEDUCCIONES ---
                data_deduction = [
                    ['Concepto', 'Importe (€)']
                ]
                
                # Deducción base I+D
                if deduction.get('id_base', 0) > 0 or assessment['results']['qualification'] in ['MIXED', 'POTENTIAL']:
                    data_deduction.append(['Deducción base I+D (25%)', format_number_spanish(deduction.get('id_base', 0))])

                # Deducción incremental I+D 
                if deduction.get('id_incremental', 0) > 0:
                    data_deduction.append(['Deducción incremental I+D (42%)', format_number_spanish(deduction.get('id_incremental', 0))])
                # Si hay datos de años anteriores y exceso, pero aún no está calculada la deducción incremental
                elif assessment['results']['qualification'] in ['MIXED', 'POTENTIAL'] and 'responses' in assessment and 'project_identification' in assessment['responses']:
                    project_info = assessment['responses']['project_identification']
                    if project_info.get('previous_expenses') == 'Sí':
                        expense_year_minus_1 = float(project_info.get('expense_year_minus_1', 0) or 0)
                        expense_year_minus_2 = float(project_info.get('expense_year_minus_2', 0) or 0)
                        previous_average = (expense_year_minus_1 + expense_year_minus_2) / 2
                        current_expense = expenses.get('total', 0)
                        
                        # Si hay exceso, mostrar la deducción incremental estimada (60% del exceso se aplica a I+D)
                        if current_expense > previous_average and previous_average > 0:
                            id_portion = 0.6
                            excess_amount = (current_expense - previous_average) * id_portion
                            incremental_deduction = excess_amount * (42 / 100)
                            data_deduction.append(['Deducción incremental I+D (42%)', format_number_spanish(incremental_deduction)])

                # Deducción por personal exclusivo I+D
                if deduction.get('id_personnel', 0) > 0 or (assessment['results']['qualification'] in ['MIXED', 'POTENTIAL'] and expenses.get('exclusive_personnel', 0) > 0):
                    personnel_deduction = deduction.get('id_personnel', 0)
                    # Si es MIXED/POTENTIAL, calcular la deducción por personal según la distribución
                    if assessment['results']['qualification'] in ['MIXED', 'POTENTIAL'] and personnel_deduction == 0:
                        id_portion = 0.6
                        personnel_deduction = expenses.get('exclusive_personnel', 0) * (17 / 100) * id_portion
                    data_deduction.append(['Deducción adicional personal I+D (17%)', format_number_spanish(personnel_deduction)])

                # Deducción IT
                if deduction.get('it', 0) > 0 or assessment['results']['qualification'] in ['MIXED', 'POTENTIAL']:
                    data_deduction.append(['Deducción IT (12%)', format_number_spanish(deduction.get('it', 0))])

                # Fila de Total
                data_deduction.append(['TOTAL DEDUCCIÓN ESTIMADA', format_number_spanish(deduction.get('total', 0))])
                # --- FIN: MODIFICACIÓN FORMATO DEDUCCIONES ---

                table_deduction = Table(data_deduction, colWidths=[10*cm, 5*cm])
                table_deduction.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),       # Header row
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),    # Footer row (Total)
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),                     # Align numbers right
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),         # Bold header
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),       # Bold footer
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),                  # Padding header
                    ('TOPPADDING', (0, -1), (-1, -1), 10)                    # Padding footer
                ]))

                elements.append(table_deduction)
                elements.append(Spacer(1, 0.5*cm))
            elif 'eligible_expenses' not in deduction or deduction['eligible_expenses'].get('total', 0) == 0 :
                # Si no hay gastos ni deducción, mostrar mensaje
                 elements.append(Paragraph('No se han introducido gastos o la deducción calculada es cero.', custom_styles['CustomNormal']))
                 elements.append(Spacer(1, 0.5*cm))


        # Recomendaciones
        if 'results' in assessment and 'recommendations' in assessment['results']:
            elements.append(Paragraph('Recomendaciones Finales', custom_styles['CustomHeading2']))

            recommendations = assessment['results']['recommendations']
            if recommendations:
                for recommendation in recommendations:
                    # Eliminar etiquetas HTML para los links en el PDF
                    clean_recommendation = recommendation.replace('<a href=', '').replace('</a>', '').replace('" target="_blank">', ' ').replace('>', ' ')
                    clean_recommendation = ' '.join(clean_recommendation.split())  # Normalizar espacios
                    # Usar estilo 'CustomNormal' con viñeta
                    elements.append(Paragraph(f"• {clean_recommendation}", custom_styles['CustomNormal']))
            else:
                 elements.append(Paragraph("No hay recomendaciones específicas.", custom_styles['CustomNormal']))
            elements.append(Spacer(1, 0.5*cm))

        # Disclaimer Final repetido
        elements.append(Paragraph(
            'Recuerde: Este informe es una estimación preliminar basada en la información proporcionada. '
            'Para confirmar la elegibilidad y cuantía de la deducción, es imprescindible consultar con '
            'un asesor fiscal especializado en I+D+i.',
            custom_styles['Disclaimer']
        ))

        # Construir el documento
        doc.build(elements)

        print(f"PDF generado exitosamente: {temp_file.name}")
        return temp_file.name

    except Exception as e:
        # Mejorar el log de errores
        import traceback
        print(f"Error detallado al generar PDF: {e}")
        print(traceback.format_exc()) # Imprime el stack trace completo
        # En caso de error, crear un PDF mínimo
        return create_minimal_pdf(assessment, e) # Pasar el error al PDF mínimo

def create_minimal_pdf(assessment, error=None):
    """
    Crea un PDF mínimo con información básica en caso de error durante la generación principal.

    Args:
        assessment (dict): Datos de la evaluación
        error (Exception, optional): El error que ocurrió

    Returns:
        str: Ruta del archivo PDF generado (o txt si falla de nuevo)
    """
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()

        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted

        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = [
            Paragraph('Error al Generar Informe Completo', styles['Heading1']),
            Spacer(1, 20),
            Paragraph('Se produjo un error al intentar generar el informe PDF detallado.', styles['Normal']),
            Spacer(1, 10),
        ]

        if error:
            elements.append(Paragraph('Detalles del Error:', styles['Heading3']))
            # Usar Preformatted para mantener formato del error y evitar problemas de renderizado HTML
            error_text = str(error)
            elements.append(Preformatted(error_text, styles['Code']))
            Spacer(1, 10)


        elements.append(Paragraph('Información Básica Recuperada:', styles['Heading3']))
        # Añadir información básica si está disponible
        company_name = "No disponible"
        if 'responses' in assessment and 'basic_info' in assessment['responses']:
            basic_info = assessment['responses']['basic_info']
            company_name = basic_info.get('company_name', 'No especificado')
        elements.append(Paragraph(f'Empresa: {company_name}', styles['Normal']))

        project_name = "No disponible"
        if 'responses' in assessment and 'project_identification' in assessment['responses']:
             project_info = assessment['responses']['project_identification']
             project_name = project_info.get('project_name', 'No especificado')
        elements.append(Paragraph(f'Proyecto: {project_name}', styles['Normal']))

        # Añadir recomendaciones si están disponibles (a menudo están incluso si falla el cálculo)
        if 'results' in assessment and 'recommendations' in assessment['results']:
            elements.append(Spacer(1, 20))
            elements.append(Paragraph('Recomendaciones (si existen):', styles['Heading3']))
            recommendations = assessment['results'].get('recommendations', [])
            if recommendations:
                for rec in recommendations:
                    # Eliminar etiquetas HTML para los links en el PDF
                    clean_rec = rec.replace('<a href=', '').replace('</a>', '').replace('" target="_blank">', ' ').replace('>', ' ')
                    clean_rec = ' '.join(clean_rec.split())  # Normalizar espacios
                    elements.append(Paragraph(f"• {clean_rec}", styles['Normal']))
            else:
                 elements.append(Paragraph("No se pudieron recuperar recomendaciones.", styles['Normal']))

        doc.build(elements)
        print(f"PDF mínimo generado debido a error: {temp_file.name}")
        return temp_file.name

    except Exception as critical_e:
        import traceback
        print(f"Error crítico al generar PDF mínimo: {critical_e}")
        print(traceback.format_exc())
        # Último recurso: archivo de texto
        try:
            txt_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            with open(txt_file.name, 'w', encoding='utf-8') as f:
                f.write("ERROR CRÍTICO AL GENERAR PDF\n\n")
                f.write("No se pudo generar ni siquiera el PDF de error.\n")
                f.write("Por favor, revise los logs de la consola para más detalles.\n\n")
                f.write(f"Error original: {error}\n\n")
                f.write(f"Error al crear PDF mínimo: {critical_e}\n")
            return txt_file.name
        except:
            return None # Falla total