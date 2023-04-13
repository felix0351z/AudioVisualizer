import numpy as np
from scipy.signal.windows import gaussian

from src.utils import view
from src.dsp import exponential_smoothing
import utils

TIME_LENGTH = 400
LED_BINS = 60

gain_normalization = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.9, alpha_decay=0.001)

output_filter = exponential_smoothing.SingleExponentialFilter(start_value=0.1, alpha_rise=0.4,
                                                              alpha_decay=0.1)


class EnergyTest:

    def __init__(self):
        window = view.Window("Energy visualization")

        x_range = (1, 400)
        y_range = (0, 1)

        self.output_plot = window.create_plot_item("Output", (1, LED_BINS), (0, 1))
        pen1 = window.create_pen(color=(0, 255, 0), width=1)
        self.plots = window.create_plot_curve_item("Smoothed RMS", x_range, y_range, [pen1])
        self.sender = utils.TestSender()

        self.mean_graph = np.tile(0, TIME_LENGTH)
        window.start(self.run)

    def run(self, raw: np.ndarray):
        self.mean_graph = np.delete(self.mean_graph, [0])
        # Get the root-mean-square of the frame
        rms = np.sqrt(np.sum(raw ** 2) / len(raw))

        # Normalize and smooth the rms
        rms /= gain_normalization.update(rms)
        smoothed = output_filter.update(rms)

        self.mean_graph = np.append(self.mean_graph, smoothed)

        length = len(self.mean_graph)
        axis = np.linspace(1, length + 1, length)
        self.plots[0].setData(x=axis, y=self.mean_graph)

        # Plot the output
        y = gaussian(LED_BINS, 10, True) * smoothed
        self.output_plot.setData(x=np.linspace(1, 61, 60), y=y)
        self.sender.send_signal(y)


EnergyTest()
