"""
DJCoach PRO
core/djcoach_agent.py

DJCoach Agent v3.0
Parte 1/3

Núcleo principal del sistema.
"""

from __future__ import annotations

import threading
import time
from typing import Callable

from core.logger import Logger

from engines.state_engine import DJStateEngine
from engines.event_engine import DJEventEngine
from engines.timing_engine import TimingEngine
from coach.coach_engine import CoachEngine


class DJCoachAgent:
    """
    Núcleo principal de DJCoach PRO.

    Pipeline:

        Raw MIDI
            │
            ▼
        State Engine
            │
            ▼
        Event Engine
            │
            ▼
        Timing Engine
            │
            ▼
        Coach Engine
            │
            ▼
        Salida
    """

    VERSION = "3.0"

    # ---------------------------------------------------------

    def __init__(
        self,
        logger: Logger | None = None,
        callback: Callable[[str], None] | None = None,
    ):

        self.logger = logger or Logger()

        self.callback = callback

        self.running = False


        self.lock = threading.RLock()

        # -------------------------------------------------
        # Motores
        # -------------------------------------------------

        self.state_engine = DJStateEngine()

        self.event_engine = DJEventEngine()

        self.timing_engine = TimingEngine()

        self.coach_engine = CoachEngine()

        # -------------------------------------------------
        # Estadísticas
        # -------------------------------------------------

        self.start_time = None

        self.raw_events = 0

        self.generated_events = 0

        self.generated_messages = 0

        # -------------------------------------------------
        # Buffers
        # -------------------------------------------------

        self.event_history = []

        self.message_history = []

        self.max_history = 500

        self.logger.info(
            "DJCoachAgent inicializado correctamente."
        )

    # ---------------------------------------------------------

    @property
    def uptime(self):

        if self.start_time is None:
            return 0.0

        return time.time() - self.start_time

    # ---------------------------------------------------------

    def start(self):

        with self.lock:

            if self.running:
                return

            self.running = True

            self.start_time = time.time()

            self.logger.info("DJCoach iniciado.")

    # ---------------------------------------------------------

    def stop(self):

        with self.lock:

            if not self.running:
                return

            self.running = False

            self.logger.info("DJCoach detenido.")

    # ---------------------------------------------------------

    def reset(self):

        with self.lock:

            self.state_engine = DJStateEngine()

            self.event_engine.reset()

            self.timing_engine = TimingEngine()

            self.coach_engine = CoachEngine()

            self.raw_events = 0

            self.generated_events = 0

            self.generated_messages = 0

            self.event_history.clear()

            self.message_history.clear()

            self.start_time = time.time()

            self.logger.info("Sistema reiniciado.")

    # ---------------------------------------------------------

    def process_raw_event(self, raw_event: dict):

        """
        Punto único de entrada del sistema.

        raw_event:
        {
            "type": "...",
            "deck": "...",
            "value": ...
        }
        """

        if not self.running:
            return []

        with self.lock:

            self.raw_events += 1

            self.state_engine.process(raw_event)

            state = self.state_engine.to_dict()

            events = self.event_engine.process(state)

            return self._process_events(events)

          # ---------------------------------------------------------

    def _process_events(self, events):

        """
        Procesa los eventos generados por el Event Engine.
        """

        if not events:
            return []

        output_messages = []

        for event in events:

            self.generated_events += 1

            self._append_event(event)

            # ---------------------------------------------
            # Timing Engine
            # ---------------------------------------------

            try:

                timing_messages = self.timing_engine.process(event)

                if timing_messages:

                    for msg in timing_messages:

                        output_messages.append(msg)

            except Exception as exc:

                self.logger.error(
                    f"TimingEngine: {exc}"
                )

            # ---------------------------------------------
            # Coach Engine
            # ---------------------------------------------

            try:

                coach_messages = self.coach_engine.process(event)

                if coach_messages:

                    for msg in coach_messages:

                        output_messages.append(msg)

            except Exception as exc:

                self.logger.error(
                    f"CoachEngine: {exc}"
                )

        # ---------------------------------------------
        # Guardar mensajes
        # ---------------------------------------------

        for message in output_messages:

            self.generated_messages += 1

            self._append_message(message)

            if self.callback is not None:

                try:

                    self.callback(message)

                except Exception as exc:

                    self.logger.error(
                        f"Callback: {exc}"
                    )

        return output_messages

    # ---------------------------------------------------------

    def _append_event(self, event):

        self.event_history.append(event)

        if len(self.event_history) > self.max_history:

            self.event_history.pop(0)

    # ---------------------------------------------------------

    def _append_message(self, message):

        self.message_history.append(message)

        if len(self.message_history) > self.max_history:

            self.message_history.pop(0)

    # ---------------------------------------------------------

    def get_last_events(
        self,
        limit: int = 20
    ):

        return self.event_history[-limit:]

    # ---------------------------------------------------------

    def get_last_messages(
        self,
        limit: int = 20
    ):

        return self.message_history[-limit:]

    # ---------------------------------------------------------

    def clear_history(self):

        self.event_history.clear()

        self.message_history.clear()

    # ---------------------------------------------------------

    def statistics(self):

        return {

            "version": self.VERSION,

            "running": self.running,

            "uptime": round(self.uptime, 2),

            "raw_events": self.raw_events,

            "generated_events": self.generated_events,

            "generated_messages": self.generated_messages,

            "events_buffer": len(self.event_history),

            "messages_buffer": len(self.message_history)

        }

    # ---------------------------------------------------------

    def state(self):

        """
        Devuelve el estado completo del sistema.
        """

        try:

            return self.state_engine.to_dict()

        except Exception:

            return {}

    # ---------------------------------------------------------

    def health(self):

        """
        Estado general del agente.
        """

        return {

            "agent": "running" if self.running else "stopped",

            "state_engine": self.state_engine is not None,

            "event_engine": self.event_engine is not None,

            "timing_engine": self.timing_engine is not None,

            "coach_engine": self.coach_engine is not None,

            "callback": self.callback is not None

        }

          # ---------------------------------------------------------

    def register_callback(
        self,
        callback: Callable[[str], None]
    ):

        """
        Registra una función para recibir los mensajes
        generados por el Coach.
        """

        self.callback = callback

    # ---------------------------------------------------------

    def unregister_callback(self):

        self.callback = None

    # ---------------------------------------------------------

    def export_session(self):

        """
        Exporta el estado completo del agente.
        """

        return {

            "version": self.VERSION,

            "statistics": self.statistics(),

            "health": self.health(),

            "state": self.state(),

            "events": list(self.event_history),

            "messages": list(self.message_history)

        }

    # ---------------------------------------------------------

    def shutdown(self):

        """
        Apagado seguro del agente.
        """

        if self.running:

            self.stop()

        self.clear_history()

        self.logger.info(
            "DJCoachAgent finalizado correctamente."
        )

    # ---------------------------------------------------------

    def __enter__(self):

        self.start()

        return self

    # ---------------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        self.shutdown()

        return False

    # ---------------------------------------------------------

    def __repr__(self):

        return (
            f"<DJCoachAgent "
            f"version={self.VERSION} "
            f"running={self.running} "
            f"events={self.generated_events} "
            f"messages={self.generated_messages}>"
        )

    # ---------------------------------------------------------

    def __len__(self):

        return self.generated_events

    # ---------------------------------------------------------

    def __bool__(self):

        return self.running

    # ---------------------------------------------------------

    @staticmethod
    def banner():

        return (
            "\n"
            "=============================================\n"
            "           DJCOACH PRO AGENT v3.0\n"
            "=============================================\n"
            " Real-Time Intelligent DJ Coaching Engine\n"
            "=============================================\n"
        )


# =============================================================
# Factory
# =============================================================

def create_agent(
    logger: Logger | None = None,
    callback: Callable[[str], None] | None = None
) -> DJCoachAgent:

    """
    Factory para crear una instancia del agente.
    """

    return DJCoachAgent(
        logger=logger,
        callback=callback
    )


# =============================================================
# Test rápido
# =============================================================

if __name__ == "__main__":

    print(DJCoachAgent.banner())

    agent = DJCoachAgent()

    agent.start()

    print(agent.statistics())

    agent.stop()

    print(agent.health())

    agent.shutdown()