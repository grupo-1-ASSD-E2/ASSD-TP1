from scipy import signal
from enum import Enum
import matplotlib.pyplot as plt

from sympy.core.tests.test_sympify import numpy


class Signal:
    def __init__(self, signal_type, freq=-1, period=-1, v_max=-1, phase=0, duty_cycle= 50):
        self.signalType = signal_type
        self.freq = freq  # hz
        self.period = period  # seconds
        self.vMax = v_max  # volts
        self.phase = phase
        self.dutyCycle = duty_cycle

    def apply_filter(self, filter):
        t = numpy.linspace(0, 1, 1000, False)
        sig = numpy.cos(2 * numpy.pi * self.freq * t + self.phase)

        filtered = filter.apply_to_signal(sig)


class SignalTypes(Enum):
    SINUSOIDAL = 0,
    EXPONENTIAL = 1,
    DELTADIRAC = 2,
    SQUARE = 3

