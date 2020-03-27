from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np


class Oscilloscope(QMainWindow):

    def __init__(self):  # Conecta los componentes del .ui realizado en QT con el programa en python

        self.program_state = {}
        self.plot_signals = []
        self.hidden = True

    def __show_oscilloscope__(self):
        QMainWindow.__init__(self)
        # loadUi('FrontEnd/oscilloscope.ui', self)

    def __window_qt_configuration__(self):
        self.setWindowTitle("Oscilloscope")

    def toggle_signal(self, index):
        if self.plot_signals[index] is not None:
            self.plot_signals[index].toggle_oscilloscope_plot()

    def add_signal_to_oscilloscope(self, signal):
        self.plot_signals.append(signal)
        if self.hidden:
            self.hidden = False
            self.__show_oscilloscope__()

    def remove_signal_from_oscilloscope(self, index):
        if self.plot_signals[index] is not None:
            self.plot_signals.pop(index)

    def remove_all_signals_from_oscilloscope(self):
        self.plot_signals.clear()
