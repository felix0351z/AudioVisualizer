import numpy as np

from src.dsp import exponential_smoothing


class PeakDetector:
    """
    Helper class to detect peaks in a spectrum frame
    """

    def __init__(self, accuracy: float = 0.1, sensitivity: float = 1.5, gain_decay: float = 0.001, smoothing: tuple[float, float] = None):
        """
        Creates a new peak detector object
        :param accuracy: Defines the type of peaks to detect. From 0.1 to 0.9
         A higher value means a faster adjustment to the original signal and a better detection for short and high peaks. (Heavily used in Hip-Hop, Pop).
         A lower value means a less adjustment to the original signal and a better detection for long peaks. (Used in Rock or Punk etc.)
        :param sensitivity: Defines how much the current signal should be higher than the average signal to detect a peak.
        Mostly 1.5 times higher or 2 times higher values are used
        :param gain_decay: Defines how fast the detector adjusts himself the output signal to the actual volume of the signal
        :param smoothing: Smoothed output signal if wished. Can be None
        """

        self.accuracy = accuracy
        self.sensitivity = sensitivity

        self.average_filter = exponential_smoothing.SingleExponentialFilter(
            start_value=0.1,
            alpha_rise=0.1,
            alpha_decay=accuracy
        )

        self.gain_filter = exponential_smoothing.SingleExponentialFilter(
            start_value=0.1,
            alpha_rise=0.9,
            alpha_decay=gain_decay
        )

        self.smoothing_filter = None if smoothing is None else exponential_smoothing.SingleExponentialFilter(
            start_value=0.1,
            alpha_rise=smoothing[0],
            alpha_decay=smoothing[1]
        )

    def get_current_value(self, frame: np.ndarray):
        """
        Get the current peak value
        :param frame: The calculated power frame
        """

        # Get the sum of all frequencies together
        sum = float(np.sum(frame))

        average_value = self.average_filter.update(sum)

        # If the current sum is (sensitivity) times bigger than the average curve, a peak will be delivered.
        output_value = sum if sum > average_value*self.sensitivity else 0.0

        # Do a maximum gain update
        self.gain_filter.update(output_value)

        # If the delivered value is two times smaller than the highest sum, the peak is too small and will not be counted
        output_value = 0.0 if output_value < (self.gain_filter.forcast/2) else output_value
        # Gain normalization
        output_value /= self.gain_filter.forcast

        if self.smoothing_filter is not None:
            return self.smoothing_filter.update(output_value)

        return output_value
