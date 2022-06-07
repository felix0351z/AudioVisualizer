import numpy as np


def hertz_to_mel(f):
    """
    Gibt die Mel-Frequenz von der linearen Hertz-Frequenz zurück

    :param f: Frequenzwert oder Array in Hertz
    :return: Mel-Frequenzwert oder Array
    """
    return 2595.0 * np.log10(1 + (f / 700.0))


def mel_to_hertz(m):
    """
    Gibt die Hz-Frequenz von der Mel-Frequenz zurück

    :param m: Mel-Frequenzwert oder Array
    :return: Frequenzwert oder Array in Hertz
    """
    return 700.0 * (10 ** (m / 2595.0) - 1)


def get_melfrequencies(num_bands, freq_min, freq_max):
    """
    Gibt die mittleren Frequenzen und die Eckbänder für oben und unten zurück

    :param num_bands: Anzahl der Mel-Bänder/Punkten
    :param freq_min: Niedrigste Frequenz fürs erste Band
    :param freq_max: Höchste Frequenz fürs letzte Band
    :return: Center, Lower-Edges und Upper-Edges Frequenz-Array
    """

    # Min und Max in mel
    mel_max = hertz_to_mel(freq_max)
    mel_min = hertz_to_mel(freq_min)

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


def compute_melmatrix(num_mel_bands=12, freq_min=64, freq_max=8000, num_fft_bands=512, sample_rate=44100):
    """
    Erstellt eine Matrix für das Mel-Spektrum

    :param num_mel_bands: Anzahl der Mel-Bänder (Def: 12)
    :param freq_min: Niedrigste Frequenz (Def. 64)
    :param freq_max:  Höchste Frequenz (Def. 8000)
    :param num_fft_bands: Anzahl der FFT-Bänder (Def. 512)
    :param sample_rate: Sample-Rate für das zu verwendende Signal
    :return: MelMatrix
    """

    center_frequencies_mel, lower_edges_mel, upper_edges_mel = \
        get_melfrequencies(num_mel_bands, freq_min, freq_max)

    center_frequencies_hz = mel_to_hertz(center_frequencies_mel)
    lower_edges_hz = mel_to_hertz(lower_edges_mel)
    upper_edges_hz = mel_to_hertz(upper_edges_mel)

    # Liste mit allen Frequenzen (bis 20.000Hz) mit N_FFT Einträgen
    freqs = np.linspace(0, sample_rate / 2, num_fft_bands)

    # MelMatrix
    melmat = np.zeros((num_mel_bands, num_fft_bands))

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
