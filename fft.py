import numpy as np

from lib import view
from dsp import filter, processing as ps

# Führt die Fourier-Transformation durch und berechnet die Power-Frames

FFT_BANDS = 1024
pre_emphasis_filter = filter.SimplePreEmphasis()


class FFT:

    def __init__(self):
        window = view.Window("Audio Visualizer")

        x_range = (1, 10 ** 5)  # Logarithmisch
        y_range = (0, 1)
        self.plot = window.create_plot_item("FFT", x_range, y_range, log=True)

        window.start(self.fft)

    def fft(self, raw: np.ndarray):
        x = pre_emphasis_filter.filter(raw)

        fft_frame = ps.rfft(x, n=FFT_BANDS)
        power_frames = (fft_frame ** 2) / (FFT_BANDS / 2)

        # Liste mit N/2 Einträgen. Von 0Hz bis 20.000Hz (Max für Menschen)
        x = np.linspace(0, 20000, int(FFT_BANDS / 2))
        self.plot.setData(x=x, y=power_frames)


FFT()
