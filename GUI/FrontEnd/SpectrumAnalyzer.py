import random

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np
from matplotlib.colors import hsv_to_rgb
from matplotlib.cm import get_cmap
from BackEnd.Signal import PlotTypes

from BackEnd.Signal import Signal


class SpectrumAnalyzer(QMainWindow):

    def __init__(self):  # Conecta los componentes del .ui realizado en QT con el programa en python
        QMainWindow.__init__(self)
        self.program_state = {}
        self.plot_signals = []
        self.hidden = True
        self.colorit = 0
        self.colors = ['b', 'g', 'y', 'c', 'm', 'k', 'r']
        self.currentMax = 0

    def closeEvent(self, event):

        self.hidden = True
        self.plot_signals.clear()
        event.accept()  # let the window close

    def __show_spectrum_analyzer__(self):

        try:
            loadUi('../GUI/FrontEnd/spectrum_analyzer.ui', self)
        except:
            loadUi('GUI/FrontEnd/spectrum_analyzer.ui', self)
        self.setWindowTitle("Analizador de Espectro")
        self.removeSignal.clicked.connect(self.remove_signal_from_spectrum_analyzer)
        self.removeAllSignals.clicked.connect(self.remove_all_signals_from_spectrum_analyzer)
        self.toggleSignal.clicked.connect(self.toggle_signal)

        self.plot_current_signals()

        self.show()

    def toggle_signal(self):
        index = self.signalList.currentRow()
        if index != -1:
            if self.plot_signals[index] is not None:
                self.plot_signals[index].toggle_spectrum_analyzer_plot()
        self.plot_current_signals()

    def add_signal_to_spectrum_analyzer(self, signal):
        if self.hidden:
            self.hidden = False
            self.__show_spectrum_analyzer__()
        new_signal = Signal(signal.timeArray)
        new_signal.copy_signal(signal)
        self.plot_signals.append(new_signal)
        list_widget_item = QListWidgetItem(new_signal.description + ' Ventana: ' + new_signal.spectrum[3])
        self.signalList.addItem(list_widget_item)
        self.plot_invidivual_signal(new_signal)

    def remove_signal_from_spectrum_analyzer(self):
        index = self.signalList.currentRow()
        if index != -1:
            item = self.signalList.takeItem(index)
            item = None
            if self.plot_signals[index] is not None:
                self.plot_signals.pop(index)
        self.plot_current_signals()

    def remove_all_signals_from_spectrum_analyzer(self):

        self.plot_signals.clear()
        self.signalList.clear()
        self.plot_current_signals()

    def plot_invidivual_signal(self, signal):
        self.spectrumGraph.figure.tight_layout()
        self.spectrumGraph.canvas.axes.set_xscale('linear')
        self.spectrumGraph.canvas.axes.set_xlabel("f [Hz]")
        self.spectrumGraph.canvas.axes.set_ylabel("A [V]")
        self.spectrumGraph.canvas.axes.axis('auto')
        self.spectrumGraph.canvas.axes.yaxis.label.set_color('white')
        self.spectrumGraph.canvas.axes.xaxis.label.set_color('white')
        self.spectrumGraph.canvas.axes.grid(True, which="both")

        if signal.spectrumAnalyzerPlotActivated:
            freq_values = signal.spectrum[0]
            y_values = signal.spectrum[1]

            window = signal.spectrum[3]

            self.make_stem(self.spectrumGraph.canvas.axes, freq_values, (np.abs(y_values) * 1 / signal.yValues.size),
                           label=signal.description + '. Ventana: ' + window)

            self.spectrumGraph.canvas.axes.set_xlim(left=-10000, right=10000)

        self.spectrumGraph.figure.tight_layout()

        self.spectrumGraph.canvas.axes.legend(loc='best')

        self.spectrumGraph.canvas.draw()  # Redrawv

    def make_stem(self, ax, x, y, label="", **kwargs):

        label_text = label
        ax.axhline(x[0], x[-1], 0, color='r')
        color = self.get_next_color()
        ax.vlines(x, 0, y, colors=color, label=label_text)
        if y.max() > self.currentMax:
            self.currentMax = y.max()
        ax.set_ylim([1.05 * y.min(), 1.05 * self.currentMax])

    def get_next_color(self):
        if self.colorit < len(self.colors):
            color = self.colors[self.colorit]
            self.colorit += 1

        else:
            r = random.randrange(0, 10, 1) / 10
            g = r / 2
            b = random.randrange(0, 10, 1) / 10
            color = (r, g, b)
        return color

    def plot_current_signals(self):
        self.colorit = 0
        self.currentMax = 0
        self.spectrumGraph.canvas.axes.clear()
        self.spectrumGraph.figure.tight_layout()
        self.spectrumGraph.canvas.axes.set_xscale('linear')
        self.spectrumGraph.canvas.axes.set_xlabel("f [Hz]")
        self.spectrumGraph.canvas.axes.set_ylabel("A [V]")
        self.spectrumGraph.canvas.axes.axis('auto')
        self.spectrumGraph.canvas.axes.yaxis.label.set_color('white')
        self.spectrumGraph.canvas.axes.xaxis.label.set_color('white')
        self.spectrumGraph.canvas.axes.grid(True, which="both")

        for signal in self.plot_signals:
            if signal.spectrumAnalyzerPlotActivated:
                freq_values = signal.spectrum[0]
                y_values = signal.spectrum[1]

                window = signal.spectrum[3]

                self.make_stem(self.spectrumGraph.canvas.axes, freq_values,
                               (np.abs(y_values) * 1 / signal.yValues.size),
                               label=signal.description + '. Ventana: ' + window)

                self.spectrumGraph.canvas.axes.set_xlim(left=-10000, right=10000)

        self.spectrumGraph.canvas.axes.legend(loc='best')
        self.spectrumGraph.figure.tight_layout()

        self.spectrumGraph.canvas.draw()  # Redraws
