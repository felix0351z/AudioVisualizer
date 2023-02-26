import numpy as np
import core.view as view
from dsp import filter, processing
import consts

N_FFT = 1024
pre_emphasis = filter.SimplePreEmphasis()

x = np.linspace(0, 20000, int(N_FFT / 2))


class Window_Test:

    def __init__(self):
        self.last_frame = np.empty(consts.FRAMES_PER_BUFFER)

        window = view.Window("Fensterung Test")
        x_range = (1, 10 ** 5)  # Logarithmisch
        y_range = (0, 1)
        self.plot_none = window.create_plot_item("Kein Fenster", x_range, y_range, log=True)
        self.plot_hamming = window.create_plot_item("Hamming Fenster", x_range, y_range, log=True)

        window.start(self.test)

    def test(self, raw: np.ndarray):
        signal = pre_emphasis.filter(raw)

        f = np.append(self.last_frame, signal)

        hamming = f * np.hanning(len(f))
        none_fft = processing.rfft(signal, n=N_FFT)**2
        hamming_fft = processing.rfft(hamming, n=N_FFT)**2

        self.plot_none.setData(x=x, y=none_fft)
        self.plot_hamming.setData(x=x, y=hamming_fft)

        self.last_frame = signal

Window_Test()
