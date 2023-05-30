import numpy as np
from src.effects.effect import AudioEffect
from src.dsp.melbank import Melbank
from src.dsp.peak_detection import PeakDetector

from scipy.signal.windows import gaussian


class BassEffect(AudioEffect):
    NAME = "Bass"
    DESCRIPTION = "Only visualize the bass"

    MIN_FREQ = 0
    MAX_FREQ = 200

    ACCURACY = 0.1
    SENSITIVITY = 1.5
    GAIN_DECAY = 0.001
    SMOOTHING = (0.6, 0.1)

    def start(self):
        self.melbank = Melbank(
            bins=super().amount_leds(),
            sample_rate=super().sample_rate(),
            min_freq=self.MIN_FREQ,
            max_freq=self.MAX_FREQ,
        )
        self.detector = PeakDetector(
            accuracy=self.ACCURACY,
            sensitivity=self.SENSITIVITY,
            gain_decay=self.GAIN_DECAY,
            smoothing=self.SMOOTHING
        )

    def update(self, config):
        pass

    def visualize(self) -> np.ndarray:
        frame = self.melbank.get_melbank_from_signal(super().power_spectrum())
        output = self.detector.update(frame)

        output *= gaussian(super().amount_leds(), 10, True)
        return output
