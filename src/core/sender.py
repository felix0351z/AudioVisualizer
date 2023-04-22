import numpy as np
import sacn


class SacnSender:

    def __init__(self, universe: int = 1):
        """
        Create a new sacn sender
        :param universe: Universe which should be used
        """

        self.universe = universe
        self.sender = sacn.sACNsender()

        self.sender.start()
        self.sender.activate_output(universe)  # Activate the first universe to send for testing
        self.sender[universe].multicast = True  # Activate multicast

    def send(self, transposed_signal: np.ndarray):
        """
        Send the current signal over the sacn multicast protocol
        """

        # Apply nulls at the end of the signal, because every dmx pacakge needs 512 entries
        to_send = np.clip(np.append(transposed_signal, np.zeros(512 - len(transposed_signal))), 0, 255)

        tup = tuple([x.item() for x in np.around(to_send).astype(
            int)])  # Numpy array to tuple, because the sacn library doesn't accept a nparray :(
        self.sender[self.universe].dmx_data = tup  # Give the signal to the sender
