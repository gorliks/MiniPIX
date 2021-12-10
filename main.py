import qtdesigner_files.minipix_gui as gui_main
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import qimage2ndarray

import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import datetime

import detection as detection
import localhost_client as localhost, utils
import data_handling as storage

#test_image = '01_gorelick.jpg'

class GUIMainWindow(gui_main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, demo):
        self.demo = demo
        print('mode demo is ', demo)
        super(GUIMainWindow, self).__init__()
        self.setupUi(self)
        self.setup_connections()
        self.initialise_hardware()
        self.client = localhost.LocalHostClient()  # initialise communication with the localhost/client/server
        self.DIR = None
        self.label_image_frames = [self.label_image_frame1, self.label_image_frame2,
                                   self.label_image_frame3, self.label_image_frame4]
        self.supported_modes = ['TOA', 'TOT', 'EVENT', 'iTOT']
        self.storage = storage.Storage()  # initialise container for data strorage and handling
        self.pushButton_abort_stack_collection.setEnabled(False)
        self._abort_clicked_status = False

    def setup_connections(self):
        self.label_demo_mode.setText('demo mode: ' + str(self.demo))
        self.pushButton_setup_acquisition.clicked.connect(lambda: self.setup_acquisition())
        self.pushButton_acquire.clicked.connect(lambda: self.get_data())
        self.pushButton_send_to_server.clicked.connect(lambda: self.send_message_to_server())
        self.pushButton_select_directory.clicked.connect(lambda: self.select_directory())
        self.pushButton_check_temperature.clicked.connect(lambda: self.update_temperature())
        self.pushButton_collect_stack.clicked.connect(lambda: self.collect_stack())
        self.pushButton_abort_stack_collection.clicked.connect(lambda: self._abort_clicked())

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

    def setup_acquisition(self):
        print('setting the acquisition parameters')
        mode = self.comboBox_mode_of_measurement.currentText()
        number_of_frames = self.spinBox_number_of_frames.value()
        integration_time = self.spinBox_integration_time.value()
        energy_threshold_keV = self.spinBox_energy_threshold.value()
        self.device.setup_acquisition(mode=mode,
                                      number_of_frames=number_of_frames,
                                      integration_time=integration_time,
                                      energy_threshold_keV=energy_threshold_keV)

    def update_temperature(self):
        if not self.demo:
            temperature = self.device.get_temperature()
        else:
            temperature = 'demo mode: ' + str((np.random.rand() + 0.05) * 100)
        self.label_temperature.setText(str(temperature))

    def update_progress_bar(self, n):
        self.progressBar.setValue(n)

    def get_data(self):
        # self.label_acquisition_progress.setText('Acquiring')
        self.update_temperature()
        ts = time.time()
        stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d.%H%M%S')  # make a timestamp for new file
        if self.DIR == None:
            self.DIR = os.getcwd()
            print(self.DIR)
        file_name = self.DIR + '/' + stamp + '.pmf'
        self.data = self.device.acquire(file_name=file_name,
                                        mode=self.comboBox_mode_of_measurement.currentText())
        for count, mode in enumerate(self.supported_modes):
            _image_by_mode = self.data[mode]
            if type(_image_by_mode) == np.ndarray:
                self.update_image(quadrant=count, image=_image_by_mode)
        return self.data

    def update_image(self, quadrant, image):
        self.update_temperature()
        image_to_display = qimage2ndarray.array2qimage(image.copy())
        if quadrant in range(0, 4):
            self.label_image_frames[quadrant].setPixmap(QtGui.QPixmap(image_to_display))
        else:
            self.label_image_frames[0].setText('No image acquired')

    def collect_stack(self):
        self.pushButton_abort_stack_collection.setEnabled(True)
        self.pushButton_acquire.setEnabled(False)
        self.pushButton_setup_acquisition.setEnabled(False)
        self.pushButton_check_temperature.setEnabled(False)
        stack_i = self.spinBox_scan_pixels_i.value()  # scan over sample, no. pixels along X
        stack_j = self.spinBox_scan_pixels_j.value()  # scan over sample, no. pixels along Y
        self.storage.initialise(i=stack_i, j=stack_j, Nx=256, Ny=256)  # TODO detector image Nx,Ny settings more generic

        # the loop will check if abort button is clicked by checking QtWidgets.QApplication.processEvents()
        # if the abort button was clicked, _return_ will break the loop
        # TODO use threads for more elegant solution
        def _run_loop():
            for ii in range(stack_i):
                for jj in range(stack_j):
                    print(ii, jj)
                    self.label_current_i.setText(f'{ii + 1} of {stack_i}')
                    self.label_current_j.setText(f'{jj + 1} of {stack_j}')
                    self.data = self.get_data()
                    self.storage.stack.data[ii][jj] = self.data['TOA']  # populate the stack
                    self.repaint()  # update the GUI to show the progress
                    QtWidgets.QApplication.processEvents()
                    if self._abort_clicked_status == True:
                        print('Abort clicked')
                        self._abort_clicked_status = False  # reinitialise back to False
                        return

        _run_loop()
        # plot the acquired stack using hyperspy's library
        self.storage.stack.plot()
        plt.show()

        self.pushButton_acquire.setEnabled(True)
        self.pushButton_setup_acquisition.setEnabled(True)
        self.pushButton_check_temperature.setEnabled(True)
        self.pushButton_abort_stack_collection.setEnabled(False)

    def _resize_images(self, Nx=256, Ny=256):
        pass

    def _abort_clicked(self):
        print('------------ abort clicked --------------')
        self.pushButton_abort_stack_collection.setEnabled(False)
        self._abort_clicked_status = True


def main(demo):
    app = QtWidgets.QApplication([])
    qt_app = GUIMainWindow(demo)
    app.aboutToQuit.connect(qt_app.disconnect)  # cleanup & teardown
    qt_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(demo=True)
