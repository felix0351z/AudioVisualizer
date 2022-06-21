import sys
import threading

import numpy as np
import pyqtgraph as pg
import sacn
from exp_filter import SimpleExpFilter
import scipy.io.wavfile as wav
from scipy.ndimage import gaussian_filter1d
from PySide2 import QtWidgets, QtCore
from pydub import AudioSegment, playback

import melbank as mel
import processing as ps

# Pfad der Audio-Datei
INPUT_PAH = "/home/felix/Musik/10.wav"

FFT_BANDS = 1024
MEL_BANDS = 30
N_PIXELS = 60

FREQ_TIME = 25
WAVE_TIME = 50

MIN_FREQ = 64
MAX_FREQ = 12000

ON_ESP = True
ESP_ADRESS = "192.168.178.160"

# Verhältnis vom Abstand eines Frames zu seiner Länge
B = 2.5

PLOT_OUTPUT = True

# Werte über 0.1 sollen mehr geglättet werden als Werte hierunter
mel_gain = SimpleExpFilter(np.tile(0.01, MEL_BANDS), alpha_decay=0.01, alpha_rise=0.99)
mel_smoothing = SimpleExpFilter(np.tile(0.01, MEL_BANDS), alpha_decay=0.5, alpha_rise=0.99)

r_filt = SimpleExpFilter(np.tile(0.01, N_PIXELS // 2), alpha_decay=0.2, alpha_rise=0.99)
b_filt = SimpleExpFilter(np.tile(0.01, N_PIXELS // 2), alpha_decay=0.1, alpha_rise=0.5)

common_mode = SimpleExpFilter(np.tile(0.01, N_PIXELS // 2), alpha_decay=0.99, alpha_rise=0.01)


class Program:
    """
    Erstellt eine Qt-Gui mit PyQT zur Visualisierung
    der verschiedenen Graphen
    """

    def __init__(self):
        # Erstellen der Haupt-Applikation und dem GraphFenster
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(title="Audio Visualizer", size=(1920, 1080))
        self.win.setAntialiasing(True)

        # Laden der Wav-Audiodatei
        self.sample_rate, data = wav.read(INPUT_PAH)
        # Initialisierung und generation der allgemeinen Frames
        signal, self.frames = self.initialize_audio_signal(data)
        # Für die Visualisierung muss 1 Sekunde addiert werden
        self.data = np.append(np.zeros(self.sample_rate), signal)

        # Variable zum Zählen des momentanen Frames
        self.current_frame = 1
        # Generieren des Wiedergabe-Tasks
        self.playback_task = self.initialize_audio_task()

        self.prev_output = None

        # Wave
        self.wave_plot, self.x_wave = self.plot_waveform()
        # Original-Spectrum
        self.spectrum_plot, self.x_spectrum = self.plot_spectrum()
        # Mel bank Spectrum Plot
        self.mel_plot, self.x_mel = self.plot_mel_spectrum()
        # LED Output
        self.r, self.g, self.b, self.x_led = self.plot_led_output()

        # SACN Sender
        self.sender = sacn.sACNsender()

    def plot_waveform(self):
        """
        Waveform, welche von rechts nach links durchläuft,
        basierend auf der SampleRate. Alle Taktstöße innerhalb einer Sekunde
        :return: WavePlot, xAxis
        """
        wave_Canvas: pg.PlotItem = self.win.addPlot(title="Waveform", row=0, col=0)
        wave_Canvas.setXRange(0, self.sample_rate)  # Immer eine Sekunde
        wave_Canvas.setYRange(-0.5, 0.5)  # Ungefähre Amplituden Höchstwerte

        # Liste von 1 bis SampleRate für WavePlot
        x = np.arange(1, self.sample_rate + 1)

        return wave_Canvas.plot(), x

    def plot_spectrum(self):
        """
        Spektrum, welches durch die Fourier-Transformation-Erzeugt wurde.
        :return: SpectrumPlot. xAxis
        """
        spectrum_Canvas: pg.PlotItem = self.win.addPlot(title="Spectrum", row=1, col=0)
        spectrum_Canvas.setYRange(0, 1)  # Maximale höher der Lautstärke
        spectrum_Canvas.setXRange(1, 10 ** 5)  # Logarithmisch
        spectrum_Canvas.setLogMode(x=True, y=False)  # dB später manuell berechnen

        # Liste mit N/2 Einträgen. Von 0Hz bis 20.000Hz (Max für Menschen)
        x = np.linspace(0, 20000, int(FFT_BANDS / 2))

        return spectrum_Canvas.plot(), x

    def plot_mel_spectrum(self):
        """
        Spektrum, welches durch die Mel-Filterbank ging und bereits auf das menschliche Ohr
        angepasst ist.
        :return: Mel bank-Spectrum Plot, xAxis
        """
        melCanvas: pg.PlotItem = self.win.addPlot(title="Melbars Sectrum", row=0, col=1)
        melCanvas.setYRange(0, 1)
        melCanvas.setXRange(0, mel.hertz_to_mel(20000))  # 40 Peaks werden genutzt

        # Liste mit N_MEL Einträgen. Von 0 Hz bis 20000Hz skaliert in Mel
        x = np.linspace(0, mel.hertz_to_mel(20000), MEL_BANDS)

        return melCanvas.plot(), x

    def plot_led_output(self):
        """
        LED Output, mit rot, grün und blauem Graphen
        :return: LED Plot, xAxis
        """

        ledCanvas: pg.PlotItem = self.win.addPlot(title="LED Output", row=1, col=1, colspan=3)
        ledCanvas.setYRange(0, 1)
        ledCanvas.setXRange(0, N_PIXELS)

        # Unterschiedliche Farben jay
        r_pen = pg.mkPen((255, 30, 30, 200), width=4)
        g_pen = pg.mkPen((30, 255, 30, 200), width=4)
        b_pen = pg.mkPen((30, 30, 255, 200), width=4)
        r_curve = pg.PlotCurveItem(pen=r_pen)
        g_curve = pg.PlotCurveItem(pen=g_pen)
        b_curve = pg.PlotCurveItem(pen=b_pen)
        ledCanvas.addItem(r_curve)
        ledCanvas.addItem(g_curve)
        ledCanvas.addItem(b_curve)

        x = np.arange(1, N_PIXELS + 1)

        return r_curve, g_curve, b_curve, x

    def initialize_audio_task(self):
        """
        Erstellt einen Wiedergabe-Task für die zu spielende Audio-Datei
        :return: Audio Task
        """

        audio = AudioSegment.from_wav(INPUT_PAH)
        task = threading.Thread(target=playback.play, args=(audio,))
        return task

    def initialize_audio_signal(self, data):
        """
        Audio-Signal von der Waveform bis zu den Frames verarbeiten
        :param data: WavData als 2D List
        :return: Converted Wav-Form, Audio-Frames
        """
        MILLIS = FREQ_TIME if PLOT_OUTPUT else WAVE_TIME
        # Die Anzahl der Diraktstöße muss auf die Anzahl der Frames (FPS) aufgeteilt werden
        frame_st = int(self.sample_rate / (1000 / MILLIS))
        # Die Länge des Frames ist um B größer als der Abstand untereinander
        frame_len = int(frame_st * B)

        mono = ps.stereo_to_mono(data)
        emphasized_signal = ps.pre_emphasis(mono)
        # Erstellen der finalen Frames
        frames = ps.samples_to_frames(emphasized_signal, frane_step=frame_st, frame_length=frame_len)
        return emphasized_signal, frames

    def initialize_plot(self):
        """
        Plottet Startsignale
        """
        # Erste Sekunde des Wav-Signals
        y_wave = self.data[:self.sample_rate]
        # Ganzen Bereich (N/2) mit 0en füllen
        y_spectrum = np.zeros(int(FFT_BANDS / 2))
        # Ganzen Bereich (N_MEL) mit 0en füllen
        y_mel = np.zeros(MEL_BANDS)

        y_led = np.zeros(N_PIXELS)

        self.wave_plot.setData(x=self.x_wave, y=y_wave)
        self.spectrum_plot.setData(x=self.x_spectrum, y=y_spectrum)
        self.mel_plot.setData(x=self.x_mel, y=y_mel)

        self.r.setData(x=self.x_led, y=y_led)
        self.g.setData(x=self.x_led, y=y_led)
        self.b.setData(x=self.x_led, y=y_led)

    def update_plot20s(self):
        """
        Updaten der Signale in den Plots.
        Wird vom QTimer FPS_mal in der Sekunde aufgerufen.
        """
        # Sample_Rate / FPS => Dirakstöße in einem Zyklus
        amount_samples = int(self.sample_rate / (1000 / WAVE_TIME))

        # Alle Diraktstöße vom letzten Update entfernen
        self.data = np.delete(self.data, np.arange(0, amount_samples))

        # Falls die Länge für keinen Zyklus mehr reicht, oder
        # kein weiteres Frame mehr existiert
        # muss beendet werden
        if (len(self.data)) <= amount_samples:
            self.app.exit()
            return

        # Updaten des WavePlots
        self.wave_plot.setData(x=self.x_wave, y=self.data[:self.sample_rate])

        if self.current_frame >= len(self.frames):
            self.app.exit()
            return

        # Updaten des SpektrumPlots
        fft_frame = ps.rfft(self.frames[self.current_frame], n=FFT_BANDS)
        spectrum_frame = ps.get_formatted_frames(fft_frame)
        self.spectrum_plot.setData(x=self.x_spectrum, y=spectrum_frame)

    def update_plot60s(self):
        if self.current_frame >= len(self.frames):
            self.app.exit()
            return

        fft_frame = ps.rfft(self.frames[self.current_frame], n=FFT_BANDS)
        # Updaten des Mel Plots
        melmat = mel.compute_melmatrix(
            num_mel_bands=MEL_BANDS,
            freq_min=MIN_FREQ,
            freq_max=MAX_FREQ,
            num_fft_bands=int(FFT_BANDS / 2)
        )

        # Melspektrum mit den FFT Daten verrechnen
        mel_frames = np.atleast_2d(ps.get_power_frames(fft_frame, FFT_BANDS)) * melmat
        mel_spectrum = np.sum(mel_frames, axis=1)

        # Gain Normalization
        max = np.max(gaussian_filter1d(mel_spectrum, sigma=1.0))
        mel_gain.update(max)
        mel_spectrum /= mel_gain.forcast
        # Mel Smoothing
        mel_spectrum = mel_smoothing.update(mel_spectrum)

        # Logarithmische Darstellung
        mellog = np.log(mel_spectrum + 1)
        self.mel_plot.setData(x=self.x_mel, y=mellog)

        # Größe auf die Anzahl der LED ändern
        output = ps.interpolate(mellog, N_PIXELS // 2)
        filtered_output = common_mode.update(output)

        if self.prev_output is None:
            self.prev_output = np.copy(output)

        # Filter auf die jeweiligen Farbsignale legen
        r = r_filt.update(output - filtered_output)
        g = np.abs(output - self.prev_output)
        b = b_filt.update(output)

        out_r = np.append(np.flip(r), r)
        out_g = np.append(np.flip(g), g)
        out_b = np.append(np.flip(b), b)
        self.r.setData(x=self.x_led, y=out_r)
        self.g.setData(x=self.x_led, y=out_g)
        self.b.setData(x=self.x_led, y=out_b)

        # TODO bis 512 auffüllen!
        compressed: np.ndarray = np.array([out_r, out_g, out_b]) * 255
        out = compressed.transpose().flatten()

        # Bei Erweiterungen muss auch geschaut werden, ob mehr als 512 in out sind!!!
        final = np.clip(np.append(out, np.zeros(512 - len(out))), 0, 255)

        tup = tuple([x.item() for x in np.around(final).astype(int)])

        if ON_ESP:
            self.sender[1].dmx_data = tup

        self.prev_output = np.copy(output)
        self.current_frame += 1

    def start(self):
        """
        Initialisieren des Plots, generieren des Timers und starten des Programs
        """
        self.initialize_plot()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update_plot20s)

        freqTimer = QtCore.QTimer()
        freqTimer.timeout.connect(self.update_plot60s)

        if PLOT_OUTPUT:
            freqTimer.start(FREQ_TIME)  # 60 FPS für Output
            if ON_ESP:
                self.sender.start()
                self.sender.activate_output(1)
                self.sender[1].multicast = True
                self.sender[1].destination = ESP_ADRESS
        else:
            timer.start(WAVE_TIME)  # 20 FPS für Waveform + Spectrum

        self.playback_task.start()
        self.run()

    def run(self):
        self.win.show()
        self.app.exec_()


if __name__ == '__main__':
    program = Program()
    program.start()
