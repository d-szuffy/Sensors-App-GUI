import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer
from concept_main_window import *
import json
# from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import pandas
import numpy as np
WINDOW_SIZE = 0
print('everything is working fine')


MENU_BUTTON_ICONS_CENTER_LEFT = [
    'background-image: url(:/icons/icons/cil-rss.png);'
    'background-repeat: none;'
    'background-position: center left;',
    'background-image: url(:/icons/icons/cil-screen-desktop.png);'
    'background-repeat: none;'
    'background-position: center left;',
    'background-image: url(:/icons/icons/cil-settings.png);'
    'background-repeat: none;'
    'background-position: center left;'
]
MENU_BUTTON_ICONS_CENTER = [
    'background-image: url(:/icons/icons/cil-rss.png);'
    'background-repeat: none;'
    'background-position: center;',
    'background-image: url(:/icons/icons/cil-screen-desktop.png);'
    'background-repeat: none;'
    'background-position: center;',
    'background-image: url(:/icons/icons/cil-settings.png);'
    'background-repeat: none;'
    'background-position: center;'
]

MENU_BUTTONS_TEXT = [
    'SENSORS',
    'REPORTS',
    'SETTINGS'
]

SENSORS_TYPE = [
    'temp',
    'humidity',
    'co2',
    'timeout',
    'temp',
    'humidity',
    'co2',
    'timeout',
    'temp',
    'humidity',
    'co2',
    'timeout',
    'temp',
    'humidity',
    'co2',
    'timeout',
]

SENSORS_INDEX = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]


class MyForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.qTimer = QTimer()
        self.ui.qTimer.setInterval(5000)
        self.ui.qTimer.timeout.connect(self.getSensorsValue)
        self.ui.qTimer.start()

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
        self.ui.reports_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.accounts_page))
        self.ui.settings_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page))
        self.ui.sensor1_next_btn.clicked.connect(lambda: self.nextPage())
        self.ui.sensor2_prev_btn.clicked.connect(lambda: self.prevPage())
        self.ui.sensor2_next_btn.clicked.connect(lambda: self.nextPage())
        self.ui.sensor3_prev_btn.clicked.connect(lambda: self.prevPage())
        self.ui.sensor3_next_btn.clicked.connect(lambda: self.nextPage())
        self.ui.sensor4_prev_btn.clicked.connect(lambda: self.prevPage())

        global MPLWIDGETS_NAMES

        MPLWIDGETS_NAMES = [
            self.ui.sensor1_MplWidget,
            self.ui.sensor2_MplWidget,
            self.ui.sensor3_MplWidget,
            self.ui.sensor4_MplWidget,
        ]


        global MENU_BUTTONS
        MENU_BUTTONS = [
            self.ui.sensors_button,
            self.ui.reports_button,
            self.ui.settings_button
        ]
        global SENSORS
        SENSORS = [
            self.ui.sensor1_temp_value,
            self.ui.sensor1_humidity_value,
            self.ui.sensor1_co2_value,
            self.ui.sensor1_status_value,
            self.ui.sensor2_temp_value,
            self.ui.sensor2_humidity_value,
            self.ui.sensor2_co2_value,
            self.ui.sensor2_status_value,
            self.ui.sensor3_temp_value,
            self.ui.sensor3_humidity_value,
            self.ui.sensor3_co2_value,
            self.ui.sensor3_status_value,
            self.ui.sensor4_temp_value,
            self.ui.sensor4_humidity_value,
            self.ui.sensor4_co2_value,
            self.ui.sensor4_status_value
        ]
        # self.ui.sensor1_temp_value.setText(whole_info['sensor1_temp'])

        self.ui.sensor1_temp_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor1_temp_trend_btn))
        self.ui.sensor1_humidity_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor1_humidity_trend_btn))
        self.ui.sensor1_co2_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor1_co2_trend_btn))
        self.ui.sensor2_temp_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor2_temp_trend_btn))
        self.ui.sensor2_humidity_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor2_humidity_trend_btn))
        self.ui.sensor2_co2_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor2_co2_trend_btn))
        self.ui.sensor3_temp_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor3_temp_trend_btn))
        self.ui.sensor3_humidity_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor3_humidity_trend_btn))
        self.ui.sensor3_co2_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor3_co2_trend_btn))
        self.ui.sensor4_temp_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor4_temp_trend_btn))
        self.ui.sensor4_humidity_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor4_humidity_trend_btn))
        self.ui.sensor4_co2_trend_btn.clicked.connect(lambda: self.updateGraph(self.ui.sensor4_co2_trend_btn))

        # self.addToolBar(NavigationToolbar(self.ui.MplWidget.canvas, self.ui.MplWidget))

        # self.addToolBar(NavigationToolbar(self.ui.MplWidget.canvas, self.ui.MplWidget))

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

        check = self.ui.sensor1_co2_trend_btn.objectName()
        print(check)
        check2 = check.replace('sensor1_', '')
        check2 = check2.replace('_trend_btn', '')
        print(type(check2))
        print(check2)

    def updateGraph(self, button: Ui_MainWindow()):
        y = []
        data = pandas.read_csv('new_data.csv')
        name = button.objectName()
        i = int(name[6]) - 1
        part_to_replace = 'sensor' + str(i+1) + '_'
        new_name = name.replace(part_to_replace, '')
        new_name = new_name.replace('_trend_btn', '')
        for value in data[new_name]:
            y.append(json.loads(value)[i])

        x = np.linspace(0, len(y), len(y))
        print(True)
        for widget in MPLWIDGETS_NAMES:
            widget_name = widget.objectName()
            if widget_name[6] == str(i + 1):
                print(True)
                widget.canvas.axes.clear()
                widget.canvas.axes.set_ylim([0, 50])
                widget.canvas.axes.plot(x, y)
                widget.canvas.axes.set_title('Sensor ' + str(i+1) + ' - ' + new_name + ' readings')
                widget.canvas.draw()


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

    def getSensorsValue(self):

        data = pandas.read_csv('new_data.csv')
        data_last_row = data.iloc[-1]
        for sensor, sensor_type, i in zip(SENSORS, SENSORS_TYPE, SENSORS_INDEX):
            sensors_value = str(round(json.loads(data_last_row[sensor_type])[i], 2))
            sensor.setText(sensors_value)

    def nextPage(self):

        i = self.ui.sensors_stacked_widget.currentIndex()
        self.ui.sensors_stacked_widget.setCurrentIndex(i + 1)

    def prevPage(self):

        i = self.ui.sensors_stacked_widget.currentIndex()
        self.ui.sensors_stacked_widget.setCurrentIndex(i - 1)



    def slideLeftMenu(self):

        width = self.ui.left_side_menu.width()
        for button, text, icon1, icon2 in zip(MENU_BUTTONS, MENU_BUTTONS_TEXT, MENU_BUTTON_ICONS_CENTER_LEFT, MENU_BUTTON_ICONS_CENTER):

            if width == 50:
                newwidth = 150
                button.setMinimumWidth(150)
                button.setText(text)
                button.setStyleSheet(icon1)
            else:
                newwidth = 50
                button.setMinimumWidth(50)
                button.setText('')
                button.setStyleSheet(icon2)

        self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newwidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(App.exec())
