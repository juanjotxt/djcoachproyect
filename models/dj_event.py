"""
DJCoach PRO
models/dj_event.py (v2.1)

Evento base del sistema con trazabilidad avanzada.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
import time

from models.event_types import EventType


@dataclass(slots=True)
class DJEvent:
    """
    Evento estándar del sistema DJCoach PRO.
    """

    # Identificador incremental del evento
    event_id: int

    # Tipo de evento
    event_type: EventType

    # Deck afectado (A/B)
    deck: Optional[str] = None

    # Estado anterior
    from_state: Optional[str] = None

    # Estado nuevo
    to_state: Optional[str] = None

    # Fuente del evento (STATE_ENGINE, etc.)
    source: str = "STATE_ENGINE"

    # Nivel de importancia
    severity: str = "INFO"  # INFO / WARNING / CRITICAL

    # Timestamp
    timestamp: float = field(default_factory=time.time)

    # Datos adicionales
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte a dict serializable."""
        result = asdict(self)
        result["event_type"] = self.event_type.value
        return result

    def __str__(self) -> str:
        return (
            f"[{self.event_id}] "
            f"{self.event_type.value} "
            f"deck={self.deck} "
            f"{self.from_state}->{self.to_state}"
        )