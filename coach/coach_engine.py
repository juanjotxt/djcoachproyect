"""
DJCoach PRO
engines/coach_engine.py

Coach Engine v1.0

Coordina el sistema de coaching a partir de los
eventos generados por el Core.

Autor: Juanjo + ChatGPT
"""

from models.dj_event import DJEvent
from models.event_types import EventType


class CoachEngine:

    def __init__(self):

        self.session_active = False
        self.transition_active = False

    # ---------------------------------------------------------

    def process(self, event: DJEvent) -> list[str]:
        """
        Procesa un DJEvent y devuelve recomendaciones
        o mensajes para el usuario.
        """

        recommendations = []

        match event.event_type:

            case EventType.TRACK_STARTED:
                recommendations.extend(
                    self._track_started(event)
                )

            case EventType.TRACK_STOPPED:
                recommendations.extend(
                    self._track_stopped(event)
                )

            case EventType.TRANSITION_STARTED:
                recommendations.extend(
                    self._transition_started(event)
                )

            case EventType.TRANSITION_FINISHED:
                recommendations.extend(
                    self._transition_finished(event)
                )

            case EventType.SESSION_IDLE:
                recommendations.extend(
                    self._session_finished(event)
                )

            case _:
                pass

        return recommendations

    # ---------------------------------------------------------

    def _track_started(self, event: DJEvent):

        messages = []

        if not self.session_active:
            self.session_active = True
            messages.append("Sesión iniciada.")

        if event.deck:
            messages.append(f"Deck {event.deck} reproduciendo.")

        return messages

    # ---------------------------------------------------------

    def _track_stopped(self, event: DJEvent):

        messages = []

        if event.deck:
            messages.append(f"Deck {event.deck} detenido.")

        return messages

    # ---------------------------------------------------------

    def _transition_started(self, event: DJEvent):

        self.transition_active = True

        return [
            "Transición iniciada.",
            "Analizando mezcla..."
        ]

    # ---------------------------------------------------------

    def _transition_finished(self, event: DJEvent):

        self.transition_active = False

        return [
            "Transición finalizada.",
            "Preparando evaluación."
        ]

    # ---------------------------------------------------------

    def _session_finished(self, event: DJEvent):

        self.session_active = False
        self.transition_active = False

        return [
            "Sesión finalizada."
        ]