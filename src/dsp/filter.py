import numpy as np


class Filter:

    def filter(self, x: np.ndarray) -> np.ndarray:
        pass


class SimplePreEmphasis(Filter):

    def filter(self, x: np.ndarray) -> np.ndarray:
        """
        Legt einen Pre-Emphasis Filter auf das Signal
        y(t) = x(t) - ax(t-1)
        :param x: 2D Audio Signal
        :return: Verarbeitetes 2D Audio Signal
        """

        # Bei einem digitalen Signal sind laute Hoch-Signale oft viel kleiner als laute Tief-Signale
        # daher macht es Sinn, um auch bessere Ergebnisse bei der Fourier Transformation zu erzielen,
        # einen Vor-Filter auf das Signal zu legen, welches die Frequenzen normalisiert.
        a = 0.9
        new_signal = np.append(x[0], x[1:] - a * x[:-1])

        return new_signal


class FilterUtils:
    AUDITORY_THRESHOLD_VALUE = 2e-4

    @staticmethod
    def auditory_threshold_filter(signal: np.ndarray):
        print(f"Value is {np.max(signal)}")
        #return np.where(signal > FilterUtils.AUDITORY_THRESHOLD_VALUE, signal, 0)

        if np.max(signal) <= FilterUtils.AUDITORY_THRESHOLD_VALUE:
            return np.tile(0, len(signal))

        return signal
