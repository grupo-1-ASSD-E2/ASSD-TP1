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
        self.duty_cycle = 1

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

    def get_frequency_spectrum(self):
        X_A = np.fft.fft(self.yValues)
        t_step_A = np.abs(self.timeArray[0] - self.timeArray[1])
        N_A = self.yValues.size
        f_A = np.fft.fftfreq(N_A, d=t_step_A)

        return f_A, X_A

    def set_x_y_values(self, x_values, y_values):
        self.timeArray = x_values.copy()
        self.yValues = y_values.copy()

    def create_cos_signal(self, hz_frequency, amplitude, phase=0):

        self.yValues = amplitude * np.cos(self.timeArray * 2 * np.pi * hz_frequency + phase)
        self.signalType = SignalTypes.SINUSOIDAL
        self.period = 1 / hz_frequency

    def create_exp_signal(self, v_max, period):
        self.yValues = self.evaluate_periodic_exp(self.timeArray, period, v_max)
        self.signalType = SignalTypes.EXPONENTIAL
        self.period = period

    def evaluate_periodic_exp(self, time_array: list, period, V_MAX):
        res = []
        for t in time_array:
            t_in_original_period = float(Decimal(str(t)) % Decimal(str(period)))
            if t_in_original_period < 0:
                t_in_original_period = period - t_in_original_period
            if t_in_original_period < period / 2:
                y = V_MAX * np.e ** (-np.abs(t_in_original_period))
            else:
                y = V_MAX * np.e ** (-np.abs(t_in_original_period - period))

            res.append(y)
        return res

    def create_dirac_signal(self):
        self.yValues = scipySignal.unit_impulse(len(self.timeArray), 0)

    # periodo en s y dutycicle de 0 a 1
    def create_square_signal(self, duty_cycle, period):
        self.yValues = (0.5 * scipySignal.square(2 * np.pi * self.timeArray * 1 / period,
                                                 duty_cycle / 100) + 0.5)  # Los 0.5 hacen que quede entre 0 y 1
        self.period = period
        self.duty_cycle = duty_cycle
        self.signalType = SignalTypes.SQUARE

    def change_time_array(self, time_array):
        self.timeArray = time_array.copy()
        if self.signalType == SignalTypes.SQUARE:
            self.create_square_signal(self.duty_cycle, self.period)

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
