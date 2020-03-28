from scipy import signal
import matplotlib.pyplot as plt
from sympy.core.tests.test_sympify import numpy
import numpy as np

from BackEnd.Filter import Filter


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

        # Numerator (b) and denominator (a) polynomials of the IIR filter
        self.b = [4.0704e-27,0,1.0136e-17,0,6.3091e-9,0,1.122]
        self.a = [4.1939e-21, 1.1734e-16, 7.9157e-13, 3.3204e-9, 9.0017e-6, 0.018014, 22.645, 20400]
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


