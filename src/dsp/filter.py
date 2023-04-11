import numpy as np

PRE_EMPHASIS_CONST = 0.9
AUDITORY_THRESHOLD_VALUE = 2e-4


def pre_emphasis(x: np.ndarray):
    """
    Applies a pre-emphasis to the given signal
    to normalize the difference between low- and high frequencies
    """

    # y(t) = x(t) - ax(t-1)
    return np.append(x[0], x[1:] - PRE_EMPHASIS_CONST * x[:-1])


def auditory_threshold_filter(signal: np.ndarray):
    """
    If the signal is under the auditory threshold, the signal will be set to 0
    """

    if np.max(signal) <= AUDITORY_THRESHOLD_VALUE:
        return np.tile(0.0, len(signal))

    return signal


def point_wise_auditory_threshold_filter(signal: np.ndarray):
    """
    All values in the signal, which are under the auditory threshold will be set to 0
    """

    return np.where(
        signal > AUDITORY_THRESHOLD_VALUE,
        # Condition, if a value is over the threshold -> then A, else B
        signal,  # A, the value will be passed
        0  # B, the value will be set to zero
    )
