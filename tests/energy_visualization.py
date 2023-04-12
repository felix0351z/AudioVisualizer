import numpy as np

from src.utils import view
from src.dsp import exponential_smoothing
import utils

# This is a test to try a direct energy visualization

normalize_gain = True

average_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1,
                                                               alpha_rise=0.1, alpha_decay=0.3)

gain_normalization = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.9, alpha_decay=0.001)


class EnergyTest:

    def __init__(self):
        window = view.Window("Energy visualization")

        x_range = (1, 400)
        y_range = (0, 10)

        pen1 = window.create_pen(color=(255, 0, 0), width=1)
        pen2 = window.create_pen(color=(0, 255, 0), width=1)
        pen3 = window.create_pen(color=(255, 255, 0), width=1)
        self.plots = window.create_plot_curve_item("Bass frequencies", x_range, y_range, [pen1, pen2, pen3])
        self.sender = utils.TestSender()
        self.melbank = utils.Melbank(bins=60, minimum_frequency=0, maximum_frequency=200)

        self.values = np.tile(0, 400)
        self.averages = np.tile(0, 400)
        self.difference = np.tile(0, 400)

        window.start(self.run)

    def run(self, raw: np.ndarray):
        mel = self.melbank.raw_to_mel_signal(raw)
        sum = float(np.max(mel))

        self.values = np.delete(self.values, [0])  # Delete last value
        self.averages = np.delete(self.averages, [0])
        self.difference = np.delete(self.difference, [0])

        self.values = np.append(self.values, sum)  # Add new element
        average = average_filter.update(sum)  # Generate smoothed graph
        self.averages = np.append(self.averages, average)

        # If the difference between the original  1.5 times bigger than the smoothed, it's a peak
        con = 1.5
        value = 0.0
        if sum > average * con:
            value = sum

        if normalize_gain:
            value /= gain_normalization.update(value)

        self.difference = np.append(self.difference, value)


        length = len(self.values)
        axis = np.linspace(1, length + 1, length)
        self.plots[0].setData(x=axis, y=self.values)
        self.plots[1].setData(x=axis, y=self.averages)
        self.plots[2].setData(x=axis, y=self.difference)
        # self.sender.send_signal(mel)


EnergyTest()
