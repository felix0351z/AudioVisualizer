import abc
import numpy as np


def pack_color_with_signal(signal: np.ndarray, color: tuple[int, int, int]) -> np.ndarray:
    r = np.round(signal * color[0])
    g = np.round(signal * color[1])
    b = np.round(signal * color[2])
    return pack_signal(r, g, b)


def pack_signal(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Transpose the color arrays to an single array.
    The r, g, b values will be rearranged together for an direct output.

    Form: (r1, g1, b1, r2, g2, b2, r3, g3, b3, ...)

    :param r The red signal color
    :param g The green signal color
    :param b The blue signal color
    :return: The transposed signal
    """

    signal = np.array([r, g, b])
    return np.transpose(signal).flatten()


class ColorEffect:
    """
    This class is the base object for all color effects.
    """

    NAME = "Base color"
    DESCRIPTION = "Abstract base color class"

    @abc.abstractmethod
    def start(self):
        """
        Called when the current effect will be loaded.
        This method should be used to initialize values at the startup
        """
        pass

    @abc.abstractmethod
    def update(self, config):
        """
        Called when the current config changes
        This method should handle all changes in the config
        """
        pass

    @abc.abstractmethod
    def visualize(self, signal: np.ndarray) -> np.ndarray:
        """
        Process the input signal to an colored signal.
        Will be called every intervall (see fps)

        Every signal value must be provided as 3 color value (R, G, B)
        If the input signal has a length of 60, 180 values must be submitted to the output.

        Also see  :class:`pack_signal()`
        """
        pass
