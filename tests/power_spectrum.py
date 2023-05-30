import numpy as np

from src.utils import view
from src.dsp import filter

# This test calculates the fourier transform of the input signal and calculates the power spectrum
# The top graph shows the classic magnitude of the fourier transform while the lower graph
# shows the power spectrum


class FftTest:

    def __init__(self):
        window = view.Window("Leistungsspektrum Test")
        window.qtWindow.setBackground("w")

        x_range = (0, 20000)
        y_range = (0, 1)
        self.plot = window.create_plot_item("Amplitudensprektrum", x_range, y_range, log=True)
        self.psd = window.create_plot_item("Leistungsspektrum", x_range, y_range, log=True)

        black_pen = window.create_pen((0, 0, 0), width=2)
        self.plot.setPen(black_pen)
        self.psd.setPen(black_pen)

        window.start(self.fft)

    def fft(self, raw: np.ndarray):
        filtered = filter.pre_emphasis(raw)  # Take the emphasized input signal

        fft_frame = np.abs(np.fft.rfft(filtered))
        power_frame = (fft_frame ** 2)

        x_axis = np.linspace(0, 20000, len(fft_frame))  # Create the x-axis for visualization
        self.plot.setData(x=x_axis, y=fft_frame)
        self.psd.setData(x=x_axis, y=power_frame)


FftTest()
