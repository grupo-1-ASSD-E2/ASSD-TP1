from scipy import signal
import matplotlib.pyplot as plt
from sympy.core.tests.test_sympify import numpy
import numpy as np

from BackEnd.Filter import Filter


class AnalogSwitch(Filter):
    def __init__(self):
        self.blockActivated = True
        self.samplingPeriod = 0

    def change_sampling_period(self, sampling_period):
        self.samplingPeriod = sampling_period

    def deactivate_block(self, deactivate):
        self.blockActivated = not deactivate

    def apply_to_signal(self, signal_in):
        if self.blockActivated:
            # todo
            i = 0