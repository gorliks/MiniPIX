import qtdesigner_files.minipix_gui as gui_main
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, QThread, QThreadPool, QTimer, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import qimage2ndarray

from importlib import reload  # Python 3.4+

import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import datetime

import detection as detection
import localhost_client as localhost
import utils
import data_handling as storage
import threads as threads
import bruker_espirit_API as SEM

#test_image = '01_gorelick.jpg'

class GUIMainWindow(gui_main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, demo):
        self.demo = demo
        self.time_counter = 0
        print('mode demo is ', demo)
        super(GUIMainWindow, self).__init__()
        self.setupUi(self)
        self.setup_connections()
        self.initialise_hardware()
        self.client = localhost.LocalHostClient()  # initialise communication with the localhost/client/server
        self.DIR = None

        self.supported_modes = ['TOA', 'TOT', 'EVENT', 'iTOT']
        self.storage_dict = dict.fromkeys(self.supported_modes) # initialise the dictionary for data sorted by modes
        for supported_mode in self.supported_modes:
            self.storage_dict[supported_mode] = storage.Storage()  # initialise container for data storage and handling

        self.label_image_frames = [self.label_image_frame1, self.label_image_frame2,
                                   self.label_image_frame3, self.label_image_frame4]

        # timer on a separate thread
        # self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        # self.timer = QTimer()
        # self.timer.setInterval(1000) #1 s intervals
        # self.timer.timeout.connect(self._time_counter)
        # self.timer.start()

        self.pushButton_abort_stack_collection.setEnabled(False)
        self._abort_clicked_status = False

        self.data_in_quadrant = [ [], [], [], []  ]


    def setup_connections(self):
        self.label_demo_mode.setText('demo mode: ' + str(self.demo))
        self.pushButton_setup_acquisition.clicked.connect(lambda: self.setup_acquisition())
        self.pushButton_acquire.clicked.connect(lambda: self.single_acquisition())
        self.pushButton_send_to_server.clicked.connect(lambda: self.send_message_to_server())
        self.pushButton_select_directory.clicked.connect(lambda: self.select_directory())
        self.pushButton_check_temperature.clicked.connect(lambda: self.update_temperature())
        self.pushButton_collect_stack.clicked.connect(lambda: self.collect_stack())
        self.pushButton_abort_stack_collection.clicked.connect(lambda: self._abort_clicked())
        self.pushButton_initialise_detector.clicked.connect(lambda: self.initialise_detector())
        self.comboBox_image_log_scale.currentIndexChanged.connect( lambda: self.change_image_scale())
        #### SEM
        self.pushButton_open_client.clicked.connect(lambda: self.open_sem_client())
        self.pushButton_update_SEM_state.clicked.connect(lambda: self.update_sem_state())
        self.checkBox_external_scan.stateChanged.connect(lambda: self.set_to_external_mode())
        self.pushButton_read_stage_position.clicked.connect(lambda: self.get_stage_position())
        self.pushButton_get_image_config.clicked.connect(lambda: self.get_image_configuration())
        self.pushButton_set_image_config.clicked.connect(lambda: self.set_image_configuration())
        self.pushButton_get_image.clicked.connect(lambda: self.get_sem_image())
        self.checkBox_beam_blank.stateChanged.connect(lambda: self.beam_blank())
        self.pushButton_set_beam_position.clicked.connect(lambda: self.set_beam_to_position())


    def open_sem_client(self):
        self.bruker.initialise(type='direct') #check which type works
        self.spinBox_CID.setValue(int(self.bruker.CID.value))
        self.label_messages.setText(self.bruker.error_message)


    def get_image_configuration(self):
        self.bruker.get_image_configuration()
        self.label_messages.setText(self.bruker.error_message)
        self.spinBox_width_pixels.setValue(int(self.bruker.width.value))
        self.spinBox_height_pixels.setValue(int(self.bruker.height.value))
        self.spinBox_width_pixels.setValue(int(self.bruker.width.value))
        self.spinBox_average.setValue(int(self.bruker.average.value))
        self.doubleSpinBox_field_width.setValue(self.bruker.field_width.value)
        self.checkBox_channel_1.setChecked(self.bruker.Ch1.value)
        self.checkBox_channel_2.setChecked(self.bruker.Ch2.value)


    def get_sem_image(self):
        self.bruker.acquire_image(demo=self.demo)
        self.label_messages.setText(self.bruker.error_message)
        utils.select_point(self.bruker.image)


    def set_image_configuration(self):
        width = self.spinBox_width_pixels.value()
        height = self.spinBox_height_pixels.value()
        average = self.spinBox_average.value()
        Ch1 = self.checkBox_channel_1.isChecked()
        Ch2 = self.checkBox_channel_2.isChecked()
        self.bruker.set_image_configuration(width=width, height=height,\
                                            average=average, Ch1=Ch1, Ch2=Ch1)
        self.label_messages.setText(self.bruker.error_message)


    def get_stage_position(self):
        self.bruker.get_sem_stage_position()
        self.label_messages.setText(self.bruker.error_message)
        self.doubleSpinBox_stage_x.setValue(self.bruker.x_pos.value)
        self.doubleSpinBox_stage_y.setValue(self.bruker.y_pos.value)
        self.doubleSpinBox_stage_z.setValue(self.bruker.z_pos.value)
        self.doubleSpinBox_stage_t.setValue(self.bruker.t_pos.value)
        self.doubleSpinBox_stage_r.setValue(self.bruker.r_pos.value)
        self.label_messages.setText(self.bruker.error_message)


    def set_to_external_mode(self):
        _state = self.checkBox_external_scan.isChecked()
        if _state == True:
            print('setting SEM to external mode')
            self.bruker.set_sem_to_external_mode(external=True)
            self.bruker.set_external_scan_mode(external=True)
        else:
            print('setting SEM to internal mode')
            self.bruker.set_sem_to_external_mode(external=False)
            self.bruker.set_external_scan_mode(external=False)
        self.label_messages.setText(self.bruker.error_message)


    def beam_blank(self):
        _state = self.checkBox_beam_blank.isChecked()
        if _state == True:
            print('blanking the beam by moving it far away')
            self.bruker.beam_blank()
        else:
            print('moving the beam from blank position to the previously stored x,y point')
            self.bruker.set_beam_to_point(x_pos=self.bruker.beam_x_pos, y_pos=self.bruker.beam_y_pos)
        self.label_messages.setText(self.bruker.error_message)


    def update_sem_state(self):
        # get all the possible sem data and copy the result to the corresponding slots in GUI
        self.bruker.get_sem_data()

        self.label_messages.setText(self.bruker.error_message)
        self.bruker.get_sem_brightness_and_contrast()
        self.label_messages.setText(self.bruker.error_message)
        self.bruker.get_sem_probe_current()
        self.label_messages.setText(self.bruker.error_message)
        self.bruker.get_sem_spot_size()
        self.label_messages.setText(self.bruker.error_message)

        self.spinBox_magnification.setValue(int(self.bruker.mag.value))
        self.doubleSpinBox_high_voltage.setValue(self.bruker.high_voltage.value)
        self.doubleSpinBox_working_distance.setValue(self.bruker.working_distance.value)
        self.doubleSpinBox_brightness.setValue(self.bruker.brightness.value)
        self.doubleSpinBox_contrast.setValue(self.bruker.contrast.value)
        self.doubleSpinBox_probe_current.setValue(self.bruker.probe_current.value)
        self.doubleSpinBox_spot_size.setValue(self.bruker.spot_size.value)

        self.bruker.get_sem_info()
        self.bruker.get_sem_capabilities()
        self.label_messages.setText(self.bruker.error_message)
        print(self.bruker.Info)
        print(self.bruker.capabilities)


    def set_beam_to_position(self):
        x_pos = self.spinBox_beam_x.value()
        y_pos = self.spinBox_beam_y.value()
        print(f'Move beam to ({x_pos}, {y_pos}) setting SEM to external mode')
        self.bruker.set_sem_to_external_mode(external=True)
        self.label_messages.setText(self.bruker.error_message)
        self.bruker.set_external_scan_mode(external=True)
        self.label_messages.setText(self.bruker.error_message)
        self.bruker.set_beam_to_point(x_pos=x_pos, y_pos=y_pos)
        self.label_messages.setText(self.bruker.error_message)




    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, caption='Select a folder')
        print(directory)
        self.label_messages.setText(directory)
        self.DIR = directory


    def send_message_to_server(self):
        message = self.plainTextEdit_command_to_server.toPlainText()
        self.client.send_message_to_server(message)
        self.response = self.client.get_response()
        self.label_messages.setText(self.response)


    def initialise_hardware(self):
        self.device = detection.Detector(demo=self.demo)
        detector_info = self.device.initialise()
        self.label_messages.setText(str(detector_info))
        # initialise Bruker API
        self.bruker = SEM.Bruker_Espirit()


    def initialise_detector(self):
        reload(detection)
        self.device = detection.Detector(demo=self.demo)
        detector_info = self.device.initialise()
        self.label_messages.setText(str(detector_info))
        self.pushButton_initialise_detector.setStyleSheet("background-color: green")


    def update_temperature(self):
        if not self.demo:
            temperature = self.device.get_temperature()
        else:
            temperature = 'demo mode: ' + str((np.random.rand() + 0.05) * 100)
        self.label_temperature.setText(str(temperature))


    def setup_acquisition(self):
        print('setting the acquisition parameters')
        type = self.comboBox_type_of_measurement.currentText()
        mode = self.comboBox_mode_of_measurement.currentText()
        number_of_frames = self.spinBox_number_of_frames.value()
        integration_time = self.spinBox_integration_time.value()
        energy_threshold_keV = self.spinBox_energy_threshold.value()
        self.device.setup_acquisition(type=type,
                                      mode=mode,
                                      number_of_frames=number_of_frames,
                                      integration_time=integration_time,
                                      energy_threshold_keV=energy_threshold_keV)
        self.active_modes = dict.fromkeys(self.supported_modes) # initialise the dictionary for data sorted by modes
        self.active_modes = dict.fromkeys(self.active_modes, False) # initialise the modes to False
        if mode == 'TOATOT' or mode == 'TOA & TOT':
            self.active_modes['TOA'] = True
            self.active_modes['TOT'] = True
        elif mode == 'TOA':
            self.active_modes['TOA'] = True
        elif mode == 'EVENT_iTOT':
            self.active_modes['EVENT'] = True
            self.active_modes['iTOT']  = True


    def single_acquisition(self):
        self.setup_acquisition()
        self.get_data()


    def get_data(self, save_dir=None, file_name=None):
        self.update_temperature()
        ts = time.time()
        stamp = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d.%H%M%S')  # make a timestamp for new file

        if save_dir:
            save_dir = save_dir
        elif self.DIR == None:
            save_dir = os.getcwd()
            # self.DIR = r'C:/TEMP'

        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        print(self.DIR, save_dir)

        if file_name:
            file_name = save_dir + '/' + file_name + '_' + stamp
        else:
            file_name = save_dir + '/' + stamp
        print(file_name)

        self.integration_time = self.device.integration_time    # TODO update device state in settings self.device.settings['integration_time']

        ##################### progress bar routine #####################
        # worker = threads.Worker(self._progress_bar_counter)  # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self._worker_result)
        # worker.signals.finished.connect(self._reset_status_bar)
        # worker.signals.progress.connect(self._update_progress_bar)
        # self.threadpool.start(worker) # Execute
        ################################################################
        self.pushButton_acquire.setEnabled(False)
        self.pushButton_setup_acquisition.setEnabled(False)
        self.pushButton_check_temperature.setEnabled(False)
        self.repaint()  # update the GUI to show the progress

        self.data = \
            self.device.acquire(file_name=file_name,
                                        type=self.comboBox_type_of_measurement.currentText(),
                                        mode=self.comboBox_mode_of_measurement.currentText())

        self.pushButton_acquire.setEnabled(True)
        self.pushButton_setup_acquisition.setEnabled(True)
        self.pushButton_check_temperature.setEnabled(True)
        self.repaint()  # update the GUI to show the progress

        for count, mode in enumerate(self.supported_modes):
            _image_by_mode = self.data[mode]
            if type(_image_by_mode) == np.ndarray:
                self.update_image(quadrant=count, image=_image_by_mode)
                self.data_in_quadrant[count] = _image_by_mode # keep the last measurement in memory

        return self.data


    def update_image(self, quadrant, image):
        self.update_temperature()
        image_to_display = qimage2ndarray.array2qimage(image.copy())
        if quadrant in range(0, 4):
            self.label_image_frames[quadrant].setPixmap(QtGui.QPixmap(image_to_display))
        else:
            self.label_image_frames[0].setText('No image acquired')


    def change_image_scale(self):
        _type = self.comboBox_image_log_scale.currentText()
        print('image scale lin/log ->', _type)
        if _type == 'Logarithm':
            print('LOG')
            for count, mode in enumerate(self.supported_modes):
                if type(self.data_in_quadrant[count]) == np.ndarray:
                    _image_log = np.log(self.data_in_quadrant[count]+1)
                    self.update_image(quadrant=count, image=_image_log)
        else:
            print('LIN')
            for count, mode in enumerate(self.supported_modes):
                self.update_image(quadrant=count, image=(self.data_in_quadrant[count]))



    def collect_stack(self):
        self.setup_acquisition() # update the acquisition parameters
        ts = time.time()
        stamp = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d.%H%M%S')  # make a timestamp for new file
        self.sample_id = self.plainTextEdit_sample_name.toPlainText()
        self.pushButton_abort_stack_collection.setEnabled(True)
        self.pushButton_acquire.setEnabled(False)
        self.pushButton_setup_acquisition.setEnabled(False)
        self.pushButton_check_temperature.setEnabled(False)
        stack_i = self.spinBox_scan_pixels_i.value()  # scan over sample, no. pixels along X
        stack_j = self.spinBox_scan_pixels_j.value()  # scan over sample, no. pixels along Y

        # reinitialise the data storage
        for supported_mode in self.supported_modes:
            self.storage_dict[supported_mode] = storage.Storage()  # initialise container for data storage and handling
            if self.active_modes[supported_mode] == True: # check if the mode is activated
                self.storage_dict[supported_mode].initialise(i=stack_i, j=stack_j, Nx=256, Ny=256)  # TODO detector image Nx,Ny settings more generic

        if self.DIR:
            self.stack_dir = self.DIR + '/stack_' + self.sample_id + '_' + stamp
        else:
            self.stack_dir = os.getcwd() + '/stack_' + self.sample_id + '_' + stamp

        # the loop will check if abort button is clicked by checking QtWidgets.QApplication.processEvents()
        # if the abort button was clicked, _return_ will break the _run_loop
        # TODO use threads for more elegant solution
        def _run_loop():
            pixel_counter = 0
            for ii in range(stack_i):
                for jj in range(stack_j):
                    print(ii, jj)
                    self.label_current_i.setText(f'{ii + 1} of {stack_i}')
                    self.label_current_j.setText(f'{jj + 1} of {stack_j}')

                    file_name = '%06d_'%pixel_counter + str(ii) + '_' + str(jj)

                    self.bruker.set_beam_to_point(x_pos=ii, y_pos=jj)
                    self.data = self.get_data(save_dir=self.stack_dir, file_name=file_name)
                    self.bruker.beam_blank()

                    for supported_mode in self.supported_modes:
                        # self.storage.stack.data[ii][jj] = self.data['TOA']  # populate the stack
                        if self.active_modes[supported_mode] == True:
                            self.storage_dict[supported_mode].stack.data[ii][jj] = \
                                self.data[supported_mode]

                    self.repaint()  # update the GUI to show the progress
                    QtWidgets.QApplication.processEvents()

                    if self._abort_clicked_status == True:
                        print('Abort clicked')
                        self._abort_clicked_status = False  # reinitialise back to False
                        return
                    pixel_counter += 1

        _run_loop()

        for supported_mode in self.supported_modes:
            # self.storage.stack.plot() # plot the acquired stack using hyperspy's library
            if self.active_modes[supported_mode] == True:
                self.storage_dict[supported_mode].stack.plot()
                plt.title(supported_mode)

        plt.show()

        self.pushButton_acquire.setEnabled(True)
        self.pushButton_setup_acquisition.setEnabled(True)
        self.pushButton_check_temperature.setEnabled(True)
        self.pushButton_abort_stack_collection.setEnabled(False)




    def _progress_bar_counter(self, progress_callback):
        N = 10
        dt = self.integration_time / N
        print('dt = ', dt)
        for n in range(1, N):
            time.sleep(dt)
            progress_callback.emit(n*10)

    def _worker_result(self, result):
        pass

    def _update_progress_bar(self, n):
        print(n)
        self.progressBar.setValue(int(n))

    def _reset_status_bar(self):
        self.progressBar.setValue(0)

    def _resize_images(self, Nx=256, Ny=256):
        pass

    def _abort_clicked(self):
        print('------------ abort clicked --------------')
        self.pushButton_abort_stack_collection.setEnabled(False)
        self._abort_clicked_status = True

    def _time_counter(self):
        self.time_counter += 1
        self.label_counter.setText("runtime: %d sec" % self.time_counter)







def main(demo):
    app = QtWidgets.QApplication([])
    qt_app = GUIMainWindow(demo)
    app.aboutToQuit.connect(qt_app.disconnect)  # cleanup & teardown
    qt_app.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main(demo=True)
