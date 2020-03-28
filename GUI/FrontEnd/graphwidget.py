# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure


class GraphWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.x_label = "X"
        self.y_label = "Y"
        self.title = " "
        self.figure = Figure()
        self.figure.patch.set_facecolor((53 / 255, 73 / 255, 80 / 255, 1))
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)  # Toolbar to work on the graphs
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        vertical_layout.addWidget(self.toolbar)  # Adding toolbar to the widget

        self.canvas.axes = self.canvas.figure.add_subplot(111)

        self.canvas.axes.tick_params(direction='out', labelsize=8, colors='w')
        self.setLayout(vertical_layout)
        self.figure.tight_layout()
