import numpy as np


def hertz_to_mel(f):
    return 2595.0 * np.log10(1 + (f / 700.0))


def mel_to_hertz(m):
    return 700.0 * (10 ** (m / 2595.0) - 1)
