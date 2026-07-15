"""
==========================================================
DJCoach Logger Pro v2.0
==========================================================
Sistema centralizado de logging para todo DJCoach.

Autor:
    Juanjo + Feder
==========================================================
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ----------------------------------------------------------
# Configuración
# ----------------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "djcoach.log"

LOG_LEVEL = logging.INFO

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)-25s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_initialized = False


# ----------------------------------------------------------
# Inicialización
# ----------------------------------------------------------

def setup_logger():

    global _initialized

    if _initialized:
        return

    formatter = logging.Formatter(
        LOG_FORMAT,
        DATE_FORMAT
    )

    # Consola

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # Archivo

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    root = logging.getLogger("DJCoach")

    root.setLevel(LOG_LEVEL)

    root.addHandler(console)
    root.addHandler(file_handler)

    root.propagate = False

    _initialized = True


# ----------------------------------------------------------
# Obtener logger
# ----------------------------------------------------------

def get_logger(module_name: str):

    setup_logger()

    return logging.getLogger(f"DJCoach.{module_name}")