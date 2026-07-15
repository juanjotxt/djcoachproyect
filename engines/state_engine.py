"""
DJCoach PRO
engines/state_engine.py

DJStateEngine v4.0

Motor central de estado del sistema.

Responsabilidades
-----------------
- Mantener el estado completo de ambos decks.
- Mantener el estado global de la mezcla.
- Actualizar el estado a partir de eventos MIDI normalizados.
- Servir de fuente de información para EventEngine,
  TimingEngine y CoachEngine.

Autor:
Juanjo + ChatGPT
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from models.deck_state import DeckState


class DJStateEngine:
    """
    Motor central de estado.

    No genera eventos.

    Únicamente mantiene el estado operativo del DJ.
    """

    # =====================================================
    # INICIALIZACIÓN
    # =====================================================

    def __init__(self) -> None:

        self.reset()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self) -> None:
        """
        Reinicia completamente el estado.
        """

        self.deck_a = DeckState(deck="A")
        self.deck_b = DeckState(deck="B")

        # ---------------------------------------------
        # Estado global
        # ---------------------------------------------

        self.crossfader: float = 0.50

        self.mix_state: str = "IDLE"

        self.current_activity: Optional[str] = None

        self.last_event: Optional[Dict[str, Any]] = None

    # =====================================================
    # DECKS
    # =====================================================

    def get_deck(self, deck: str) -> DeckState:
        """
        Devuelve el DeckState correspondiente.
        """

        deck = deck.upper()

        if deck == "A":
            return self.deck_a

        if deck == "B":
            return self.deck_b

        raise ValueError(f"Deck desconocido: {deck}")

    # =====================================================
    # API PRINCIPAL
    # =====================================================

    def process(self, event: Dict[str, Any]) -> None:
        """
        Actualiza el estado interno.

        El evento debe tener el formato:

        {
            "type": "...",
            "deck": "A",
            "value": ...
        }
        """

        if not event:
            return

        self.last_event = event

        event_type = event.get("type")

        deck_id = str(event.get("deck", "A")).upper()

        value = event.get("value")

        deck = self.get_deck(deck_id)

        # -------------------------------------------------
        # PLAY
        # -------------------------------------------------

        if event_type == "PLAY":

            deck.playing = bool(value)
            deck.last_action = "PLAY"

            self.current_activity = "PLAYING"

            return

        # -------------------------------------------------
        # CUE
        # -------------------------------------------------

        if event_type == "CUE":

            deck.cue = bool(value)
            deck.last_action = "CUE"

            self.current_activity = "CUEING"

            return

        # -------------------------------------------------
        # SYNC
        # -------------------------------------------------

        if event_type == "SYNC":

            deck.sync = bool(value)
            deck.last_action = "SYNC"

            self.current_activity = "SYNC"

            return

        # -------------------------------------------------
        # Continúa en el bloque 2...


        # -------------------------------------------------
        # TRACK LOADED
        # -------------------------------------------------

        if event_type == "TRACK_LOADED":

            deck.loaded = bool(value)

            if "track" in event:
                deck.track = event["track"]

            if "bpm" in event:
                deck.bpm = event["bpm"]

            deck.last_action = "TRACK_LOADED"

            self.current_activity = "LOADING_TRACK"

            return

        # -------------------------------------------------
        # BPM
        # -------------------------------------------------

        if event_type == "BPM":

            try:
                deck.bpm = float(value)
            except (TypeError, ValueError):
                pass

            deck.last_action = "BPM_CHANGE"

            return

        # -------------------------------------------------
        # PITCH
        # -------------------------------------------------

        if event_type == "PITCH":

            try:
                deck.pitch = float(value)
            except (TypeError, ValueError):
                pass

            deck.last_action = "PITCH_CHANGE"

            self.current_activity = "ADJUSTING_TEMPO"

            return

        # -------------------------------------------------
        # CHANNEL FADER
        # -------------------------------------------------

        if event_type == "CHANNEL_FADER":

            try:
                deck.channel_fader = float(value)
            except (TypeError, ValueError):
                pass

            deck.last_action = "CHANNEL_FADER"

            return

        # -------------------------------------------------
        # CROSSFADER
        # -------------------------------------------------

        if event_type == "CROSSFADER":

            try:
                self.crossfader = max(0.0, min(1.0, float(value)))
            except (TypeError, ValueError):
                return

            self._update_mix_state()

            self.current_activity = "MIXING"

            return

        # -------------------------------------------------
        # HEADPHONES
        # -------------------------------------------------

        if event_type == "HEADPHONES":

            deck.headphones = bool(value)

            deck.last_action = "HEADPHONES"

            return

        # -------------------------------------------------
        # JOG TOUCH
        # -------------------------------------------------

        if event_type == "JOG_TOUCH":

            deck.jog_touch = bool(value)

            deck.last_action = "JOG_TOUCH"

            self.current_activity = "SCRATCH_READY"

            return

        # -------------------------------------------------
        # JOG SCRATCH
        # -------------------------------------------------

        if event_type == "JOG_SCRATCH":

            deck.last_action = "SCRATCH"

            self.current_activity = "SCRATCHING"

            return

        # -------------------------------------------------
        # JOG BEND
        # -------------------------------------------------

        if event_type == "JOG_BEND":

            deck.last_action = "JOG_BEND"

            self.current_activity = "BENDING"

            return

    # =====================================================
    # ESTADO DE MEZCLA
    # =====================================================

    def _update_mix_state(self) -> None:
        """
        Calcula automáticamente el estado de la mezcla.
        """

        if self.crossfader <= 0.05:
            self.mix_state = "A_ONLY"

        elif self.crossfader >= 0.95:
            self.mix_state = "B_ONLY"

        else:
            self.mix_state = "TRANSITION"

    # =====================================================
    # CONSULTAS
    # =====================================================

    def is_playing(self, deck: str) -> bool:
        """
        Indica si un deck está reproduciendo.
        """

        return self.get_deck(deck).playing

    # -----------------------------------------------------

    def is_loaded(self, deck: str) -> bool:
        """
        Indica si hay un tema cargado.
        """

        return self.get_deck(deck).loaded

    # -----------------------------------------------------

    def get_crossfader(self) -> float:
        """
        Devuelve la posición del crossfader.
        """

        return self.crossfader

    # -----------------------------------------------------

    def get_mix_state(self) -> str:
        """
        Devuelve el estado actual de la mezcla.
        """

        return self.mix_state

    # -----------------------------------------------------

    def active_decks(self) -> list[str]:
        """
        Devuelve una lista con los decks reproduciendo.
        """

        active = []

        if self.deck_a.playing:
            active.append("A")

        if self.deck_b.playing:
            active.append("B")

        return active

    # -----------------------------------------------------

    def is_transition_active(self) -> bool:
        """
        Hay transición cuando ambos decks están sonando
        y el crossfader está entre los extremos.
        """

        return (
            self.deck_a.playing
            and self.deck_b.playing
            and 0.05 < self.crossfader < 0.95
        )

    # -----------------------------------------------------

    def get_state(self) -> Dict[str, Any]:
        """
        Devuelve todo el estado del sistema.
        """

        return {
            "deck_a": self.deck_a.to_dict(),
            "deck_b": self.deck_b.to_dict(),
            "crossfader": self.crossfader,
            "mix_state": self.mix_state,
            "current_activity": self.current_activity,
            "transition_active": self.is_transition_active(),
        }

    # -----------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Alias de get_state().
        """

        return self.get_state()

    # -----------------------------------------------------

    def __repr__(self) -> str:

        return (
            "DJStateEngine("
            f"mix_state={self.mix_state}, "
            f"crossfader={self.crossfader:.2f}, "
            f"activity={self.current_activity})"
        )