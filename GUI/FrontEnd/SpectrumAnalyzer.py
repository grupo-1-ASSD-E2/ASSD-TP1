from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np


class SpectrumAnalyzer(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.program_state = {}
        self.plot_signals = []
        self.hidden = True

    def closeEvent(self, event):

        self.hidden = True
        self.plot_signals.clear()
        event.accept()  # let the window close

    def __show_spectrum_analyzer__(self):

        loadUi('GUI/FrontEnd/spectrum_analyzer.ui', self)
        self.setWindowTitle("Analizador de Espectro")
        self.removeSignal.clicked.connect(self.remove_signal_from_spectrum_analyzer)
        self.removeAllSignals.clicked.connect(self.remove_all_signals_from_spectrum_analyzer)
        self.toggleSignal.clicked.connect(self.toggle_signal)
        self.plot_current_signals()

        self.show()

    def toggle_signal(self, index):
        if self.plot_signals[index] is not None:
            self.plot_signals[index].toggle_spectrum_analyzer_plot()
        self.plot_current_signals()

    def add_signal_to_spectrum_analyzer(self, signal):
        self.plot_signals.append(signal)
        if self.hidden:
            self.hidden = False
            self.__show_spectrum_analyzer__()
        self.plot_signals.append(signal)
        list_widget_item = QListWidgetItem(signal.description)
        self.signalList.addItem(list_widget_item)
        self.plot_current_signals()

    def remove_signal_from_spectrum_analyzer(self, index):
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

    def plot_current_signals(self):
        self.spectrumGraph.canvas.axes.clear()
        self.spectrumGraph.canvas.axes.set_xscale('log')
        self.spectrumGraph.canvas.axes.set_xlabel("f [Hz]")
        self.spectrumGraph.canvas.axes.set_ylabel("P [W]")
        self.spectrumGraph.canvas.axes.axis('auto')
        self.spectrumGraph.canvas.axes.yaxis.label.set_color('white')
        self.spectrumGraph.canvas.axes.xaxis.label.set_color('white')
        self.spectrumGraph.canvas.axes.grid(True, which="both")
        self.spectrumGraph.figure.tight_layout()
        for signal in self.plot_signals:
            if signal.spectrumAnalyzerPlotActivated:
                freq_values, y_values = signal.get_frequency_spectrum()
                self.spectrumGraph.canvas.axes.plot(freq_values, y_values, label=signal.description)
        self.spectrumGraph.canvas.axes.axis('auto')
        self.spectrumGraph.canvas.axes.legend(loc='best')
        self.spectrumGraph.canvas.draw()  #
