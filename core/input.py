import pyaudio
import numpy as np
from PySide2.QtCore import QThread

import consts


class BufferThread(QThread):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def run(self):
        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=pyaudio.paFloat32,
            rate=consts.SAMPLE_RATE,
            channels=consts.CHANNELS,
            input=True,
            frames_per_buffer=consts.FRAMES_PER_BUFFER
        )

        # Anzahl der Overflows
        overflows = 0

        while True:
            try:
                y = np.frombuffer(stream.read(consts.FRAMES_PER_BUFFER, exception_on_overflow=False), dtype=np.float32)
                stream.read(stream.get_read_available(), exception_on_overflow=False)
                self.callback(y)

            except IOError:
                overflows += 1
                print("Audio buffer has overflowed {} times".format(overflows))
