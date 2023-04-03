import numpy as np
from src.utils import view

from src.dsp.filter import SimplePreEmphasis

# This test calculates the fourier transform of the input signal and calculates the power spectrum
# The top graph shows the classic magnitude of the fourier transform while the lower graph
# shows the power spectrum


pre_emphasis_filter = SimplePreEmphasis()  # Reduce the amount low frequencies for a better representation


class FftTest:

    def __init__(self):
        window = view.Window("Leistungsspektrum Test")

        x_range = (1, 10 ** 5)
        y_range = (0, 1)
        self.plot = window.create_plot_item("Amplitudensprektrum", x_range, y_range, log=True)
        self.psd = window.create_plot_item("Leistungsspektrum", x_range, y_range, log=True)

        window.start(self.fft)

    def fft(self, raw: np.ndarray):
        filtered = pre_emphasis_filter.filter(raw)  # Take the emphasized input signal

        fft_frame = np.abs(np.fft.rfft(filtered))
        power_frame = (fft_frame ** 2)

        x_axis = np.linspace(0, 20000, len(fft_frame))  # Create the x-axis for visualization
        self.plot.setData(x=x_axis, y=fft_frame)
        self.psd.setData(x=x_axis, y=power_frame)


FftTest()