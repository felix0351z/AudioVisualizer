import numpy as np


# Methoden für die digitale Audio-Verarbeitung

def stereo_to_mono(data):
    """
    Konvertiert ein Stereo Signal in ein Mono-Signal
    :param data: WavData als 2D List
    :return: Mono WavData als 1D List
    """
    original_len = len(data)
    # Zweite Spur hinter der ersten anordnen, und diese verwerfen
    mono_data = np.reshape(data, -1, order='F')[:original_len]
    return mono_data


def samples_to_frames(data, frame_length: int, frane_step: int):
    """
    Kodiert die einzelnen Dirakstöße zu Frames zusammen

    :param data: Signal in Waveform
    :param frame_length: Länge des Frames in Hz
    :param frane_step: Abstand zum nächsten Frame in Hz
    :return:
    """

    # Anzahl der benötigten Frames | Letzter Frame wird abgezogen
    amount_frames = int(np.ceil((len(data) - frame_length) / frane_step))
    # Neue Länge der späteren Frame-Liste
    new_len = int(round(amount_frames * frane_step + frame_length))
    # Leere Stellen mit 0en füllen
    new_data = np.append(data, np.zeros(new_len - len(data)))

    # Fenster erzeugen
    i = np.tile(np.arange(0, frame_length), (amount_frames, 1)) + \
        np.tile(np.arange(0, amount_frames * frane_step, frane_step), (frame_length, 1)).T
    frames = new_data[i.astype(np.int32, copy=False)]
    return frames


def rfft(frame, n=1024):
    """
    Führt eine Fourier-Transformation über das Frame aus.

    :param n: Anzahl der Punkte entlang der FT in der zu verwendeten Eingabe
    :param frame: 1D Audio Frame
    :return: Fourier Frame
    """
    fft_frame = np.fft.rfft(frame, n)
    # Nur positive Signale
    return np.absolute(fft_frame[:int(n/2)])


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
    pow_frame = ((1.0 / (N/2) * 2 + 1) * (frame ** 2))
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
