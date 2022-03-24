import sys, time
import numpy as np
import backend_hardware_communication as hardware
import datetime

from importlib import reload  # Python 3.4+
reload(hardware)

# path_to_pixet = r'C:\Program Files\PIXet Pro'
# sys.path.append(path_to_pixet)
# import pypixet
# pypixet.start()
# pixet = pypixet.pixet
# print( pixet.pixetVersion() )



class Detector():
    def __init__(self, demo=True):
        self.type = 'TPX3'
        self.devices = []
        self.device = None
        self.path_to_pixet = r'C:\Program Files\PIXet Pro'
        self.demo = demo
        self.initialised = False
        self.settings = {
            'type' : 'Frames',
            'mode' : 'TOATOT',
            'number_of_frames' : 1,
            'integration_time' : 1.0,
            'energy_threshold_keV' : 2.0,
        }
        self.detector_info = ''


    def initialise(self):
        self.full_name = None
        self.width = None
        self.pixel_count = None
        self.chip_count = None
        self.chip_id = None

        if self.demo == False:
            # hardware
            # get all connected devices
            self.devices = hardware.initialise(path_to_pixet=self.path_to_pixet)
            # select the fist connected device
            self.device = self.devices[0]
            print('detection: device = ', self.device)
            if self.device == 'no device connected':
                self.initialised = False
                self.detector_info = {'full_name': 'None', 'width': 'None',
                                 'pixel_count': 'None', 'chip_count': 'None',
                                 'chip_id': 'None'}
            elif self.device:
                self.initialised = True
                self.detector_info = hardware.get_detector_info(self.device)
            print(self.detector_info)

        else:
            # demo mode
            print('Demo mode, no detector connected')
            print('Device full name:', self.full_name)
            print('Width x height  :', self.width, ' x ', self.width)
            print('Pixel count     :', self.pixel_count)
            print('Chip count      :', self.chip_count)
            print('Chip ID         :', self.chip_id)  # list of detector chip IDs
            self.detector_info = {'full_name': self.full_name, 'width': self.width, 'pixel_count': self.pixel_count,
                    'chip_count': self.chip_count, 'chip_id': self.chip_id}
            print('Initialised to ', self.demo, 'mode')
            print('Detector info: ', self.detector_info)

        return self.detector_info


    def set_acquisition_type(self, type='Frames'):
        if not self.demo:
            hardware.set_acquisition_type(device=self.device,
                                          type=type)
        else:
            print(f'demo mode, acquisition mode = {type}')
        self.settings['type'] = type


    def set_acquisition_mode(self, mode='TOATOT'):
        if not self.demo:
            hardware.set_acquisition_mode(device=self.device,
                                          mode=mode)
        else:
            print(f'demo mode, acquisition mode = {mode}')
        self.settings['mode'] = mode


    def set_number_of_frames(self, number_of_frames=1):
        if int(number_of_frames) > 0:
            self.number_of_frames = int(number_of_frames)
        else:
            self.number_of_frames = 1
        print(f'Number of frames set to {self.number_of_frames}')

        if not self.demo:
            hardware.set_number_of_frames(self.device,
                                          number_of_frames=self.number_of_frames)
        else:
            print(f'demo mode, number of frames = {number_of_frames}')
        #
        # update settings library
        self.settings['number_of_frames'] = self.number_of_frames


    def set_integration_time(self, integration_time=0.1):
        if float(integration_time) > 0:
            self.integration_time = float(integration_time)
        else:
            print('Wrong setting of integration time, setting to 0.1 sec')
            self.integration_time = 0.1
        print(f'Integration time set to {self.integration_time}')

        if not self.demo:
            hardware.set_integration_time(device=self.device,
                                          integration_time=integration_time)
        else:
            print(f'demo mode, integration time = {integration_time}')
        # update settings library
        self.settings['integration_time'] = self.integration_time


    def set_threshold_energy(self, energy_threshold_keV=2.0):
        # TODO check the maximum threshold energy, perhaps available from the device readout
        self.energy_threshold = energy_threshold_keV
        if not self.demo:
            hardware.set_threshold_energy(device=self.device,
                                          energy_threshold_keV=energy_threshold_keV)
            # device.setThreshold(0, 5, pixet.PX_THLFLAG_ENERGY) FLAG energy in keV seems to be "2"
        else:
            print(f'demo mode, Energy threshold = {energy_threshold_keV} keV')
        self.settings['energy_threshold_keV'] = self.energy_threshold


    def get_temperature(self):
        if not self.demo:
            temperature = hardware.get_temperature(device=self.device)
            temperature = round(temperature, 2)
        else:
            temperature = 278.15
        print(f'Temperature = {temperature} C')
        return temperature


    def setup_acquisition(self, type, mode, number_of_frames, integration_time, energy_threshold_keV):
        self.set_acquisition_type(type=type)
        self.set_acquisition_mode(mode=mode)
        self.set_number_of_frames(number_of_frames=number_of_frames)
        self.set_integration_time(integration_time=integration_time)
        self.set_threshold_energy(energy_threshold_keV=energy_threshold_keV)


    def acquire(self, type, mode, file_name=''):
        print('detection: acquire: mode =  ', mode)
        #
        if not self.demo: # data from the detector, not simulated data
            print('detection filename = ', file_name)
            data = hardware.acquire(device=self.device,
                                    number_of_frames=self.number_of_frames,
                                    integration_time=self.integration_time,
                                    file_name=file_name)

        #
        else: # simulated data,
            types = ['Frames', 'Pixels', 'Test pulses']
            modes = ['TOA',      'TOT',       'EVENT',       'iTOT']
            data = {'TOA': None, 'TOT': None, 'EVENT': None, 'iTOT': None}
            print('demo mode, waiting for ', self.integration_time)
            #time.sleep(self.integration_time)
            if mode == 'TOATOT' or mode == 'TOA & TOT':
                simulated_image = np.random.randint(0, 255, [256, 256])
                data['TOA'] = simulated_image
                simulated_image = np.random.randint(0, 255, [256, 256])
                data['TOT'] = simulated_image
            elif mode == 'TOA':
                simulated_image = np.random.randint(0, 255, [256, 256])
                data['TOA'] = simulated_image
            elif mode == 'EVENT_iTOT':
                simulated_image = np.random.randint(0, 255, [256, 256])
                data['EVENT'] = simulated_image
                simulated_image = np.random.randint(0, 255, [256, 256])
                data['iTOT'] = simulated_image
            elif mode == 'TOT_not_OA':
                pass

        return data





if __name__ == '__main__':
   print('detection')