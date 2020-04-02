from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np
from BackEnd.Signal import PlotTypes

from BackEnd.Signal import Signal


class SpectrumAnalyzer(QMainWindow):

    def __init__(self):  # Conecta los componentes del .ui realizado en QT con el programa en python
        QMainWindow.__init__(self)
        self.program_state = {}
        self.plot_signals = []
        self.hidden = True

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
            '''
            fo = (freq_values[2] - freq_values[1]) / 20
            width = 30
            if freq_values[1] != 0:
                width = fo * freq_values / freq_values[1]'''

            self.spectrumGraph.canvas.axes.bar(freq_values, (np.abs(y_values) * 1 / signal.yValues.size),
                                               label=signal.description + '. Ventana: ' + window,
                                               width=40)
            self.spectrumGraph.canvas.axes.set_xlim( left=-10000, right=10000)

        self.spectrumGraph.canvas.axes.legend(loc='best')

        self.spectrumGraph.canvas.draw()  # Redraw

    def plot_current_signals(self):
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
                '''
                fo = (freq_values[2] - freq_values[1]) / 20
                width = 30
                if freq_values[1] != 0:
                    width = fo * freq_values / freq_values[1]'''

                self.spectrumGraph.canvas.axes.bar(freq_values, (np.abs(y_values) * 1 / signal.yValues.size),
                                                   label=signal.description + '. Ventana: ' + window,
                                                   width=40)
                self.spectrumGraph.canvas.axes.set_xlim( left=-10000, right=10000)

        self.spectrumGraph.canvas.axes.legend(loc='best')

        self.spectrumGraph.canvas.draw()  # Redraws
