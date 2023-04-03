import numpy as np
import src.utils.view as view
from src.dsp import filter
import consts

# This test will analyse the influence and the importance
# of a window over the signal.
# One Graph will show the fourier transform without a window,
# and the second screen wil show a signal with a window placed on the original signal

pre_emphasis = filter.SimplePreEmphasis()  # Reduce the amount low frequencies for a better representation


class WindowTest:

    def __init__(self):
        self.last_frame = np.empty(consts.FRAMES_PER_BUFFER)  # Fill the nullable last frame with empty zeros

        window = view.Window("Windowing Test")
        x_range = (1, 10 ** 5)
        y_range = (0, 1)
        self.plot_none = window.create_plot_item("No Window", x_range, y_range, log=True)
        self.plot_hamming = window.create_plot_item("Hanning Window", x_range, y_range, log=True)

        window.start(self.test)

    def test(self, raw: np.ndarray):
        signal = pre_emphasis.filter(raw)  # Take the emphasized input signal

        moving_signal = np.append(self.last_frame, signal)  # Create a moving signal, because of the data leakage with the window

        none_fft = np.abs(np.fft.rfft(signal)) ** 2  # Apply the fourier transform without a window
        hanning_fft = np.abs(np.fft.rfft(moving_signal)) ** 2  # Apply a fourier transform with a window on the moving signal

        def x_axis(n): np.linspace(0, 20000, len(n))  # Create the x-axis for visualization

        self.plot_none.setData(x=x_axis(none_fft), y=none_fft)
        self.plot_hamming.setData(x=x_axis(hanning_fft), y=hanning_fft)
        self.last_frame = signal  # Set the current frame as last frame for the next iteration


WindowTest()