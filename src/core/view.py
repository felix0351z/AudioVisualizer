from PySide2 import QtWidgets, QtGui
import pyqtgraph as pg

from src.core.input import BufferThread


class Window:
    """
    QtGraph Fenster mit Plotting-Funktionen
    """

    def __init__(self, title: str):
        """
        Erstellt das Hauptfenster
        :param title: Name des Fensters
        """

        # Erstelle Haupt-Fenster
        self.qtApp = QtWidgets.QApplication()
        self.qtWindow = pg.GraphicsLayoutWidget(title=title, size=(1920, 1080))
        self.qtWindow.setAntialiasing(True)

        # Momentane Anzahl an Plots im Fenster
        self.plotRow = 0
        self.plotColumn = 0

    def _increase_window_size(self):
        # Erhöht die momentane Anzahl an Plots.

        if self.plotColumn >= self.plotRow:
            self.plotRow = self.plotRow + 1
            return

        if self.plotColumn < self.plotRow:
            self.plotColumn, self.plotRow = self.plotRow, self.plotColumn

    def create_pen(self, color=(255, 255, 255, 200), width=2) -> QtGui.QPen:
        """
        Erstellt ein QPen
        Alternative: pyqtgraph.mkPen()
        Beispiele::
            mkPen(color)
            mkPen(color, width=2)
            color = (R, G, B, A) //Tuple
        """
        return pg.mkPen(color, width=width)

    def create_plot_item(
            self, title: str,
            x_range: (int, int),
            y_range: (int, int),
            log=False) -> pg.PlotItem:
        """
        Erstellt ein PlotItem-Objekt.
        (plot.setData(x: nparray, y:ndarray))
        :param title: Name des Plots
        :param x_range: Grenzbereiche der X-Achse (x_min - x_max)
        :param y_range: Grenzbereiche der Y-Achse (y_min - y_max)
        :param log: Logarithmische Darstellung der x-Achse
        :return: PlotItem
        """

        canvas: pg.PlotItem = self.qtWindow.addPlot(title=title, row=self.plotRow, col=self.plotColumn)
        self._increase_window_size()

        canvas.setRange(xRange=x_range, yRange=y_range)
        canvas.setLogMode(x=log, y=False)

        return canvas.plot()

    def create_plot_curve_item(
            self,
            title: str,
            x_range: (int, int),
            y_range: (int, int),
            pens: [QtGui.QPen],
            log=False) -> list[pg.PlotCurveItem]:
        """
        Erstellt ein PlotItem-Objekt aus mehreren Graphen
        :param title: Name des Plots
        :param x_range: Grenzbereiche der X-Achse (x_min - x_max)
        :param y_range: Grenzbereiche der Y-Achse (y_min - y_max)
        :param pens: Graphen, welche der Plot darstellen soll.
        :param log: Logarithmische Darstellung der x-Achse
        :return: list of all curves
        """

        curves = []
        canvas: pg.PlotItem = self.qtWindow.addPlot(title=title, row=self.plotRow, col=self.plotColumn, colspan=3)

        canvas.setRange(xRange=x_range, yRange=y_range)
        canvas.setLogMode(log, False)

        for pen in pens:
            curve = pg.PlotCurveItem(pen=pen)
            curves.append(curve)
            canvas.addItem(curve)

        return curves

    def start(self, callback):
        """
        Fenster anzeigen und starten
        """

        thread = BufferThread(callback)
        thread.finished.connect(self.qtApp.exit)
        thread.start()

        self.qtWindow.show()  # QT-Fenster anzeigen
        self.qtApp.exec_()  # QT-App starten
