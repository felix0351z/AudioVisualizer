import numpy as np

from src.dsp.melbank import Melbank
from src.effects.spectrum import SpectrumEffect
from src.effects.effect import ColorRender
from src.colors.effect import pack_color_with_signal


class ColorSpectrumEffect(SpectrumEffect, ColorRender):
    NAME = "Color Spectrum"
    DESCRIPTION = "Separates the current spectrum in three parts (low, middle and high frequencies) and displays each with a different color"

    COLOR_LOW = (255, 0, 0)
    COLOR_MIDDLE = (0, 255, 0)
    COLOR_HIGH = (0, 0, 255)

    def start(self):
        self.melbank = Melbank(
            bins=super().amount_leds(),
            min_freq=super().MIN_FREQ,
            max_freq=super().MAX_FREQ,
            sample_rate=super().sample_rate(),
            gain=self.GAIN,
            smoothing=self.SMOOTHING
        )

    def update(self, config):
        pass

    def get_color_spectrum(self, melbank):
        low, middle, high = np.split(melbank, 3)

        low = np.concatenate((low, low, low), axis=None)
        middle = np.concatenate((middle, middle, middle), axis=None)
        high = np.concatenate((high, high, high), axis=None)

        low_flipped = pack_color_with_signal(np.append(np.flip(low), low), self.COLOR_LOW)
        middle_flipped = pack_color_with_signal(np.append(np.flip(middle), middle), self.COLOR_MIDDLE)
        high_flipped = pack_color_with_signal(np.append(np.flip(high), high), self.COLOR_HIGH)

        stack = np.stack((low_flipped, middle_flipped))
        output = np.max(stack, axis=0)

        stack = np.stack((output, high_flipped))
        output = np.max(stack, axis=0)

        return output

    def visualize_rgb(self) -> np.ndarray:
        power_frame = super().power_spectrum()
        melbank = self.melbank.get_melbank_from_signal(power_frame)

        effect = self.get_color_spectrum(melbank)
        return effect
