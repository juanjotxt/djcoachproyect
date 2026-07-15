import mido


class DJMidiBridge:

    def __init__(self, port_name=None):

        self.port_name = port_name

    def handle_midi(self, msg):

        print("MIDI:", msg)

    def start(self):

        print("DJCoach MIDI Bridge iniciado...")

        ports = mido.get_input_names()

        print("Puertos MIDI detectados:")
        for p in ports:
            print(" -", p)

        if not ports:
            raise RuntimeError("No hay puertos MIDI disponibles")

        port_name = self.port_name or ports[0]

        print(f"Usando puerto: {port_name}")

        with mido.open_input(port_name) as port:

            print("Escuchando MIDI en tiempo real...")

            for msg in port:
                self.handle_midi(msg)


if __name__ == "__main__":

    bridge = DJMidiBridge()

    bridge.start()