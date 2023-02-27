import numpy as np
import src.core.view as view
from src.dsp import filter
import consts

N_FFT = 1024
pre_emphasis = filter.SimplePreEmphasis()


class Window_Test:

    def __init__(self):
        self.last_frame = np.empty(consts.FRAMES_PER_BUFFER)

        window = view.Window("Fensterung Test")
        x_range = (1, 10 ** 5)  # Logarithmisch
        y_range = (0, 1)
        self.plot_none = window.create_plot_item("Kein Fenster", x_range, y_range, log=True)
        self.plot_hamming = window.create_plot_item("Hanning Fenster", x_range, y_range, log=True)

        window.start(self.test)

    def test(self, raw: np.ndarray):
        signal = pre_emphasis.filter(raw)

        f = np.append(self.last_frame, signal)

        hanning = f * np.hanning(len(f))
        none_fft = np.abs(np.fft.rfft(signal)) ** 2
        hanning_fft = np.abs(np.fft.rfft(hanning)) ** 2

        x = lambda n: np.linspace(0, 20000, len(n))
        self.plot_none.setData(x=x(none_fft), y=none_fft)
        self.plot_hamming.setData(x=x(hanning_fft), y=hanning_fft)

        self.last_frame = signal


Window_Test()
