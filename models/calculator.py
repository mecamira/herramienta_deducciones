"""
Módulo que contiene la lógica de cálculo para la herramienta de deducciones fiscales
"""

def qualify_project(responses):
    """
    Califica un proyecto como I+D o IT basado en las respuestas del cuestionario
    
    Args:
        responses (dict): Diccionario con las respuestas del cuestionario
    
    Returns:
        str: Calificación del proyecto ('ID', 'IT', 'NOT_QUALIFIED')
    """
    # Verificar que existen respuestas en la sección de calificación
    if 'qualification' not in responses:
        return 'NOT_QUALIFIED'
    
    qualification_responses = responses['qualification']
    
    # Inicializar puntuaciones
    id_score = 0
    it_score = 0
    max_id_score = 0
    max_it_score = 0
    
    # Pesos para cada respuesta según los criterios de I+D e IT
    weights = {
        'novelty_type': {'Novedad objetiva (no existe en el mercado mundial)': {'id': 5, 'it': 1}, 
                          'Novedad subjetiva (nuevo para la empresa)': {'id': 1, 'it': 5}},
        
        'scientific_uncertainty': {'Sí, aborda una incertidumbre sin solución evidente': {'id': 5, 'it': 0}, 
                                   'No, utiliza conocimiento establecido': {'id': 0, 'it': 3}, 
                                   'No estoy seguro': {'id': 2, 'it': 2}},
        
        'methodology': {'Sí, sigue metodología científica': {'id': 4, 'it': 1}, 
                        'Parcialmente': {'id': 2, 'it': 2}, 
                        'No': {'id': 0, 'it': 3}},
        
        'technological_improvement': {'Sí, mejora sustancial': {'id': 3, 'it': 4}, 
                                     'Mejora incremental': {'id': 1, 'it': 4}, 
                                     'No hay mejora tecnológica': {'id': 0, 'it': 0}},
        
        'prototypes': {'Sí': {'id': 3, 'it': 1}, 
                       'No': {'id': 1, 'it': 1}},
        
        'technical_risk': {'Sí, riesgo alto': {'id': 4, 'it': 2}, 
                          'Riesgo moderado': {'id': 2, 'it': 3}, 
                          'Riesgo bajo o nulo': {'id': 0, 'it': 1}},
        
        'software_development': {'Sí, avances significativos': {'id': 5, 'it': 3}, 
                                'Mejoras incrementales': {'id': 1, 'it': 5}, 
                                'No aplica/No incluye software': {'id': 3, 'it': 3}}
    }
    
    # Calcular puntuaciones
    for question_id, response in qualification_responses.items():
        if question_id in weights and response in weights[question_id]:
            # Sumar puntuación para I+D
            id_score += weights[question_id][response]['id']
            # Sumar puntuación para IT
            it_score += weights[question_id][response]['it']
            
            # Actualizar puntuaciones máximas posibles
            max_id_score += max(weight['id'] for weight in weights[question_id].values())
            max_it_score += max(weight['it'] for weight in weights[question_id].values())
    
    # Calcular porcentajes
    id_percentage = (id_score / max_id_score * 100) if max_id_score > 0 else 0
    it_percentage = (it_score / max_it_score * 100) if max_it_score > 0 else 0
    
    # Determinar calificación
    if id_percentage >= 70 and it_percentage < 50:
        return 'ID'
    elif it_percentage >= 70 and id_percentage < 50:
        return 'IT'
    elif id_percentage >= 60 and it_percentage >= 60:
        # Calificación mixta - proyecto con componentes de I+D e IT
        return 'MIXED'
    elif id_percentage >= 50 or it_percentage >= 50:
        # Calificación potencial pero no definitiva
        return 'POTENTIAL'
    else:
        return 'NOT_QUALIFIED'

