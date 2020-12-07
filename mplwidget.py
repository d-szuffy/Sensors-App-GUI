# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.fig = Figure()
        # self.fig.set_facecolor('none')
        self.canvas = FigureCanvasQTAgg(self.fig)
        # self.setStyleSheet('background-color: rgb(34, 34, 34);')

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
