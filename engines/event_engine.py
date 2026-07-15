"""
DJCoach PRO
engines/event_engine.py

EventEngine v3.0

Genera eventos de alto nivel a partir del estado del DJ.

Arquitectura

DJStateEngine
        │
        ▼
EventEngine
        │
        ▼
List[DJEvent]

Autor:
Juanjo + ChatGPT
"""

from __future__ import annotations

from copy import deepcopy
from typing import List, Optional

from models.dj_event import DJEvent
from models.event_types import EventType

from engines.state_engine import DJStateEngine


class EventEngine:
    """
    Motor encargado de detectar cambios
    en el estado del sistema.

    No modifica el estado.

    Sólo observa y genera DJEvent.
    """

    # -----------------------------------------------------

    def __init__(self):

        self._event_id = 0

        self._previous_state = None

    # -----------------------------------------------------

    def _next_event_id(self) -> int:

        self._event_id += 1

        return self._event_id

    # -----------------------------------------------------

    def process(
        self,
        state: DJStateEngine
    ) -> List[DJEvent]:

        """
        Compara el estado anterior con el actual.

        Devuelve únicamente los eventos
        que hayan cambiado.
        """

        events: List[DJEvent] = []

        # Primera ejecución

        if self._previous_state is None:

            self._previous_state = deepcopy(
                state.get_state()
            )

            return events

        current = state.get_state()

        # ------------------------------------------
        # Deck A
        # ------------------------------------------

        events.extend(

            self._process_deck(
                "A",
                self._previous_state["deck_a"],
                current["deck_a"]
            )

        )

        # ------------------------------------------
        # Deck B
        # ------------------------------------------

        events.extend(

            self._process_deck(
                "B",
                self._previous_state["deck_b"],
                current["deck_b"]
            )

        )

        # ------------------------------------------
        # Mix
        # ------------------------------------------

        events.extend(

            self._process_mix(
                self._previous_state,
                current
            )

        )

        # Guardamos snapshot

        self._previous_state = deepcopy(current)

        return events

    # =====================================================
    # DECK
    # =====================================================

    def _process_deck(
        self,
        deck: str,
        previous: dict,
        current: dict
    ) -> List[DJEvent]:

        """
        Procesa un deck.

        Continúa en el bloque 2.
        """

        return []

    # =====================================================
    # MIX
    # =====================================================

    def _process_mix(
        self,
        previous: dict,
        current: dict
    ) -> List[DJEvent]:

        """
        Procesa el estado global.

        Continúa en el bloque 2.
        """

        return []

    # =====================================================
    # DECK
    # =====================================================

    def _process_deck(
        self,
        deck: str,
        previous: dict,
        current: dict
    ) -> List[DJEvent]:

        events: List[DJEvent] = []

        # --------------------------------------------
        # PLAY
        # --------------------------------------------

        if previous["playing"] != current["playing"]:

            event_type = (
                EventType.TRACK_STARTED
                if current["playing"]
                else EventType.TRACK_STOPPED
            )

            events.append(
                self._create_event(
                    event_type=event_type,
                    deck=deck,
                    previous=previous["playing"],
                    current=current["playing"]
                )
            )

        # --------------------------------------------
        # PITCH
        # --------------------------------------------

        if previous["pitch"] != current["pitch"]:

            events.append(
                self._create_event(
                    event_type=EventType.PITCH_CHANGED,
                    deck=deck,
                    previous=previous["pitch"],
                    current=current["pitch"]
                )
            )

        return events

    # =====================================================
    # MIX
    # =====================================================

    def _process_mix(
        self,
        previous: dict,
        current: dict
    ) -> List[DJEvent]:

        events: List[DJEvent] = []

        # --------------------------------------------
        # MIX STATE
        # --------------------------------------------

        if previous["mix_state"] != current["mix_state"]:

            events.append(
                self._create_event(
                    event_type=EventType.MIX_STATE_CHANGED,
                    deck=None,
                    previous=previous["mix_state"],
                    current=current["mix_state"]
                )
            )

        # --------------------------------------------
        # TRANSITION
        # --------------------------------------------

        prev_transition = previous["transition_active"]
        cur_transition = current["transition_active"]

        if prev_transition != cur_transition:

            event_type = (
                EventType.TRANSITION_STARTED
                if cur_transition
                else EventType.TRANSITION_FINISHED
            )

            events.append(
                self._create_event(
                    event_type=event_type,
                    deck=None,
                    previous=prev_transition,
                    current=cur_transition
                )
            )

        return events

    # =====================================================
    # EVENT FACTORY
    # =====================================================

    def _create_event(
        self,
        event_type: EventType,
        deck: Optional[str],
        previous,
        current,
        severity: str = "INFO"
    ) -> DJEvent:

        return DJEvent(

            event_id=self._next_event_id(),

            event_type=event_type,

            deck=deck,

            from_state=str(previous),

            to_state=str(current),

            source="EVENT_ENGINE",

            severity=severity,

            data={}
        )