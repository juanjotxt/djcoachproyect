"""
DJCoach PRO
Timing Engine v1

Mide la duración de pistas, mezclas y de la sesión.
No toma decisiones; solo calcula tiempos.
"""

from time import time


class DJTimingEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.session_start = time()

        self.track_start = {
            "A": None,
            "B": None
        }

        self.transition_start = None

        self.stats = {
            "tracks_a": 0,
            "tracks_b": 0,
            "time_a": 0.0,
            "time_b": 0.0,
            "transitions": 0,
            "transition_time": 0.0
        }

    def process_event(self, event):

        event_type = event.event_type
        deck = event.deck

        if event_type == "TRACK_STARTED":
            self.track_start[deck] = time()

        elif event_type == "TRACK_STOPPED":
            self._stop_track(deck)

        elif event_type == "TRANSITION_STARTED":
            self.transition_start = time()

        elif event_type == "TRANSITION_ENDED":
            self._stop_transition()

    def _stop_track(self, deck):

        start = self.track_start.get(deck)

        if start is None:
            return

        duration = time() - start

        if deck == "A":
            self.stats["tracks_a"] += 1
            self.stats["time_a"] += duration
        else:
            self.stats["tracks_b"] += 1
            self.stats["time_b"] += duration

        self.track_start[deck] = None

    def _stop_transition(self):

        if self.transition_start is None:
            return

        duration = time() - self.transition_start

        self.stats["transitions"] += 1
        self.stats["transition_time"] += duration

        self.transition_start = None

    def get_statistics(self):

        session_time = time() - self.session_start

        return {
            "session_time": round(session_time, 1),
            "tracks_a": self.stats["tracks_a"],
            "tracks_b": self.stats["tracks_b"],
            "time_a": round(self.stats["time_a"], 1),
            "time_b": round(self.stats["time_b"], 1),
            "transitions": self.stats["transitions"],
            "transition_time": round(self.stats["transition_time"], 1)
        }