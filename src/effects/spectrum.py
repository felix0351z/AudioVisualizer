import numpy as np

from src.effects.melbank import MelbankEffect
from src.dsp.melbank import Melbank


class SpectrumEffect(MelbankEffect):
    NAME = "Spectrum"
    DESCRIPTION = ""

    MIN_FREQ = 20
    MAX_FREQ = 12000

    def start(self):
        self.melbank = Melbank(
            bins=super().amount_leds()//2,
            sample_rate=super().sample_rate(),
            min_freq=self.MIN_FREQ,
            max_freq=self.MAX_FREQ,
            gain=super().GAIN,
            smoothing=super().SMOOTHING,
        )

    def update(self):
        pass

    def visualize(self) -> np.ndarray:
        spectrum = super().power_spectrum()
        melbank = self.melbank.get_melbank_from_signal(spectrum)

        # Reflect the frequency
        animation = np.append(np.flip(melbank), melbank)
        return animation
