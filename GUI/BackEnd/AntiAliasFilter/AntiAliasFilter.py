from scipy import signal
import matplotlib.pyplot as plt
from sympy.core.tests.test_sympify import numpy
import numpy as np

from GUI.BackEnd.Filter import Filter


class AntiAliasFilter(Filter):
    def __init__(self):
        self.blockActivated = True


        # A scalar or length-2 sequence giving the critical frequencies.
        # For Type II filters, this is the point in the transition band at which the gain first reaches -rs.
        # For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample.
        # (Wn is thus in half-cycles / sample.)

        # {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, optional
        self.filterType = 'lowpass'

        self.analogFilter = True

        # Creo un coseno para probar el filtro
        self.timeArray = np.arange(0, 0.0003, 0.000001)
        self.cos = np.cos(self.timeArray * 2 * np.pi * 10000)

        # Numerator (b) and denominator (a) polynomials of the IIR filter
        self.b = [4.0704e-27,0,1.0136e-17,0,6.3091e-9,0,1.122]
		self.a = [4.1939e-21,1.1734e-16,7.9157e-13,3.3204e-9,9.0017e-6,0.018014,22.645,20400]
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


