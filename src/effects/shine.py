import numpy as np

from src.dsp.melbank import Melbank
from src.dsp.peak_detection import PeakDetector
from src.effects.spectrum import SpectrumEffect
from src.effects.effect import ColorRender

from src.colors.effect import pack_color_with_signal
from src.colors.transition import ColorTransition

from scipy.signal.windows import gaussian


class ShineEffect(SpectrumEffect, ColorRender):
    NAME = ""
    DESCRIPTION = ""

    SHINE_FREQ = (0, 200)
    SHINE_SMOOTHING = (0.8, 0.15)

    MAIN_COLOR = (0, 100, 255)
    SHINE_COLOR = (255, 255, 255)

    def start(self):
        sr = super().sample_rate()

        self.melbank = Melbank(
            bins=super().amount_leds() // 2,
            sample_rate=sr,
            min_freq=super().MIN_FREQ,
            max_freq=super().MAX_FREQ,
            gain=super().GAIN,
            smoothing=super().SMOOTHING,
        )
        self.shine_melbank = Melbank(
            bins=super().amount_leds(),
            sample_rate=sr,
            min_freq=self.SHINE_FREQ[0],
            max_freq=self.SHINE_FREQ[1]
        )

        self.detector = PeakDetector(
            accuracy=0.1,
            sensitivity=1.5,
            gain_decay=0.001,
            smoothing=self.SHINE_SMOOTHING
        )

    def update(self, config):
        pass

    def get_spectrum_animation(self):
        power_frame = super().power_spectrum()
        main_frame = self.melbank.get_melbank_from_signal(power_frame)

        animation = np.append(np.flip(main_frame), main_frame)
        return pack_color_with_signal(animation, self.MAIN_COLOR)

    def get_shine_animation(self):
        power_frame = super().power_spectrum()
        peak_frame = self.shine_melbank.get_melbank_from_signal(power_frame)

        peak_value = self.detector.get_current_value(peak_frame)
        shine_output = peak_value * np.tile(1.0, reps=super().amount_leds())
        return pack_color_with_signal(shine_output, self.SHINE_COLOR)

    def visualize_rgb(self) -> np.ndarray:
        main_animation = self.get_spectrum_animation()
        shine_animation = self.get_shine_animation()

        stack = np.stack((main_animation, shine_animation))
        output = np.max(stack, axis=0)

        return output
