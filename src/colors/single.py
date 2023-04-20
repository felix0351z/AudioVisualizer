import numpy as np

from src.colors.effect import ColorEffect, pack_signal
from src.colors.transition import ColorTransition


class SingleColor(ColorEffect):
    NAME = ""
    DESCRIPTION = ""

    COLOR = (255, 255, 255)
    TRANSITION_TIME = 20

    def start(self):
        self.transition = ColorTransition(self.COLOR, self.TRANSITION_TIME)

    def update(self, config):
        pass

    def visualize(self, signal: np.ndarray) -> np.ndarray:
        color = self.transition.update()

        r = np.round(signal * color[0])
        g = np.round(signal * color[1])
        b = np.round(signal * color[2])

        return pack_signal(r, g, b)
