import numpy as np
import scipy.signal
import soundfile

import dsp.processing as ps

# Beispiel für die Faltung welches ein Audiosignal mit einem Impuls kombiniert.

data, sample_rate = soundfile.read("/home/felix/Musik/3.wav")
impulse_data, impulse_sample_rate = soundfile.read("/home/felix/Musik/impulse.wav")

x = ps.stereo_to_mono(data)
h = ps.stereo_to_mono(impulse_data)

assert sample_rate == impulse_sample_rate

y = scipy.signal.fftconvolve(x, h)

# Normalize amplitude
max = np.max(np.abs(y))
scaled = y / max

soundfile.write(
    file="y.wav",
    data=scaled,
    samplerate=sample_rate
)
