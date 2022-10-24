import numpy as np


class FIRFilter:

    def filter(self, x: np.ndarray) -> np.ndarray:
        pass


class SimplePreEmphasis(FIRFilter):

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
        new_signal = new_signal / 2 ** 15

        return new_signal