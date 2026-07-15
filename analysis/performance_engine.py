import time

class PerformanceEngine:

    def __init__(self):
        self.transition_start = None
        self.last_mode = None

    def process(self, state, transition_event):

        mode = state["mode"]
        feedback = None

        # =========================
        # START MEASUREMENT
        # =========================
        if transition_event and transition_event.get("event") == "TRANSITION_START":
            self.transition_start = time.time()

        # =========================
        # END MEASUREMENT
        # =========================
        if transition_event and transition_event.get("event") == "TRANSITION_END":

            if self.transition_start is None:
                return None

            duration = time.time() - self.transition_start

            score = self._calculate_score(duration)

            feedback = {
                "event": "PERFORMANCE_SCORE",
                "duration": round(duration, 2),
                "score": score
            }

            self.transition_start = None

        return feedback

    def _calculate_score(self, duration):

        if duration < 5:
            return "EXCELLENT"
        elif duration < 10:
            return "GOOD"
        elif duration < 20:
            return "OK"
        else:
            return "POOR"