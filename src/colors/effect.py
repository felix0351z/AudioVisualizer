import abc
import numpy as np


def pack_signal(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> np.ndarray:
    signal = np.array([r, g, b])
    return np.transpose(signal).flatten()


class ColorEffect:
    NAME = ""
    DESCRIPTION = ""

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def update(self, config):
        pass

    @abc.abstractmethod
    def visualize(self, signal: np.ndarray) -> np.ndarray:
        pass
