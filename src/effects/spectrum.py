import numpy as np

from src.effects.melbank import MelbankEffect


class SpectrumEffect(MelbankEffect):
    NAME = "Spectrum"
    DESCRIPTION = ""

    MIN_FREQ = 20
    MAX_FREQ = 12000

    def visualize(self) -> np.ndarray:
        bins = super().amount_leds() // 2
        melbank = super().melbank_frame(bins=bins, min_frequency=self.MIN_FREQ, max_frequency=self.MAX_FREQ)

        # Reflect the frequency
        animation = np.append(np.flip(melbank), melbank)
        return animation
