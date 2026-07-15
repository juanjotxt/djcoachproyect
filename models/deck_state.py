"""
DJCoach PRO
models/deck_state.py

Modelo de estado de un deck.

Autor: Juanjo + ChatGPT
Versión: 1.1
"""

from dataclasses import dataclass, asdict
from typing import Optional, Any


@dataclass
class DeckState:
    """
    Estado completo de un deck.
    """

    # ----------------------------------
    # Identificación
    # ----------------------------------

    deck: str = ""

    # ----------------------------------
    # Estado de reproducción
    # ----------------------------------

    playing: bool = False
    loaded: bool = False
    track: Optional[str] = None

    # ----------------------------------
    # Parámetros musicales
    # ----------------------------------

    pitch: float = 0.5
    bpm: Optional[float] = None

    sync: bool = False
    cue: bool = False

    # ----------------------------------
    # Mezcla
    # ----------------------------------

    channel_fader: float = 1.0

    # ----------------------------------
    # Monitorización
    # ----------------------------------

    headphones: bool = False

    # ----------------------------------
    # Jog Wheel
    # ----------------------------------

    jog_touch: bool = False

    # ----------------------------------
    # Última actividad
    # ----------------------------------

    last_action: Optional[str] = None
    last_event: Optional[Any] = None

    # ----------------------------------

    def to_dict(self) -> dict:
        """Devuelve el estado como diccionario."""
        return asdict(self)

    # ----------------------------------

    def reset(self):
        """Restaura el estado inicial del deck."""
        deck_id = self.deck
        self.__dict__.update(DeckState(deck=deck_id).__dict__)