def calculate_deduction(qualification, expenses_responses, tax_rates):
    """
    Calcula la deducción fiscal basado en la calificación y los gastos
    
    Args:
        qualification (str): Calificación del proyecto ('ID', 'IT', 'POTENTIAL', 'NOT_QUALIFIED')
        expenses_responses (dict): Diccionario con las respuestas de gastos
        tax_rates (dict): Tasas de impuestos para I+D e IT
    
    Returns:
        dict: Resultados de la deducción
    """
    # Inicializar resultados
    result = {
        'id_base': 0,
        'id_personnel': 0,
        'id_incremental': 0, # No implementado aún
        'it': 0,
        'total': 0,
        'eligible_expenses': {
            'personnel': 0,
            'exclusive_personnel': 0,
            'external': 0,
            'equipment': 0,
            'materials': 0,
            'general': 0,
            'total': 0
        }
    }
    
    # Extraer gastos
    try:
        print(f"Procesando gastos: {expenses_responses}")
        # Comprobar todos los posibles nombres de campo para personal
        if 'personnel' in expenses_responses:
            result['eligible_expenses']['personnel'] = float(expenses_responses.get('personnel', 0))
        
        # Comprobar todos los posibles nombres de campo para personal exclusivo
        if 'exclusive_personnel' in expenses_responses:
            result['eligible_expenses']['exclusive_personnel'] = float(expenses_responses.get('exclusive_personnel', 0))
        
        # Comprobar todos los posibles nombres de campo para colaboraciones externas
        if 'external_collaborations' in expenses_responses:
            result['eligible_expenses']['external'] = float(expenses_responses.get('external_collaborations', 0))
        
        # Comprobar todos los posibles nombres de campo para equipamiento
        if 'equipment' in expenses_responses:
            result['eligible_expenses']['equipment'] = float(expenses_responses.get('equipment', 0))
        
        # Comprobar todos los posibles nombres de campo para materiales
        if 'materials' in expenses_responses:
            result['eligible_expenses']['materials'] = float(expenses_responses.get('materials', 0))
        
        # Comprobar todos los posibles nombres de campo para gastos generales
        if 'general_expenses' in expenses_responses:
            result['eligible_expenses']['general'] = float(expenses_responses.get('general_expenses', 0))
        
    except (ValueError, TypeError) as e:
        # En caso de error en la conversión, mantener los valores en 0
        print(f"Error al procesar gastos: {e}")
    
    # Calcular total de gastos elegibles
    result['eligible_expenses']['total'] = (
        result['eligible_expenses']['personnel'] +
        result['eligible_expenses']['external'] +
        result['eligible_expenses']['equipment'] +
        result['eligible_expenses']['materials'] +
        result['eligible_expenses']['general']
    )
    
    # Calcular deducciones según calificación
    if qualification == 'ID':
        # Obtener datos de los años anteriores si existen
        has_previous_data = False
        if 'project_identification' in responses:
            has_previous_data = responses['project_identification'].get('previous_expenses') == 'Sí'
        
        # Calcular posible deducción incremental (42%)
        if has_previous_data:
            try:
                # Obtener gastos de años anteriores
                expense_year_minus_1 = float(responses['project_identification'].get('expense_year_minus_1', 0) or 0)
                expense_year_minus_2 = float(responses['project_identification'].get('expense_year_minus_2', 0) or 0)
                
                # Calcular media de los dos años anteriores
                previous_average = (expense_year_minus_1 + expense_year_minus_2) / 2 if (expense_year_minus_1 + expense_year_minus_2) > 0 else 0
                
                # Si el gasto actual es mayor que la media, calcular el exceso
                current_expense = result['eligible_expenses']['total']
                if current_expense > previous_average and previous_average > 0:
                    excess_amount = current_expense - previous_average
                    
                    # Calcular deducción incremental (42% sobre el exceso)
                    result['id_incremental'] = excess_amount * (tax_rates['id']['incremental'] / 100)
                    
                    # Reducir la deducción base (se aplica solo al 25% de la parte no incremental)
                    result['id_base'] = previous_average * (tax_rates['id']['base'] / 100)
                else:
                    # Si no hay exceso, toda la deducción va al 25%
                    result['id_base'] = result['eligible_expenses']['total'] * (tax_rates['id']['base'] / 100)
            except (ValueError, TypeError, KeyError) as e:
                print(f"Error al calcular deducción incremental: {e}")
                # Si hay error, aplicar la deducción base normal
                result['id_base'] = result['eligible_expenses']['total'] * (tax_rates['id']['base'] / 100)
        else:
            # Si no hay datos de años anteriores, aplicar deducción base normal
            result['id_base'] = result['eligible_expenses']['total'] * (tax_rates['id']['base'] / 100)
        
        # Deducción adicional por personal exclusivo I+D
        result['id_personnel'] = result['eligible_expenses']['exclusive_personnel'] * (tax_rates['id']['personnel'] / 100)
        
        # Total
        result['total'] = result['id_base'] + result['id_personnel'] + result['id_incremental']
        
    elif qualification == 'IT':
        # Deducción de IT
        result['it'] = result['eligible_expenses']['total'] * (tax_rates['it']['base'] / 100)
        
        # Total
        result['total'] = result['it']
        
    elif qualification == 'MIXED':
        # Para proyectos mixtos, dividimos los gastos entre I+D e IT
        # Por defecto, asumimos una distribución 60/40 entre I+D e IT
        id_portion = 0.6
        it_portion = 0.4
        
        # Distribuir gastos entre I+D e IT
        id_expenses = result['eligible_expenses']['total'] * id_portion
        it_expenses = result['eligible_expenses']['total'] * it_portion
        
        # Calcular deducción I+D
        result['id_base'] = id_expenses * (tax_rates['id']['base'] / 100)
        
        # Deducción adicional por personal exclusivo I+D (aplicada solo a la parte de I+D)
        result['id_personnel'] = result['eligible_expenses']['exclusive_personnel'] * (tax_rates['id']['personnel'] / 100)
        
        # Calcular deducción IT
        result['it'] = it_expenses * (tax_rates['it']['base'] / 100)
        
        # Total
        result['total'] = result['id_base'] + result['id_personnel'] + result['it']
        
    elif qualification == 'POTENTIAL':
        # Calcular ambas deducciones pero con un factor de incertidumbre
        # Deducción base de I+D (reducida por incertidumbre)
        result['id_base'] = result['eligible_expenses']['total'] * (tax_rates['id']['base'] / 100) * 0.5
        
        # Deducción de IT (reducida por incertidumbre)
        result['it'] = result['eligible_expenses']['total'] * (tax_rates['it']['base'] / 100) * 0.5
        
        # Deducción adicional por personal exclusivo I+D (reducida por incertidumbre)
        result['id_personnel'] = result['eligible_expenses']['exclusive_personnel'] * (tax_rates['id']['personnel'] / 100) * 0.5
        
        # Total
        result['total'] = result['id_base'] + result['id_personnel'] + result['it']
    
    # Redondear valores a 2 decimales
    for key in result:
        if isinstance(result[key], float):
            result[key] = round(result[key], 2)
    
    for category in result['eligible_expenses']:
        result['eligible_expenses'][category] = round(result['eligible_expenses'][category], 2)
    
    return result

