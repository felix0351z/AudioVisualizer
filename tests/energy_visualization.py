import numpy as np

from src.utils import view
from src.dsp import exponential_smoothing
import utils

# This is a test to try a direct energy visualization

LED_BINS = 60

gain_normalization_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1,
                                                                          alpha_rise=0.99, alpha_decay=0.001)

time_smooth_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1,
                                                                   alpha_rise=0.8, alpha_decay=0.3)
x_axis = np.linspace(1, LED_BINS + 1, LED_BINS)


class EnergyTest:

    def __init__(self):
        window = view.Window("Energy visualization")

        x_range = (1, LED_BINS)
        y_range = (0, 1)

        self.plot = window.create_plot_item("Energy", x_range, y_range)
        self.sender = utils.TestSender()

        window.start(self.run)

    def run(self, raw: np.ndarray):
        energy_value = np.sum(raw ** 2)

        gain_normalization_filter.update(energy_value)
        gain_normalized = energy_value / gain_normalization_filter.forcast

        smoothed = time_smooth_filter.update(gain_normalized)

        # effect = scipy.signal.windows.gaussian(LED_BINS, std=10, sym=True)*smoothed
        effect = np.tile(smoothed, LED_BINS)

        self.plot.setData(x=x_axis, y=effect)

        self.sender.send_signal(effect)

        pass


EnergyTest()
