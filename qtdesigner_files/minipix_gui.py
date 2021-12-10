# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'minipix_gui__v2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1220, 822)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_1 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_1.sizePolicy().hasHeightForWidth())
        self.frame_1.setSizePolicy(sizePolicy)
        self.frame_1.setMinimumSize(QtCore.QSize(450, 500))
        self.frame_1.setMaximumSize(QtCore.QSize(450, 1000))
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.label_9 = QtWidgets.QLabel(self.frame_1)
        self.label_9.setGeometry(QtCore.QRect(10, 170, 101, 16))
        self.label_9.setObjectName("label_9")
        self.progressBar = QtWidgets.QProgressBar(self.frame_1)
        self.progressBar.setGeometry(QtCore.QRect(283, 180, 101, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButton_select_directory = QtWidgets.QPushButton(self.frame_1)
        self.pushButton_select_directory.setGeometry(QtCore.QRect(282, 130, 100, 28))
        self.pushButton_select_directory.setObjectName("pushButton_select_directory")
        self.label_temperature = QtWidgets.QLabel(self.frame_1)
        self.label_temperature.setGeometry(QtCore.QRect(10, 190, 101, 41))
        self.label_temperature.setWordWrap(True)
        self.label_temperature.setObjectName("label_temperature")
        self.pushButton_setup_acquisition = QtWidgets.QPushButton(self.frame_1)
        self.pushButton_setup_acquisition.setGeometry(QtCore.QRect(10, 130, 241, 28))
        self.pushButton_setup_acquisition.setObjectName("pushButton_setup_acquisition")
        self.label = QtWidgets.QLabel(self.frame_1)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 16))
        self.label.setObjectName("label")
        self.spinBox_number_of_frames = QtWidgets.QSpinBox(self.frame_1)
        self.spinBox_number_of_frames.setGeometry(QtCore.QRect(140, 30, 42, 22))
        self.spinBox_number_of_frames.setMaximum(10000)
        self.spinBox_number_of_frames.setProperty("value", 1)
        self.spinBox_number_of_frames.setObjectName("spinBox_number_of_frames")
        self.label_4 = QtWidgets.QLabel(self.frame_1)
        self.label_4.setGeometry(QtCore.QRect(140, 10, 71, 16))
        self.label_4.setObjectName("label_4")
        self.spinBox_energy_threshold = QtWidgets.QDoubleSpinBox(self.frame_1)
        self.spinBox_energy_threshold.setGeometry(QtCore.QRect(140, 90, 111, 22))
        self.spinBox_energy_threshold.setProperty("value", 2.2)
        self.spinBox_energy_threshold.setObjectName("spinBox_energy_threshold")
        self.comboBox_mode_of_measurement = QtWidgets.QComboBox(self.frame_1)
        self.comboBox_mode_of_measurement.setGeometry(QtCore.QRect(10, 30, 101, 22))
        self.comboBox_mode_of_measurement.setObjectName("comboBox_mode_of_measurement")
        self.comboBox_mode_of_measurement.addItem("")
        self.comboBox_mode_of_measurement.addItem("")
        self.comboBox_mode_of_measurement.addItem("")
        self.comboBox_mode_of_measurement.addItem("")
        self.pushButton_acquire = QtWidgets.QPushButton(self.frame_1)
        self.pushButton_acquire.setGeometry(QtCore.QRect(284, 10, 101, 101))
        self.pushButton_acquire.setObjectName("pushButton_acquire")
        self.label_2 = QtWidgets.QLabel(self.frame_1)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 111, 16))
        self.label_2.setObjectName("label_2")
        self.spinBox_integration_time = QtWidgets.QDoubleSpinBox(self.frame_1)
        self.spinBox_integration_time.setGeometry(QtCore.QRect(10, 90, 101, 22))
        self.spinBox_integration_time.setMaximum(10000000.0)
        self.spinBox_integration_time.setProperty("value", 1.1)
        self.spinBox_integration_time.setObjectName("spinBox_integration_time")
        self.label_3 = QtWidgets.QLabel(self.frame_1)
        self.label_3.setGeometry(QtCore.QRect(140, 70, 131, 16))
        self.label_3.setObjectName("label_3")
        self.label_messages = QtWidgets.QLabel(self.frame_1)
        self.label_messages.setGeometry(QtCore.QRect(10, 580, 411, 61))
        self.label_messages.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_messages.setText("")
        self.label_messages.setWordWrap(True)
        self.label_messages.setObjectName("label_messages")
        self.plainTextEdit_command_to_server = QtWidgets.QPlainTextEdit(self.frame_1)
        self.plainTextEdit_command_to_server.setGeometry(QtCore.QRect(10, 650, 121, 40))
        self.plainTextEdit_command_to_server.setObjectName("plainTextEdit_command_to_server")
        self.pushButton_send_to_server = QtWidgets.QPushButton(self.frame_1)
        self.pushButton_send_to_server.setGeometry(QtCore.QRect(140, 656, 93, 28))
        self.pushButton_send_to_server.setObjectName("pushButton_send_to_server")
        self.label_10 = QtWidgets.QLabel(self.frame_1)
        self.label_10.setGeometry(QtCore.QRect(10, 560, 81, 16))
        self.label_10.setObjectName("label_10")
        self.label_acquisition_progress = QtWidgets.QLabel(self.frame_1)
        self.label_acquisition_progress.setGeometry(QtCore.QRect(280, 200, 101, 16))
        self.label_acquisition_progress.setText("")
        self.label_acquisition_progress.setObjectName("label_acquisition_progress")
        self.pushButton_check_temperature = QtWidgets.QPushButton(self.frame_1)
        self.pushButton_check_temperature.setGeometry(QtCore.QRect(110, 172, 121, 28))
        self.pushButton_check_temperature.setObjectName("pushButton_check_temperature")
        self.label_demo_mode = QtWidgets.QLabel(self.frame_1)
        self.label_demo_mode.setGeometry(QtCore.QRect(10, 716, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_demo_mode.setFont(font)
        self.label_demo_mode.setText("")
        self.label_demo_mode.setWordWrap(True)
        self.label_demo_mode.setObjectName("label_demo_mode")
        self.label_5 = QtWidgets.QLabel(self.frame_1)
        self.label_5.setGeometry(QtCore.QRect(16, 322, 91, 16))
        self.label_5.setObjectName("label_5")
        self.plainTextEdit_sample_name = QtWidgets.QPlainTextEdit(self.frame_1)
        self.plainTextEdit_sample_name.setGeometry(QtCore.QRect(106, 316, 321, 31))
        self.plainTextEdit_sample_name.setObjectName("plainTextEdit_sample_name")
        self.label_6 = QtWidgets.QLabel(self.frame_1)
        self.label_6.setGeometry(QtCore.QRect(15, 410, 111, 16))
        self.label_6.setObjectName("label_6")
        self.spinBox_scan_pixels_i = QtWidgets.QSpinBox(self.frame_1)
        self.spinBox_scan_pixels_i.setGeometry(QtCore.QRect(126, 407, 61, 22))
        self.spinBox_scan_pixels_i.setMinimum(1)
        self.spinBox_scan_pixels_i.setMaximum(100000)
        self.spinBox_scan_pixels_i.setProperty("value", 3)
        self.spinBox_scan_pixels_i.setObjectName("spinBox_scan_pixels_i")
        self.label_7 = QtWidgets.QLabel(self.frame_1)
        self.label_7.setGeometry(QtCore.QRect(196, 410, 20, 16))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.spinBox_scan_pixels_j = QtWidgets.QSpinBox(self.frame_1)
        self.spinBox_scan_pixels_j.setGeometry(QtCore.QRect(217, 407, 61, 22))
        self.spinBox_scan_pixels_j.setMinimum(1)
        self.spinBox_scan_pixels_j.setMaximum(10000)
        self.spinBox_scan_pixels_j.setProperty("value", 3)
        self.spinBox_scan_pixels_j.setObjectName("spinBox_scan_pixels_j")
        self.pushButton_collect_stack = QtWidgets.QPushButton(self.frame_1)
        self.pushButton_collect_stack.setGeometry(QtCore.QRect(296, 404, 93, 28))
        self.pushButton_collect_stack.setObjectName("pushButton_collect_stack")
        self.label_current_i = QtWidgets.QLabel(self.frame_1)
        self.label_current_i.setGeometry(QtCore.QRect(126, 386, 55, 16))
        self.label_current_i.setText("")
        self.label_current_i.setObjectName("label_current_i")
        self.label_current_j = QtWidgets.QLabel(self.frame_1)
        self.label_current_j.setGeometry(QtCore.QRect(216, 387, 55, 16))
        self.label_current_j.setText("")
        self.label_current_j.setObjectName("label_current_j")
        self.pushButton_abort_stack_collection = QtWidgets.QPushButton(self.frame_1)
        self.pushButton_abort_stack_collection.setGeometry(QtCore.QRect(295, 440, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.pushButton_abort_stack_collection.setFont(font)
        self.pushButton_abort_stack_collection.setObjectName("pushButton_abort_stack_collection")
        self.horizontalLayout.addWidget(self.frame_1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_image_frame1 = QtWidgets.QLabel(self.frame)
        self.label_image_frame1.setGeometry(QtCore.QRect(0, 20, 256, 256))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_image_frame1.sizePolicy().hasHeightForWidth())
        self.label_image_frame1.setSizePolicy(sizePolicy)
        self.label_image_frame1.setMinimumSize(QtCore.QSize(256, 256))
        self.label_image_frame1.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image_frame1.setText("")
        self.label_image_frame1.setObjectName("label_image_frame1")
        self.label_image_frame2 = QtWidgets.QLabel(self.frame)
        self.label_image_frame2.setGeometry(QtCore.QRect(0, 310, 256, 256))
        self.label_image_frame2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image_frame2.setText("")
        self.label_image_frame2.setObjectName("label_image_frame2")
        self.label_measurement_type1 = QtWidgets.QLabel(self.frame)
        self.label_measurement_type1.setGeometry(QtCore.QRect(10, 0, 55, 16))
        self.label_measurement_type1.setObjectName("label_measurement_type1")
        self.label_measurement_type2 = QtWidgets.QLabel(self.frame)
        self.label_measurement_type2.setGeometry(QtCore.QRect(10, 290, 55, 16))
        self.label_measurement_type2.setObjectName("label_measurement_type2")
        self.label_image_frame3 = QtWidgets.QLabel(self.frame)
        self.label_image_frame3.setGeometry(QtCore.QRect(290, 20, 256, 256))
        self.label_image_frame3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image_frame3.setText("")
        self.label_image_frame3.setObjectName("label_image_frame3")
        self.label_measurement_type3 = QtWidgets.QLabel(self.frame)
        self.label_measurement_type3.setGeometry(QtCore.QRect(300, 0, 55, 16))
        self.label_measurement_type3.setObjectName("label_measurement_type3")
        self.label_image_frame4 = QtWidgets.QLabel(self.frame)
        self.label_image_frame4.setGeometry(QtCore.QRect(290, 310, 256, 256))
        self.label_image_frame4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image_frame4.setText("")
        self.label_image_frame4.setObjectName("label_image_frame4")
        self.label_measurement_type4 = QtWidgets.QLabel(self.frame)
        self.label_measurement_type4.setGeometry(QtCore.QRect(290, 290, 55, 16))
        self.label_measurement_type4.setObjectName("label_measurement_type4")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(-170, 790, 55, 16))
        self.label_8.setObjectName("label_8")
        self.label_counter = QtWidgets.QLabel(self.frame)
        self.label_counter.setGeometry(QtCore.QRect(10, 705, 431, 31))
        self.label_counter.setText("")
        self.label_counter.setObjectName("label_counter")
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1220, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_9.setText(_translate("MainWindow", "Temperature, C"))
        self.pushButton_select_directory.setText(_translate("MainWindow", "select directory"))
        self.label_temperature.setText(_translate("MainWindow", "0"))
        self.pushButton_setup_acquisition.setText(_translate("MainWindow", "setup acquisition"))
        self.label.setText(_translate("MainWindow", "Mode of measurement"))
        self.label_4.setText(_translate("MainWindow", "No. frames"))
        self.comboBox_mode_of_measurement.setItemText(0, _translate("MainWindow", "TOA & TOT"))
        self.comboBox_mode_of_measurement.setItemText(1, _translate("MainWindow", "TOA"))
        self.comboBox_mode_of_measurement.setItemText(2, _translate("MainWindow", "EVENT_iTOT"))
        self.comboBox_mode_of_measurement.setItemText(3, _translate("MainWindow", "TOT_not_TOA"))
        self.pushButton_acquire.setText(_translate("MainWindow", "Acquire"))
        self.label_2.setText(_translate("MainWindow", "Integration time, s"))
        self.label_3.setText(_translate("MainWindow", "Energy threshold, keV"))
        self.plainTextEdit_command_to_server.setPlainText(_translate("MainWindow", "abcd"))
        self.pushButton_send_to_server.setText(_translate("MainWindow", "send"))
        self.label_10.setText(_translate("MainWindow", "messages"))
        self.pushButton_check_temperature.setText(_translate("MainWindow", "check temperature"))
        self.label_5.setText(_translate("MainWindow", "Sample name:"))
        self.plainTextEdit_sample_name.setPlainText(_translate("MainWindow", "HfLaOsF2"))
        self.label_6.setText(_translate("MainWindow", "Scan area, pixels"))
        self.label_7.setText(_translate("MainWindow", "×"))
        self.pushButton_collect_stack.setText(_translate("MainWindow", "collect stack"))
        self.pushButton_abort_stack_collection.setText(_translate("MainWindow", "Abort"))
        self.label_measurement_type1.setText(_translate("MainWindow", "TOA"))
        self.label_measurement_type2.setText(_translate("MainWindow", "TOT"))
        self.label_measurement_type3.setText(_translate("MainWindow", "Event"))
        self.label_measurement_type4.setText(_translate("MainWindow", "iTOT"))
        self.label_8.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
