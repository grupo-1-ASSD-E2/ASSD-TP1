from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np


class SpectrumAnalyzer(QMainWindow):

    def __init__(self):
        self.program_state = {}
        self.plot_signals = []
        self.hidden = True

    def __show_spectrum_analyzer__(self):
        QMainWindow.__init__(self)
        # loadUi('FrontEnd/spectrum_analyzer.ui', self)

    def __window_qt_configuration__(self):
        self.setWindowTitle("Spectrum Analyzer")

    def toggle_signal(self, index):
        if self.plot_signals[index] is not None:
            self.plot_signals[index].toggle_spectrum_analyzer_plot()

    def add_signal_to_spectrum_analyzer(self, signal):
        self.plot_signals.append(signal)
        if self.hidden:
            self.hidden = False
            self.__show_spectrum_analyzer__()

    def remove_signal_from_spectrum_analyzer(self, index):
        if self.plot_signals[index] is not None:
            self.plot_signals.pop(index)

    def remove_all_signals_from_spectrum_analyzer(self):
        self.plot_signals.clear()
