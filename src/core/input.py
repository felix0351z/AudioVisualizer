import pyaudio
import numpy as np
from PySide2.QtCore import QThread


class BufferThread(QThread):
    SAMPLE_RATE = 48000
    CHANNELS = 1
    FPS = 50

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.frames_per_buffer = int(self.SAMPLE_RATE/self.FPS)

    def run(self):
        """
        Open an audio stream with Pyaudio and start
        a playback to the callback function
        """

        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=pyaudio.paFloat32,
            rate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            input=True,
            frames_per_buffer=self.frames_per_buffer
        )

        overflows = 0

        while True:
            try:
                # Read the data from the pyaudio stream
                y = np.frombuffer(stream.read(self.frames_per_buffer, exception_on_overflow=False), dtype=np.float32)
                stream.read(stream.get_read_available(), exception_on_overflow=False)
                self.callback(y)

            except IOError:
                overflows += 1
                print("Audio buffer has overflowed {} times".format(overflows))
