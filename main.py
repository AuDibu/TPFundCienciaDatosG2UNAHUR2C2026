# # Trabajo Práctico: Impacto de la IA en el Empleo (2020-2026)
# ## Sector Asignado: Finanzas (Finance)
# 
# ### 1. Introducción Académica
# El avance de la Inteligencia Artificial no es solo un fenómeno técnico, sino una fuerza socioeconómica que está redefiniendo la naturaleza del trabajo. En los próximos años, diversos sectores experimentarán cambios sin precedentes en sus estructuras salariales, demandas de habilidades y estabilidad laboral. Este Trabajo Práctico propone analizar estas tendencias con rigor científico y pensamiento crítico.
# 
# ### 2. Ficha del Proyecto: Grupo 2
# *   **Sector**: Finanzas.
# *   **Objetivo General**: Analizar el impacto de la IA en la volatilidad salarial y la brecha de habilidades dentro del sector financiero, identificando países con mayor estrés de transición.

# #### Setup y parametros

from src.configuracion import RUTA_CSV
from src.fase_i_saneamiento import (
    analizar_vacios_y_duplicados,
    cargar_y_mostrar_dataset,
    filtrar_outliers,
    identificar_inconsistencias_categoricas,
    limpiar_dataset,
)
from src.fase_ii_eda import (
    analizar_brecha_habilidades,
    calcular_volatilidad_ingresos,
    detectar_outliers,
)

# ### 3. Fase I: Diagnóstico y Saneamiento (Caja Negra)
# Ustedes trabajarán con la fuente de datos `ai_job_replacement_dirty.csv`. **Advertencia**: La fuente posee anomalías estructuradas.
# - **Auditoría de Calidad**: Realicen un reporte inicial sobre el estado de la información. Deben identificar inconsistencias lógicas, errores de formato y vacíos de datos sin guía externa.
# - **Protocolo de Curación**: Implementen y documenten un proceso sistemático de limpieza. Cada decisión (casteo de tipos, manejo de nulos, eliminación de duplicados) debe estar técnicamente justificada en su bitácora.
# - **Normalización**: Traduzcan y estandaricen los campos para asegurar una lectura fluida en español.

df = cargar_y_mostrar_dataset(RUTA_CSV)

analizar_vacios_y_duplicados(df)

identificar_inconsistencias_categoricas(df)

# #### Limpieza inicial del dataset
# 
# *Puntos a atacar:*
# 
# - Repetidos:
#   - Detectados: 
#     - 50 filas repetidas
#   - Estrategia:
#     - Se dejara una fila única por cada repetido
# - Conflictos en columnas categóricas:
#   - Detectados:
#     - Industry presenta inconsistencias en su uso de mayúsculas y minúsculas
#     - Salary_before_usd y salary_after_usd: floats que estan en formato string y presentan uso inconsistente del carácter "$"
#   - Estrategia:
#     - Industry sera pasado a solo minúscula de manera general
#     - Salary_before_usd y salary_after_usd seran convertidos a float
# - Vacios:
#   - Detectados:
#     - salary_after_usd: 754
#     - salary_before_usd: 753
#     - automation_risk_percent: 752
#     - industry: 751
#   - Estrategia:
#     - Los casos vacios de Industry se completaran con "unknown"
#     - Los vacios de automation_risk_percent seran completados analizando el promedio a nivel job_role/industry.
#     - Los vacios de salary_before_usd y salary_after_usd seran completados analizando la mediana a nivel job_role/industry.
#       - Se usa la mediana ya que los sueldos muy altos o muy bajos harian del promedio un valor poco representativo. 

# Limpieza de duplicados
# Saneamiento de strings
# Conversión de columnas de salario a tipo numérico
df = limpiar_dataset(df)

# #### Añadido pre análisis: generación de copia para outliers
# 
# Se genera una copia del dataset previo al tratamiento de los outliers. El análisis de los mismos se detalla en la sección correspondiente. 
# 
# Los outliers son eliminados de la muestra.
df, df_outliers = filtrar_outliers(df)

# ### 4. Fase II: Análisis Estadístico y Exploratorio (EDA)
# Utilizando las librerías Pandas y NumPy, resuelvan las siguientes problemáticas:
# - **Volatilidad de Ingresos**: Calculen el rango y la varianza de los salarios antes y después de la IA. ¿Qué nos dice esto sobre la estabilidad del sector?
# - **Brecha de Habilidades**: Determinen el promedio de `skill_gap_index` por país y encuentren dónde es más crítico el desfase formativo.
# - **Detección de Outliers**: Identifiquen salarios que desafíen los rangos normales del mercado (valores negativos o extremos) y decidan su tratamiento.

# #### Volatilidad de Ingresos
# 
# En este caso se agrupo por job_role y country, considerando el mismo puesto dentro del mercado local. Posteriormente se obtuvo el porcentaje de incremento o decremento entre los valores pre y post tanto de rango como varianza. Dichos valores fueron promediados para tener un indicador general del estado del mercado.
calcular_volatilidad_ingresos(df)

# #### Brecha de Habilidades
analizar_brecha_habilidades(df)

# #### Detección de outliers
# Para detectar los outliers se usa IQR. Se segmenta por job_role y country para que el rango comprenda puestos similares dentro la misma economia local.
# En resumen, el IQR representa el rango central de los datos obtenido a partir de restar el cuartil 25 al cuartil 75. No representa el punto medio sino la distancia entre el Q25 y Q75.
# Posteriormente podemos usar dicha distancia multiplicada por 1,5 para establecer topes inferiores y superiores (conocidos como barreras de Tukey) para determinar los outliers.
# Aquellos outliers detectados fueron eliminados en un paso previo. En el bloque siguiente se aprecia la detección en detalle de los mismos usando una copia de respaldo previo a dicho tratamiento.
# Referencia: https://metricgate.com/docs/es/interquartile-range-outlier/
detectar_outliers(df_outliers)


# ### 5. Fase III: Visualización y Comunicación
# Diseñen las siguientes piezas utilizando Matplotlib:
# - **Gráfico de Evolución**: Tendencia anual del salario promedio en finanzas desde 2020 a 2026.
# - **Gráfico de Distribución (Pie/Pie Chart)**: Distribución de los roles según su categoría de riesgo de automatización.
# - **Heatmap o Barras Geográficas**: Comparativa del `ai_adoption_level` por país para este sector.

# ### 6. Fase IV: Reflexión Crítica (Anti-LLM)
# *Responda basándose estrictamente en los hallazgos de su procesamiento de datos:*
# - ¿Existe evidencia de que la IA esté "empobreciendo" los roles tradicionales de finanzas?
# - Según sus datos, ¿la factibilidad de trabajo remoto protege o expone más al trabajador financiero frente al reemplazo por IA?

# ### 7. Requerimientos de Entrega y Defensa
# 1.  **Informe Profesional**: PDF o Markdown con resumen ejecutivo, bitácora de saneamiento e interpretación de resultados.
# 2.  **Código Fuente**: Script o Notebook estructurado, comentado y reproducible.
# 3.  **Defensa Oral**: Justificación técnica de la limpieza e interpretación de las visualizaciones ante el curso.
#