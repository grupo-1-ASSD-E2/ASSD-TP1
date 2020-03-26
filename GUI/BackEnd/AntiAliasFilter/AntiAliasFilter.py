from scipy import signal
import matplotlib.pyplot as plt
from sympy.core.tests.test_sympify import numpy
import numpy as np

from GUI.BackEnd.Filter import Filter


class AntiAliasFilter(Filter):
    def __init__(self):
        self.blockActivated = True

        self.filter_order = 4
        # The minimum attenuation required in the stop band. Specified in decibels, as a positive number.
        self.minAttStopBand_dB = 40

        # A scalar or length-2 sequence giving the critical frequencies.
        # For Type II filters, this is the point in the transition band at which the gain first reaches -rs.
        # For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample.
        # (Wn is thus in half-cycles / sample.)
        # For analog filters, Wn is an angular frequency (e.g. rad/s).
        self.FreqAtFirstMinAttWn = 100000

        # {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, optional
        self.filterType = 'lowpass'

        self.analogFilter = True

        # Creo un coseno para probar el filtro
        self.timeArray = np.arange(0, 0.0003, 0.000001)
        self.cos = np.cos(self.timeArray * 2 * np.pi * 10000)

        # Numerator (b) and denominator (a) polynomials of the IIR filter
        self.b, self.a = signal.cheby2(self.filter_order, self.minAttStopBand_dB, self.FreqAtFirstMinAttWn,
                                       self.filterType,
                                       analog=self.analogFilter)
        self.sos = signal.cheby2(self.filter_order, self.minAttStopBand_dB, self.FreqAtFirstMinAttWn, self.filterType,
                                 analog=self.analogFilter, output="sos")
        # angularFreq : The angular frequencies at which h was computed.
        # freqResponse : The frequency response.
        self.angularFreq, self.freqResponse = signal.freqs(self.b, self.a)

        self.timeOut, self.signalOut, self.xOut = signal.lsim((self.b, self.a), self.cos, self.timeArray)

    def plot_signal(self):
        if self.blockActivated:
            plt.plot(self.timeOut, self.signalOut)
            plt.title('Out')
            plt.xlabel('Time')
            plt.ylabel('V')
            plt.margins(0, 0.1)
            plt.grid(which='both', axis='both')
            plt.show()
        else:
            plt.plot(self.timeArray, self.cos)
            plt.title('cos')
            plt.xlabel('Time')
            plt.ylabel('V')
            plt.margins(0, 0.1)
            plt.grid(which='both', axis='both')
            plt.show()

    def deactivate_block(self, deactivate):
        self.blockActivated = not deactivate

    def apply_to_signal(self, signal_in):
        return signal.lsim((self.b, self.a), signal_in.timeValues, signal_in.yValues)

    def get_filter_freq_response(self):
        return self.angularFreq, self.freqResponse


