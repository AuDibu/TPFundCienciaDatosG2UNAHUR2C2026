# Trabajo Práctico: Impacto de la IA en el Empleo (2020-2026)
## Sector Asignado: Finanzas (Finance)

### 1. Introducción Académica
El avance de la Inteligencia Artificial no es solo un fenómeno técnico, sino una fuerza socioeconómica que está redefiniendo la naturaleza del trabajo. En los próximos años, diversos sectores experimentarán cambios sin precedentes en sus estructuras salariales, demandas de habilidades y estabilidad laboral. Este Trabajo Práctico propone analizar estas tendencias con rigor científico y pensamiento crítico.

### 2. Ficha del Proyecto: Grupo 2
*   **Sector**: Finanzas.
*   **Objetivo General**: Analizar el impacto de la IA en la volatilidad salarial y la brecha de habilidades dentro del sector financiero, identificando países con mayor estrés de transición.

### 3. Fase I: Diagnóstico y Saneamiento (Caja Negra)
Ustedes trabajarán con la fuente de datos `ai_job_replacement_dirty.csv`. **Advertencia**: La fuente posee anomalías estructuradas.
- **Auditoría de Calidad**: Realicen un reporte inicial sobre el estado de la información. Deben identificar inconsistencias lógicas, errores de formato y vacíos de datos sin guía externa.
- **Protocolo de Curación**: Implementen y documenten un proceso sistemático de limpieza. Cada decisión (casteo de tipos, manejo de nulos, eliminación de duplicados) debe estar técnicamente justificada en su bitácora.
- **Normalización**: Traduzcan y estandaricen los campos para asegurar una lectura fluida en español.

### 4. Fase II: Análisis Estadístico y Exploratorio (EDA)
Utilizando las librerías Pandas y NumPy, resuelvan las siguientes problemáticas:
- **Volatilidad de Ingresos**: Calculen el rango y la varianza de los salarios antes y después de la IA. ¿Qué nos dice esto sobre la estabilidad del sector?
- **Brecha de Habilidades**: Determinen el promedio de `skill_gap_index` por país y encuentren dónde es más crítico el desfase formativo.
- **Detección de Outliers**: Identifiquen salarios que desafíen los rangos normales del mercado (valores negativos o extremos) y decidan su tratamiento.

### 5. Fase III: Visualización y Comunicación
Diseñen las siguientes piezas utilizando Matplotlib:
- **Gráfico de Evolución**: Tendencia anual del salario promedio en finanzas desde 2020 a 2026.
- **Gráfico de Distribución (Pie/Pie Chart)**: Distribución de los roles según su categoría de riesgo de automatización.
- **Heatmap o Barras Geográficas**: Comparativa del `ai_adoption_level` por país para este sector.

### 6. Fase IV: Reflexión Crítica (Anti-LLM)
*Responda basándose estrictamente en los hallazgos de su procesamiento de datos:*
- ¿Existe evidencia de que la IA esté "empobreciendo" los roles tradicionales de finanzas?
- Según sus datos, ¿la factibilidad de trabajo remoto protege o expone más al trabajador financiero frente al reemplazo por IA?

### 7. Requerimientos de Entrega y Defensa
1.  **Informe Profesional**: PDF o Markdown con resumen ejecutivo, bitácora de saneamiento e interpretación de resultados.
2.  **Código Fuente**: Script o Notebook estructurado, comentado y reproducible.
3.  **Defensa Oral**: Justificación técnica de la limpieza e interpretación de las visualizaciones ante el curso.
