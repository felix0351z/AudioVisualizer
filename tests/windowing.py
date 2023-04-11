import numpy as np

from src.utils import view
from src.dsp import filter

# This test will analyse the influence and the importance
# of a window over the signal.
# One Graph will show the fourier transform without a window,
# and the second screen wil show a signal with a window placed on the original signal

class WindowTest:

    def __init__(self):

        window = view.Window("Windowing Test")
        x_range = (1, 10 ** 5)
        y_range = (0, 1)
        self.plot_none = window.create_plot_item("No Window", x_range, y_range, log=True)
        self.plot_hamming = window.create_plot_item("Hanning Window", x_range, y_range, log=True)

        window.start(self.test)

    def test(self, raw: np.ndarray):
        signal = filter.pre_emphasis(raw)  # Take the emphasized input signal

        if self.last_frame is None:
            self.last_frame = np.tile(0.0, len(raw))  # Fill the nullable last frame with empty zeros

        moving_signal = np.append(self.last_frame,
                                  signal)  # Create a moving signal, because of the data leakage with the window
        windowed = moving_signal * np.hanning(len(moving_signal))

        none_fft = np.abs(np.fft.rfft(signal)) ** 2  # Apply the fourier transform without a window
        hanning_fft = np.abs(np.fft.rfft(windowed)) ** 2  # Apply a fourier transform with a window on the moving signal

        def x_axis(n): np.linspace(0, 20000, len(n))  # Create the x-axis for visualization

        self.plot_none.setData(x=x_axis(none_fft), y=none_fft)
        self.plot_hamming.setData(x=x_axis(hanning_fft), y=hanning_fft)
        self.last_frame = signal  # Set the current frame as last frame for the next iteration


WindowTest()
