"""
DJCoach PRO
core/timing_engine.py

Timing Engine v2.0
Motor encargado de medir tiempos de sesión,
tracks y transiciones.

Autor: Juanjo + ChatGPT
"""

from models.dj_event import DJEvent
from models.event_types import EventType


class TimingEngine:

    def __init__(self):

        self.session_start = None
        self.transition_start = None

        self.track_start = {
            "A": None,
            "B": None
        }

    # ---------------------------------------------------------

    def process(self, event: DJEvent) -> list[DJEvent]:

        generated = []

        match event.event_type:

            case EventType.TRACK_STARTED:
                self._track_started(event)

            case EventType.TRACK_STOPPED:
                generated.extend(self._track_stopped(event))

            case EventType.TRANSITION_STARTED:
                self._transition_started(event)

            case EventType.TRANSITION_FINISHED:
                generated.extend(self._transition_finished(event))

            case EventType.SESSION_IDLE:
                generated.extend(self._session_finished(event))

            case _:
                pass

        return generated

    # ---------------------------------------------------------

    def _track_started(self, event: DJEvent):

        if self.session_start is None:
            self.session_start = event.timestamp

        if event.deck in self.track_start:
            if self.track_start[event.deck] is None:
                self.track_start[event.deck] = event.timestamp

    # ---------------------------------------------------------

    def _track_stopped(self, event: DJEvent):

        generated = []

        if event.deck not in self.track_start:
            return generated

        start = self.track_start[event.deck]

        if start is None:
            return generated

        duration = event.timestamp - start

        self.track_start[event.deck] = None

        generated.append(
            DJEvent(
                event_id=0,
                event_type=EventType.TRACK_STOPPED,
                deck=event.deck,
                source="TIMING_ENGINE",
                timestamp=event.timestamp,
                data={
                    "track_duration": duration
                }
            )
        )

        return generated

    # ---------------------------------------------------------

    def _transition_started(self, event: DJEvent):

        if self.transition_start is None:
            self.transition_start = event.timestamp

    # ---------------------------------------------------------

    def _transition_finished(self, event: DJEvent):

        generated = []

        if self.transition_start is None:
            return generated

        duration = event.timestamp - self.transition_start

        self.transition_start = None

        generated.append(
            DJEvent(
                event_id=0,
                event_type=EventType.TRANSITION_FINISHED,
                source="TIMING_ENGINE",
                timestamp=event.timestamp,
                data={
                    "transition_duration": duration
                }
            )
        )

        return generated

    # ---------------------------------------------------------

    def _session_finished(self, event: DJEvent):

        generated = []

        if self.session_start is None:
            return generated

        duration = event.timestamp - self.session_start

        self.session_start = None
        self.transition_start = None

        self.track_start["A"] = None
        self.track_start["B"] = None

        generated.append(
            DJEvent(
                event_id=0,
                event_type=EventType.SESSION_IDLE,
                source="TIMING_ENGINE",
                timestamp=event.timestamp,
                data={
                    "session_duration": duration
                }
            )
        )

        return generated