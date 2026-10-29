from pathlib import Path


RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_OUTPUT = RUTA_BASE / "data" / "output"

RUTA_CSV = (
    RUTA_BASE / "data" / "raw" / "ai_job_replacement_dirty.csv"
)