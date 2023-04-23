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


