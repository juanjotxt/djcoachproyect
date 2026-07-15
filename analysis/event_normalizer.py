"""
=========================================================
DJCoach Pro
Archivo : event_normalizer.py
Versión : 1.0.0
Estado  : MIDI EVENT CLEANER
=========================================================
"""

import time
from typing import Optional
from event_engine import DJEvent


class DJEventNormalizer:

    def __init__(self, debounce_ms: int = 80):

        self.debounce = debounce_ms / 1000.0
        self._last_event_time = {}
        self._last_value = {}

    # -----------------------------------------------------

    def process(self, event: DJEvent) -> Optional[DJEvent]:

        key = f"{event.category}:{event.field}"
        now = event.timestamp

        # -------------------------------------------------
        # 1. BINARIOS → NO FILTRAR
        # -------------------------------------------------

        if event.field in ("playing", "cue", "sync", "loaded"):

            self._last_event_time[key] = now
            self._last_value[key] = event.value
            return event

        # -------------------------------------------------
        # 2. DEBOUNCE TEMPORAL (CONTINUOS)
        # -------------------------------------------------

        last_time = self._last_event_time.get(key)

        if last_time and (now - last_time) < self.debounce:
            return None

        # -------------------------------------------------
        # 3. FILTRO DE DUPLICADOS (CONTINUOS)
        # -------------------------------------------------

        last_value = self._last_value.get(key)

        if last_value is not None and last_value == event.value:
            return None

        # actualizar estado interno
        self._last_event_time[key] = now
        self._last_value[key] = event.value

        return event

    # -----------------------------------------------------

    def reset(self):
        self._last_event_time.clear()
        self._last_value.clear()