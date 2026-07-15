#!/usr/bin/env python3
# ==========================================================
# DJCoach Agent v1.0
# Núcleo principal del sistema
# Autor: Juanjo + Feder
# ==========================================================

import time
import signal
import sys

# ---------- MIDI ----------
from midi.midi_bridge import MidiBridge
from midi.midi_event_translator import MidiEventTranslator
from midi.event_normalizer import EventNormalizer

# ---------- MIXXX ----------
from mixxx.mixxx_bridge import MixxxBridge

# ---------- CORE ----------
from core.state_engine import DJStateEngine
from core.timing_engine import TimingEngine
from core.event_engine import EventEngine
from core.reasoning_engine import ReasoningEngine
from core.memory_manager import MemoryManager

# ---------- AI ----------
from ai.coach_engine import CoachEngine


class DJCoachAgent:

    def __init__(self):

        print("=" * 60)
        print(" DJCoach Agent v1.0")
        print("=" * 60)

        self.running = True

        # -------------------------
        # Inicializar módulos
        # -------------------------

        print("[INIT] MIDI Bridge...")
        self.midi = MidiBridge()

        print("[INIT] Midi Translator...")
        self.translator = MidiEventTranslator()

        print("[INIT] Event Normalizer...")
        self.normalizer = EventNormalizer()

        print("[INIT] Mixxx Bridge...")
        self.mixxx = MixxxBridge()

        print("[INIT] State Engine...")
        self.state = DJStateEngine()

        print("[INIT] Timing Engine...")
        self.timing = TimingEngine()

        print("[INIT] Event Engine...")
        self.events = EventEngine()

        print("[INIT] Reasoning Engine...")
        self.reasoning = ReasoningEngine()

        print("[INIT] Coach Engine...")
        self.coach = CoachEngine()

        print("[INIT] Memory Manager...")
        self.memory = MemoryManager()

        print()
        print("Sistema listo.")
        print()

    # --------------------------------------------------

    def stop(self):

        self.running = False

    # --------------------------------------------------

    def process_event(self, midi_message):

        # Traducir MIDI
        semantic = self.translator.translate(midi_message)

        if semantic is None:
            return

        # Normalizar
        event = self.normalizer.normalize(semantic)

        # Actualizar estado
        self.state.update(event)

        # Actualizar tiempos
        self.timing.update(event)

        # Generar eventos
        detected_events = self.events.process(event)

        # Razonamiento
        advice = self.reasoning.process(
            detected_events,
            self.state
        )

        # IA
        if advice:

            response = self.coach.generate(
                advice
            )

            print()
            print("[COACH]")
            print(response)
            print()

    # --------------------------------------------------

    def run(self):

        print("DJCoach iniciado.")
        print()

        while self.running:

            midi = self.midi.get_event()

            if midi is not None:
                self.process_event(midi)

            time.sleep(0.001)

        print("DJCoach detenido.")


# ==========================================================

agent = DJCoachAgent()


def signal_handler(sig, frame):

    print("\nCerrando DJCoach...")

    agent.stop()

    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

agent.run()