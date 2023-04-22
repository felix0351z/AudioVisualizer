import numpy as np
from scipy.signal.windows import gaussian

from src.dsp.exponential_smoothing import SingleExponentialFilter
from src.effects.effect import AudioEffect


class EnergyEffect(AudioEffect):
    NAME = "Energy"
    DESCRIPTION = "Displays the energy of the musical as an gaussian curve"

    GAIN_RISE = 0.9
    GAIN_DECAY = 0.001
    SMOOTHING_RISE = 0.4
    SMOOTHING_DECAY = 0.4

    STANDARD_DEVIATION = 10

    def start(self):
        self.gain_normalize_filter = SingleExponentialFilter(start_value=0.1, alpha_rise=self.GAIN_RISE,
                                                             alpha_decay=self.GAIN_DECAY)
        self.smoothing_filter = SingleExponentialFilter(start_value=0.1, alpha_rise=self.SMOOTHING_RISE,
                                                        alpha_decay=self.SMOOTHING_DECAY)

    def update(self, config):
        pass

    def smoothed_rms(self) -> float:
        rms = super().rms()
        rms /= self.gain_normalize_filter.update(rms)
        return self.smoothing_filter.update(rms)

    def visualize(self) -> np.ndarray:
        gaussian_curve = gaussian(M=super().amount_leds(), std=self.STANDARD_DEVIATION, sym=True)
        return gaussian_curve * self.smoothed_rms()
