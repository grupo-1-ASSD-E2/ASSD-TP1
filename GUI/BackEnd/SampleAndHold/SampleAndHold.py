from scipy import signal
import matplotlib.pyplot as plt
from sympy.core.tests.test_sympify import numpy
import numpy as np

from BackEnd.Filter import Filter

from BackEnd.Signal import Signal


class SampleAndHold(Filter):
    def __init__(self):
        self.blockActivated = True
        self.samplingPeriod = 0.01
        self.samplingSignal = None

    def control_by_sampling_signal(self, sampling_signal):
        self.samplingSignal = Signal(sampling_signal.timeArray)
        self.samplingSignal.copy_signal(sampling_signal)

    def deactivate_block(self, deactivate):
        self.blockActivated = not deactivate

    def apply_to_signal(self, signal_in):
        if self.blockActivated:

            out_x_array = signal_in.timeArray.copy()
            out_y_array = signal_in.yValues.copy()

            for it in range(0, len(signal_in.timeArray)):
                if self.samplingSignal.yValues[it] > 0.5:  # Chequea si la senal de sampleo esta activa
                    out_y_array[it] = signal_in.yValues[it]
                else:
                    if it > 0 and out_y_array[it - 1] is not None:
                        out_y_array[it] = out_y_array[it - 1]
                    else:
                        out_y_array[it] = 0

            signal_in.set_x_y_values(out_x_array, out_y_array)
            signal_in.set_step_plot(True)