def generate_recommendations(qualification, deduction, responses=None):
    """
    Genera recomendaciones basadas en la calificación y la deducción calculada
    
    Args:
        qualification (str): Calificación del proyecto ('ID', 'IT', 'POTENTIAL', 'NOT_QUALIFIED')
        deduction (dict): Resultados de la deducción
        responses (dict, optional): Respuestas del cuestionario
    
    Returns:
        list: Lista de recomendaciones
    """
    recommendations = []
    
    # Recomendaciones según la calificación
    if qualification == 'ID':
        recommendations.append("Según sus respuestas, su proyecto muestra indicadores claros de calificar como Investigación y Desarrollo (I+D).")
        recommendations.append("Los proyectos de I+D tienen la mayor deducción fiscal disponible (25% base).")        
        
        if deduction['id_incremental'] > 0:
            recommendations.append(f"Su proyecto tiene un incremento de gastos respecto a la media de los dos años anteriores, lo que le permite acceder a una deducción incremental del 42% sobre dicho exceso (aproximadamente {deduction['id_incremental']:,.2f} €).")
        
        if deduction['id_personnel'] > 0:
            recommendations.append("Ha identificado personal exclusivo dedicado a I+D, lo que le permite acceder a una deducción adicional del 17%.")
    
    elif qualification == 'IT':
        recommendations.append("Según sus respuestas, su proyecto muestra indicadores de calificar como Innovación Tecnológica (IT).")
        recommendations.append("Los proyectos de IT tienen una deducción fiscal del 12% sobre los gastos elegibles.")
    
    elif qualification == 'MIXED':
        recommendations.append("Según sus respuestas, su proyecto tiene características tanto de Investigación y Desarrollo (I+D) como de Innovación Tecnológica (IT).")
        recommendations.append("En estos casos, es recomendable separar los gastos de cada tipología para maximizar la deducción.")
        recommendations.append(f"Hemos estimado una aproximación de 60% para I+D (deducción del 25%) y 40% para IT (deducción del 12%), pero un análisis detallado podría modificar esta distribución.")
        
        if deduction['id_personnel'] > 0:
            recommendations.append("El personal exclusivo dedicado a I+D permite acceder a una deducción adicional del 17% sobre dichos gastos.")
    
    elif qualification == 'POTENTIAL':
        recommendations.append("Según sus respuestas, su proyecto muestra algunos indicadores de I+D y/o IT, pero la calificación no es definitiva.")
        recommendations.append("Se recomienda un análisis más detallado para determinar la calificación exacta.")
    
    else:  # NOT_QUALIFIED
        recommendations.append("Según sus respuestas, su proyecto podría no calificar directamente para deducciones fiscales por I+D+i.")
        recommendations.append("Sin embargo, recomendamos consultar con un experto fiscal especializado en I+D+i para un análisis más detallado.")
        return recommendations  # Retornar temprano ya que no hay más recomendaciones
    
    # Recomendaciones sobre el potencial de deducción
    if deduction['total'] > 20000:
        recommendations.append("El potencial de deducción fiscal es significativo. Se recomienda encarecidamente buscar asesoramiento fiscal especializado para maximizar el beneficio.")
    elif deduction['total'] > 5000:
        recommendations.append("El potencial de deducción fiscal es relevante. Un asesoramiento fiscal especializado podría ayudarle a maximizar este beneficio.")
    
    # Recomendaciones sobre las subvenciones
    if 'project_identification' in responses and responses['project_identification'].get('subsidy_received') == 'Sí':
        recommendations.append("Ha indicado que el proyecto ha recibido subvenciones. Recuerde que la parte subvencionada del proyecto NO puede aplicar para deducciones fiscales, ya que esos gastos ya han sido cubiertos.")
        recommendations.append("Para un cálculo preciso, debería restar del total de gastos elegibles aquella parte que ha sido financiada mediante subvenciones públicas.")
    
    # Recomendaciones sobre la seguridad jurídica
    recommendations.append("Para mayor seguridad jurídica, considere la solicitud de un <a href='/info/imv' target='_blank'>Informe Motivado Vinculante (IMV)</a> al Ministerio de Ciencia e Innovación.")
    
    # Recomendaciones sobre la documentación
    recommendations.append("Es fundamental mantener una documentación técnica detallada del proyecto, que evidencie las actividades de I+D+i realizadas.")
    recommendations.append("Asegúrese de documentar adecuadamente todos los gastos relacionados con el proyecto para justificar la deducción ante una posible inspección.")
    
    # Recomendaciones sobre monetización
    if deduction['total'] > 0:
        recommendations.append("Si su empresa no tiene suficiente cuota íntegra para aplicar la deducción, explore la opción de monetización de la misma (artículo 39.2 LIS).")
    
    # Recomendación final
    recommendations.append("Contacte con FADE para recibir orientación especializada sobre cómo proceder con su caso específico.")
    
    return recommendations
