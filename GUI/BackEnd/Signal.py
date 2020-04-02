from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
from scipy import signal as ss
import numpy as np
import scipy.signal as ss


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
        self.f_A = None
        self.X_A = None

    def copy_signal(self, signal):
        self.yValues = signal.yValues.copy()
        self.signalType = signal.signalType
        self.description = signal.description
        self.timeArray = signal.timeArray.copy()
        self.plotType = signal.plotType
        self.oscilloscopePlotActivated = signal.oscilloscopePlotActivated
        self.spectrumAnalyzerPlotActivated = signal.spectrumAnalyzerPlotActivated
        self.period = signal.period
        self.X_A = signal.X_A
        self.f_A = signal.f_A
        self.duty_cycle = signal.duty_cycle

    def toggle_oscilloscope_plot(self):
        self.oscilloscopePlotActivated = not self.oscilloscopePlotActivated

    def toggle_spectrum_analyzer_plot(self):
        self.spectrumAnalyzerPlotActivated = not self.spectrumAnalyzerPlotActivated

    def set_step_plot(self, step_plot=True):
        if step_plot:
            self.plotType = PlotTypes.STEP
        else:
            self.plotType = PlotTypes.NORMAL

    def calculate_frequency_spectrum(self):
        self.X_A = np.fft.fft(self.yValues)
        t_step_A = np.abs(self.timeArray[0] - self.timeArray[1])
        N_A = self.yValues.size
        self.f_A = np.fft.fftfreq(N_A, d=t_step_A)

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

        res = np.asarray(res)
        return res

    def create_dirac_signal(self):
        self.yValues = ss.unit_impulse(len(self.timeArray), 0)

    # periodo en s y dutycicle de 0 a 1
    def create_square_signal(self, duty_cycle, period):
        self.yValues = (0.5 * ss.square(2 * np.pi * self.timeArray * 1 / period,
                                        duty_cycle / 100) + 0.5)  # Los 0.5 hacen que quede entre 0 y 1
        self.period = period
        self.duty_cycle = duty_cycle
        self.signalType = SignalTypes.SQUARE

    def create_half_sine_signal(self, hz_frequency, amplitude, phase=0):
        self.yValues = self.evaluate_half_sine(self.timeArray, hz_frequency, amplitude, phase)
        self.signalType = SignalTypes.HALFSINE
        self.period = 1 / hz_frequency * 3 / 2

    def evaluate_half_sine(self, time_array: list, freq, amplitude, phase):
        res = []
        period = 3 / 2 * 1 / freq
        for t in time_array + 1 / (2 * freq):
            t_in_original_period = float(Decimal(str(t)) % Decimal(str(period)))
            if t_in_original_period < 0:
                t_in_original_period = period - t_in_original_period
            if t_in_original_period < (1 / freq) / 2:
                y = amplitude * np.sin(t_in_original_period * 2 * np.pi * freq + phase)
            else:
                y = amplitude * np.sin((t_in_original_period - period) * 2 * np.pi * freq + phase)

            res.append(y)

        res = np.asarray(res)
        return res

    def change_time_array(self, time_array):
        self.timeArray = time_array.copy()
        if self.signalType == SignalTypes.SQUARE:
            self.create_square_signal(self.duty_cycle, self.period)

    def add_description(self, description):
        self.description = description

    def compute_fft(self, time_interval, signal, period, n_periods=1, window='boxcar'):
        ''' window can be:
            'boxcar' (rectangle),
            'barthann' (Bartlett-Hann),
            'bartlett',
            'hanning',
            'hamming',
            'tukey',
            'flattop',
            'hann',
            'nuttall',
            'parzen',
            'cosine',
            'blackman',
            'bohman',
            'blackmanharris' '''

        t_step = (max(time_interval) - min(time_interval)) / len(time_interval)
        points_in_period = int(np.rint(period / t_step))

        try:
            window = getattr(ss, window)((points_in_period * n_periods))
            amount_of_zeros_to_pad = len(signal) - len(window)
            window = np.append(window, [0] * amount_of_zeros_to_pad)
            signal_for_fft = np.multiply(signal, window)[:(points_in_period * n_periods)]
        except AttributeError:
            return

        fft = np.fft.fft(signal_for_fft)
        N = signal_for_fft.size
        f = np.fft.fftfreq(N, d=t_step)

        return f, fft, N

    def fft(self, time_interval, signal, period, mode='fast'):
        ''' time_interval: array containing time values for the signal meant to be transformed.

            signal: array containing signal meant to be transformed.

            period: period of the signal to be transformed.

            If mode='fast', only one period will be used from the input signal.
            If mode='best', the max amount of periods will be used.
            'fast' is default.'''

        if mode == 'best':
            n_p = int(np.rint((max(time_interval) - min(time_interval)) / period))
        elif mode == 'fast':
            n_p = 1
        else:
            return

        window_types = ['boxcar', 'barthann', 'bartlett', 'hanning', 'hamming', 'tukey', 'hann', 'nuttall', 'parzen',
                        'cosine', 'blackman', 'bohman', 'blackmanharris']

        fft = []
        merits = []
        for w in window_types:
            f, X, N = self.compute_fft(time_interval, signal, period, n_periods=n_p, window=w)
            new_fft = [f, X, N, w]
            fft.append(new_fft)

            merit = 0
            max_bin = max(np.abs(X))
            for X_bin in X:
                if np.abs(X_bin) < (0.2 * max_bin):
                    merit = merit + np.abs(X_bin)

            merits.append(merit)

        return fft[merits.index(min(merits))]


class SignalTypes(Enum):
    SINUSOIDAL = 0,
    EXPONENTIAL = 1,
    DELTA_DIRAC = 2,
    SQUARE = 3,
    CUSTOM = 4,
    HALFSINE = 5


class PlotTypes(Enum):
    NORMAL = 0,
    STEP = 1
