from dataclasses import dataclass

import numpy as np


@dataclass()
class AudioInformation:
    raw: np.ndarray
    mel: np.ndarray

    def __init__(self, raw, mel):
        self.raw = raw
        self.mel = mel


class AudioAnalyser():

    def process(self, frame: np.ndarray) -> AudioInformation:
        pass

    def __process_fft(self) -> np.ndarray:
        pass

    def __process_mel(self) -> np.ndarray:
        pass

    # Methoden für die digitale Audio-Verarbeitung


def rfft(frame, n=1024):
    """
    Führt eine Fourier-Transformation über das Frame aus.

    :param n: Anzahl der Punkte entlang der FT in der zu verwendeten Eingabe
    :param frame: 1D Audio Frame
    :return: Fourier Frame
    """
    fft_frame = np.fft.rfft(frame, n)
    # Nur positive Signale
    return np.absolute(fft_frame[:int(n / 2)])


def get_formatted_frames(frame):
    """
    Erstellt aus dem Fourier-Frame besser ein direkt visualisierbaren Frame

    :param frame: 1D Foruier Frame
    :return: Formatted 1D Foruier Frame
    """
    formatted_frame = frame * 2 / (256 * 5512)
    # Amplitude zu dB konvertieren, um einen natürlichen Graphen darzustellen
    return np.log10(formatted_frame + 1)


def get_power_frames(frame, N):
    """
    Erstellt aus dem Fourier-Frame, einen datenreicheren Frame, welcher bei der Weiterverarbeitung
    wie der Mel bank wichtig ist.

    :param frame: 1D Fourier Frame
    :return: 1D Power Frame
    """
    pow_frame = ((1.0 / (N / 2) * 2 + 1) * (frame ** 2))
    return pow_frame


def interpolate(frame, N: int):
    """
    Ändert die Größe des Frames
    :param frame:1D Audio-Frame
    :param N: Neue Länge
    :return: Neu angeordneter Frame
    """
    x = np.linspace(0, 1, N)
    xp = np.linspace(0, 1, len(frame))

    return np.interp(x, xp, frame)
