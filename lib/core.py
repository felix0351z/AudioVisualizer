import threading
import scipy.io.wavfile as wav
from PySide2 import QtCore
import simpleaudio as sa


from dsp import processing
from lib import view, consts


class Program:

    def __init__(self, window: view.Window, filename):
        self.filename = filename
        self.app = window

        # Lade wave datei
        sample_rate, samples = wav.read(filename)
        consts.SAMPLE_RATE = sample_rate
        mono = processing.stereo_to_mono(samples)

        # Die Anzahl der Diraktstöße muss auf die Anzahl der FPS aufgeteilt werden
        frame_step = int(sample_rate / consts.FPS)
        # Die Länge des Frames ist um B größer als der Abstand untereinander
        frame_length = int(frame_step * consts.B)
        # Anzahl der benötigten Frames | Letzter Frame wird abgezogen
        # amount_frames = int(np.ceil((len(samples) - frame_length) / frame_step))

        self.frames = processing.samples_to_frames(
            data=mono,
            frame_length=frame_length,
            frane_step=frame_step
        )
        self.i = 0

    def start(self, callback, plot):
        self.callback = callback
        self.plot = plot

        # Musik abspielen
        #self._playback_task(self.filename).start()
        self._playback_task(self.filename).start()

        # Visualisierung starten
        timer = QtCore.QTimer()
        timer.timeout.connect(self._visualize_task)

        timer.start(1000 / consts.FPS)
        self.app.start()

    def _visualize_task(self):
        self.callback(self.plot, self.frames[self.i])
        self.i += 1

    def _playback_task(self, filename):
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        task = threading.Thread(target=play_obj.wait_done)

        return task