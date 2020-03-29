from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np
from BackEnd.Signal import PlotTypes

from BackEnd.Signal import Signal


class Oscilloscope(QMainWindow):

    def __init__(self):  # Conecta los componentes del .ui realizado en QT con el programa en python
        QMainWindow.__init__(self)
        self.program_state = {}
        self.plot_signals = []
        self.hidden = True

    def closeEvent(self, event):

        self.hidden = True
        self.plot_signals.clear()
        event.accept()  # let the window close

    def __show_oscilloscope__(self):

        loadUi('FrontEnd/oscilloscope.ui', self)
        self.setWindowTitle("Osciloscopio")
        self.removeSignal.clicked.connect(self.remove_signal_from_oscilloscope)
        self.removeAllSignals.clicked.connect(self.remove_all_signals_from_oscilloscope)
        self.toggleSignal.clicked.connect(self.toggle_signal)
        self.plot_current_signals()

        self.show()

    def toggle_signal(self):
        index = self.signalList.currentRow()
        if index != -1:
            if self.plot_signals[index] is not None:
                self.plot_signals[index].toggle_oscilloscope_plot()
        self.plot_current_signals()

    def add_signal_to_oscilloscope(self, signal):
        if self.hidden:
            self.hidden = False
            self.__show_oscilloscope__()
        new_signal = Signal(signal.timeArray)
        new_signal.copy_signal(signal)
        self.plot_signals.append(new_signal)
        list_widget_item = QListWidgetItem(new_signal.description)
        self.signalList.addItem(list_widget_item)
        self.plot_current_signals()

    def remove_signal_from_oscilloscope(self):
        index = self.signalList.currentRow()
        if index != -1:
            item = self.signalList.takeItem(index)
            item = None
            if self.plot_signals[index] is not None:
                self.plot_signals.pop(index)
        self.plot_current_signals()

    def remove_all_signals_from_oscilloscope(self):
        self.plot_signals.clear()
        self.signalList.clear()
        self.plot_current_signals()

    def plot_current_signals(self):
        self.oscilloscopeGraph.canvas.axes.clear()
        self.oscilloscopeGraph.figure.tight_layout()
        self.oscilloscopeGraph.canvas.axes.set_xlabel("t [s]")
        self.oscilloscopeGraph.canvas.axes.set_ylabel("A [V]")
        self.oscilloscopeGraph.canvas.axes.axis('auto')
        self.oscilloscopeGraph.canvas.axes.yaxis.label.set_color('white')
        self.oscilloscopeGraph.canvas.axes.xaxis.label.set_color('white')
        self.oscilloscopeGraph.canvas.axes.grid(True, which="both")

        period_found = False
        min_period = -1

        for signal in self.plot_signals:
            if signal.oscilloscopePlotActivated:

                if signal.plotType == PlotTypes.STEP:
                    self.oscilloscopeGraph.canvas.axes.step(signal.timeArray, signal.yValues
                                                            , where='post', label=signal.description)
                else:
                    self.oscilloscopeGraph.canvas.axes.plot(signal.timeArray, signal.yValues, label=signal.description)

                if signal.period != -1:
                    if not period_found:
                        min_period = signal.period
                        period_found = True
                    else:
                        if signal.period < min_period:
                            min_period = signal.period

        if period_found:
            self.oscilloscopeGraph.canvas.axes.set(xlim=(0, 3* min_period))
            self.oscilloscopeGraph.canvas.axes.set_ylim(auto=True)
        else:
            self.oscilloscopeGraph.canvas.axes.axis('auto')
        self.oscilloscopeGraph.canvas.axes.ticklabel_format(useOffset=False)
        self.oscilloscopeGraph.canvas.axes.legend(loc='best')
        self.oscilloscopeGraph.figure.tight_layout()

        self.oscilloscopeGraph.canvas.draw()  # Redraws
