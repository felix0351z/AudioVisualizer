import numpy as np
from scipy.signal.windows import gaussian

from src.utils import view
from src.dsp import exponential_smoothing
import utils

# This is a test to try a bass peak detection

SENSITIVITY = 1.5  # Value from 1 to 3. Describes how far the original value has to be higher than the mean. A higher value means less sensitivity
ACCURACY = 0.1  # Describes the smoothing of the mean. For a bigger value, the mean will be more on the original graph and so less accuracy
CORRECTION = 0.2

# Signal smoothing constants
BASS_RICE = 0.6  #
BASS_DECAY = 0.1


TIME_LENGTH = 400
LED_BINS = 60

average_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1,
                                                               alpha_rise=0.1, alpha_decay=ACCURACY)
gain_normalization = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.9, alpha_decay=0.001)

output_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=BASS_RICE,
                                                              alpha_decay=BASS_DECAY)


class BassPeakDetection:

    def __init__(self):
        window = view.Window("Energy visualization")

        x_range = (1, 400)
        y_range = (0, 10)

        self.output_plot = window.create_plot_item("Output", (1, 60), (0, 1))
        pen1 = window.create_pen(color=(255, 0, 0), width=1)
        pen2 = window.create_pen(color=(0, 255, 0), width=1)
        pen3 = window.create_pen(color=(255, 255, 0), width=1)
        pen4 = window.create_pen(color=(0, 0, 255), width=1)
        self.plots = window.create_plot_curve_item("Bass frequencies", x_range, y_range, [pen1, pen2, pen3, pen4])
        self.sender = utils.TestSender()
        self.melbank = utils.Melbank(bins=60, minimum_frequency=0, maximum_frequency=200)

        self.original_graph = np.tile(0, TIME_LENGTH)
        self.mean_graph = np.tile(0, TIME_LENGTH)
        self.peak_graph = np.tile(0, TIME_LENGTH)
        self.gain_max_graph = np.tile(0, 400)


        window.start(self.run)

    def run(self, raw: np.ndarray):
        mel = self.melbank.raw_to_mel_signal(raw)
        sum = float(np.sum(mel))

        self.original_graph = np.delete(self.original_graph, [0])  # Delete last value
        self.mean_graph = np.delete(self.mean_graph, [0])
        self.peak_graph = np.delete(self.peak_graph, [0])
        self.gain_max_graph = np.delete(self.gain_max_graph, [0])

        self.original_graph = np.append(self.original_graph, sum)  # Add new element

        average = average_filter.update(sum)  # Generate smoothed graph
        self.mean_graph = np.append(self.mean_graph, average)

        # If the difference between the original  1.5 times bigger than the smoothed, it's a peak
        value = sum if sum > average*SENSITIVITY else 0.0

        gain_normalization.update(value)

        # Check for sound peak
        value = 0.0 if value < (gain_normalization.forcast/2) else value

        # Do a gain normalization
        value /= gain_normalization.forcast

        #value = 0.0 if value < CORRECTION else value

        self.peak_graph = np.append(self.peak_graph, value)
        self.gain_max_graph = np.append(self.gain_max_graph, gain_normalization.forcast)

        length = len(self.original_graph)
        axis = np.linspace(1, length + 1, length)

        self.plots[0].setData(x=axis, y=self.original_graph)
        self.plots[1].setData(x=axis, y=self.mean_graph)
        self.plots[2].setData(x=axis, y=self.peak_graph)
        self.plots[3].setData(x=axis, y=self.gain_max_graph)

        # Apply a gaussian curve
        smoothed = output_filter.update(value)
        y = gaussian(LED_BINS, 10, True) * smoothed
        self.output_plot.setData(x=np.linspace(1, 61, 60), y=y)
        self.sender.send_signal(y)


BassPeakDetection()
