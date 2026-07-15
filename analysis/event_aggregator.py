"""
event_aggregator.py v1.1

DJCoach Pro - Intelligent Event Aggregator

Convierte streams MIDI ruidosos en eventos de alto nivel:
- START / MOVING / STOP
- Filtrado de redundancia
"""

import time
from collections import defaultdict


class DJEventAggregator:

    def __init__(self, stop_threshold=0.25):
        """
        stop_threshold: segundos sin cambios para considerar STOP
        """

        self.last_event = {}
        self.last_value = {}
        self.last_time = {}

        self.stop_threshold = stop_threshold

        self.output_queue = []

    # -------------------------------------------------

    def receive(self, event):
        """
        Entrada principal del sistema.
        Espera eventos con estructura tipo:

        event = {
            "type": "PITCH",
            "value": 0.52,
            ...
        }
        """

        if event is None:
            return

        etype = event.get("type")
        value = event.get("value")

        if etype is None:
            return

        now = time.time()

        # -------------------------------------------------
        # 1. Detectar inicio de movimiento
        # -------------------------------------------------

        if etype not in self.last_event:
            self.output_queue.append({
                "type": f"{etype}_START",
                "value": value
            })

        # -------------------------------------------------
        # 2. Detectar cambio significativo
        # -------------------------------------------------

        last_val = self.last_value.get(etype)

        if last_val is None or abs(last_val - value) > 0.0005:

            self.output_queue.append({
                "type": f"{etype}_MOVING",
                "value": value
            })

            self.last_time[etype] = now

        # -------------------------------------------------
        # 3. Guardar estado
        # -------------------------------------------------

        self.last_event[etype] = event
        self.last_value[etype] = value

    # -------------------------------------------------

    def update(self):
        """
        Debe llamarse periódicamente desde el main loop.
        Detecta STOP por inactividad.
        """

        now = time.time()

        for etype, last_t in list(self.last_time.items()):

            if now - last_t > self.stop_threshold:

                self.output_queue.append({
                    "type": f"{etype}_STOP"
                })

                # evitar múltiples STOP
                del self.last_time[etype]

    # -------------------------------------------------

    def get_events(self):
        """
        Devuelve eventos procesados y limpia cola.
        """

        events = self.output_queue[:]
        self.output_queue.clear()

        return events

    # -------------------------------------------------

    def reset(self):

        self.last_event.clear()
        self.last_value.clear()
        self.last_time.clear()
        self.output_queue.clear()

    # -------------------------------------------------

    def pending(self):

        return len(self.output_queue)