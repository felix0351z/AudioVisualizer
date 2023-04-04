import numpy as np
from scipy.ndimage import gaussian_filter1d

import utils
from src.dsp import exponential_smoothing
from src.dsp import filter
from src.utils import view

# This test is based on the melbank test and shows the usage of exponential filters
# for gain normalization.
# Two exponential filters will be used. For the first filter, the maximum of the melbank frame will be used as input.
# The second filter takes the normal distribution of the melbank frame

mel_bins = 60  # Number of mel bins
minimum_frequency = 200  # Minimum frequency, which will be measured by the filterbank
maximum_frequency = 3000  # Maximum frequency, which will be measured by the filterbank

pre_emphasis_filter = filter.SimplePreEmphasis()  # Reduce the amount low frequencies for a better representation
x_axis = np.linspace(1, mel_bins + 1, mel_bins)

gain_normalization_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.99,
                                                                          alpha_decay=0.1)
gain_normalization_gauss = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.99,
                                                                         alpha_decay=0.1)


class GainNormalization:

    def __init__(self):
        window = view.Window("Gain Normalization Test")

        x_range = (1, 60)
        y_range = (0, 1)

        self.mel_plot = window.create_plot_item("Melbank", x_range, y_range, log=True)

        self.gain1 = window.create_pen(color=(255, 0, 0, 200), width=1.5)
        self.gain2 = window.create_pen(color=(0, 255, 0, 200), width=1.5)
        self.gain_plots = window.create_plot_curve_item("Normalized Gain", x_range, y_range,
                                                        pens=[self.gain1, self.gain2],
                                                        log=False)

        # self.normalized_plot = window.create_plot_item("Gain Normalization", x_range_mel, y_range, log=False)
        window.start(self.run)

    def run(self, raw: np.ndarray):
        mel_spectrum = utils.raw_to_mel_signal(mel_bins, raw, minimum_frequency, maximum_frequency)

        max = np.max(mel_spectrum)
        max_gaus = np.max(gaussian_filter1d(mel_spectrum, sigma=1.0))
        gain_normalization_filter.update(max)
        gain_normalization_gauss.update(max_gaus)

        normalized = mel_spectrum / gain_normalization_filter.forcast
        normalized_gauss = mel_spectrum / gain_normalization_gauss.forcast

        self.mel_plot.setData(x=x_axis, y=mel_spectrum)

        self.gain_plots[0].setData(x=x_axis, y=normalized)
        self.gain_plots[1].setData(x=x_axis, y=normalized_gauss)


GainNormalization()
