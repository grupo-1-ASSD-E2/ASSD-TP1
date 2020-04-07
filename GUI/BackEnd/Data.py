from enum import Enum

from BackEnd.Signal import Signal


class Data:
    def __init__(self):
        self.signals = [None, None, None, None, None]
        self.blocks = [None, None, None, None]
        self.samplingSignal = None

    def block_property_changed(self, block_num):
        for i in range(block_num, len(self.blocks)):  # reconstruyo desde el bloque que cambio hasta el final
            self.signals[i + 1] = None

    def xin_changed(self, xin):
        self.signals = [None, None, None, None, None, None]
        self.signals[0] = Signal(xin.timeArray)
        self.signals[0].copy_signal(xin)
        if self.samplingSignal is not None:
            self.samplingSignal.change_time_array(self.signals[0].timeArray)
            self.blocks[BlockOrder.SampleAndHold.value].control_by_sampling_signal(self.samplingSignal)
            self.blocks[BlockOrder.AnalogSwitch.value].control_by_sampling_signal(self.samplingSignal)

    def sampling_signal_changed(self, duty_cycle, period):
        if (self.blocks[BlockOrder.SampleAndHold.value].blockActivated and self.blocks[
            BlockOrder.AnalogSwitch.value].blockActivated):
            for i in range(SignalOrder.SampleAndHoldOut.value, len(self.signals)):
                self.signals[i] = None

        self.samplingSignal = Signal(self.signals[0].timeArray)
        self.samplingSignal.create_square_signal(duty_cycle, period)
        self.blocks[BlockOrder.SampleAndHold.value].control_by_sampling_signal(self.samplingSignal)
        self.blocks[BlockOrder.AnalogSwitch.value].control_by_sampling_signal(self.samplingSignal)

    def valid_sampling_period(self, period):
        signal_period = self.signals[0].period
        if signal_period/1000 <= period <= signal_period*2:
            return True
        return False
    def add_signal(self, signal, signal_order):
        new_aux = Signal(signal.timeArray)
        new_aux.copy_signal(signal)
        self.signals[signal_order] = new_aux

    def add_block(self, block, block_order):
        self.blocks[block_order] = block

    def get_signal(self, signal_order):
        returning_signal = Signal(None)
        if self.signals[signal_order] is not None:

            returning_signal.copy_signal(self.signals[signal_order])
            return returning_signal
        else:
            found = False
            i = signal_order - 1
            while not found and i >= 0:
                if self.signals[i] is not None:
                    found = True
                else:
                    i -= 1
            if not found:
                return None
            else:
                for it in range(i, signal_order):
                    self.signals[it + 1] = self.blocks[it].apply_to_signal(self.signals[it])


                returning_signal.copy_signal(self.signals[signal_order])

                return returning_signal

    def xin_exists(self):
        if self.signals[0] is not None:
            return True
        else:
            return False

    def sampling_exists(self):
        if self.samplingSignal is not None:
            return True
        elif not self.blocks[BlockOrder.SampleAndHold.value].blockActivated and not self.blocks[
            BlockOrder.AnalogSwitch.value].blockActivated:  # no necesito sampleo
            return True
        else:
            return False


class SignalOrder(Enum):
    Xin = 0
    AntiAliasOut = 1
    SampleAndHoldOut = 2
    AnalogSwitchOut = 3
    RecoveryOut = 4
    XOut = 4


class BlockOrder(Enum):
    AntiAlias = 0
    SampleAndHold = 1
    AnalogSwitch = 2
    Recovery = 3
