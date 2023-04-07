import numpy as np

import utils
from src.dsp import exponential_smoothing
from src.dsp import filter
from src.utils import view

# This test is a fork of the smoothing test and will show the difference between a normal mel spectrum and a logarithmic mel spectrumm

mel_bins = 60  # Number of mel bins
minimum_frequency = 20  # Minimum frequency, which will be measured by the filterbank
maximum_frequency = 12000  # Maximum frequency, which will be measured by the filterbank

pre_emphasis_filter = filter.SimplePreEmphasis()  # Reduce the amount low frequencies for a better representation
x_axis = np.linspace(1, mel_bins + 1, mel_bins)

gain_normalization_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.99,
                                                                          alpha_decay=0.3)

gain_normalization_filter_log = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.99,
                                                                              alpha_decay=0.3)

# If the smoothing factor of the decay is lower, the decay will need more time to come back to the bottom.
# The result should be a better transition over time.
mel_smoothing = exponential_smoothing.DimensionalExponentialFilter(start_value=np.tile(0.1, mel_bins), alpha_rise=0.99,
                                                                   alpha_decay=0.3)
mel_smoothing_log = exponential_smoothing.DimensionalExponentialFilter(start_value=np.tile(0.1, mel_bins),
                                                                       alpha_rise=0.99,
                                                                       alpha_decay=0.3)


class Smoothing:

    def __init__(self):
        window = view.Window("Smoothing Test")

        x_range = (1, 60)
        y_range = (0, 1)

        self.mel_plot = window.create_plot_item("Melbank", x_range, y_range, log=True)
        self.melbank = utils.Melbank(mel_bins, minimum_frequency, maximum_frequency)

        self.smoothed1 = window.create_pen(color=(255, 0, 0, 200), width=1.5)
        self.smoothed2 = window.create_pen(color=(0, 255, 0, 200), width=1.5)
        self.s_plots = window.create_plot_curve_item("Smoothed Signal", x_range, y_range,
                                                     pens=[self.smoothed1, self.smoothed2],
                                                     log=False)

        window.start(self.run)

    def run(self, raw: np.ndarray):
        mel_spectrum = self.melbank.raw_to_mel_signal(raw)

        log_spectrum = 10 * np.log10(mel_spectrum + 1)

        gain_normalization_filter.update(np.max(mel_spectrum))
        gain_normalization_filter_log.update(np.max(log_spectrum))

        normalized = mel_spectrum / gain_normalization_filter.forcast  # Normalize gain
        normalized_log = log_spectrum / gain_normalization_filter_log.forcast

        smoothed = mel_smoothing.update(normalized)  # Take the forcast of the smoothing filter as actual value
        smoothed_log = mel_smoothing_log.update(normalized_log)

        self.mel_plot.setData(x=x_axis, y=normalized)
        self.s_plots[0].setData(x=x_axis, y=smoothed)
        self.s_plots[1].setData(x=x_axis, y=smoothed_log)


Smoothing()
