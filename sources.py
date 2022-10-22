import time
import numpy as np
import pyaudio
import scipy.io.wavfile as wav

import consts
import processing


def microphone(callback):
    p = pyaudio.PyAudio()
    frames_per_buffer = consts.SAMPLE_RATE / consts.FPS
    overflows = 0

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=consts.SAMPLE_RATE,
        input=True,
        frames_per_buffer=frames_per_buffer
    )

    # Stream laufen lassen und
    while True:
        try:
            frame = np.frombuffer(stream, dtype=np.float32)
            callback(frame)
            time.sleep(1000 / consts.FPS)

        except IOError:
            overflows += 1
            print(f"Audiobuffer overflowed {overflows} times")


def wav_file(filename, callback, withWavSignal=False):
    sample_rate, samples = wav.read(filename)
    consts.SAMPLE_RATE = sample_rate
    mono = processing.stereo_to_mono(samples)

    # Die Anzahl der Diraktstöße muss auf die Anzahl der FPS aufgeteilt werden
    frame_step = int(sample_rate / consts.FPS)
    # Die Länge des Frames ist um B größer als der Abstand untereinander
    frame_length = int(frame_step * consts.B)

    frames = processing.samples_to_frames(
        data=samples,
        frame_length=frame_length,
        frane_step=frame_step
    )

    # Anzahl der benötigten Frames | Letzter Frame wird abgezogen
    amount_frames = int(np.ceil((len(samples) - frame_length) / frame_step))

    for i in range(1, amount_frames):
        callback(frames[i])
        time.sleep(1000 / consts.FPS)
