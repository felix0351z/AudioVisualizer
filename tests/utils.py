import sacn
import numpy as np

from src.dsp.filter import SimplePreEmphasis
from src.dsp import melbank
import consts

pre_emphasis_filter = SimplePreEmphasis()


def raw_to_mel_signal(bins: int, raw: np.ndarray, minimum_frequency: int, maximum_frequency: int) -> np.ndarray:
    """
    Takes a raw signal and calculates the complete melbank of it
    :param bins: Amount of bins in the final signal
    :param raw: The raw input signal
    :param minimum_frequency: The minimum frequency of the melbank
    :param maximum_frequency: The maximum frequency of the melbank
    :return: The filtered signal
    """

    filtered = pre_emphasis_filter.filter(raw)  # Take the emphasized input signal

    fft_frame = np.abs(np.fft.rfft(filtered))
    power_frames = (fft_frame ** 2)

    mel_matrix = melbank.compute_melmatrix(  # Create a mel matrix with the given configurations
        num_mel_bands=bins,
        freq_min=minimum_frequency,
        freq_max=maximum_frequency,
        num_fft_bands=int(len(filtered) / 2 + 1),
        sample_rate=consts.SAMPLE_RATE
    )

    # Multiplication of the mel matrix with power frame to a new matrix, which contains multiple band passed versions of the original power frame
    mel_frames = np.atleast_2d(power_frames * mel_matrix)
    # Sum the different band passed versions up to create a one dimensional frame
    mel_spectrum = np.sum(mel_frames, axis=1)
    return mel_spectrum


class TestSender:

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
