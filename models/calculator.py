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

def calculate_deduction(qualification, expenses_responses, tax_rates, id_portion=1.0, it_portion=0.0, responses=None):
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
        'id_incremental': 0,
        'id_assets': 0,  # Deducción del 8% para activos fijos I+D
        'it': 0,
        'total': 0,
        'eligible_expenses': {
            'personnel': 0,
            'exclusive_personnel': 0,
            'external': 0,
            'equipment': 0,
            'materials': 0,
            'general': 0,
            'inmovilizado_id': 0,  # Inversiones en activos fijos para I+D
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
        
        # Comprobar gastos en activos fijos exclusivos para I+D
        if 'inmovilizado_id' in expenses_responses:
            result['eligible_expenses']['inmovilizado_id'] = float(expenses_responses.get('inmovilizado_id', 0))
        
    except (ValueError, TypeError) as e:
        # En caso de error en la conversión, mantener los valores en 0
        print(f"Error al procesar gastos: {e}")
    
    # Calcular total de gastos elegibles (sin incluir inmovilizado_id que tiene su propia deducción)
    result['eligible_expenses']['total'] = (
        result['eligible_expenses']['personnel'] +
        result['eligible_expenses']['external'] +
        result['eligible_expenses']['equipment'] +
        result['eligible_expenses']['materials'] +
        result['eligible_expenses']['general']
    )
    
    # Calcular deducciones según calificación y distribución de porcentajes
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
            result['id_base'] = result['eligible_expenses']['total'] * id_portion * (tax_rates['id']['base'] / 100)
            
            # Si hay parte de IT, calcularla también
            if it_portion > 0:
                result['it'] = result['eligible_expenses']['total'] * it_portion * (tax_rates['it']['base'] / 100)
        
        # Deducción adicional por personal exclusivo I+D - Siempre sobre el total indicado por el usuario
        # El personal exclusivo I+D no debe verse afectado por el ajuste de porcentajes id_portion/it_portion
        result['id_personnel'] = result['eligible_expenses']['exclusive_personnel'] * (tax_rates['id']['personnel'] / 100)
        
        # Deducción adicional por inversiones en activos para I+D (8%)
        if result['eligible_expenses']['inmovilizado_id'] > 0:
            result['id_assets'] = result['eligible_expenses']['inmovilizado_id'] * (tax_rates['id']['assets'] / 100)
        
        # Total
        result['total'] = result['id_base'] + result['id_personnel'] + result['id_incremental'] + result['id_assets']
        
    elif qualification == 'IT':
        # Deducción de IT
        result['it'] = result['eligible_expenses']['total'] * it_portion * (tax_rates['it']['base'] / 100)
        
        # Si hay parte de I+D por ajuste manual del usuario
        if id_portion > 0:
            result['id_base'] = result['eligible_expenses']['total'] * id_portion * (tax_rates['id']['base'] / 100)
            
            # Deducción adicional por personal exclusivo I+D - no afectada por los porcentajes
            result['id_personnel'] = result['eligible_expenses']['exclusive_personnel'] * (tax_rates['id']['personnel'] / 100)
            
            # Deducción adicional por inversiones en activos para I+D (8%)
            if result['eligible_expenses']['inmovilizado_id'] > 0 and id_portion > 0:
                result['id_assets'] = result['eligible_expenses']['inmovilizado_id'] * (tax_rates['id']['assets'] / 100)
        
        # Total
        result['total'] = result['id_base'] + result['id_personnel'] + result['id_assets'] + result['it']
        
    elif qualification == 'MIXED':
        # Para proyectos mixtos, usamos la distribución indicada en los parámetros
        # Si no se especifican, por defecto seguimos usando 60/40 entre I+D e IT
        if id_portion == 1.0 and it_portion == 0.0:  # Si se usan los valores por defecto
            id_portion = 0.6
            it_portion = 0.4
        
        # Distribuir gastos entre I+D e IT
        id_expenses = result['eligible_expenses']['total'] * id_portion
        it_expenses = result['eligible_expenses']['total'] * it_portion
        
        # Calcular deducción I+D
        result['id_base'] = id_expenses * (tax_rates['id']['base'] / 100)
        
        # Deducción adicional por personal exclusivo I+D (NO afectada por los porcentajes)
        result['id_personnel'] = result['eligible_expenses']['exclusive_personnel'] * (tax_rates['id']['personnel'] / 100)
        
        # Calcular deducción IT
        result['it'] = it_expenses * (tax_rates['it']['base'] / 100)
        
        # Deducción adicional por inversiones en activos para I+D (8%)
        if result['eligible_expenses']['inmovilizado_id'] > 0:
            result['id_assets'] = result['eligible_expenses']['inmovilizado_id'] * (tax_rates['id']['assets'] / 100) * id_portion
        
        # Total
        result['total'] = result['id_base'] + result['id_personnel'] + result['id_assets'] + result['it']
        
    elif qualification == 'POTENTIAL':
        # Calcular ambas deducciones pero con un factor de incertidumbre
        # Usar los porcentajes proporcionados o valores predeterminados ajustados por incertidumbre
        if id_portion == 1.0 and it_portion == 0.0:  # Si se usan los valores por defecto
            id_portion = 0.5
            it_portion = 0.5
        else:
            # Reducimos la certeza en los porcentajes ajustados por el usuario
            id_portion = id_portion * 0.8  # Reducción del 20% por incertidumbre
            it_portion = it_portion * 0.8  # Reducción del 20% por incertidumbre
        
        # Deducción base de I+D (ajustada por incertidumbre)
        result['id_base'] = result['eligible_expenses']['total'] * id_portion * (tax_rates['id']['base'] / 100)
        
        # Deducción de IT (ajustada por incertidumbre)
        result['it'] = result['eligible_expenses']['total'] * it_portion * (tax_rates['it']['base'] / 100)
        
        # Deducción adicional por personal exclusivo I+D (reducida por incertidumbre)
        result['id_personnel'] = result['eligible_expenses']['exclusive_personnel'] * (tax_rates['id']['personnel'] / 100) * 0.5
        
        # Deducción adicional por inversiones en activos para I+D (8%) (reducida por incertidumbre)
        if result['eligible_expenses']['inmovilizado_id'] > 0:
            result['id_assets'] = result['eligible_expenses']['inmovilizado_id'] * (tax_rates['id']['assets'] / 100) * id_portion * 0.5
        
        # Total
        result['total'] = result['id_base'] + result['id_personnel'] + result['id_assets'] + result['it']
    
    # Redondear valores a 2 decimales
    for key in result:
        if isinstance(result[key], float):
            result[key] = round(result[key], 2)
    
    for category in result['eligible_expenses']:
        result['eligible_expenses'][category] = round(result['eligible_expenses'][category], 2)
    
    return result

def calculate_deduction_limits(deduction, quota, tax_rates):
    """
    Calcula los límites de aplicación para la deducción fiscal
    
    Args:
        deduction (dict): Resultados de la deducción calculada
        quota (float): Cuota íntegra minorada (CIM) para calcular límites
        tax_rates (dict): Tasas de impuestos para I+D e IT
    
    Returns:
        dict: Resultados con información sobre límites y aplicación
    """
    result = {
        'cim': quota,
        'limit_25': round(quota * 0.25, 2),  # Límite general 25%
        'limit_50': round(quota * 0.50, 2),  # Límite incrementado 50%
        'applicable_limit': 0,
        'is_limit_50_applicable': False,
        'deduction_applicable': 0,
        'deduction_pending': 0,
        'monetization_option': {
            'is_available': False,
            'amount_before_discount': 0,
            'discount': 0,
            'net_amount': 0
        }
    }
    
    # Total deducción bruta
    total_deduction = deduction['total']
    
    # Verificar si aplica límite incrementado (50%)
    # La deducción del ejercicio supera el 10% de la CIM
    if total_deduction > (quota * 0.10):
        result['is_limit_50_applicable'] = True
        result['applicable_limit'] = result['limit_50']
    else:
        result['applicable_limit'] = result['limit_25']
    
    # Calcular deducción aplicable y pendiente
    if total_deduction <= result['applicable_limit']:
        result['deduction_applicable'] = total_deduction
        result['deduction_pending'] = 0
    else:
        result['deduction_applicable'] = result['applicable_limit']
        result['deduction_pending'] = round(total_deduction - result['applicable_limit'], 2)
    
    # Verificar si puede aplicar la monetización (si hay pendiente o CIM insuficiente)
    if result['deduction_pending'] > 0 or quota == 0:
        result['monetization_option']['is_available'] = True
        
        # Calcular importes para monetización
        amount_to_monetize = result['deduction_pending'] if result['deduction_pending'] > 0 else total_deduction
        result['monetization_option']['amount_before_discount'] = amount_to_monetize
        result['monetization_option']['discount'] = round(amount_to_monetize * 0.20, 2)  # 20% de descuento
        result['monetization_option']['net_amount'] = round(amount_to_monetize * 0.80, 2)  # 80% del importe
    
    return result

def calculate_assets_deduction(asset_investment, tax_rates):
    """
    Calcula la deducción fiscal por inversiones en elementos del inmovilizado material 
    e intangible afectos exclusivamente a actividades de I+D
    
    Args:
        asset_investment (float): Valor de las inversiones en inmovilizado para I+D
        tax_rates (dict): Tasas de impuestos para I+D e IT
    
    Returns:
        float: Importe de la deducción por inversiones en activos para I+D
    """
    # Verificar si existe la tasa para inversiones en el diccionario
    if 'assets' in tax_rates['id']:
        assets_rate = tax_rates['id']['assets']
    else:
        assets_rate = 8  # Valor por defecto si no está definido
    
    # Calcular deducción (8% del valor de las inversiones)
    return round(asset_investment * (assets_rate / 100), 2)

def calculate_social_security_bonus(researcher_costs, months=12):
    """
    Calcula la bonificación en la cotización a la Seguridad Social para personal investigador
    
    Args:
        researcher_costs (float): Coste salarial del personal investigador
        months (int): Número de meses a considerar (por defecto 12)
    
    Returns:
        dict: Información sobre la bonificación calculada
    """
    result = {
        'monthly_salary': round(researcher_costs / months, 2),
        'monthly_ss_cost': 0,  # Coste mensual aprox. de SS
        'monthly_bonus': 0,    # Bonificación mensual (40%)
        'annual_bonus': 0      # Bonificación anual
    }
    
    # Estimación de coste de SS empresarial (aprox. 30% del salario bruto)
    ss_rate = 0.30  # 30% es una estimación del coste de SS empresarial
    result['monthly_ss_cost'] = round(result['monthly_salary'] * ss_rate, 2)
    
    # Bonificación del 40% sobre el coste de SS
    bonus_rate = 0.40  # 40% de bonificación según RD 475/2014
    result['monthly_bonus'] = round(result['monthly_ss_cost'] * bonus_rate, 2)
    result['annual_bonus'] = round(result['monthly_bonus'] * months, 2)
    
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
        
        if deduction['id_assets'] > 0:
            recommendations.append(f"Ha indicado inversiones en elementos del inmovilizado material e intangible exclusivos para I+D, lo que le permite acceder a una deducción adicional del 8% sobre dichas inversiones (aproximadamente {deduction['id_assets']:,.2f} €).")
    
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
    recommendations.append("Para mayor seguridad jurídica, considere la solicitud de un <a href='/info/imv' target='_blank'>Informe Motivado Vinculante (IMV)</a> al Ministerio de Ciencia e Innovación que certifique la naturaleza de I+D+i de su proyecto.")
    recommendations.append("El IMV es un documento que aporta seguridad jurídica total frente a posibles inspecciones, validando tanto la calificación como los gastos deducibles. Además, es obligatorio para acceder a la monetización de la deducción si no puede aplicarla por insuficiencia de cuota.")
    
    # Recomendaciones sobre la documentación
    recommendations.append("Es fundamental mantener una documentación técnica detallada del proyecto, que evidencie las actividades de I+D+i realizadas.")
    recommendations.append("Asegúrese de documentar adecuadamente todos los gastos relacionados con el proyecto para justificar la deducción ante una posible inspección.")
    
    # Recomendaciones sobre monetización
    if deduction['total'] > 0:
        recommendations.append("Si su empresa no tiene suficiente cuota íntegra para aplicar la deducción, explore la opción de monetización de la misma (artículo 39.2 LIS) que permite recuperar hasta el 80% de la deducción cuando no se puede aplicar por insuficiencia de cuota o por exceder los límites.")
        recommendations.append("También considere la libertad de amortización para elementos del inmovilizado material e intangible afectos a actividades de I+D, lo que permite acelerar la recuperación fiscal de la inversión.")
    
    # Recomendaciones adicionales sobre personal investigador
    if 'exclusive_personnel' in deduction['eligible_expenses'] and deduction['eligible_expenses']['exclusive_personnel'] > 0:
        recommendations.append("Considere la bonificación del 40% en las cotizaciones a la Seguridad Social para el personal investigador con dedicación exclusiva a actividades de I+D+i.")
        recommendations.append("Para compatibilizar esta bonificación con la deducción fiscal puede ser necesario obtener el Sello de PYME Innovadora. Sin este sello, generalmente habrá que optar por uno de los dos incentivos.")
    
    # Recomendación IMV específica para régimen opcional
    if deduction['total'] > 20000:
        recommendations.append("Para aplicar el régimen opcional de monetización (art. 39.2 LIS) es obligatorio disponer de un Informe Motivado Vinculante (IMV) que certifique la naturaleza de I+D o IT de las actividades.")
    
    # Recomendación final
    recommendations.append("Contacte con FADE para recibir orientación especializada sobre cómo proceder con su caso específico.")
    
    return recommendations
