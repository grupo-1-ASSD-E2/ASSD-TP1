from scipy import signal

import numpy as np

from BackEnd.Filter import Filter

from BackEnd.Signal import Signal


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
        self.filter_order1 = 8
        self.minAttStopBand_dB1 = 48
        self.freqAtFirstMinAttWn1 = 2 * np.pi * 12
        self.filter_order2 = 8
        self.minAttStopBand_dB2 = 48
        self.freqAtFirstMinAttWn2 = 2 * np.pi * 2700
        self.filter_order3 = 8
        self.minAttStopBand_dB3 = 48
        self.freqAtFirstMinAttWn3 = 2 * np.pi * 375000
        self.analogFilter = True

        # Numerator (b) and denominator (a) polynomials of the IIR filter
        self.b1, self.a1 = signal.cheby2(self.filter_order1, self.minAttStopBand_dB1, self.freqAtFirstMinAttWn1,
                                         self.filterType,
                                         analog=self.analogFilter)
        self.b2, self.a2 = signal.cheby2(self.filter_order2, self.minAttStopBand_dB2, self.freqAtFirstMinAttWn2,
                                         self.filterType,
                                         analog=self.analogFilter)
        self.b3, self.a3 = signal.cheby2(self.filter_order3, self.minAttStopBand_dB3, self.freqAtFirstMinAttWn3,
                                         self.filterType,
                                         analog=self.analogFilter)

    def deactivate_block(self, deactivate):
        self.blockActivated = not deactivate

    def apply_to_signal(self, signal_in):
        returning_signal = Signal(None)
        returning_signal.copy_signal(signal_in)
        if self.blockActivated:
            if 1 / signal_in.period <= 8:
                tout, y, ni = signal.lsim((self.b1, self.a1), signal_in.yValues, signal_in.timeArray)
                returning_signal.set_x_y_values(tout, y)
            elif 1800 >= 1 / signal_in.period > 8:
                tout, y, ni = signal.lsim((self.b2, self.a2), signal_in.yValues, signal_in.timeArray)
                returning_signal.set_x_y_values(tout, y)
            else:
                tout, y, ni = signal.lsim((self.b3, self.a3), signal_in.yValues, signal_in.timeArray)
                returning_signal.set_x_y_values(tout, y)
        return returning_signal
