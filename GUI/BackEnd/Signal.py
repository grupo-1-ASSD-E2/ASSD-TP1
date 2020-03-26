from enum import Enum
import numpy as np


class Signal:
    def __init__(self, description_text="", signal_type=4):
        self.timeValues = []
        self.yValues = []
        self.signalType = signal_type
        self.description = description_text

    # todo
    def get_frequency_spectrum(self):
        frequency_values = []  # Hz
        y_values = []  # W

        return frequency_values, y_values

    def create_cos_signal(self, hz_frequency, amplitude, phase=0):
        self.timeValues = np.arange(0, 0.0003, 0.000001)
        self.yValues = amplitude * np.cos(self.timeArray * 2 * np.pi * hz_frequency + phase)
        self.signalType = SignalTypes.SINUSOIDAL

    def create_exp_signal(self, v_max, period):
        # todo
        a = 0

    def create_dirac_signal(self):
        # todo
        i = 0

    def create_square_signal(self):
        # todo
        i = 0


class SignalTypes(Enum):
    SINUSOIDAL = 0,
    EXPONENTIAL = 1,
    DELTA_DIRAC = 2,
    SQUARE = 3,
    CUSTOM = 4
