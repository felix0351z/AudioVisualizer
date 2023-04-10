import numpy as np

import utils
from src.dsp import exponential_smoothing
from src.utils import view

# This test is based on the gain normalization test and goes a step further and tries to apply a smoothing transition over time

mel_bins = 60  # Number of mel bins
minimum_frequency = 20  # Minimum frequency, which will be measured by the filterbank
maximum_frequency = 1200  # Maximum frequency, which will be measured by the filterbank

x_axis = np.linspace(1, mel_bins + 1, mel_bins)

gain_normalization_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.99,
                                                                          alpha_decay=0.1)
gain_normalization_threshold = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.99,
                                                                             alpha_decay=0.1)

# If the smoothing factor of the decay is lower, the decay will need more time to come back to the bottom.
# The result should be a better transition over time.
mel_smoothing = exponential_smoothing.DimensionalExponentialFilter(start_value=np.tile(0.1, mel_bins), alpha_rise=0.99,
                                                                   alpha_decay=0.2)
mel_smoothing_filtered = exponential_smoothing.DimensionalExponentialFilter(start_value=np.tile(0.1, mel_bins),
                                                                            alpha_rise=0.99,
                                                                            alpha_decay=0.2)


class ThresholdTest:

    def __init__(self):
        window = view.Window("Smoothing Test")

        x_range = (1, 60)
        y_range = (0, 1)

        self.mel_plot = window.create_plot_item("Melbank", x_range, y_range)
        self.melbank = utils.Melbank(mel_bins, minimum_frequency, maximum_frequency)
        self.melbank_threshold = utils.Melbank(mel_bins, minimum_frequency, maximum_frequency)

        self.smoothed1 = window.create_pen(color=(255, 0, 0, 200), width=1.5)
        self.smoothed2 = window.create_pen(color=(0, 255, 0, 200), width=1.5)
        self.s_plots = window.create_plot_curve_item("Smoothed Signal", x_range, y_range,
                                                     pens=[self.smoothed1, self.smoothed2],
                                                     log=False)
        self.sender = utils.TestSender()

        window.start(self.run)

    def run(self, raw: np.ndarray):
        mel_spectrum = self.melbank.raw_to_mel_signal(raw, threshold_filter=False)
        mel_spectrum_filtered = self.melbank_threshold.raw_to_mel_signal(raw, threshold_filter=True)

        max = np.max(mel_spectrum)
        max_filtered = np.max(mel_spectrum_filtered)

        gain_normalization_filter.update(max)
        gain_normalization_threshold.update(max_filtered)

        normalized = mel_spectrum / gain_normalization_filter.forcast  # Normalize gain
        normalized_filtered = mel_spectrum_filtered / gain_normalization_threshold.forcast  # Normalize gain

        smoothed = mel_smoothing.update(normalized)  # Take the forcast of the smoothing filter as actual value
        smoothed_filtered = mel_smoothing_filtered.update(normalized_filtered)

        self.mel_plot.setData(x=x_axis, y=normalized)
        self.s_plots[0].setData(x=x_axis, y=smoothed)
        self.s_plots[1].setData(x=x_axis, y=smoothed_filtered)
        self.sender.send_signal(smoothed, color=(255, 255, 255))


ThresholdTest()
