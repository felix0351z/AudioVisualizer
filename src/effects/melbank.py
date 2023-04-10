import numpy as np

from effect import AudioEffect


class MelbankEffect(AudioEffect):
    NAME = "Blabla"
    DESCRIPTION = "Hehe"
    MEL_BINS = 30

    def start(self, n_led: int):
        pass

    def calc_melbank_frame(self):
        pass

    def visualize(self, raw: np.ndarray):
        pass
