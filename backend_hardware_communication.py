import sys, time
import numpy as np
import localhost_client as localhost
import utils


def send_message_to_server(message):
    client = localhost.LocalHostClient()
    client.send_message_to_server(message)
    response = client.get_response()
    return response

def initialise(device):
    # hardware
    # full_name = device.fullName()
    # width = device.width()
    # pixel_count = device.pixelCount()
    # chip_count = device.chipCount()
    # chip_id = device.chipIDs()
    # detector_info = {'full_name' : full_name, 'width' : width,
    #                'pixel_count' : pixel_count, 'chip_count' : chip_count,
    #                'chip_id' : chip_id }
    ### localhost :
    message = "info?"
    detector_info = send_message_to_server(message)
    return detector_info

def set_acquisition_mode(device, mode='TOATOT'):
    if mode == 'TOATOT' or mode == 'TOA & TOT':
        print('Setting detector mode to (1) ', mode)
        message = "mode=TOATOT"
        response = send_message_to_server(message)
        ##########################################
        #hardware option
        #device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
    elif mode == 'TOA':
        print('Setting detector mode to (2)', mode)
        message = "mode=TOA"
        response = send_message_to_server(message)
        ##########################################
        #hardware option
        #device.setOperationMode(pixet.PX_TPX3_OPM_TOA)
    elif mode == 'EVENT_iTOT':
        print('Setting detector mode to (3)', mode)
        message = "mode=EVENT_iTOT"
        response = send_message_to_server(message)
        ##########################################
        #hardware option
        #device.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
    elif mode == 'TOT_not_OA':
        print('Setting detector mode to (4)', mode)
        message = "mode=TOT_not_OA"
        response = send_message_to_server(message)
        ##########################################
        #hardware option
        #device.setOperationMode(pixet.PX_TPX3_OPM_TOT_NOTOA)
    else:
        print('Setting detector mode to (1) ', mode)
        message = "mode=TOATOT"
        response = send_message_to_server(message)
        ##########################################
        #hardware option
        #device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
    return response


def set_number_of_frames(device, number_of_frames=1):
    message = "number_of_frames=" + str(number_of_frames)
    response = send_message_to_server(message)

def set_integration_time(device, integration_time=0.1):
    message = "integration_time=" + str(integration_time)
    response = send_message_to_server(message)

def set_threshold_energy(device, energy_threshold_keV=2.0):
    #hardware option
    #device.setThreshold(0, energy_threshold_keV, 2)
    #print('Energy threshold = ', device.threshold(0, 2), ' keV')
    #
    message = "energy_threshold_keV=" + str(energy_threshold_keV)
    response = send_message_to_server(message)

def get_temperature(device):
    message = "temperature?"
    temperature = send_message_to_server(message)
    return temperature
    #
    #hardware
    #temperature = device.temperature()
    #return temperature


def acquire(device, number_of_frames=1, integration_time=0.1, file_name=''):
    # data = np.random.randint(0, 255, [256, 256])
    message = 'acquire=' + file_name
    response_file_name = send_message_to_server(message)
    response_file_name = str( response_file_name )
    response_file_name = response_file_name.replace('.pmf', '')

    modes = ['TOA',        'TOT',       'EVENT',       'iTOT']
    DATA  = {'TOA' : None, 'TOT': None, 'EVENT': None, 'iTOT': None }
    for mode in modes:
        # the client running on the detector will acquire only images for the selected mode, e.g. TOA
        # and save the data into a file name with the key name of the mode e.g. qwert_TOA.pmf
        # the read_data_file will try to read all the time possible files *TOA.pmf, TOT.pmf etc
        # if the file is not found, the image data will be None in the returned dictionary
        # when trying to plot the data, if None, the gui will skip the plotting
        print(response_file_name + '_' + mode + '.pmf')
        data = utils.read_data_file( response_file_name + '_' + mode + '.pmf' )
        DATA[mode] = data # either np.array or None
    return DATA

    #
    #hardware
    #rc = self.device.doSimpleAcquisition(number_of_frames,
    #                                     integration_time,
    #                                     pixet.PX_FTYPE_AUTODETECT,
    #                                     file_name)
    #acqCount = self.device.acqFrameCount()  # number of measured acquisitions (frames)
    #for index in range(acqCount):
    #   frame = self.device.acqFrameRefInc(index)  # get frame with index from last acquisition series
    #   # get frame data to python array/list:
    #   data = frame.data()
    #   data = np.array(data)
    #   data = data.reshape((256, 256))
    #return data



