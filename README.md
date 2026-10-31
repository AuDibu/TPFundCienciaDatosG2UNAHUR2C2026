# Impacto de la IA en el empleo: sector Finanzas

Trabajo práctico del Grupo 2 para la materia Fundamentos de Ciencia de Datos. El proyecto analiza datos sobre el impacto de la inteligencia artificial en el empleo entre 2020 y 2026, con foco en el sector financiero.

El objetivo es estudiar la volatilidad de los salarios, la brecha de habilidades y el riesgo de automatización, y comunicar los resultados mediante un informe y visualizaciones.

## Requisitos

- Python 3
- `pip`

Las dependencias del análisis están listadas en [`requirements.txt`](requirements.txt): Pandas, NumPy y Matplotlib.

## Ejecución

Desde la carpeta del repositorio:

**Linux**

```bash
bash run.sh
```

**Windows**

```bat
run.bat
```

Los lanzadores crean el entorno virtual `.venv` si aún no existe, instalan las dependencias y ejecutan `main.py`. También se puede ejecutar el programa manualmente:

```bash
python -m venv .venv

# Linux
source .venv/bin/activate

# Windows (CMD)
.venv\Scripts\activate

python -m pip install -r requirements.txt
python main.py
```

El conjunto de datos de entrada debe estar en `data/raw/ai_job_replacement_dirty.csv`, la ubicación configurada por el proyecto.

## Proceso de análisis

El programa ejecuta estas etapas:

1. **Auditoría:** carga el CSV y revisa sus dimensiones, valores faltantes, duplicados y categorías de texto.
2. **Saneamiento:** elimina filas duplicadas, normaliza espacios y nombres de industria, convierte los salarios a valores numéricos e imputa faltantes. La industria se completa con `unknown`; el riesgo de automatización se imputa con el promedio por puesto e industria, y los salarios con la mediana del mismo grupo.
3. **Outliers:** calcula límites de Tukey (1,5 × IQR) por puesto y país para los salarios. Conserva una copia previa al filtrado para detallar los valores atípicos en el informe y excluye esos registros del análisis posterior.
4. **Análisis exploratorio:** filtra los datos a la industria `finance`, calcula la volatilidad de ingresos por puesto y país, compara el índice de brecha de habilidades por país e informa los salarios atípicos.
5. **Visualización:** genera gráficos sobre salarios promedio por año, categorías de riesgo de automatización y adopción promedio de IA por país.
6. **Reflexión crítica:** compara la variación porcentual del salario mediano post IA entre 2020 y 2026 por país, incluyendo todos los roles; además, calcula los promedios de `ai_replacement_score` y `automation_risk_percent` por rangos de 25 puntos de factibilidad de trabajo remoto.

## Archivos generados

Los resultados se guardan en `data/output/`:

- `report.txt`: auditoría, decisiones de saneamiento, resultados estadísticos y referencias a los gráficos generados.
- `evolucion_salarial_finanzas.png`: evolución anual del salario promedio posterior a la IA.
- `distribucion_riesgo_automatizacion_finanzas.png`: distribución de los registros por categoría de riesgo.
- `adopcion_ia_por_pais_finanzas.png`: adopción promedio de IA por país.

Estos archivos se regeneran al ejecutar el programa. `data/output/` está excluida del control de versiones, salvo por el archivo `.gitkeep`.

## Estructura del repositorio

```text
main.py                         Punto de entrada del análisis
requirements.txt                Dependencias de Python
run.sh / run.bat                Lanzadores para Linux y Windows
data/
  raw/                          Dataset de entrada
  output/                       Informe y gráficos generados
src/
  configuracion.py              Rutas del proyecto
  saneamiento.py                Auditoría, limpieza e imputación
  outliers.py                   Límites de Tukey
  eda.py                        Análisis exploratorio y visualizaciones
```
