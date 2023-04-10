import numpy as np
import sacn


class SacnSender:

    def __init__(self, universe: int = 1):
        self.universe = universe
        self.sender = sacn.sACNsender()

        self.sender.start()
        self.sender.activate_output(universe)  # Activate the first universe to send for testing
        self.sender[universe].multicast = True  # Activate multicast

    def send_signal(self, signal: np.ndarray, color: tuple[int, int, int] = (255, 255, 255)):
        r = np.round(signal * color[0])
        g = np.round(signal * color[1])
        b = np.round(signal * color[2])

        normalization_for_led = np.array([r, g, b])  # Apply the colors
        transposed = np.transpose(
            normalization_for_led).flatten()  # In the dmx package the rgb values are directly behind each other, so the signal needs to be transposed

        self._send(transposed)

    def send_color_signal(self, r_signal: np.ndarray, g_signal: np.ndarray, b_signal: np.ndarray):
        transposed = np.transpose(r_signal, g_signal,
                                  b_signal)  # In the dmx package the rgb values are directly behind each other, so the signal needs to be transposed
        self._send(transposed)

    def _send(self, transposed_signal: np.ndarray):
        # Apply nulls at the end of the signal, because every dmx pacakge needs 512 entries
        to_send = np.clip(np.append(transposed_signal, np.zeros(512 - len(transposed_signal))), 0, 255)

        tup = tuple([x.item() for x in np.around(to_send).astype(
            int)])  # Numpy array to tuple, because the sacn library doesn't accept a nparray :(
        self.sender[self.universe].dmx_data = tup  # Give the signal to the sender
