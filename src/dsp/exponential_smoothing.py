# Custom exponential filter classes
# Idea based on https://github.com/scottlawsonbc/audio-reactive-led-strip/blob/master/python/dsp.py

import numpy as np


class SingleExponentialFilter:
    """
    Custom exponential filter for a single value
    """

    def __init__(self, start_value: float, alpha_rise: float, alpha_decay: float):
        """
        Create a new exponential filter with a start value
        :param start_value: The first value as forcast
        :param alpha_rise: Smooth factor for values which are higher than the current forcast
        :param alpha_decay: Smooth factor for values which are lower than the current forcast
        """

        self.forcast = start_value  # Start value for the exponential filter/ the exponential forcast

        self.alpha_rise = alpha_rise  # Smooth factor for values, higher than the forcast
        self.alpha_decay = alpha_decay  # Smooth factor for values, lower than the  forcast

    def update(self, x: float) -> float:
        """
        Calculate the next forcast for a given value
        :param x: Current value
        :return: The forcast for the input value
        """

        # Adjust the smoothing factor to the given input value x
        alpha = self.alpha_rise if x > self.forcast else self.alpha_decay

        # Calculate the next forcast
        self.forcast = alpha * x + (1.0 - alpha) * self.forcast

        # Return the current calculated forcast
        return self.forcast


class DimensionalExponentialFilter:
    """
    Custom exponential filter for an array of 1 dimensional values
    """

    def __init__(self, start_value: np.ndarray, alpha_rise: float, alpha_decay: float):
        """
        Creates a new 1-dimensional exponential filter with a start array
        :param start_value: The first array as forcast
        :param alpha_rise: Smooth factor for values which are higher than there current forcast
        :param alpha_decay: Smooth factor for values which are lower than the current forcast
        """

        self.forcast = start_value  # Start values for the exponential forcast

        self.alpha_rise = alpha_rise  # Smooth factor for values,higher than there forcast
        self.alpha_decay = alpha_decay  # Smooth factor for values, lower than there forcast

    def update(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate the next forcast for every value in given array
        :param x: Current values
        :return: The forcast for all given input values
        """

        alpha = x - self.forcast

        # Values which are higher, than there current forcast, will have a smoothing scale of alpha_rise
        alpha[alpha > 0.0] = self.alpha_rise
        # Values which are lower, than there current forcast, will have a smoothing scale of alpha_delay
        alpha[alpha < 0.0] = self.alpha_decay

        # Calculate the next forcast for every value in the array
        self.forcast = alpha * x + (1.0 - alpha) * self.forcast
        return self.forcast
