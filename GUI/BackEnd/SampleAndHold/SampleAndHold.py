from scipy import signal
import matplotlib.pyplot as plt
from sympy.core.tests.test_sympify import numpy
import numpy as np

from BackEnd.Filter import Filter

from BackEnd.Signal import Signal


class SampleAndHold(Filter):
    def __init__(self):
        self.blockActivated = True
        self.samplingSignal = None

    def control_by_sampling_signal(self, sampling_signal):
        self.samplingSignal = None
        self.samplingSignal = Signal(sampling_signal.timeArray)
        self.samplingSignal.copy_signal(sampling_signal)

    def deactivate_block(self, deactivate):
        self.blockActivated = not deactivate

    def apply_to_signal(self, signal_in):
        returning_signal = Signal(None)
        returning_signal.copy_signal(signal_in)

        if self.blockActivated:

            out_x_array = signal_in.timeArray.copy()
            out_y_array = signal_in.yValues.copy()

            for it in range(0, len(signal_in.timeArray)):
                if self.samplingSignal.yValues[it] > 0.4:  # Chequea si la senal de sampleo esta activa
                    out_y_array[it] = signal_in.yValues[it]
                else:
                    if it > 0 and out_y_array[it - 1] is not None:
                        out_y_array[it] = out_y_array[it - 1]
                    else:
                        out_y_array[it] = 0

            returning_signal.set_x_y_values(out_x_array, out_y_array)
            returning_signal.set_step_plot(True)
        return returning_signal
