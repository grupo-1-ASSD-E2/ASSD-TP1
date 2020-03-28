from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
from scipy import signal as scipySignal


class Signal:
    def __init__(self, timeArray, description_text="", signal_type=4, ploting_type=0):
        self.yValues = []
        self.signalType = signal_type
        self.description = description_text
        self.timeArray = timeArray
        self.plotType = ploting_type
        self.oscilloscopePlotActivated = True  # Permite togglear una senal en el osciloscopio
        self.spectrumAnalyzerPlotActivated = True  # Permite togglear una senal en el analizador de espectro
        self.period = -1

    def copy_signal(self, signal):
        self.yValues = signal.yValues.copy()
        self.signalType = signal.signalType
        self.description = signal.description
        self.timeArray = signal.timeArray.copy()
        self.plotType = signal.plotType
        self.oscilloscopePlotActivated = signal.oscilloscopePlotActivated
        self.spectrumAnalyzerPlotActivated = signal.spectrumAnalyzerPlotActivated
        self.period = signal.period

    def toggle_oscilloscope_plot(self):
        self.oscilloscopePlotActivated = not self.oscilloscopePlotActivated

    def toggle_spectrum_analyzer_plot(self):
        self.spectrumAnalyzerPlotActivated = not self.spectrumAnalyzerPlotActivated

    def set_step_plot(self, step_plot=True):
        if step_plot:
            self.plotType = PlotTypes.STEP
        else:
            self.plotType = PlotTypes.NORMAL

    # todo
    def get_frequency_spectrum(self):
        frequency_values = []  # Hz
        y_values = []  # W

        return frequency_values, y_values

    def set_x_y_values(self, x_values, y_values):
        self.timeArray = x_values.copy()
        self.yValues = y_values.copy()

    def create_cos_signal(self, hz_frequency, amplitude, phase=0):

        self.yValues = amplitude * np.cos(self.timeArray * 2 * np.pi * hz_frequency + phase)
        self.signalType = SignalTypes.SINUSOIDAL
        self.period = 1/hz_frequency

    def create_exp_signal(self, v_max, period):
        self.yValues = self.evaluate_periodic_exp(self.timeArray, period, v_max)
        self.signalType = SignalTypes.EXPONENTIAL
        self.period = period

    def evaluate_periodic_exp(self, time_array: list, period, V_MAX):
        res = []
        for t in time_array:
            t_in_oritginal_period = float(Decimal(str(t)) % Decimal(str(period)))
            if t_in_oritginal_period < 0:
                t_in_oritginal_period = period - t_in_oritginal_period
            if t_in_oritginal_period < period / 2:
                y = V_MAX * np.e ** (-np.abs(t_in_oritginal_period))
            else:
                y = V_MAX * np.e ** (-np.abs(t_in_oritginal_period - period))

            res.append(y)
        return res

    def create_dirac_signal(self):
        i = 0
        zeroIndex = -1
        found = False

        while not found and i < len(self.timeArray):
            if abs(self.timeArray[i]) <= 0.00001:
                Found = True
                zeroIndex = i
            i += 1
        self.yValues = scipySignal.unit_impulse(len(self.timeArray), zeroIndex)

    # periodo en s y dutycicle de 0 a 1
    def create_square_signal(self, dutyCicle, period):
        yValue = scipySignal.square(2 * np.pi * self.timeArray * 1 / period, dutyCicle)
        self.period = period

    def add_description(self, description):
        self.description = description


class SignalTypes(Enum):
    SINUSOIDAL = 0,
    EXPONENTIAL = 1,
    DELTA_DIRAC = 2,
    SQUARE = 3,
    CUSTOM = 4


class PlotTypes(Enum):
    NORMAL = 0,
    STEP = 1
