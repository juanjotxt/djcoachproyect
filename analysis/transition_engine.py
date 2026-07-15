import time

class TransitionEngine:

    def __init__(self):
        self.in_transition = False
        self.start_time = None
        self.last_mode = "IDLE"
        self.last_direction = None

    def process(self, state):

        mode = state["mode"]
        now = time.time()

        # =========================
        # START TRANSITION
        # =========================
        if self.last_mode != "MIXING" and mode == "MIXING":
            self.in_transition = True
            self.start_time = now
            self.last_direction = self._detect_direction(state)

            return {
                "event": "TRANSITION_START",
                "direction": self.last_direction
            }

        # =========================
        # END TRANSITION
        # =========================
        if self.last_mode == "MIXING" and mode != "MIXING" and self.in_transition:

            duration = now - self.start_time
            self.in_transition = False

            score = self._score_transition(duration)

            return {
                "event": "TRANSITION_END",
                "duration": round(duration, 2),
                "score": score
            }

        self.last_mode = mode
        return None

    # =========================
    # DETECT DIRECTION
    # =========================
    def _detect_direction(self, state):

        if state["A"]["playing"] and not state["B"]["playing"]:
            return "A_ONLY"

        if state["B"]["playing"] and not state["A"]["playing"]:
            return "B_ONLY"

        return "UNKNOWN"

    # =========================
    # SIMPLE SCORING
    # =========================
    def _score_transition(self, duration):

        if duration < 5:
            return "FAST / CLEAN"
        elif duration < 15:
            return "NORMAL"
        else:
            return "LONG / POSSIBLE ISSUE"