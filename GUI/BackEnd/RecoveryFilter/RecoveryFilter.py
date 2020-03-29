from scipy import signal
import matplotlib.pyplot as plt
from sympy.core.tests.test_sympify import numpy
import numpy as np

from BackEnd.Filter import Filter


class RecoveryFilter(Filter):
    def __init__(self):
        self.blockActivated = True

        # A scalar or length-2 sequence giving the critical frequencies.
        # For Type II filters, this is the point in the transition band at which the gain first reaches -rs.
        # For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample.
        # (Wn is thus in half-cycles / sample.)
        # For analog filters, Wn is an angular frequency (e.g. rad/s).

        # {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, optional
        self.filterType = 'lowpass'
        self.filter_order = 7
        self.minAttStopBand_dB = 41
        self.freqAtFirstMinAttWn = 2 * np.pi * 1800
        self.analogFilter = True

        # Numerator (b) and denominator (a) polynomials of the IIR filter
        self.b, self.a = signal.cheby2(self.filter_order, self.minAttStopBand_dB, self.freqAtFirstMinAttWn,
                                       self.filterType,
                                       analog=self.analogFilter)
        # angularFreq : The angular frequencies at which h was computed.
        # freqResponse : The frequency response.
        self.angularFreq, self.freqResponse = signal.freqs(self.b, self.a)



    def deactivate_block(self, deactivate):
        self.blockActivated = not deactivate

    def apply_to_signal(self, signal_in):
        if self.blockActivated:
            tout, y, ni = signal.lsim((self.b, self.a), signal_in.yValues, signal_in.timeArray)
            signal_in.set_x_y_values(tout, y)
       

    def get_filter_freq_response(self):
        return self.angularFreq, self.freqResponse
