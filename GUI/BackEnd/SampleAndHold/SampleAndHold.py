from scipy import signal
import matplotlib.pyplot as plt
from sympy.core.tests.test_sympify import numpy
import numpy as np

from GUI.BackEnd.Filter import Filter


class SampleAndHold(Filter):
    def __init__(self):
        self.blockActivated = True
        self.samplingPeriod = 0 

    def change_sampling_period(sampling_period):
        self.samplingPeriod = sampling_period

    def deactivate_block(self, deactivate):
        self.blockActivated = not deactivate

    def apply_to_signal(self, signal_in):
        out_x_array = signal_in.timeValues
        out_y_array = signal_in.yValues

        sample_time = 0
        for (i in range(0, len(out_x_array))):
            if (abs(out_x_array[i] - sample_time) < 0.00001):
                out_y_array[i] = signal_in.yValues[i]
                sample_time += self.samplingPeriod
            else:
                if (i>0):
                    out_y_array[i] = out_y_array[i-1]

        return out_x_array, out_y_array


        return signal.lsim((self.b, self.a), signal_in.timeValues, signal_in.yValues)

    def get_filter_freq_response(self):
        return self.angularFreq, self.freqResponse
