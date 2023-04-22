import abc
import numpy as np
from dataclasses import dataclass

from src.dsp import filter


@dataclass
class EffectInformation:
    name: str
    description: str
    # config


class AudioEffect:
    """
    This class is the base object for all other effects. Every effect must extend the class.
    Several methods to access the current audio stream and the features of it will be provided
    """
    NAME = "Basic Effect"
    DESCRIPTION = "Only subclass for other effects"

    @abc.abstractmethod
    def start(self):
        """
        Called when the current effect will be loaded.
        This method should be used to initialize values at the startup
        """
        pass

    @abc.abstractmethod
    def update(self, config):
        """
        Called when the current config changes
        This method should handle all changes in the config
        """
        pass

    @abc.abstractmethod
    def visualize(self) -> np.ndarray:
        """
        This method  processes the visualization and has to be implemented by every effect
        This function will be executed every intervall. (See the frames per second value)

        :return: The visualized signal
        """
        pass

    def activate(self, n_led: int, sample_rate: int):
        """
        Load and initialize all necessary information about the audio stream.
        Must be called before :class:`run()` method.

        :param sample_rate: The current sample rate
        :param n_led: The amount of led pixels
        """
        self._amount_leds = n_led
        self._sample_rate = sample_rate
        self._last_frame = None
        self._moving_signal = None

        self.use_color_render = isinstance(self, ColorRender)
        self.start()

    def description(self) -> EffectInformation:
        """
        Get information's of the effect
        """
        
        return EffectInformation(
            self.NAME,
            self.DESCRIPTION
        )

    def process(self, raw: np.ndarray) -> np.ndarray:
        """
        Processes the visualization from the current input signal
        Must be called every interval.

        :param raw: The audio signal in time domain
        """

        #  Initialize the latest frame with zeros
        if self._last_frame is None:
            self._last_frame = np.tile(0, len(raw))

        # Create a moving signal for a window
        self._moving_signal = np.append(self._last_frame, raw)
        self._last_frame = raw

        if self.use_color_render:
            return self.visualize_rgb()

        return self.visualize()

    def sample_rate(self) -> int:
        """
        Get the current sample rate of the input stream
        """

        return self._sample_rate

    def amount_leds(self) -> int:
        """
        Get the current amount of installed leds
        """

        return self._amount_leds

    def power_spectrum(self, threshold_filter: bool = True) -> np.ndarray:
        """
        Get the current power spectrum of the input signal
        :param threshold_filter: If true, a pre-threshold filter is used to decrease white noise
        """

        # Apply a simple pre-emphasis
        filtered = filter.pre_emphasis(self._moving_signal)
        # Apply the threshold filter if wished
        if threshold_filter:
            filtered = filter.auditory_threshold_filter(filtered)

        # Apply a window over the complete signal
        windowed = filtered * np.hanning(len(filtered))
        return np.abs(np.fft.rfft(windowed)) ** 2

    def rms(self) -> float:
        """
        Get the root mean square of the input signal
        """

        energy = np.sum(self._moving_signal**2)
        return np.sqrt((energy/len(self._moving_signal)))


class ColorRender:
    """
    Utility class for an effect.
    Provides the ability to visualize an own color schema to the current effect instead of pre-defined color effects.
    If this class is implemented the standard :class:`AudioEffect.visualize()` method will be ignored.
    """

    @abc.abstractmethod
    def visualize_rgb(self) -> np.ndarray:
        """
        This method processes the current visualization. Same as :class:`AudioEffect.visualize()`
        But this method requires also the color information to the signal.

        Every signal value must be provided as 3 color value (R, G, B)
        If the current led amount is 60 leds, 180 values must be submitted.

        Also see  :class:`src.colors.effect.pack_signal()`
        :return: The color visualized signal
        """
        pass
