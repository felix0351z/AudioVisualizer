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
    It provides several methods to access the current audio stream
    """
    NAME = "Basic Effect"
    DESCRIPTION = "Only subclass for other effects"

    def start(self, n_led: int):
        """
        Will be executed if the effect will be selected as current effect.
        :param n_led: The amount of led pixels
        """
        self.__n_led = n_led
        print(f"Effect with the class name {__name__} loaded!")

    @abc.abstractmethod
    def visualize(self) -> np.ndarray:
        """
        Takes the current visualized signal. This function will be executed every intervall.
        For a refresh rate of 60 fps, the function will be executed 60 times in a second.
        This method has to be implemented by every effect
        :return: The visualized signal
        """
        pass

    def __init__(self):
        # Initialize all values
        self.__n_led = 0
        self.__last_frame = None
        self.__moving_signal = None

    def description(self) -> EffectInformation:
        return EffectInformation(
            self.NAME,
            self.DESCRIPTION
        )

    def run(self, raw: np.ndarray) -> np.ndarray:
        """
        Start method of the effect
        :param raw: The audio signal in time domain
        """

        #  Initialize the latest frame with zeros
        if self.__last_frame is None:
            self.__last_frame = np.tile(0, len(raw))

        # Create a moving signal for a window
        self.__moving_signal = np.append(self.__last_frame, raw)
        self.__last_frame = raw
        return self.visualize()

    def power_spectrum(self, threshold_filter: bool = True) -> np.ndarray:
        """
        Gives the current power spectrum of the input signal
        :param threshold_filter: If true, a threshold filter is used to decrease white noise
        :return: The current power spectrum
        """

        # Apply a simple pre-emphasis
        filtered = filter.pre_emphasis(self.__moving_signal)
        # Apply the threshold filter if wished
        if threshold_filter:
            filtered = filter.auditory_threshold_filter(filtered)

        # Apply a window over the complete signal
        windowed = filtered * np.hanning(len(filtered))
        return np.abs(np.fft.rfft(windowed)) ** 2

    def amount_leds(self) -> int:
        """
        Gives the amount of installed leds
        :return: The amount
        """

        return self.__n_led
