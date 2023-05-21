import numpy as np

from src.core.input import InputStreamThread
from src.utils import view
from src.dsp import filter
from src.dsp.melbank import Melbank

# This test shows the usage of a mel filterbank and the difference between
# the fourier transform representation (here the power spectrum)

mel_bins = 60  # Number of mel bins
minimum_frequency = 20  # Minimum frequency, which will be measured by the filterbank
maximum_frequency = 12000  # Maximum frequency, which will be measured by the filterbank


class MelbankTest:

    def __init__(self):
        window = view.Window("Melbank Test")

        x_range_power = (1, 10 ** 5)
        x_range_mel = (1, 60)
        y_range = (0, 1)

        self.power_plot = window.create_plot_item("Power Spectrum", x_range_power, y_range, log=True)
        self.mel_plot = window.create_plot_item("Melbank", x_range_mel, y_range, log=False)

        self.melbank = Melbank(
            bins=mel_bins,
            sample_rate=InputStreamThread.SAMPLE_RATE,
            min_freq=minimum_frequency,
            max_freq=maximum_frequency,
        )

        window.start(self.run)

    def run(self, raw: np.ndarray):
        filtered = filter.pre_emphasis(raw)  # Take the emphasized input signal

        fft_frame = np.abs(np.fft.rfft(filtered))
        power_frames = (fft_frame ** 2)

        mel_spectrum = self.melbank.get_melbank_from_signal(power_frames)

        self.power_plot.setData(
            x=np.linspace(0, 20000, len(power_frames)),
            y=power_frames
        )
        self.mel_plot.setData(
            x=np.linspace(1, 61, 60),
            y=mel_spectrum
        )


MelbankTest()
