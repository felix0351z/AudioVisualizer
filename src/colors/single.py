from typing import Optional
import numpy as np

from src.colors.effect import ColorEffect, pack_signal


def transition_step_size(start_color: tuple, end_color: tuple, steps: int) -> tuple[int, int, int]:
    values = np.subtract(end_color, start_color) / steps
    return tuple(values)


class SingleColor(ColorEffect):
    NAME = ""
    DESCRIPTION = ""

    COLOR = (100, 0, 255)
    TRANSITION_STEP = 20

    def __init__(self):
        super().__init__()
        self.transition: Optional[tuple[int, int, int]] = None
        self.transition_steps = 0

    def update(self, config):
        new_color = (255, 255, 255)

        # Create a transition tuple with the values which are needed, to update the color every period
        self.transition = transition_step_size(start_color=self.COLOR, end_color=new_color, steps=self.TRANSITION_STEP)
        self.transition_steps = 0

    def visualize(self, signal: np.ndarray) -> np.ndarray:

        if self.transition_steps < self.TRANSITION_STEP and self.transition is not None:  # Update the color if a transition is going on
            self.COLOR = np.add(
                self.COLOR,
                self.transition
            )
            self.transition_steps += 1
            print(f"Color transition update: {self.COLOR}")

        r = np.round(signal * self.COLOR[0])
        g = np.round(signal * self.COLOR[1])
        b = np.round(signal * self.COLOR[2])

        return pack_signal(r, g, b)
