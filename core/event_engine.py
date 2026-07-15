"""
DJCoach PRO
core/event_engine.py

Motor encargado de generar eventos de alto nivel
a partir de los eventos producidos por el StateEngine.

Autor: Juanjo + ChatGPT
Versión: 2.0
"""

from typing import List

from models.dj_event import DJEvent
from models.event_types import EventType


class EventEngine:
    """
    Genera eventos derivados de alto nivel.

    Entrada:
        DJEvent

    Salida:
        List[DJEvent]
    """

    def process(self, event: DJEvent) -> List[DJEvent]:

        generated: List[DJEvent] = []

        match event.type:

            case EventType.TRACK_STARTED:
                generated.extend(
                    self._handle_track_started(event)
                )

            case EventType.TRACK_STOPPED:
                generated.extend(
                    self._handle_track_stopped(event)
                )

            case EventType.MIX_STATE_CHANGED:
                generated.extend(
                    self._handle_mix_state(event)
                )

            case EventType.TRANSITION_STARTED:
                generated.extend(
                    self._handle_transition_started(event)
                )

            case EventType.TRANSITION_FINISHED:
                generated.extend(
                    self._handle_transition_finished(event)
                )

            case _:
                pass

        return generated

    # ---------------------------------------------------------

    def _handle_track_started(self, event: DJEvent) -> List[DJEvent]:
        return []

    # ---------------------------------------------------------

    def _handle_track_stopped(self, event: DJEvent) -> List[DJEvent]:
        return []

    # ---------------------------------------------------------

    def _handle_mix_state(self, event: DJEvent) -> List[DJEvent]:
        return []

    # ---------------------------------------------------------

    def _handle_transition_started(self, event: DJEvent) -> List[DJEvent]:
        return []

    # ---------------------------------------------------------

    def _handle_transition_finished(self, event: DJEvent) -> List[DJEvent]:
        return []