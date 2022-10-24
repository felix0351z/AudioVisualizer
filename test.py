import numpy as np
from pyqtgraph import PlotItem

from lib import view, core
from dsp import processing as ps

# Führt die Fourier-Transformation durch und berechnet die Power-Frames

INPUT_PAH = "/home/felix/Musik/3.wav"
FFT_BANDS = 1024


def fft(plot: PlotItem, x: np.ndarray):
    fft_frame = ps.rfft(x, n=FFT_BANDS)
    power_frames = (fft_frame ** 2) / (FFT_BANDS / 2)

    # Liste mit N/2 Einträgen. Von 0Hz bis 20.000Hz (Max für Menschen)
    x = np.linspace(0, 20000, int(FFT_BANDS / 2))
    plot.setData(x=x, y=power_frames)


window = view.Window("Audio Visualizer")

x_range = (1, 10 ** 5)  # Logarithmisch
y_range = (0, 1)
plot = window.create_plot_item("FFT", x_range, y_range, log=True)

app = core.Program(window=window, filename=INPUT_PAH)
app.start(fft, plot)
