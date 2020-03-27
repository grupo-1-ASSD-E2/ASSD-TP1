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

'''For ploting: def plot_signal(self):
        if self.blockActivated:
            plt.plot(self.timeOut, self.signalOut)
            plt.title('Out')
            plt.xlabel('Time')
            plt.ylabel('V')
            plt.margins(0, 0.1)
            plt.grid(which='both', axis='both')
            plt.show()
        else:
            plt.plot(self.timeArray, self.cos)
            plt.title('cos')
            plt.xlabel('Time')
            plt.ylabel('V')
            plt.margins(0, 0.1)
            plt.grid(which='both', axis='both')
            plt.show()'''


# Clase UIWindow. Maneja lo relacionado con la ventana mostrada al usuario.
class UIWindow(QMainWindow):

    def __init__(self):  # Conecta los componentes del .ui realizado en QT con el programa en python
        QMainWindow.__init__(self)
        self.spectrumAnalyzer = SpectrumAnalyzer()
        self.oscilloscope = Oscilloscope()
        self.program_state = {}
        loadUi('GUI/FrontEnd/samplingui.ui', self)

        self.minTension = 1
        self.minFreq = 1
        self.minPhase = 0
        self.minPeriod = 1
        self.minDC = 1

        self.__window_qt_configuration__()

        self.timeArray = np.arange(-10, 10, 0.0001)
        self.xinSignal = Signal(self.timeArray)
		self.auxSignal = self.xinSignal
        self.samplingSignal = Signal(self.timeArray)

        # inicializo clases
        self.antiAlias = AntiAliasFilter()
        self.recovery = RecoveryFilter()
        self.sampleAndHold = SampleAndHold()
        self.analogSwitch = AnalogSwitch()



    def __window_qt_configuration__(self):
        self.setWindowTitle("Sampling Tool")
        self.refreshSampleButton.clicked.connect(self.refresh_sample_clicked)
        self.pulseRadio.toggled.connect(self.pulse_radio_toggled)
        self.expRadio.toggled.connect(self.exp_radio_toggled)
        self.sineRadio.toggled.connect(self.sine_radio_toggled)
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
                                     "GHz": 1000000000}
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

        self.periodUnit.clear()

        for unit in self.periodMultipliers:
            self.periodUnit.addItem(unit)

    def pulse_radio_toggled(self):
        self.sineRadio.setChecked(False)
        self.expRadio.setChecked(False)

        self.xinFunction.setText("Xin = δ(t)")

        self.__disable_param_box__(1)
        self.__disable_param_box__(2)
        self.__disable_param_box__(3)

    def exp_radio_toggled(self):
        self.sineRadio.setChecked(False)
        self.pulseRadio.setChecked(False)

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
        self.samplingSignal = Signal(SignalTypes.SQUARE, period=self.periodValue.value() * self.periodMultipliers[
            self.periodValue.currentText()],
                                     duty_cycle=self.dcValue.value())

    def refresh_xin_clicked(self):
        self.xinSignal = None
        if self.pulseRadio.isChecked():
            
            self.xinSignal = Signal(signal_type)
            self.xinSignal.add_description("Input: Pulse.")
        elif self.sineRadio.isChecked():
            freq = self.param2Value.value()
            freqMultText = self.param2Unit.currentText()
            freqMultValue = self.frequencyMultipliers[freqMultText]

            amplitude = self.param1Value.value()
            amplitudeMultText = self.param1Unit.currentText()
            amplitudeMultValue = self.tensionMultipliers[amplitudeMultText]

            phase = self.param3Value.value()
            phaseMultText = self.param3Unit.currentText()
            phaseMultValue = self.phaseMultipliers[phaseMultText]
            self.xinSignal.create_cos_signal(freq * freqMultValue, amplitude * amplitudeMultValue, phase=phase * phaseMultValue)
            self.xinSignal.add_description("Input: " + str(amplitude) + amplitudeMultText + "*cos(2π*" +str(freq) + freqMultText + " +" + str(phase) + phaseMultText +")") )

        elif self.expRadio.isChecked():
            signal_type = SignalTypes.EXPONENTIAL
            vmaxV = self.param1Value.value()
            vmaxUnitText = self.param1Unit.currentText()
            vmaxUnitValue = self.tensionMultipliers[vmaxUnitText]

            periodValue = self.param2Value.value()
            periodMultText = self.param2Unit.currentText()
            periodMultValue = self.periodMultipliers[periodMultText]
            self.signal = Signal(signal_type, v_max=vmaxV * vmaxUnitValue,
                                 period=periodValue * periodMultValue )
            self.xinSignal.add_description("Input: " + str(vmaxV) + vmaxUnitText + "*e^(-|t|), período: " + str(periodValue) + periodMultText )
		self.auxSignal = self.xinSignal


	def xin_plot_clicked(self):
		self.oscilloscope.add_signal_to_oscilloscope(self.xinSignal)

	def anti_alias_plot_clicked(self):
		self.auxSignal = self.xinSignal
        self.antiAlias.apply_to_signal(self.auxSignal)
		

        aux_signal_description = self.auxSignal.description
        aux_signal_description = "AntiAlias OUT. " + aux_signal_description
        self.auxSignal.set_description(aux_signal_description)

        self.oscilloscope.add_signal_to_oscilloscope(self.auxSignal)

	def sample_hold_plot_clicked(self):
		self.auxSignal = self.xinSignal
		self.antiAlias.apply_to_signal(self.auxSignal)
		self.sampleAndHold.apply_to_signal(self.auxSignal)

        aux_signal_description = self.auxSignal.description
        aux_signal_description = "Sample & Hold OUT. " + aux_signal_description
        self.auxSignal.set_description(aux_signal_description)

        self.oscilloscope.add_signal_to_oscilloscope(self.auxSignal)

    def analog_plot_clicked(self):
		self.auxSignal = self.xinSignal
		self.antiAlias.apply_to_signal(self.auxSignal)
		self.sampleAndHold.apply_to_signal(self.auxSignal)
		self.analogSwitch.apply_to_signal(self.auxSignal)

        aux_signal_description = self.auxSignal.description
        aux_signal_description = "Analog Switch OUT. " + aux_signal_description
        self.auxSignal.set_description(aux_signal_description)

        self.oscilloscope.add_signal_to_oscilloscope(self.auxSignal)

	def xout_plot_clicked(self):
		self.auxSignal = self.xinSignal
        self.antiAlias.apply_to_signal(self.auxSignal)
		self.sampleAndHold.apply_to_signal(self.auxSignal)
		self.analogSwitch.apply_to_signal(self.auxSignal)
		self.recovery.apply_to_signal(self.auxSignal)

        aux_signal_description = self.auxSignal.description
        aux_signal_description = "Xout Signal. " + aux_signal_description
        self.auxSignal.set_description(aux_signal_description)

		self.oscilloscope.add_signal_to_oscilloscope(self.auxSignal)


    def anti_alias_check_clicked(self):
        if self.antiAliasCheck.isChecked():
            self.antiAlias.deactivate_block(False)
        else:
            self.antiAlias.deactivate_block(True)

    def sample_hold_check_clicked(self):
        if self.sampleholdCheck.isChecked():
            self.sampleHold.deactivate_block(False)
        else:
            self.sampleHold.deactivate_block(True)

	def analog_check_clicked(self):
		if self.analogCheck.isChecked():
			self.analog.deactivate_block(False)
		else:
			self.analog.deactivate_block(True)

    def recup_check_clicked(self):
        if self.recupCheck.isChecked():
            self.recovery.deactivate_block(False)
        else:
            self.recovery.deactivate_block(True)




    def testing_osc(self):
        self.xinSignal.create_cos_signal(10000,5)
        self.xinSignal.add_description("hola")
        self.oscilloscope.add_signal_to_oscilloscope(self.xinSignal)
        
