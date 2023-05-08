import numpy as np

from src.dsp import exponential_smoothing


class PeakDetector:

    def __init__(self, accuracy: float = 0.1, sensitivity: float = 1.5, gain_decay: float = 0.001, smoothing: tuple[float, float] = None):
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
