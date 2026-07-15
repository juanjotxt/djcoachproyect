class MidiEventTranslator:

    def __init__(self):

        self.pending = {}

        # NOTE mapping (PLAY / CUE / SYNC)
        self.note_map = {
            (0, 7): ("PLAY", "deck_a"),
            (0, 6): ("CUE", "deck_a"),
            (0, 5): ("SYNC", "deck_a"),

            (1, 7): ("PLAY", "deck_b"),
            (1, 6): ("CUE", "deck_b"),
            (1, 5): ("SYNC", "deck_b"),
        }

        # 14-bit controls
        self.cc_14bit_controls = {0, 8, 16}

    def translate(self, msg):

        if msg.type == "note_on":
            return self._note(msg)

        if msg.type == "control_change":
            return self._cc(msg)

        return None

    # -----------------------
    # NOTES
    # -----------------------
    def _note(self, msg):

        if msg.velocity == 0:
            return None

        key = (msg.channel, msg.note)

        if key not in self.note_map:
            return None

        action, deck = self.note_map[key]

        return {
            "type": action,
            "deck": deck,
            "channel": msg.channel,
            "note": msg.note,
            "velocity": msg.velocity
        }

    # -----------------------
    # CC HANDLER
    # -----------------------
    def _cc(self, msg):

        # 14-bit controls
        if msg.control in self.cc_14bit_controls:

            key = (msg.channel, msg.control)

            self.pending[key] = msg.value

            msb = self.pending.get(key, 0)
            lsb = self.pending.get((msg.channel, msg.control + 32), 0)

            value = (msb << 7) + lsb

            return {
                "type": self._map_14bit(msg.control),
                "channel": msg.channel,
                "value": value,
                "normalized": value / 16383
            }

        # normal CC
        return {
            "type": "CC",
            "channel": msg.channel,
            "control": msg.control,
            "value": msg.value
        }

    # -----------------------
    # MAPPING LOGIC
    # -----------------------
    def _map_14bit(self, control):

        if control == 0:
            return "CROSSFADER"

        if control == 8:
            return "PITCH_A"

        if control == 16:
            return "PITCH_B"

        return "CC_14BIT"