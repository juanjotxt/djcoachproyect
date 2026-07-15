"""
DJCoach PRO
models/event_types.py

Define todos los tipos de eventos del sistema.
"""

from enum import Enum


class EventType(str, Enum):
    """Tipos de eventos generados por el Event Engine."""

    TRACK_STARTED = "TRACK_STARTED"
    TRACK_STOPPED = "TRACK_STOPPED"

    TRANSITION_STARTED = "TRANSITION_STARTED"
    TRANSITION_FINISHED = "TRANSITION_FINISHED"

    MIX_STATE_CHANGED = "MIX_STATE_CHANGED"

    SESSION_IDLE = "SESSION_IDLE"

    PLAY_STATE_CHANGED = "PLAY_STATE_CHANGED"

    PITCH_CHANGED = "PITCH_CHANGED"

    CROSSFADER_MOVED = "CROSSFADER_MOVED"