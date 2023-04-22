import numpy as np

from src.dsp.exponential_smoothing import SingleExponentialFilter, DimensionalExponentialFilter
from src.dsp import filter


class Melbank:
    @staticmethod
    def hertz_to_mel(hertz: float):
        """
        Get the mel frequency from the hertz frequency
        """
        return 2595.0 * np.log10(1 + (hertz / 700.0))

    @staticmethod
    def mel_to_hertz(mel: float):
        """
        Get the hertz frequency from the mel frequency
        """
        return 700.0 * (10 ** (mel / 2595.0) - 1)

    @staticmethod
    def get_mel_frequencies(num_bands, freq_min, freq_max):
        """
        Gibt die mittleren Frequenzen und die Eckbänder für oben und unten zurück

        :param num_bands: Anzahl der Mel-Bänder/Punkten
        :param freq_min: Niedrigste Frequenz fürs erste Band
        :param freq_max: Höchste Frequenz fürs letzte Band
        :return: Center, Lower-Edges und Upper-Edges Frequenz-Array
        """

        # Min und Max in mel
        mel_max = Melbank.hertz_to_mel(freq_max)
        mel_min = Melbank.hertz_to_mel(freq_min)

        # Abstand zwischen den Bändern - muss um 1 addiert werden, da für die Eckenden 2 Werte extra benötigt werden
        delta_mel = abs(mel_max - mel_min) / (num_bands + 1.0)

        # Liste mit den Frequenzen von Min bis Max mit N+2 Einträgen
        band_list = np.arange(0, num_bands + 2)
        frequencies_mel = mel_min + delta_mel * band_list

        # Eckbänder - Fallen jeweils 2 weg
        lower_edges_mel = frequencies_mel[:-2]  # Anfang bis 2 vor Ende
        upper_edges_mel = frequencies_mel[2:]  # 2 bis Ende
        center_frequencies_mel = frequencies_mel[1:-1]  # 1 bis 1 vor Ende

        return center_frequencies_mel, lower_edges_mel, upper_edges_mel

    def _compute_mel_matrix(self, num_fft_bands=512):
        """
        Create a 2d mel matrix

        :param num_fft_bands: Amount of fft bins
        :return: A mel matrix
        """

        center_frequencies_mel, lower_edges_mel, upper_edges_mel = \
            self.get_mel_frequencies(self.bins, self.min_freq, self.max_freq)

        center_frequencies_hz = self.mel_to_hertz(center_frequencies_mel)
        lower_edges_hz = self.mel_to_hertz(lower_edges_mel)
        upper_edges_hz = self.mel_to_hertz(upper_edges_mel)

        # Liste mit allen Frequenzen (bis 20.000Hz) mit N_FFT Einträgen
        freqs = np.linspace(0, self.sample_rate / 2, num_fft_bands)

        # MelMatrix
        melmat = np.zeros((self.bins, num_fft_bands))

        # Alle Mel-Bands durchgehen (imelband)
        # Center, Lower, Upper erhöhen sich bei jedem nächsten Mel-Band
        for imelband, (center, lower, upper) in enumerate(zip(center_frequencies_hz, lower_edges_hz, upper_edges_hz)):
            # Boolean-List, mit Einträgen im unteren Bereich
            left_slope = (freqs >= lower) == (freqs <= center)

            # Hinzufügen der Einträge im unteren Bereich
            melmat[imelband, left_slope] = (
                # Stärkewert
                    (freqs[left_slope] - lower) / (center - lower)
            )

            # Boolean-List, mit Einträgen im oberen Bereich
            right_slope = (freqs >= center) == (freqs <= upper)

            # Hinzufügen der Einträge im oberen Bereich
            melmat[imelband, right_slope] = (
                    (upper - freqs[right_slope]) / (upper - center)
            )

        return melmat

    def __init__(self, bins: int, sample_rate: int, min_freq: int = 20, max_freq: int = 18000,
                 gain: tuple[float, float] = None,
                 smoothing: tuple[float, float] = None,
                 threshold_filter: bool = True
                 ):
        """
        Create a new melbank for an input stream
        :param bins: The amount if bins along the melbank.
        :param sample_rate: The sample rate of the input stream.
        :param min_freq: The minimum frequency which should be captured.
        :param max_freq: The maximum frequency which should be captured.
        :param gain: Gain normalization with a rise factor and and a decay factor. See :class:`SingleExponentialFilter`
        :param smoothing: smoothing over time with a rise factor and a decay factor. See :class:`DimensionalExponentialFilter`
        :param threshold_filter: If a threshold filter should be used to reduce white noise.
        """

        self.bins = bins
        self.sample_rate = sample_rate
        self.min_freq: int = min_freq
        self.max_freq: int = max_freq

        if gain is not None:
            self.gain_filter = SingleExponentialFilter(start_value=0.1, alpha_rise=gain[0], alpha_decay=gain[1])
        else:
            self.gain_filter = None

        if smoothing is not None:
            self.smoothing_filter = DimensionalExponentialFilter(start_value=np.tile(0.1, self.bins),
                                                                 alpha_rise=smoothing[0], alpha_decay=smoothing[1])
        else:
            self.smoothing_filter = None

        self.use_threshold = True if threshold_filter else None

    def get_melbank_from_signal(self, power_spectrum: np.ndarray) -> np.ndarray:
        """
        Get the melbank spectrum from the power spectrum
        """

        # Generate and apply the mel matrix
        matrix = self._compute_mel_matrix(num_fft_bands=len(power_spectrum))

        # Multiplication of the mel matrix with power frame to a new matrix, which contains multiple band passed versions of the original power frame
        mel_frames = np.atleast_2d(power_spectrum * matrix)
        # Sum the different band passed versions up to create a one dimensional frame
        mel_frame = np.sum(mel_frames, axis=1)

        # Apply the threshold filter if it's enabled
        if self.use_threshold:
            mel_frame = filter.auditory_threshold_filter(mel_frame)

        # Apply a gain normalization
        if self.gain_filter is not None:
            self.gain_filter.update(np.max(mel_frames))
            mel_frame /= self.gain_filter.forcast

        # Apply a smoothing filter
        if self.smoothing_filter is not None:
            mel_frame = self.smoothing_filter.update(mel_frame)

        return mel_frame
