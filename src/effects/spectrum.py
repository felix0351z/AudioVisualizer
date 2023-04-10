import numpy as np

from melbank import MelbankEffect


class SpectrumEffect(MelbankEffect):
    NAME = "Spectrum"
    DESCRIPTION = ""

    def start(self, n_led: int):
        pass

    def visualize(self, raw: np.ndarray):
        pass
