"""
DJCoach PRO
core/phrase_engine.py

Phrase Engine v1.0

Responsable de:

- Contabilizar beats y compases
- Detectar frases musicales
- Calcular inicio y final de frases
- Generar información temporal para CoachEngine
- Preparar futuras sincronizaciones con Mixxx

Autor: DJCoach PRO
"""

from __future__ import annotations

import logging
import time

from dataclasses import dataclass, field
from typing import Optional

from models.dj_event import DJEvent
from models.event_types import EventType


# ============================================================
# CONFIGURACIÓN POR DEFECTO
# ============================================================

DEFAULT_BEATS_PER_BAR = 4
DEFAULT_PHRASE_BARS = 8


# ============================================================
# PHRASE STATE
# ============================================================

@dataclass(slots=True)
class PhraseState:
    """
    Estado interno del PhraseEngine.
    """

    beat_counter: int = 0
    bar_counter: int = 0
    phrase_counter: int = 0

    beat_in_bar: int = 0
    bar_in_phrase: int = 0

    last_timestamp: float = field(default_factory=time.time)

    bpm: float = 0.0

    phrase_started: bool = False
    phrase_finished: bool = False

    running: bool = False


# ============================================================
# PHRASE ENGINE
# ============================================================

class PhraseEngine:
    """
    Motor de análisis de frases musicales.

    Este módulo NO genera recomendaciones.

    Únicamente mantiene el estado temporal
    que posteriormente utilizarán:

        - CoachEngine
        - AI Engine
        - Performance Engine
    """

    def __init__(
        self,
        beats_per_bar: int = DEFAULT_BEATS_PER_BAR,
        phrase_bars: int = DEFAULT_PHRASE_BARS,
        logger: Optional[logging.Logger] = None,
    ):

        self.logger = logger or logging.getLogger("PhraseEngine")

        self.beats_per_bar = beats_per_bar
        self.phrase_bars = phrase_bars

        self.beats_per_phrase = (
            self.beats_per_bar *
            self.phrase_bars
        )

        self.state = PhraseState()

        self.logger.info(
            "PhraseEngine inicializado "
            "(%d beats/bar, %d bars/phrase)",
            self.beats_per_bar,
            self.phrase_bars,
        )

    # ========================================================
    # API PRINCIPAL
    # ========================================================

    def process(self, event: DJEvent) -> None:
        """
        Procesa un DJEvent.

        En la versión 1 únicamente se tendrán
        en cuenta eventos relacionados con
        CLOCK y BPM.

        Las siguientes versiones añadirán:

            - sincronización Mixxx
            - Phase Lock
            - Beat Grid
            - Quantize
        """

        if event is None:
            return

        self.state.last_timestamp = event.timestamp

        # Continúa en el módulo 2...

              # ----------------------------------------------------
        # Actualización de BPM (si viene informado)
        # ----------------------------------------------------

        bpm = event.data.get("bpm")

        if bpm is not None:
            try:
                self.state.bpm = float(bpm)
            except (TypeError, ValueError):
                pass

        # ----------------------------------------------------
        # Procesamiento de eventos BEAT
        # ----------------------------------------------------

        if event.event_type == EventType.BEAT:

            self._advance_beat()

            return

        # ----------------------------------------------------
        # Reinicio al cargar un tema
        # ----------------------------------------------------

        if event.event_type == EventType.TRACK_LOADED:

            self.reset()

            return

    # ========================================================
    # MOTOR INTERNO
    # ========================================================

    def _advance_beat(self) -> None:
        """
        Avanza un beat dentro del contador musical.
        """

        self.state.running = True

        self.state.phrase_started = False
        self.state.phrase_finished = False

        self.state.beat_counter += 1
        self.state.beat_in_bar += 1

        # --------------------------------------------
        # Nuevo compás
        # --------------------------------------------

        if self.state.beat_in_bar > self.beats_per_bar:

            self.state.beat_in_bar = 1

            self.state.bar_counter += 1
            self.state.bar_in_phrase += 1

            self.logger.debug(
                "Nuevo compás %d",
                self.state.bar_counter,
            )

        # --------------------------------------------
        # Inicio de frase
        # --------------------------------------------

        if self.state.bar_in_phrase == 1:

            self.state.phrase_started = True

        # --------------------------------------------
        # Fin de frase
        # --------------------------------------------

        if self.state.bar_in_phrase >= self.phrase_bars:

            self.state.phrase_finished = True

            self.state.bar_in_phrase = 0

            self.state.phrase_counter += 1

            self.logger.info(
                "Frase %d completada",
                self.state.phrase_counter,
            )

    # ========================================================
    # CONSULTAS
    # ========================================================

    def is_phrase_start(self) -> bool:
        """
        Indica si acaba de comenzar una frase.
        """

        return self.state.phrase_started

    def is_phrase_end(self) -> bool:
        """
        Indica si acaba de finalizar una frase.
        """

        return self.state.phrase_finished

    def current_bar(self) -> int:
        """
        Compás absoluto.
        """

        return self.state.bar_counter

    def current_phrase(self) -> int:
        """
        Número de frase actual.
        """

        return self.state.phrase_counter