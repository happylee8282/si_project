from PyQt5 import QtCore, QtGui, QtWidgets
import time

class BluetoothConnectionThread(QtCore.QThread):
    finished = QtCore.pyqtSignal(bool)

    def __init__(self, serial_num, board_type):
        super().__init__()
        self.serial_num = serial_num
        self.board_type = board_type
        self.success = False

    def run(self):
        try:
            # 블루투스 연결 시뮬레이션
            if self.serial_num == "1234" and self.board_type == "Arduino":
                time.sleep(5)  # 블루투스 연결이 완료될 때까지 대기하는 시간 (예제)
                self.success = True
            else:
                raise Exception("Bluetooth connection failed")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", str(e))
            self.success = False
        self.finished.emit(self.success)

class LoadingDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading")
        self.setFixedSize(200, 100)
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Connecting...")
        layout.addWidget(self.label)
        self.setLayout(layout)

class Ui_ConnectionWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 80, 321, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(370, 230, 241, 37))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(20)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 220, 191, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(125, 364, 261, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(370, 377, 241, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(20)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(638, 378, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.connect_bluetooth)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Robot Control"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Arduino"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Raspberry Pi Pico"))
        self.label_2.setText(_translate("MainWindow", "Select Board:"))
        self.label_3.setText(_translate("MainWindow", "Bluetooth Num:"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        
    def connect_bluetooth(self):
        board_type = self.comboBox.currentText()
        serial_num = self.lineEdit.text()
        if not serial_num:
            QtWidgets.QMessageBox.warning(None, "Warning", "Please enter a serial number.")
            return
        
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.show()

        self.thread = BluetoothConnectionThread(serial_num, board_type)
        self.thread.finished.connect(self.loading_dialog.close)
        self.thread.finished.connect(lambda success: self.show_next_ui(success, board_type))
        self.thread.start()

    def show_next_ui(self, success, board_type):
        if success:
            self.centralwidget.deleteLater()
            ui = Ui_RC_Car_Control()
            ui.setupUi(MainWindow)
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Bluetooth connection failed.")

class Ui_RC_Car_Control(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title_ardu = QtWidgets.QLabel(self.centralwidget)
        self.title_ardu.setGeometry(QtCore.QRect(250, 80, 301, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(36)
        self.title_ardu.setFont(font)
        self.title_ardu.setObjectName("title_ardu")
        self.label_board_name = QtWidgets.QLabel(self.centralwidget)
        self.label_board_name.setGeometry(QtCore.QRect(260, 190, 121, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(24)
        self.label_board_name.setFont(font)
        self.label_board_name.setObjectName("label_board_name")
        self.label_connected = QtWidgets.QLabel(self.centralwidget)
        self.label_connected.setGeometry(QtCore.QRect(70, 190, 171, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(16)
        self.label_connected.setFont(font)
        self.label_connected.setObjectName("label_connected")
        self.label_robot_type = QtWidgets.QLabel(self.centralwidget)
        self.label_robot_type.setGeometry(QtCore.QRect(125, 250, 111, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(16)
        self.label_robot_type.setFont(font)
        self.label_robot_type.setObjectName("label_robot_type")
        self.label_robot = QtWidgets.QLabel(self.centralwidget)
        self.label_robot.setGeometry(QtCore.QRect(260, 250, 121, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(24)
        self.label_robot.setFont(font)
        self.label_robot.setObjectName("label_robot")
        self.label_control = QtWidgets.QLabel(self.centralwidget)
        self.label_control.setGeometry(QtCore.QRect(90, 415, 111, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(24)
        self.label_control.setFont(font)
        self.label_control.setObjectName("label_control")
        self.pushButton_forward = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_forward.setGeometry(QtCore.QRect(220, 430, 75, 23))
        self.pushButton_forward.setObjectName("pushButton_forward")
        self.pushButton_backward = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_backward.setGeometry(QtCore.QRect(310, 430, 75, 23))
        self.pushButton_backward.setObjectName("pushButton_backward")
        self.pushButton_counter_rotation = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_counter_rotation.setGeometry(QtCore.QRect(410, 430, 101, 23))
        self.pushButton_counter_rotation.setObjectName("pushButton_counter_rotation")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(650, 430, 75, 23))
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.lineEdit_speed = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_speed.setGeometry(QtCore.QRect(255, 320, 113, 31))
        self.lineEdit_speed.setObjectName("lineEdit_speed")
        self.label_speed = QtWidgets.QLabel(self.centralwidget)
        self.label_speed.setGeometry(QtCore.QRect(175, 310, 71, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(16)
        self.label_speed.setFont(font)
        self.label_speed.setObjectName("label_speed")
        self.pushButton_discounter_rotation = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_discounter_rotation.setGeometry(QtCore.QRect(520, 430, 111, 23))
        self.pushButton_discounter_rotation.setObjectName("pushButton_discounter_rotation")
        self.pushButton_disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_disconnect.setGeometry(QtCore.QRect(20, 20, 121, 41))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(16)
        self.pushButton_disconnect.setFont(font)
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_forward.clicked.connect(MainWindow.motor_forward) # type: ignore
        self.pushButton_backward.clicked.connect(MainWindow.motor_backward) # type: ignore
        self.pushButton_counter_rotation.clicked.connect(MainWindow.motor_clockwise_rotation) # type: ignore
        self.pushButton_discounter_rotation.clicked.connect(MainWindow.motor_counterclockwise_rotation) # type: ignore
        self.pushButton_stop.clicked.connect(MainWindow.motor_stop) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_ardu.setText(_translate("MainWindow", "Robot Control"))
        self.label_board_name.setText(_translate("MainWindow", "Arduino"))
        self.label_connected.setText(_translate("MainWindow", "Connected Board:"))
        self.label_robot_type.setText(_translate("MainWindow", "Robot Type:"))
        self.label_robot.setText(_translate("MainWindow", "RC Car"))
        self.label_control.setText(_translate("MainWindow", "Control"))
        self.pushButton_forward.setText(_translate("MainWindow", "전진"))
        self.pushButton_backward.setText(_translate("MainWindow", "후진"))
        self.pushButton_counter_rotation.setText(_translate("MainWindow", "회전(시계 방향)"))
        self.pushButton_stop.setText(_translate("MainWindow", "정지"))
        self.label_speed.setText(_translate("MainWindow", "Speed:"))
        self.pushButton_discounter_rotation.setText(_translate("MainWindow", "회전(반시계 방향)"))
        self.pushButton_disconnect.setText(_translate("MainWindow", "Disconnect"))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ConnectionWindow()
        self.ui.setupUi(self)

    def motor_forward(self):
        pass

    def motor_backward(self):
        pass

    def motor_clockwise_rotation(self):
        pass

    def motor_counterclockwise_rotation(self):
        pass

    def motor_stop(self):
        pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
