from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal


class Signal:
    def __init__(self, timeArray, description_text="", signal_type=4, ploting_type=0):
        self.timeValues = None
        self.yValues = []
        self.signalType = signal_type
        self.description = description_text
        self.timeArray = timeArray
        self.plotType = ploting_type
        self.oscilloscopePlotActivated = True  # Permite togglear una senal en el osciloscopio
        self.spectrumAnalyzerPlotActivated = True  # Permite togglear una senal en el analizador de espectro

    def toggle_oscilloscope_plot(self):
        self.oscilloscopePlotActivated = not self.oscilloscopePlotActivated

    def toggle_spectrum_analyzer_plot(self):
        self.spectrumAnalyzerPlotActivated = not self.spectrumAnalyzerPlotActivated

    def set_step_plot(self, step_plot=True):
        if step_plot:
            self.plotType = PlotingTypes.STEP
        else:
            self.plotType = PlotingTypes.NORMAL

    # todo
    def get_frequency_spectrum(self):
        frequency_values = []  # Hz
        y_values = []  # W

        return frequency_values, y_values

    def set_x_y_values(self, x_values, y_values):
        self.timeArray = x_values
        self.yArray = y_values

    def create_cos_signal(self, hz_frequency, amplitude, phase=0):
        self.timeValues = self.timeArray
        self.yValues = amplitude * np.cos(self.timeArray * 2 * np.pi * hz_frequency + phase)
        self.signalType = SignalTypes.SINUSOIDAL

    def create_exp_signal(self, v_max, period):
        self.timeValues = self.timeArray
        self.yValues = self.evaluate_periodic_exp(self.timeValues, period, v_max)
        self.signalType = SignalTypes.EXPONENTIAL
        plt.plot(self.timeValues, self.yValues)

        plt.show()

    def evaluate_periodic_exp(self, time_array: list, period, V_MAX):
        res = []
        for t in time_array:
            t_in_oritginal_period = float(Decimal(str(t)) % Decimal(str(period)))
            if t_in_oritginal_period < 0:
                t_in_oritginal_period = 10 - t_in_oritginal_period
            if t_in_oritginal_period < 5:
                y = V_MAX * np.e ** (-np.abs(t_in_oritginal_period))
            else:
                y = V_MAX * np.e ** (-np.abs(t_in_oritginal_period - 10))

            res.append(y)
        return res

    def create_dirac_signal(self):
        # todo
        i = 0

    def create_square_signal(self):
        # todo
        i = 0


class SignalTypes(Enum):
    SINUSOIDAL = 0,
    EXPONENTIAL = 1,
    DELTA_DIRAC = 2,
    SQUARE = 3,
    CUSTOM = 4


class PlotingTypes(Enum):
    NORMAL = 0,
    STEP = 1
