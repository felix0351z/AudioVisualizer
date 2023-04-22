from typing import Callable

import numpy
from PySide2 import QtWidgets, QtGui
import pyqtgraph as pg

from src.core.input import InputStreamThread


class Window:
    """
    A window is a PyQt-Graph overlay which gives the functionality to create and display different measurement data in the form of plotted graphs.
    An input callback stream to the current music output starts and the informational data will be provided as callback.
    """

    def __init__(self, title: str):
        """
        Create a new PyQt-Graph plotting window
        :param title: Name of the window
        """

        self.qtApp = QtWidgets.QApplication()
        self.qtWindow = pg.GraphicsLayoutWidget(title=title, size=(1920, 1080))
        self.qtWindow.setAntialiasing(True)

        # Next free plot spaces
        self.plotRow = 0
        self.plotColumn = 0

    def _increase_window_size(self):
        # Set the plot attributes to the next empy position

        if self.plotColumn >= self.plotRow:
            self.plotRow = self.plotRow + 1
            return

        if self.plotColumn < self.plotRow:
            self.plotColumn, self.plotRow = self.plotRow, self.plotColumn

    def create_pen(self, color=(255, 255, 255, 200), width=2) -> QtGui.QPen:
        """
        Create a new Qt-Graph pen.
        This function is a abbreviation to the :class:`pg.mkPen()` function and does exactly the same.

        :param color: The color of the plotted graph. (R, G, B, W)
        :param width: The width of the plotted graph.
        """
        return pg.mkPen(color, width=width)

    def create_plot_item(
            self, title: str,
            x_range: tuple[int, int],
            y_range: tuple[int, int],
            log=False) -> pg.PlotDataItem:
        """
        Create a new plot field in the window.
        The plot will have a standard width of 1 and the color white.
        For a more specific plot look at the create_plot_curve_item() function.

        :param title: Name of the plot field
        :param x_range: Border area of the x-axis (x_min - x_max)
        :param y_range: Border area of the y-axis (y_min - y_max)
        :param log: If the graph should be plotted logarithmic in the x-axis
        :return:
                A pyqt-graph :class:`pg.PlotDataItem`
                Use the :class:`setData()` function to plot the data.
        """

        canvas: pg.PlotItem = self.qtWindow.addPlot(title=title, row=self.plotRow, col=self.plotColumn)
        self._increase_window_size()

        canvas.setRange(xRange=x_range, yRange=y_range)
        canvas.setLogMode(x=log, y=False)

        return canvas.plot()

    def create_plot_curve_item(
            self,
            title: str,
            x_range: tuple[int, int],
            y_range: tuple[int, int],
            pens: list[QtGui.QPen],
            log=False) -> list[pg.PlotCurveItem]:
        """
        Create a new plot field with multiple graphs.
        The plot will have as many graphs as given pens with the same attributes from the pens

        :param title: Name of the plot field
        :param x_range: Border area of the x-axis (x_min - x_max)
        :param y_range: Border area of the y-axis (y_min - y_max)
        :param pens: The pens, which are representing the graphs
        :param log: If the graph should be plotted logarithmic in the x-axis
        :return:
                A list of pyqt-graph :class:`pg.PlotCurveItem` objects
                To transmit the data, use the :class:`setData()` function from each item
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

    def start(self, callback: Callable[[numpy.ndarray], None]):
        """
        Open the window and start the listening to the audio source.
        The function will return the current music data as waveform to the callback.

        :param callback:
                Callback function for the music input stream.
                Provides the current waveform as :class:`numpy.ndarray`
        """

        thread = InputStreamThread(callback)
        thread.finished.connect(self.qtApp.exit)
        thread.start()

        self.qtWindow.show()  # Show the window
        self.qtApp.exec_()  # Start the application (suspending)
