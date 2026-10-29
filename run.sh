#!/usr/bin/env bash
set -euo pipefail

log() {
    printf '[run.sh] %s\n' "$1"
}

abrir_en_terminal_si_hace_falta() {
    if [[ "${RUN_SH_LAUNCHED:-0}" == "1" ]]; then
        return
    fi

    if [[ -t 1 ]]; then
        return
    fi

    if [[ -z "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]]; then
        return
    fi

    local script_path
    script_path="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/$(basename -- "${BASH_SOURCE[0]}")"
    local relaunch_cmd
    relaunch_cmd="RUN_SH_LAUNCHED=1 $(printf '%q' "$script_path")"

    if command -v gnome-terminal >/dev/null 2>&1; then
        exec gnome-terminal -- bash -lc "$relaunch_cmd"
    elif command -v konsole >/dev/null 2>&1; then
        exec konsole -e bash -lc "$relaunch_cmd"
    elif command -v xfce4-terminal >/dev/null 2>&1; then
        exec xfce4-terminal --command="bash -lc \"$relaunch_cmd\""
    elif command -v mate-terminal >/dev/null 2>&1; then
        exec mate-terminal -- bash -lc "$relaunch_cmd"
    elif command -v x-terminal-emulator >/dev/null 2>&1; then
        exec x-terminal-emulator -e bash -lc "$relaunch_cmd"
    elif command -v xterm >/dev/null 2>&1; then
        exec xterm -e bash -lc "$relaunch_cmd"
    fi

    printf 'No se encontró un emulador de terminal compatible para abrir este script por doble clic.\n' >&2
    printf 'Probá ejecutarlo desde una consola: bash run.sh\n' >&2
    exit 1
}

abrir_en_terminal_si_hace_falta

log "Inicio del lanzador"
trap 'printf "[run.sh] Error en la linea %s.\n" "$LINENO" >&2' ERR

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"
log "Directorio del proyecto: $PROJECT_DIR"

PYTHON="${PYTHON:-python3}"
log "Verificando intérprete de Python: $PYTHON"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
    printf 'No se encontró el intérprete: %s\n' "$PYTHON" >&2
    exit 1
fi

if [[ ! -x ".venv/bin/python" ]]; then
    log "Creando entorno virtual en .venv"
    "$PYTHON" -m venv .venv
else
    log "Entorno virtual existente detectado en .venv"
fi

log "Activando entorno virtual"
source .venv/bin/activate
log "Instalando dependencias desde requirements.txt"
python -m pip install -r requirements.txt
log "Lanzando main.py"
python main.py
log "Proceso finalizado"
