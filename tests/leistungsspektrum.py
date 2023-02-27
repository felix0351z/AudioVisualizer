import numpy as np
from src.core import view

from src.dsp import processing as ps
from src.dsp.filter import SimplePreEmphasis

# Führt die Fourier-Transformation durch und berechnet das Leistungsspektrum

FFT_BANDS = 1024
pre_emphasis_filter = SimplePreEmphasis()

# Liste mit N/2 Einträgen
x = np.linspace(0, 20000, int(FFT_BANDS / 2))


class FFT_Test:

    def __init__(self):
        window = view.Window("Leistungsspektrum Test")

        x_range = (1, 10 ** 5)  # Logarithmisch
        y_range = (0, 1)
        self.plot = window.create_plot_item("Amplitudensprektrum", x_range, y_range, log=True)
        self.psd = window.create_plot_item("Leistungsspektrum", x_range, y_range, log=True)

        window.start(self.fft)

    def fft(self, raw: np.ndarray):
        filtered = pre_emphasis_filter.filter(raw)

        fft_frame = np.abs(np.fft.rfft(filtered))

        power_frames = (fft_frame ** 2)

        b = np.linspace(0, 20000, len(fft_frame))

        self.plot.setData(x=b, y=fft_frame)
        self.psd.setData(x=b, y=power_frames)


FFT_Test()
