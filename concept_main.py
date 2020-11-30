import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation
from concept_main_window import *


WINDOW_SIZE = 0


class MyForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Button click events to our top bar buttons

        # Minimize window
        self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized())
        # Close window
        self.ui.closeButton.clicked.connect(lambda: self.close())
        # Restore/Maximize window
        self.ui.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())

        self.ui.stackedWidget.setCurrentWidget(self.ui.sensors_page)
        self.ui.sensors_stacked_widget.setCurrentIndex(0)
        self.ui.sensors_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sensors_page))
        self.ui.accounts_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.accounts_page))
        self.ui.settings_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page))
        self.ui.sensor1_next_btn.clicked.connect(lambda: self.nextPage())
        self.ui.sensor2_prev_btn.clicked.connect(lambda: self.prevPage())
        self.ui.sensor2_next_btn.clicked.connect(lambda: self.nextPage())
        self.ui.sensor3_prev_btn.clicked.connect(lambda: self.prevPage())
        self.ui.sensor3_next_btn.clicked.connect(lambda: self.nextPage())
        self.ui.sensor4_prev_btn.clicked.connect(lambda: self.prevPage())


#        self.ui.pushButton_generate_random_signal.clicked.connect(lambda: self.updateGraph())

#        self.addToolBar(NavigationToolbar(self.ui.MplWidget.canvas, self.ui.MplWidget))

    # Restore or maximize your window

        def moveWindow(e):

            # Detect if the window is  normal size
            # ###############################################
            if not self.isMaximized():  # Not maximized
                # Move window only when window is normal size
                # ###############################################
                # if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:
                    # Move window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
            # ###############################################

        self.ui.main_header.mouseMoveEvent = moveWindow

        self.ui.pushButton.clicked.connect(lambda: self.slideLeftMenu())
        self.show()


#    def updateGraph(self):
#
#        data = pandas.read_csv('data.csv')
#        x = data['x_val']
#        y = data['y_val']
#        self.ui.MplWidget.canvas.axes.clear()
#        self.ui.MplWidget.canvas.axes.plot(y)
#        self.ui.MplWidget.canvas.axes.set_title('Sensor 1 - temperature readings')
#        self.ui.MplWidget.canvas.draw()

    def mousePressEvent(self, event):

        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to move the window
        # ###############################################

    # ###############################################

    def restore_or_maximize_window(self):

        # Global windows state
        global WINDOW_SIZE
        # The default value is zero to show that the size is not maximized
        win_status = WINDOW_SIZE

        if win_status == 0:
            # If the window is not maximized
        	WINDOW_SIZE = 1
            # Update value to show that the window has been maximized
        	self.showMaximized()
            # Update button icon
            # self.ui.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-maximize.png"))#Show maximized icon
        else:
            # If the window is on its default size
            WINDOW_SIZE = 0
            # Update value to show that the window has been minimized/set to normal size (which is 800 by 400)
            self.showNormal()
            # Update button icon
            # self.ui.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-restore.png"))#Show minized icon

    def nextPage(self):

        i = self.ui.sensors_stacked_widget.currentIndex()
        self.ui.sensors_stacked_widget.setCurrentIndex(i + 1)

    def prevPage(self):

        i = self.ui.sensors_stacked_widget.currentIndex()
        self.ui.sensors_stacked_widget.setCurrentIndex(i - 1)

    def slideLeftMenu(self):

        width = self.ui.left_side_menu.width()

        if width == 50:
            newwidth = 150
        else:
            newwidth = 50

        self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")
        self.animation.setDuration(150)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newwidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(App.exec())
