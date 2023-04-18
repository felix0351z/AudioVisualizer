import abc
import numpy as np


def pack_signal(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> np.ndarray:
    signal = np.array([r, g, b])
    return np.transpose(signal).flatten()


class ColorEffect:
    NAME = ""
    DESCRIPTION = ""

    def __init__(self):
        self.__n_led = None
    
    def start(self, n_led: int):
        self.__n_led = n_led
        pass

    def update(self, config):
        pass

    @abc.abstractmethod
    def visualize(self, signal: np.ndarray) -> np.ndarray:
        pass

    def amount_leds(self) -> int:
        return self.__n_led
