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


def pre_emphasis(data):
    """
    Legt einen Pre-Emphasis Filter auf das Signal
    y(t) = x(t) - ax(t-1)
    :param data: 2D Audio Signal
    :return: Verarbeitetes 2D Audio Signal
    """

    # Bei einem digitalen Signal sind laute Hoch-Signale oft viel kleiner als laute Tief-Signale
    # daher macht es Sinn, um auch bessere Ergebnisse bei der Fourier Transformation zu erzielen,
    # einen Vor-Filter auf das Signal zu legen, welches die Frequenzen normalisiert.
    a = 0.94
    new_signal = np.append(data[0], data[1:] - a * data[:-1])
    new_signal = new_signal / 2**19

    return new_signal


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
    # Hamming Window über das Signal legen
    frames *= np.hamming(frame_length)
    return frames


def rfft(frame, n=1024):
    """
    Führt eine Fourier-Transformation über das Frame aaus.

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
    #return np.log10(pow_frame + 1)
    return pow_frame
