import numpy as np

from src.core.input import BufferThread
from src.dsp import melbank, filter, exponential_smoothing as exp
from src.effects.effect import AudioEffect


class MelbankEffect(AudioEffect):
    NAME = "Melbank"
    DESCRIPTION = "Visualizes the melbank output"

    GAIN_ALPHA_RISE = 0.99
    GAIN_ALPHA_DECAY = 0.1
    SMOOTHING_ALPHA_RISE = 0.99
    SMOOTHING_ALPHA_DECAY = 0.2

    # config

    def melbank_frame(self, bins: int = 60, min_frequency: int = 20,
                      max_frequency: int = 18000, threshold_filter: bool = True, pre_normalization: bool = True):
        """
        Creates a filtered melbank for the actual signal
        :param bins: The amount of bins on the melbank
        :param min_frequency: The minimum frequency of the melbank
        :param max_frequency: The maximum frequency of the melbank
        :param threshold_filter: If true, a threshold filter is used to decrease white noise
        :param pre_normalization: If true, a pre-configured gain and smoothing filter will be applied
        :return: A filtered melbank of the actual signal
        """
        power_spectrum = super().power_spectrum(threshold_filter=False)

        # Generate and apply the melbank
        matrix = melbank.compute_melmatrix(
            num_mel_bands=bins,
            freq_min=min_frequency,
            freq_max=max_frequency,
            num_fft_bands=len(power_spectrum),
            sample_rate=BufferThread.SAMPLE_RATE
        )

        # Multiplication of the mel matrix with power frame to a new matrix, which contains multiple band passed versions of the original power frame
        mel_frames = np.atleast_2d(power_spectrum * matrix)

        # Sum the different band passed versions up to create a one dimensional frame
        mel_frame = np.sum(mel_frames, axis=1)

        if threshold_filter:
            self.mel_frame = filter.auditory_threshold_filter(mel_frame)

        if pre_normalization:
            self._normalize_gain()
            self._smooth_signal(bins)

        return self.mel_frame

    def __init__(self):
        super().__init__()
        self.mel_frame = None
        self.gain_filter = None
        self.smoothing_filter = None

    def _normalize_gain(self):
        if self.gain_filter is None:
            self.gain_filter = exp.SingleExponentialFilter(
                start_value=0.1,
                alpha_rise=self.GAIN_ALPHA_RISE,
                alpha_decay=self.GAIN_ALPHA_DECAY
            )

        self.gain_filter.update(np.max(self.mel_frame))
        self.mel_frame /= self.gain_filter.forcast

    def _smooth_signal(self, bins: int):
        if self.smoothing_filter is None:
            self.smoothing_filter = exp.DimensionalExponentialFilter(
                start_value=np.tile(0.1, bins),
                alpha_rise=self.SMOOTHING_ALPHA_RISE,
                alpha_decay=self.SMOOTHING_ALPHA_DECAY
            )

        self.mel_frame = self.smoothing_filter.update(self.mel_frame)

    def visualize(self) -> np.ndarray:
        return self.melbank_frame()

    def start(self):
        pass

    def update(self):
        pass
