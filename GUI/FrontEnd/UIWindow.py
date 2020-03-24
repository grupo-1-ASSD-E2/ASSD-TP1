from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


# Clase UIWindow. Maneja lo relacionado con la ventana mostrada al usuario.


class UIWindow(QMainWindow):

    def __init__(self):  # Conecta los componentes del .ui realizado en QT con el programa en python
        QMainWindow.__init__(self)
        self.program_state = {}
        loadUi('samplingui.ui', self)

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

        self.minTension = 1
        self.minFreq = 1
        self.minPhase = 0
        self.minPeriod = 1
        self.minDC = 1

        self.periodValue.setMinimum(self.minPeriod)
        self.dcValue.setMinimum(self.minDC)
        self.periodValue.setValue(self.minPeriod)
        self.dcValue.setValue(self.minDC)

        self.periodUnit.clear()

        for unit in self.periodMultipliers:
            self.periodUnit.addItem(unit)

    def pulse_radio_toggled(self):
        if self.pulseRadio.isChecked():
            self.pulseRadio.setChecked(True)
        self.sineRadio.setChecked(False)
        self.expRadio.setChecked(False)

        self.xinFunction.setText("Xin = δ(t)")

        self.__disable_param_box__(1)
        self.__disable_param_box__(2)
        self.__disable_param_box__(3)

    def exp_radio_toggled(self):
        if self.expRadio.isChecked():
            self.expRadio.setChecked(True)
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
        if self.sineRadio.isChecked():
            self.sineRadio.setChecked(True)
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
        i = 0

    def refresh_xin_clicked(self):
        a = 0

    def analog_plot_clicked(self):
        i = 0

    def sample_hold_plot_clicked(self):
        u = 0

    def anti_alias_plot_clicked(self):
        a = 0

    def xout_plot_clicked(self):
        i = 0

    def xin_plot_clicked(self):
        a=0
