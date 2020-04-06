from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np
from BackEnd.AntiAliasFilter.AntiAliasFilter import AntiAliasFilter
from BackEnd.RecoveryFilter.RecoveryFilter import RecoveryFilter
from BackEnd.AnalogSwitch.AnalogSwitch import AnalogSwitch
from BackEnd.SampleAndHold.SampleAndHold import SampleAndHold
from BackEnd.Signal import SignalTypes, Signal

from FrontEnd.Oscilloscope import Oscilloscope
from FrontEnd.SpectrumAnalyzer import SpectrumAnalyzer

# Clase UIWindow. Maneja lo relacionado con la ventana mostrada al usuario.
from BackEnd.Data import Data, BlockOrder, SignalOrder


class UIWindow(QMainWindow):

    def __init__(self):  # Conecta los componentes del .ui realizado en QT con el programa en python
        QMainWindow.__init__(self)

        self.oscilloscope = Oscilloscope()
        self.program_state = {}
        try:
            loadUi('../GUI/FrontEnd/samplingui.ui', self)
        except:
            loadUi('GUI/FrontEnd/samplingui.ui', self)

        self.minTension = 1
        self.minFreq = 1
        self.minPhase = 0
        self.minPeriod = 1
        self.minDC = 1

        self.__window_qt_configuration__()

        # inicializo clases
        self.antiAlias = AntiAliasFilter()
        self.recovery = RecoveryFilter()
        self.sampleAndHold = SampleAndHold()
        self.analogSwitch = AnalogSwitch()
        self.data = Data()

        self.data.add_block(self.antiAlias, BlockOrder.AntiAlias.value)
        self.data.add_block(self.recovery, BlockOrder.Recovery.value)
        self.data.add_block(self.sampleAndHold, BlockOrder.SampleAndHold.value)
        self.data.add_block(self.analogSwitch, BlockOrder.AnalogSwitch.value)

    def __window_qt_configuration__(self):
        self.setWindowTitle("Sampling Tool")
        self.refreshSampleButton.clicked.connect(self.refresh_sample_clicked)
        self.pulseRadio.toggled.connect(self.pulse_radio_toggled)
        self.expRadio.toggled.connect(self.exp_radio_toggled)
        self.sineRadio.toggled.connect(self.sine_radio_toggled)
        self.halfSineRadio.toggled.connect(self.half_sine_radio_toggled)
        self.amRadio.toggled.connect(self.am_radio_toggled)
        self.refreshXinButton.clicked.connect(self.refresh_xin_clicked)
        self.analogPlotButton.clicked.connect(self.analog_plot_clicked)
        self.antiAliasPlotButton.clicked.connect(self.anti_alias_plot_clicked)
        self.sampleHoldPlotButton.clicked.connect(self.sample_hold_plot_clicked)
        self.xinPlotButton.clicked.connect(self.xin_plot_clicked)
        self.xoutPlotButton.clicked.connect(self.xout_plot_clicked)
        self.antiAliasCheck.clicked.connect(self.anti_alias_check_clicked)
        self.sampleholdCheck.clicked.connect(self.sample_hold_check_clicked)
        self.recupCheck.clicked.connect(self.recup_check_clicked)
        self.analogCheck.clicked.connect(self.analog_check_clicked)

        self.frequencyMultipliers = {"Hz": 1,
                                     "kHz": 1000,
                                     "MHz": 1000000,
                                     }
        self.tensionMultipliers = {"mV": 1 / 1000,
                                   "V": 1}
        self.phaseMultipliers = {"°": 1}
        self.periodMultipliers = {"ns": 1 / 1000000000,
                                  "us": 1 / 1000000,
                                  "ms": 1 / 1000,
                                  "s": 1}

        self.periodValue.setMinimum(self.minPeriod)
        self.dcValue.setMinimum(self.minDC)
        self.periodValue.setValue(self.minPeriod)
        self.dcValue.setValue(self.minDC)
        self.param2Value.setMinimum(self.minFreq)
        self.param2Value.setValue(self.minFreq)
        self.param1Value.setMinimum(self.minTension)
        self.param1Value.setValue(self.minTension)
        self.param3Value.setMinimum(self.minPhase)
        self.param3Value.setValue(self.minPhase)
        self.periodUnit.clear()

        for unit in self.periodMultipliers:
            self.periodUnit.addItem(unit)

    def pulse_radio_toggled(self):
        self.sineRadio.setChecked(False)
        self.expRadio.setChecked(False)
        self.halfSineRadio.setChecked(False)
        self.amRadio.setChecked(False)
        self.halfSineRadio.setVisible(False)
        self.amRadio.setVisible(False)

        self.xinFunction.setText("Xin = δ(t)")

        self.__disable_param_box__(1)
        self.__disable_param_box__(2)
        self.__disable_param_box__(3)

    def exp_radio_toggled(self):
        self.sineRadio.setChecked(False)
        self.pulseRadio.setChecked(False)
        self.halfSineRadio.setChecked(False)
        self.amRadio.setChecked(False)
        self.halfSineRadio.setVisible(False)
        self.amRadio.setVisible(False)


        self.xinFunction.setText("Xin = Vmax*e^(-|t|), período T.")

        self.__enable_param_box__(1)
        self.__enable_param_box__(2)
        self.__disable_param_box__(3)

        self.param1Title.setText("Vmax")
        self.param1Value.setMinimum(self.minTension)
        self.param1Value.setValue(self.minTension)
        self.param1Unit.clear()
        for unit in self.tensionMultipliers.keys():
            self.param1Unit.addItem(unit)

        self.param2Title.setText("T")
        self.param2Value.setMinimum(self.minPeriod)
        self.param2Value.setValue(self.minPeriod)
        self.param2Unit.clear()
        for unit in self.periodMultipliers.keys():
            self.param2Unit.addItem(unit)

    def sine_radio_toggled(self):
        self.pulseRadio.setChecked(False)
        self.expRadio.setChecked(False)
        self.halfSineRadio.setChecked(False)
        self.amRadio.setChecked(False)
        self.halfSineRadio.setVisible(True)
        self.amRadio.setVisible(True)
        
        self.xinFunction.setText("Xin = Vp*cos(2π*f*t+θ)")
        self.__enable_param_box__(1)
        self.__enable_param_box__(2)
        self.__enable_param_box__(3)

        self.param1Title.setText("Vp")
        self.param1Value.setMinimum(self.minTension)
        self.param1Value.setValue(self.minTension)
        self.param1Unit.clear()
        for unit in self.tensionMultipliers.keys():
            self.param1Unit.addItem(unit)

        self.param2Title.setText("f")
        self.param2Value.setMinimum(self.minFreq)
        self.param2Value.setValue(self.minFreq)
        self.param2Unit.clear()
        for unit in self.frequencyMultipliers.keys():
            self.param2Unit.addItem(unit)

        self.param3Title.setText("θ")
        self.param3Value.setMinimum(self.minPhase)
        self.param3Value.setValue(self.minPhase)
        self.param3Unit.clear()
        for unit in self.phaseMultipliers.keys():
            self.param3Unit.addItem(unit)

    def half_sine_radio_toggled(self):
        self.pulseRadio.setChecked(False)
        self.expRadio.setChecked(False)
        self.sineRadio.setChecked(False)
        self.amRadio.setChecked(False)
        
        self.xinFunction.setText("Xin = Vp*sin(2π*f*t+θ), período: 3/(2*f)")
        self.__enable_param_box__(1)
        self.__enable_param_box__(2)
        self.__enable_param_box__(3)

        self.param1Title.setText("Vp")
        self.param1Value.setMinimum(self.minTension)
        self.param1Value.setValue(self.minTension)
        self.param1Unit.clear()
        for unit in self.tensionMultipliers.keys():
            self.param1Unit.addItem(unit)

        self.param2Title.setText("f")
        self.param2Value.setMinimum(self.minFreq)
        self.param2Value.setValue(self.minFreq)
        self.param2Unit.clear()
        for unit in self.frequencyMultipliers.keys():
            self.param2Unit.addItem(unit)

        self.param3Title.setText("θ")
        self.param3Value.setMinimum(self.minPhase)
        self.param3Value.setValue(self.minPhase)
        self.param3Unit.clear()
        for unit in self.phaseMultipliers.keys():
            self.param3Unit.addItem(unit)

    def am_radio_toggled(self):
        self.pulseRadio.setChecked(False)
        self.expRadio.setChecked(False)
        self.sineRadio.setChecked(False)
        self.halfSineRadio.setChecked(False)
        
        self.xinFunction.setText("Xin = Vp*(1/2*cos(2π*1,8*f*t+θ) + cos(2π*2*f*t+θ) + 1/2*cos(2π*2,2*f*t+θ))")
        self.__enable_param_box__(1)
        self.__enable_param_box__(2)
        self.__enable_param_box__(3)

        self.param1Title.setText("Vp")
        self.param1Value.setMinimum(self.minTension)
        self.param1Value.setValue(self.minTension)
        self.param1Unit.clear()
        for unit in self.tensionMultipliers.keys():
            self.param1Unit.addItem(unit)

        self.param2Title.setText("f")
        self.param2Value.setMinimum(self.minFreq)
        self.param2Value.setValue(self.minFreq)
        self.param2Unit.clear()
        for unit in self.frequencyMultipliers.keys():
            self.param2Unit.addItem(unit)

        self.param3Title.setText("θ")
        self.param3Value.setMinimum(self.minPhase)
        self.param3Value.setValue(self.minPhase)
        self.param3Unit.clear()
        for unit in self.phaseMultipliers.keys():
            self.param3Unit.addItem(unit)

    def __disable_param_box__(self, nr_of_param):
        if nr_of_param == 3:
            self.param3Title.setVisible(False)
            self.param3Unit.setVisible(False)
            self.param3Value.setVisible(False)
        elif nr_of_param == 2:
            self.param2Title.setVisible(False)
            self.param2Unit.setVisible(False)
            self.param2Value.setVisible(False)
        elif nr_of_param == 1:
            self.param1Title.setVisible(False)
            self.param1Unit.setVisible(False)
            self.param1Value.setVisible(False)

    def __enable_param_box__(self, nr_of_param):
        if nr_of_param == 3:
            self.param3Title.setVisible(True)
            self.param3Unit.setVisible(True)
            self.param3Value.setVisible(True)
        elif nr_of_param == 2:
            self.param2Title.setVisible(True)
            self.param2Unit.setVisible(True)
            self.param2Value.setVisible(True)
        elif nr_of_param == 1:
            self.param1Title.setVisible(True)
            self.param1Unit.setVisible(True)
            self.param1Value.setVisible(True)

    def refresh_sample_clicked(self):
        self.errorLabel.setText('')

        error = not self.data.xin_exists()
        if error:
            self.errorLabel.setText("Primero ingresa una señal de entrada")
        else:
            self.data.sampling_signal_changed(self.dcValue.value(),
                                              self.periodValue.value() * self.periodMultipliers[
                                                  self.periodUnit.currentText()])

    def refresh_xin_clicked(self):
        self.errorLabel.setText('')
        if self.pulseRadio.isChecked():
            time_array = np.linspace(0, 1, 1/Signal.timeTick)
            xin_signal = Signal(time_array)
            xin_signal.create_dirac_signal()
            xin_signal.add_description("Input: Impulso.")

            self.data.xin_changed(xin_signal)

        elif self.sineRadio.isChecked():
            freq = self.param2Value.value()
            freq_mult_text = self.param2Unit.currentText()
            freq_mult_value = self.frequencyMultipliers[freq_mult_text]
            total_freq = freq * freq_mult_value

            amplitude = self.param1Value.value()
            amplitude_mult_text = self.param1Unit.currentText()
            amplitude_mult_value = self.tensionMultipliers[amplitude_mult_text]

            phase = self.param3Value.value()
            phase_mult_text = self.param3Unit.currentText()
            phase_mult_value = self.phaseMultipliers[phase_mult_text]

            time_array = np.linspace(0, Signal.showingPeriods  / total_freq,  Signal.showingPeriods/Signal.timeTick )
            xin_signal = Signal(time_array)

            xin_signal.create_cos_signal(total_freq, amplitude * amplitude_mult_value,
                                        phase=phase * phase_mult_value)
            xin_signal.add_description(
                "Input: " + str(amplitude) + amplitude_mult_text + "*cos(2π*" + str(freq) + freq_mult_text + " + " + str(
                    phase) + phase_mult_text + ")")

            self.data.xin_changed(xin_signal)

        elif self.halfSineRadio.isChecked():
            freq = self.param2Value.value()
            freq_mult_text = self.param2Unit.currentText()
            freq_mult_value = self.frequencyMultipliers[freq_mult_text]
            total_freq = freq * freq_mult_value

            amplitude = self.param1Value.value()
            amplitude_mult_text = self.param1Unit.currentText()
            amplitude_mult_value = self.tensionMultipliers[amplitude_mult_text]

            phase = self.param3Value.value()
            phase_mult_text = self.param3Unit.currentText()
            phase_mult_value = self.phaseMultipliers[phase_mult_text]

            time_array = np.linspace(0, (Signal.showingPeriods * 3/2) / total_freq, Signal.showingPeriods/Signal.timeTick )
            xin_signal = Signal(time_array)

            xin_signal.create_half_sine_signal(total_freq, amplitude * amplitude_mult_value, 
                                              phase=phase * phase_mult_value)
            xin_signal.add_description("Input: " + str(amplitude) + amplitude_mult_text + "*sin(2π*" + str(freq) + freq_mult_text + " + " + str(
                                       phase) + phase_mult_text + " ), período: " + str( (3 / 2) * (1 / total_freq) ) + "s")

            self.data.xin_changed(xin_signal)

        elif self.amRadio.isChecked():
            freq = self.param2Value.value()
            freq_mult_text = self.param2Unit.currentText()
            freq_mult_value = self.frequencyMultipliers[freq_mult_text]
            total_freq = freq * freq_mult_value

            amplitude = self.param1Value.value()
            amplitude_mult_text = self.param1Unit.currentText()
            amplitude_mult_value = self.tensionMultipliers[amplitude_mult_text]

            phase = self.param3Value.value()
            phase_mult_text = self.param3Unit.currentText()
            phase_mult_value = self.phaseMultipliers[phase_mult_text]

            time_array = np.linspace(0, Signal.showingPeriods  * 5 / total_freq, Signal.showingPeriods/Signal.timeTick )
            xin_signal = Signal(time_array)
            
            xin_signal.create_am_signal(total_freq, amplitude * amplitude_mult_value, 
                                              phase=phase * phase_mult_value)
            xin_signal.add_description("Input: Señal AM")                                  
            '''xin_signal.add_description("Input: " + str(amplitude) + amplitude_mult_text + "*(1/2*cos(2π*1,8*" + str(freq) + freq_mult_text + "*t + " + str(
                                       phase) + phase_mult_text + ") + cos(2π*2*" + str(freq) + freq_mult_text + "*t + " + str(
                                       phase) + phase_mult_text + ") + 1/2*cos(2π*2,2*" + str(freq) + freq_mult_text + "*t + " + str(
                                       phase) + phase_mult_text + ")), período: " + str((5 / total_freq)) + "s")'''

            self.data.xin_changed(xin_signal)

        elif self.expRadio.isChecked():
            vmax_v = self.param1Value.value()
            vmax_unit_text = self.param1Unit.currentText()
            vmax_unit_value = self.tensionMultipliers[vmax_unit_text]

            period_value = self.param2Value.value()
            period_mult_text = self.param2Unit.currentText()
            period_mult_value = self.periodMultipliers[period_mult_text]
            total_period = period_value * period_mult_value

            time_array = np.linspace(0, Signal.showingPeriods * total_period,Signal.showingPeriods/Signal.timeTick)
            xin_signal = Signal(time_array)

            xin_signal.create_exp_signal(vmax_v * vmax_unit_value, total_period)

            xin_signal.add_description(
                "Input: " + str(vmax_v) + vmax_unit_text + "*e^(-|t|), período: " + str(
                    period_value) + period_mult_text)

            self.data.xin_changed(xin_signal)

    def xin_plot_clicked(self):
        if self.__check_input_exists__():
            to_plot_signal = self.data.get_signal(SignalOrder.Xin.value)
            self.oscilloscope.add_signal_to_oscilloscope(to_plot_signal)

    def anti_alias_plot_clicked(self):
        if self.__check_input_exists__():
            to_plot_signal = self.data.get_signal(SignalOrder.AntiAliasOut.value)

            aux_signal_description = to_plot_signal.description
            aux_signal_description = "AntiAlias OUT. " + aux_signal_description
            to_plot_signal.add_description(aux_signal_description)

            self.oscilloscope.add_signal_to_oscilloscope(to_plot_signal)

    def sample_hold_plot_clicked(self):
        if self.__check_input_exists__() and self.__check_sample_signal_exists__():
            to_plot_signal = self.data.get_signal(SignalOrder.SampleAndHoldOut.value)

            aux_signal_description = to_plot_signal.description
            aux_signal_description = "Sample & Hold OUT. " + aux_signal_description
            to_plot_signal.add_description(aux_signal_description)

            self.oscilloscope.add_signal_to_oscilloscope(to_plot_signal)

    def __check_input_exists__(self):
        error = True
        if self.data.xin_exists():
            error = False
            self.errorLabel.setText('')
        else:
            self.errorLabel.setText('No input signal')

        return not error

    def __check_sample_signal_exists__(self):
        error = True
        if self.data.sampling_exists():
            error = False
            self.errorLabel.setText('')
        else:
            self.errorLabel.setText('No sampling signal')

        return not error

    def analog_plot_clicked(self):
        if self.__check_input_exists__() and self.__check_sample_signal_exists__():
            to_plot_signal = self.data.get_signal(SignalOrder.AnalogSwitchOut.value)

            aux_signal_description = to_plot_signal.description
            aux_signal_description = "Analog Switch OUT. " + aux_signal_description
            to_plot_signal.add_description(aux_signal_description)

            self.oscilloscope.add_signal_to_oscilloscope(to_plot_signal)

    def xout_plot_clicked(self):
        if self.__check_input_exists__() and self.__check_sample_signal_exists__():
            to_plot_signal = self.data.get_signal(SignalOrder.XOut.value)

            aux_signal_description = to_plot_signal.description
            aux_signal_description = "Xout. " + aux_signal_description
            to_plot_signal.add_description(aux_signal_description)

            self.oscilloscope.add_signal_to_oscilloscope(to_plot_signal)

    def anti_alias_check_clicked(self):
        if self.antiAliasCheck.isChecked():
            self.antiAlias.deactivate_block(False)
        else:
            self.antiAlias.deactivate_block(True)
        self.data.block_property_changed(BlockOrder.AntiAlias.value)

    def sample_hold_check_clicked(self):
        if self.sampleholdCheck.isChecked():
            self.sampleAndHold.deactivate_block(False)
        else:
            self.sampleAndHold.deactivate_block(True)
        self.data.block_property_changed(BlockOrder.SampleAndHold.value)

    def analog_check_clicked(self):
        if self.analogCheck.isChecked():
            self.analogSwitch.deactivate_block(False)
        else:
            self.analogSwitch.deactivate_block(True)
        self.data.block_property_changed(BlockOrder.AnalogSwitch.value)

    def recup_check_clicked(self):
        if self.recupCheck.isChecked():
            self.recovery.deactivate_block(False)
        else:
            self.recovery.deactivate_block(True)
        self.data.block_property_changed(BlockOrder.Recovery.value)
