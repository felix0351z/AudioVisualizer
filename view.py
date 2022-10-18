from PySide2 import QtWidgets, QtCore
import pyqtgraph as pg


# TODO Commenting
# TODO Debug


class Window:

    def __init__(self, title: str):
        # Erstelle Haupt-Fenster
        self.qtApp = QtWidgets.QApplication()
        self.qtWindow = pg.GraphicsLayoutWidget(title=title, size=(1920, 1080))
        self.qtWindow.setAntialiasing(True)

        # Momentane Anzahl an Plots im Fenster
        self.plotRow = 0
        self.plotColumn = 0

    # Erhöht die momentane Anzahl an Plots. Spaltdesign wird bevorzugt.
    def _increase_window_size(self):

        if self.plotRow >= self.plotColumn:
            self.plotColumn = self.plotColumn + 1

        if self.plotRow < self.plotColumn:
            self.plotRow = self.plotRow + 1

    create_pen = pg.mkPen

    def create_plot_item(
            self, title: str,
            x_range: (int, int),
            y_range: (int, int),
            log=False) -> pg.PlotItem:

        canvas: pg.PlotItem = self.qtWindow.addPlot(title, row=self.plotRow, col=self.plotColumn)
        self._increase_window_size()

        canvas.setXRange(x_range)
        canvas.setYRange(y_range)
        canvas.setLogMode(x=log, y=False)

        return canvas.plot()

    def create_curve_item(self, pen, width: int):
        return pg.PlotCurveItem(pen=pen, width=width)

    def create_plot_curve_item(
            self,
            title: str,
            x_range: (int, int),
            y_range: (int, int),
            curves: []) -> pg.PlotCurveItem:

        canvas: pg.PlotItem = self.qtWindow.addPlot(title=title, row=self.plotRow, col=self.plotColumn)
        canvas.setXRange(x_range)
        canvas.setYRange(y_range)

        for curve in curves:
            canvas.addItem(curve)

        return canvas.plot()
