import numpy as np

from src.core.input import InputStreamThread
from src.dsp.melbank import Melbank
from src.effects.effect import AudioEffect


class MelbankEffect(AudioEffect):
    NAME = "Melbank"
    DESCRIPTION = "Displays the melbank output"

    GAIN = (0.99, 0.1)
    SMOOTHING = (0.99, 0.2)

    # config

    def start(self):
        self.melbank = Melbank(
            bins=super().amount_leds(),
            sample_rate=super().sample_rate(),
            gain=self.GAIN,
            smoothing=self.SMOOTHING
        )

    def update(self, config):
        pass

    def visualize(self) -> np.ndarray:
        spectrum = super().power_spectrum(threshold_filter=False)
        return self.melbank.get_melbank_from_signal(spectrum)
