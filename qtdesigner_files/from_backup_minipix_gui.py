from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1041, 867)
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
        self.label_messages = QtWidgets.QLabel(self.frame_1)
        self.label_messages.setGeometry(QtCore.QRect(10, 634, 431, 61))
        self.label_messages.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_messages.setText("")
        self.label_messages.setWordWrap(True)
        self.label_messages.setObjectName("label_messages")
        self.plainTextEdit_command_to_server = QtWidgets.QPlainTextEdit(self.frame_1)
        self.plainTextEdit_command_to_server.setGeometry(QtCore.QRect(10, 704, 121, 40))
        self.plainTextEdit_command_to_server.setObjectName("plainTextEdit_command_to_server")
        self.pushButton_send_to_server = QtWidgets.QPushButton(self.frame_1)
        self.pushButton_send_to_server.setGeometry(QtCore.QRect(140, 710, 93, 28))
        self.pushButton_send_to_server.setObjectName("pushButton_send_to_server")
        self.label_10 = QtWidgets.QLabel(self.frame_1)
        self.label_10.setGeometry(QtCore.QRect(10, 614, 81, 16))
        self.label_10.setObjectName("label_10")
        self.label_acquisition_progress = QtWidgets.QLabel(self.frame_1)
        self.label_acquisition_progress.setGeometry(QtCore.QRect(280, 200, 101, 16))
        self.label_acquisition_progress.setText("")
        self.label_acquisition_progress.setObjectName("label_acquisition_progress")
        self.label_demo_mode = QtWidgets.QLabel(self.frame_1)
        self.label_demo_mode.setGeometry(QtCore.QRect(10, 765, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_demo_mode.setFont(font)
        self.label_demo_mode.setText("")
        self.label_demo_mode.setWordWrap(True)
        self.label_demo_mode.setObjectName("label_demo_mode")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_1)
        self.tabWidget.setGeometry(QtCore.QRect(5, 0, 440, 571))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_acquire = QtWidgets.QPushButton(self.tab)
        self.pushButton_acquire.setGeometry(QtCore.QRect(290, 20, 101, 101))
        self.pushButton_acquire.setObjectName("pushButton_acquire")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(146, 80, 131, 16))
        self.label_3.setObjectName("label_3")
        self.spinBox_number_of_frames = QtWidgets.QSpinBox(self.tab)
        self.spinBox_number_of_frames.setGeometry(QtCore.QRect(146, 40, 42, 22))
        self.spinBox_number_of_frames.setMaximum(10000)
        self.spinBox_number_of_frames.setProperty("value", 1)
        self.spinBox_number_of_frames.setObjectName("spinBox_number_of_frames")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(146, 20, 71, 16))
        self.label_4.setObjectName("label_4")
        self.comboBox_mode_of_measurement = QtWidgets.QComboBox(self.tab)
        self.comboBox_mode_of_measurement.setGeometry(QtCore.QRect(16, 40, 101, 22))
        self.comboBox_mode_of_measurement.setObjectName("comboBox_mode_of_measurement")
        self.comboBox_mode_of_measurement.addItem("")
        self.comboBox_mode_of_measurement.addItem("")
        self.comboBox_mode_of_measurement.addItem("")
        self.comboBox_mode_of_measurement.addItem("")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(16, 20, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(16, 80, 111, 16))
        self.label_2.setObjectName("label_2")
        self.spinBox_energy_threshold = QtWidgets.QDoubleSpinBox(self.tab)
        self.spinBox_energy_threshold.setGeometry(QtCore.QRect(146, 100, 111, 22))
        self.spinBox_energy_threshold.setProperty("value", 2.2)
        self.spinBox_energy_threshold.setObjectName("spinBox_energy_threshold")
        self.spinBox_integration_time = QtWidgets.QDoubleSpinBox(self.tab)
        self.spinBox_integration_time.setGeometry(QtCore.QRect(16, 100, 101, 22))
        self.spinBox_integration_time.setMaximum(10000000.0)
        self.spinBox_integration_time.setProperty("value", 1.1)
        self.spinBox_integration_time.setObjectName("spinBox_integration_time")
        self.pushButton_select_directory = QtWidgets.QPushButton(self.tab)
        self.pushButton_select_directory.setGeometry(QtCore.QRect(290, 140, 100, 28))
        self.pushButton_select_directory.setObjectName("pushButton_select_directory")
        self.pushButton_setup_acquisition = QtWidgets.QPushButton(self.tab)
        self.pushButton_setup_acquisition.setGeometry(QtCore.QRect(8, 140, 241, 28))
        self.pushButton_setup_acquisition.setObjectName("pushButton_setup_acquisition")
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setGeometry(QtCore.QRect(290, 190, 101, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(17, 185, 91, 16))
        self.label_9.setObjectName("label_9")
        self.label_temperature = QtWidgets.QLabel(self.tab)
        self.label_temperature.setGeometry(QtCore.QRect(17, 200, 101, 21))
        self.label_temperature.setWordWrap(True)
        self.label_temperature.setObjectName("label_temperature")
        self.pushButton_check_temperature = QtWidgets.QPushButton(self.tab)
        self.pushButton_check_temperature.setGeometry(QtCore.QRect(117, 182, 131, 28))
        self.pushButton_check_temperature.setObjectName("pushButton_check_temperature")
        self.plainTextEdit_sample_name = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit_sample_name.setGeometry(QtCore.QRect(90, 280, 311, 31))
        self.plainTextEdit_sample_name.setObjectName("plainTextEdit_sample_name")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(0, 286, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(20, 340, 101, 16))
        self.label_6.setObjectName("label_6")
        self.pushButton_abort_stack_collection = QtWidgets.QPushButton(self.tab)
        self.pushButton_abort_stack_collection.setGeometry(QtCore.QRect(300, 370, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.pushButton_abort_stack_collection.setFont(font)
        self.pushButton_abort_stack_collection.setObjectName("pushButton_abort_stack_collection")
        self.pushButton_collect_stack = QtWidgets.QPushButton(self.tab)
        self.pushButton_collect_stack.setGeometry(QtCore.QRect(301, 334, 93, 28))
        self.pushButton_collect_stack.setObjectName("pushButton_collect_stack")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(201, 340, 20, 16))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.spinBox_scan_pixels_i = QtWidgets.QSpinBox(self.tab)
        self.spinBox_scan_pixels_i.setGeometry(QtCore.QRect(131, 337, 61, 22))
        self.spinBox_scan_pixels_i.setMinimum(1)
        self.spinBox_scan_pixels_i.setMaximum(100000)
        self.spinBox_scan_pixels_i.setProperty("value", 3)
        self.spinBox_scan_pixels_i.setObjectName("spinBox_scan_pixels_i")
        self.spinBox_scan_pixels_j = QtWidgets.QSpinBox(self.tab)
        self.spinBox_scan_pixels_j.setGeometry(QtCore.QRect(222, 337, 61, 22))
        self.spinBox_scan_pixels_j.setMinimum(1)
        self.spinBox_scan_pixels_j.setMaximum(10000)
        self.spinBox_scan_pixels_j.setProperty("value", 3)
        self.spinBox_scan_pixels_j.setObjectName("spinBox_scan_pixels_j")
        self.label_current_i = QtWidgets.QLabel(self.tab)
        self.label_current_i.setGeometry(QtCore.QRect(135, 320, 55, 16))
        self.label_current_i.setText("")
        self.label_current_i.setObjectName("label_current_i")
        self.label_current_j = QtWidgets.QLabel(self.tab)
        self.label_current_j.setGeometry(QtCore.QRect(225, 320, 55, 16))
        self.label_current_j.setText("")
        self.label_current_j.setObjectName("label_current_j")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(130, 10, 55, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(130, 42, 55, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(260, 42, 61, 16))
        self.label_13.setObjectName("label_13")
        self.lineEdit_server = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_server.setGeometry(QtCore.QRect(170, 10, 231, 22))
        self.lineEdit_server.setObjectName("lineEdit_server")
        self.lineEdit_user = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_user.setGeometry(QtCore.QRect(170, 40, 81, 22))
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.lineEdit_password = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_password.setGeometry(QtCore.QRect(320, 40, 81, 22))
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        self.label_14.setGeometry(QtCore.QRect(130, 70, 55, 16))
        self.label_14.setObjectName("label_14")
        self.lineEdit_host = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_host.setGeometry(QtCore.QRect(170, 70, 81, 22))
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.label_15 = QtWidgets.QLabel(self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(260, 70, 55, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_port = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_port.setGeometry(QtCore.QRect(320, 70, 81, 22))
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.checkBox_start_new = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_start_new.setGeometry(QtCore.QRect(10, 10, 81, 20))
        self.checkBox_start_new.setObjectName("checkBox_start_new")
        self.checkBox_gui = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_gui.setGeometry(QtCore.QRect(10, 30, 77, 20))
        self.checkBox_gui.setChecked(True)
        self.checkBox_gui.setObjectName("checkBox_gui")
        self.pushButton_open_client = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_open_client.setGeometry(QtCore.QRect(10, 60, 75, 24))
        self.pushButton_open_client.setObjectName("pushButton_open_client")
        self.spinBox_magnification = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_magnification.setGeometry(QtCore.QRect(105, 140, 80, 22))
        self.spinBox_magnification.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spinBox_magnification.setMinimum(0)
        self.spinBox_magnification.setMaximum(1000000)
        self.spinBox_magnification.setObjectName("spinBox_magnification")
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(10, 140, 81, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(10, 170, 101, 21))
        self.label_17.setObjectName("label_17")
        self.doubleSpinBox_high_voltage = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_high_voltage.setGeometry(QtCore.QRect(105, 170, 80, 22))
        self.doubleSpinBox_high_voltage.setMaximum(30.0)
        self.doubleSpinBox_high_voltage.setObjectName("doubleSpinBox_high_voltage")
        self.doubleSpinBox_working_distance = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_working_distance.setGeometry(QtCore.QRect(105, 200, 80, 22))
        self.doubleSpinBox_working_distance.setObjectName("doubleSpinBox_working_distance")
        self.label_18 = QtWidgets.QLabel(self.tab_2)
        self.label_18.setGeometry(QtCore.QRect(10, 200, 101, 16))
        self.label_18.setObjectName("label_18")
        self.doubleSpinBox_brightness = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_brightness.setGeometry(QtCore.QRect(105, 230, 80, 22))
        self.doubleSpinBox_brightness.setMaximum(100.0)
        self.doubleSpinBox_brightness.setObjectName("doubleSpinBox_brightness")
        self.label_19 = QtWidgets.QLabel(self.tab_2)
        self.label_19.setGeometry(QtCore.QRect(10, 230, 101, 21))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.tab_2)
        self.label_20.setGeometry(QtCore.QRect(10, 260, 101, 16))
        self.label_20.setObjectName("label_20")
        self.doubleSpinBox_contrast = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_contrast.setGeometry(QtCore.QRect(105, 260, 80, 22))
        self.doubleSpinBox_contrast.setMaximum(100.0)
        self.doubleSpinBox_contrast.setObjectName("doubleSpinBox_contrast")
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(10, 290, 101, 16))
        self.label_21.setObjectName("label_21")
        self.doubleSpinBox_probe_current = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_probe_current.setGeometry(QtCore.QRect(105, 290, 80, 22))
        self.doubleSpinBox_probe_current.setObjectName("doubleSpinBox_probe_current")
        self.doubleSpinBox_spot_size = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_spot_size.setGeometry(QtCore.QRect(105, 320, 80, 22))
        self.doubleSpinBox_spot_size.setMaximum(1000.0)
        self.doubleSpinBox_spot_size.setObjectName("doubleSpinBox_spot_size")
        self.label_22 = QtWidgets.QLabel(self.tab_2)
        self.label_22.setGeometry(QtCore.QRect(10, 320, 101, 16))
        self.label_22.setObjectName("label_22")
        self.pushButton_update_SEM_state = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_update_SEM_state.setGeometry(QtCore.QRect(10, 350, 171, 24))
        self.pushButton_update_SEM_state.setObjectName("pushButton_update_SEM_state")
        self.doubleSpinBox_stage_x = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_stage_x.setGeometry(QtCore.QRect(275, 140, 80, 22))
        self.doubleSpinBox_stage_x.setObjectName("doubleSpinBox_stage_x")
        self.label_23 = QtWidgets.QLabel(self.tab_2)
        self.label_23.setGeometry(QtCore.QRect(260, 142, 21, 16))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.tab_2)
        self.label_24.setGeometry(QtCore.QRect(260, 170, 21, 16))
        self.label_24.setObjectName("label_24")
        self.doubleSpinBox_stage_y = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_stage_y.setGeometry(QtCore.QRect(275, 168, 80, 22))
        self.doubleSpinBox_stage_y.setObjectName("doubleSpinBox_stage_y")
        self.label_25 = QtWidgets.QLabel(self.tab_2)
        self.label_25.setGeometry(QtCore.QRect(260, 200, 21, 16))
        self.label_25.setObjectName("label_25")
        self.doubleSpinBox_stage_z = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_stage_z.setGeometry(QtCore.QRect(275, 198, 80, 22))
        self.doubleSpinBox_stage_z.setObjectName("doubleSpinBox_stage_z")
        self.doubleSpinBox_stage_r = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_stage_r.setGeometry(QtCore.QRect(275, 228, 80, 22))
        self.doubleSpinBox_stage_r.setObjectName("doubleSpinBox_stage_r")
        self.label_26 = QtWidgets.QLabel(self.tab_2)
        self.label_26.setGeometry(QtCore.QRect(260, 230, 21, 16))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.tab_2)
        self.label_27.setGeometry(QtCore.QRect(260, 260, 21, 16))
        self.label_27.setObjectName("label_27")
        self.doubleSpinBox_stage_t = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_stage_t.setGeometry(QtCore.QRect(275, 258, 80, 22))
        self.doubleSpinBox_stage_t.setObjectName("doubleSpinBox_stage_t")
        self.pushButton_read_stage_position = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_read_stage_position.setGeometry(QtCore.QRect(260, 290, 101, 24))
        self.pushButton_read_stage_position.setObjectName("pushButton_read_stage_position")
        self.pushButton_move_stage = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_move_stage.setGeometry(QtCore.QRect(260, 320, 101, 31))
        self.pushButton_move_stage.setObjectName("pushButton_move_stage")
        self.label_29 = QtWidgets.QLabel(self.tab_2)
        self.label_29.setGeometry(QtCore.QRect(10, 410, 101, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.spinBox_width_pixels = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_width_pixels.setGeometry(QtCore.QRect(95, 430, 71, 22))
        self.spinBox_width_pixels.setMinimum(0)
        self.spinBox_width_pixels.setMaximum(8000)
        self.spinBox_width_pixels.setObjectName("spinBox_width_pixels")
        self.label_30 = QtWidgets.QLabel(self.tab_2)
        self.label_30.setGeometry(QtCore.QRect(8, 432, 81, 16))
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.tab_2)
        self.label_31.setGeometry(QtCore.QRect(8, 452, 81, 16))
        self.label_31.setObjectName("label_31")
        self.spinBox_height_pixels = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_height_pixels.setGeometry(QtCore.QRect(95, 450, 71, 22))
        self.spinBox_height_pixels.setMinimum(0)
        self.spinBox_height_pixels.setMaximum(8000)
        self.spinBox_height_pixels.setObjectName("spinBox_height_pixels")
        self.checkBox_external_scan = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_external_scan.setGeometry(QtCore.QRect(10, 100, 101, 20))
        self.checkBox_external_scan.setObjectName("checkBox_external_scan")
        self.label_32 = QtWidgets.QLabel(self.tab_2)
        self.label_32.setGeometry(QtCore.QRect(190, 432, 51, 16))
        self.label_32.setObjectName("label_32")
        self.spinBox_average = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_average.setGeometry(QtCore.QRect(240, 430, 71, 22))
        self.spinBox_average.setMinimum(1)
        self.spinBox_average.setMaximum(8000)
        self.spinBox_average.setObjectName("spinBox_average")
        self.label_33 = QtWidgets.QLabel(self.tab_2)
        self.label_33.setGeometry(QtCore.QRect(190, 450, 51, 16))
        self.label_33.setObjectName("label_33")
        self.doubleSpinBox_field_width = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_field_width.setGeometry(QtCore.QRect(240, 450, 71, 22))
        self.doubleSpinBox_field_width.setMaximum(30.0)
        self.doubleSpinBox_field_width.setObjectName("doubleSpinBox_field_width")
        self.checkBox_channel_1 = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_channel_1.setGeometry(QtCore.QRect(330, 430, 77, 20))
        self.checkBox_channel_1.setChecked(True)
        self.checkBox_channel_1.setObjectName("checkBox_channel_1")
        self.checkBox_channel_2 = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_channel_2.setGeometry(QtCore.QRect(330, 450, 77, 20))
        self.checkBox_channel_2.setChecked(False)
        self.checkBox_channel_2.setObjectName("checkBox_channel_2")
        self.pushButton_get_image_config = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_get_image_config.setGeometry(QtCore.QRect(10, 490, 110, 24))
        self.pushButton_get_image_config.setObjectName("pushButton_get_image_config")
        self.pushButton_set_image_config = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_set_image_config.setGeometry(QtCore.QRect(130, 490, 110, 24))
        self.pushButton_set_image_config.setObjectName("pushButton_set_image_config")
        self.pushButton_get_image = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_get_image.setGeometry(QtCore.QRect(250, 490, 110, 24))
        self.pushButton_get_image.setObjectName("pushButton_get_image")
        self.checkBox_beam_blank = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_beam_blank.setGeometry(QtCore.QRect(380, 430, 73, 16))
        self.checkBox_beam_blank.setObjectName("checkBox_beam_blank")
        self.tabWidget.addTab(self.tab_2, "")
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
        self.label_counter.setGeometry(QtCore.QRect(10, 760, 431, 31))
        self.label_counter.setText("")
        self.label_counter.setObjectName("label_counter")
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1041, 21))
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
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plainTextEdit_command_to_server.setPlainText(_translate("MainWindow", "abcd"))
        self.pushButton_send_to_server.setText(_translate("MainWindow", "send"))
        self.label_10.setText(_translate("MainWindow", "messages"))
        self.pushButton_acquire.setText(_translate("MainWindow", "Acquire"))
        self.label_3.setText(_translate("MainWindow", "Energy threshold, keV"))
        self.label_4.setText(_translate("MainWindow", "No. frames"))
        self.comboBox_mode_of_measurement.setItemText(0, _translate("MainWindow", "TOA & TOT"))
        self.comboBox_mode_of_measurement.setItemText(1, _translate("MainWindow", "TOA"))
        self.comboBox_mode_of_measurement.setItemText(2, _translate("MainWindow", "EVENT_iTOT"))
        self.comboBox_mode_of_measurement.setItemText(3, _translate("MainWindow", "TOT_not_TOA"))
        self.label.setText(_translate("MainWindow", "Mode of measurement"))
        self.label_2.setText(_translate("MainWindow", "Integration time, s"))
        self.pushButton_select_directory.setText(_translate("MainWindow", "select directory"))
        self.pushButton_setup_acquisition.setText(_translate("MainWindow", "setup acquisition"))
        self.label_9.setText(_translate("MainWindow", "Temperature, C"))
        self.label_temperature.setText(_translate("MainWindow", "0"))
        self.pushButton_check_temperature.setText(_translate("MainWindow", "check temperature"))
        self.plainTextEdit_sample_name.setPlainText(_translate("MainWindow", "HfLaOsF2"))
        self.label_5.setText(_translate("MainWindow", "Sample name:"))
        self.label_6.setText(_translate("MainWindow", "Scan area, pixels"))
        self.pushButton_abort_stack_collection.setText(_translate("MainWindow", "Abort"))
        self.pushButton_collect_stack.setText(_translate("MainWindow", "collect stack"))
        self.label_7.setText(_translate("MainWindow", "×"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Minipix"))
        self.label_11.setText(_translate("MainWindow", "Server"))
        self.label_12.setText(_translate("MainWindow", "User"))
        self.label_13.setText(_translate("MainWindow", "Password"))
        self.lineEdit_user.setText(_translate("MainWindow", "edx"))
        self.lineEdit_password.setText(_translate("MainWindow", "edx"))
        self.label_14.setText(_translate("MainWindow", "Host"))
        self.lineEdit_host.setText(_translate("MainWindow", "127.0.0.1"))
        self.label_15.setText(_translate("MainWindow", "Port"))
        self.lineEdit_port.setText(_translate("MainWindow", "0"))
        self.checkBox_start_new.setText(_translate("MainWindow", "Start new"))
        self.checkBox_gui.setText(_translate("MainWindow", "GUI"))
        self.pushButton_open_client.setText(_translate("MainWindow", "Open client"))
        self.label_16.setText(_translate("MainWindow", "Magnification"))
        self.label_17.setText(_translate("MainWindow", "High voltage, kV"))
        self.label_18.setText(_translate("MainWindow", "WD, mm"))
        self.label_19.setText(_translate("MainWindow", "Brightness %"))
        self.label_20.setText(_translate("MainWindow", "Contrast %"))
        self.label_21.setText(_translate("MainWindow", "Probe current nA"))
        self.label_22.setText(_translate("MainWindow", "Spot size"))
        self.pushButton_update_SEM_state.setText(_translate("MainWindow", "Update values"))
        self.label_23.setText(_translate("MainWindow", "X"))
        self.label_24.setText(_translate("MainWindow", "Y"))
        self.label_25.setText(_translate("MainWindow", "Z"))
        self.label_26.setText(_translate("MainWindow", "R"))
        self.label_27.setText(_translate("MainWindow", "T"))
        self.pushButton_read_stage_position.setText(_translate("MainWindow", "Get position"))
        self.pushButton_move_stage.setText(_translate("MainWindow", "Move to position"))
        self.label_29.setText(_translate("MainWindow", "SEM  imaging"))
        self.label_30.setText(_translate("MainWindow", "Width, pixels"))
        self.label_31.setText(_translate("MainWindow", "Height, pixels"))
        self.checkBox_external_scan.setText(_translate("MainWindow", "External scan"))
        self.label_32.setText(_translate("MainWindow", "Average"))
        self.label_33.setText(_translate("MainWindow", "Field W"))
        self.checkBox_channel_1.setText(_translate("MainWindow", "Ch1"))
        self.checkBox_channel_2.setText(_translate("MainWindow", "Ch2"))
        self.pushButton_get_image_config.setText(_translate("MainWindow", "Get image config"))
        self.pushButton_set_image_config.setText(_translate("MainWindow", "Set image config"))
        self.pushButton_get_image.setText(_translate("MainWindow", "Get image"))
        self.checkBox_beam_blank.setText(_translate("MainWindow", "Blank"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Bruker"))
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
