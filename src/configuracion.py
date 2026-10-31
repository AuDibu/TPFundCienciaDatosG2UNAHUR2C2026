from pathlib import Path


# Rutas centralizadas del proyecto. Se calculan a partir de la ubicación de este
# archivo, así el análisis funciona igual sin importar desde dónde se ejecute
# (reproducibilidad: cualquier integrante del grupo obtiene el mismo resultado).

# Carpeta raíz del proyecto (un nivel arriba de /src).
RUTA_BASE = Path(__file__).resolve().parents[1]

# Carpeta donde se guardan los resultados: reporte de texto y gráficos.
RUTA_OUTPUT = RUTA_BASE / "data" / "output"

# Fuente de datos original ("sucia"): nunca se modifica, toda la limpieza se
# hace en memoria para conservar el dato crudo intacto.
RUTA_CSV = (
    RUTA_BASE / "data" / "raw" / "ai_job_replacement_dirty.csv"
)