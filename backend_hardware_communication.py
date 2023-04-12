import sys, time
import numpy as np
import localhost_client as localhost
import utils

type_of_communication = 'hardware'
# type_of_communication = 'localhost'
# type_of_communication = 'demo'

# global, need pixet for e.g. mode definitions, pixet.PX_TPX3_OPM_TOATOT
path_to_pixet = r'C:\Program Files\PIXet Pro'
sys.path.append(path_to_pixet)
import pypixet
pixet = pypixet.pixet


def send_message_to_server(message):
    client = localhost.LocalHostClient()
    client.send_message_to_server(message)
    response = client.get_response()
    return response


def initialise(path_to_pixet):
    #
    if type_of_communication == 'hardware':
        import pypixet
        pypixet.start()
        pixet = pypixet.pixet
        print( pixet.pixetVersion() )
        devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)
        print('low level: devices = ', devices)
        if devices == []:
            print('No device connected')
            devices = ['no device connected']
    #
    elif type_of_communication == 'localhost':
        devices=[0,1,3]

    return devices


def get_detector_info(device):
    if type_of_communication == 'hardware':
        full_name   = device.fullName()
        width       = device.width()
        pixel_count = device.pixelCount()
        chip_count  = device.chipCount()
        chip_id     = device.chipIDs()
        detector_info = {'full_name': full_name, 'width': width,
                         'pixel_count': pixel_count, 'chip_count': chip_count,
                         'chip_id': chip_id}
    #
    elif type_of_communication == 'localhost':
        message = "info?"
        detector_info = \
            send_message_to_server(message)
    #
    return detector_info


def set_acquisition_type(device, type='Frames'):
    if type=='Frames':
        acquisition_type = pixet.PX_ACQTYPE_FRAMES
    elif type=='Test pulses':
        acquisition_type = pixet.PX_ACQTYPE_TESTPULSES
    else:
        acquisition_type = pixet.PX_ACQTYPE_FRAMES
    print('setting acquisition type to ', type, 'pixet = ', acquisition_type)
    return acquisition_type


def set_acquisition_mode(device, mode='TOATOT'):
    ##################################################
    if type_of_communication == 'hardware':
        if mode == 'TOATOT' or mode == 'TOA & TOT':
            print('Setting detector mode to (1) ', mode)
            device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
        elif mode == 'TOA':
            print('Setting detector mode to (2)', mode)
            device.setOperationMode(pixet.PX_TPX3_OPM_TOA)
        elif mode == 'EVENT_iTOT':
            print('Setting detector mode to (3)', mode)
            device.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
        elif mode == 'TOT_not_OA':
            print('Setting detector mode to (4)', mode)
            device.setOperationMode(pixet.PX_TPX3_OPM_TOT_NOTOA)
        else:
            print('Setting detector mode to (1) ', mode)
            device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
        response = mode + ' set'

    ##################################################
    ##################################################
    if type_of_communication == 'localhost':
        if mode == 'TOATOT' or mode == 'TOA & TOT':
            print('Setting detector mode to (1) ', mode)
            message = "mode=TOATOT"
            response = send_message_to_server(message)
        elif mode == 'TOA':
            print('Setting detector mode to (2)', mode)
            message = "mode=TOA"
            response = send_message_to_server(message)
        elif mode == 'EVENT_iTOT':
            print('Setting detector mode to (3)', mode)
            message = "mode=EVENT_iTOT"
            response = send_message_to_server(message)
        elif mode == 'TOT_not_OA':
            print('Setting detector mode to (4)', mode)
            message = "mode=TOT_not_OA"
            response = send_message_to_server(message)
        else:
            print('Setting detector mode to (1) ', mode)
            message = "mode=TOATOT"
            response = send_message_to_server(message)
            ##########################################
            ##########################################
    return response


def set_number_of_frames(device, number_of_frames=1):
    if type_of_communication == 'hardware':
        pass # send settings[] library with all the setting when needed
    if type_of_communication == 'localhost':
        message = "number_of_frames=" + str(number_of_frames)
        response = send_message_to_server(message)


def set_integration_time(device, integration_time=0.1):
    if type_of_communication == 'hardware':
        pass # send settings[] library with all the setting when needed
    if type_of_communication == 'localhost':
        message = "integration_time=" + str(integration_time)
        response = send_message_to_server(message)


def set_threshold_energy(device, energy_threshold_keV=2.0):
    if type_of_communication == 'hardware':
        device.setThreshold(0, energy_threshold_keV, 2)
        print('Energy threshold = ', device.threshold(0, 2), ' keV')
    #
    elif type_of_communication == 'localhost':
        message = "energy_threshold_keV=" + str(energy_threshold_keV)
        response = send_message_to_server(message)


def get_temperature(device):
    if type_of_communication == 'hardware':
        temperature = device.temperature()
    #
    elif type_of_communication == 'localhost':
        message = "temperature?"
        temperature = send_message_to_server(message)
    #
    return temperature


def acquire(device, number_of_frames=1, integration_time=0.1, file_name=''):
    if type_of_communication == 'hardware':
        file_name_template = file_name
        file_name = file_name + '.pmf'

        print('hardware file name = ', file_name)
        rc = device.doSimpleAcquisition(number_of_frames,
                                        integration_time,
                                        pixet.PX_FTYPE_AUTODETECT,
                                        file_name)
        #  frames are saved into a file after acquisition
        acqCount = device.acqFrameCount()  # number of measured acquisitions (frames)
        integrated_frame = np.zeros( (256, 256) )
        for index in range(acqCount):
            frame = device.acqFrameRefInc(index)  # get frame with index from last acquisition series
            # get frame data to python array/list:
            data = frame.data()
            data = np.array(data)
            data = data.reshape((256, 256))
            integrated_frame = integrated_frame + data # average frames, integrate frames
        # load data into modes and slots for plotting
        modes = ['TOA',        'TOT',       'EVENT',       'iTOT']
        DATA  = {'TOA' : None, 'TOT': None, 'EVENT': None, 'iTOT': None }
        for mode in modes:
            # the client running on the detector will acquire only images for the selected mode, e.g. TOA
            # and save the data into a file name with the key name of the mode e.g. qwert_TOA.pmf
            # the read_data_file will try to read all the time possible files *TOA.pmf, TOT.pmf etc
            # if the file is not found, the image data will be None in the returned dictionary
            # when trying to plot the data, if None, the gui will skip the plotting
            print(file_name_template + '_' + mode + '.pmf')
            data = utils.read_data_file(file_name_template + '_' + mode + '.pmf' )
            DATA[mode] = data # either np.array or None

    elif type_of_communication == 'localhost':
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


def acquire_frame(device, number_of_frames=1,
                  integration_time=0.1,
                  integral=False):
    output = -1. # initialised error to False
    # only one frame taken
    if not integral:
        output = device.doSimpleAcquisition(1,
                                        integration_time,
                                        pixet.PX_FTYPE_AUTODETECT, "")

    # integrate frames
    else:
        # does integral acquisition of N int_times frames -> sums N frames of int_times to one
        output = device.doSimpleIntegralAcquisition(number_of_frames,
                                                integration_time,
                                                pixet.PX_FTYPE_AUTODETECT, "")

        ######################### multi-frame #########################
        # rc = device.doSimpleAcquisition(number_of_frames,
        #                                 integration_time,
        #                                 pixet.PX_FTYPE_AUTODETECT,
        #                                 '')
        # integrated_frame = np.zeros((256, 256))
        # if rc==0:
        #     acqCount = device.acqFrameCount() # number of measured acquisitions (frames)
        #     print(f'acqCount = {acqCount}')
        #     for ii in range(4):
        #         frame = device.acqFrameRefInc(ii) # get frame with index from last acquisition series
        #         data = frame.data()
        #         data = np.reshape(data, (256,256))
        #         integrated_frame = integrated_frame + data
        # return integrated_frame

    if output == 0:
        # no error, get last frame
        frame = device.lastAcqFrameRefInc()
        # get frame data to python array/list:
        data = frame.data()
        data = np.reshape(data, (256, 256))
        return data
    else:
        # error happened, return empty image with zeros
        return np.zeros((256, 256))



def acquire_pixels(device, number_of_frames=1, integration_time=0.1):
    output = -1. # initialised error to False

    # pixel modes only in TOA/TOT mode
    device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)

    # TODO arbitrary number of frames
    number_of_frames = 1
    acq_type = pixet.PX_ACQTYPE_DATADRIVEN # pixet.PX_ACQTYPE_FRAMES, pixet.PX_ACQTYPE_TESTPULSES
    acq_mode = pixet.PX_ACQMODE_NORMAL # pixet.PX_ACQMODE_TRG_HWSTART, pixet.PX_ACQMODE_TDI, ...
    file_type = pixet.PX_FTYPE_AUTODETECT
    file_flags = 0
    output_file = "" #"test.pmf"
    output = \
        device.doAdvancedAcquisition(number_of_frames, integration_time,
                                     acq_type, acq_mode,
                                     file_type, file_flags, output_file)
    print(f'output = {output}')

    if output == 0:
        ######################## get tpx3 pixels ########################
        pixels = device.lastAcqPixelsRefInc()
        pixel_count = pixels.totalPixelCount()
        pixel_data = pixels.pixels()
        print("PixelCount: %d " % pixel_count)
        return np.array(pixel_data)
    else:
        # error happened, return empty image with zeros
        return np.zeros((3,1000))


def close():
    try:
        pypixet.close()
    except:
        raise


if __name__ == '__main__':
    path_to_pixet = r'C:\Program Files\PIXet Pro'
    sys.path.append(path_to_pixet)
    import pypixet

    pixet = pypixet.pixet
    pypixet.start()

    print(pixet.pixetVersion())
    devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)

    device = devices[0]
    # device.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
    device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)

    # make integral acquisition 100 frames, 0.1 s and save to file
    # device.doSimpleIntegralAcquisition(100, 0.1, pixet.PX_FTYPE_AUTODETECT, "test2.pmf")
    # make data driven acquisition for 5 seconds and save to file:
    # device.doAdvancedAcquisition(1, 1, pixet.PX_ACQTYPE_DATADRIVEN, pixet.PX_ACQMODE_NORMAL, pixet.PX_FTYPE_AUTODETECT, 0, "test.t3pa")



    # make data driven acquisition and process the pixels in the script. Note: if you want to process
    # the data online you cannot save the data in the acquisition function. You can save them later by calling
    # pixels.save()
    # acqCount = 10
    # acqTime = 0.1 # in seconds, 0.1 s
    # acqType = pixet.PX_ACQTYPE_FRAMES # pixet.PX_ACQTYPE_DATADRIVEN, pixet.PX_ACQTYPE_TESTPULSES
    # acqMode = pixet.PX_ACQMODE_NORMAL # pixet.PX_ACQMODE_TRG_HWSTART, pixet.PX_ACQMODE_TDI, ...
    # fileType = pixet.PX_FTYPE_AUTODETECT
    # fileFlags = 0
    # outputFile = "test.pmf"
    # device.doAdvancedAcquisition(acqCount, acqTime, acqType, acqMode, fileType, fileFlags, outputFile)
    #

    device.doAdvancedAcquisition(10, 0.1, pixet.PX_ACQTYPE_DATADRIVEN, pixet.PX_ACQMODE_NORMAL, pixet.PX_FTYPE_AUTODETECT, 0, "")

    TPX3_INDEX = 0
    TPX3_TOT = 1
    TPX3_TOA = 2

    # get tpx3 pixels:
    pixels = device.lastAcqPixelsRefInc()
    pixelCount = pixels.totalPixelCount()
    pixelData = pixels.pixels()
    print("PixelCount: %d " % pixelCount)

    # get first pixel values:
    matrixIndex = pixelData[TPX3_INDEX][0]
    event = pixelData[TPX3_TOT][0]
    itot = pixelData[TPX3_TOA][0]

    # get second pixel values:
    matrixIndex = pixelData[TPX3_INDEX][1]
    event = pixelData[TPX3_TOT][1]
    itot = pixelData[TPX3_TOA][1]

    # save data to a file
    pixels.save("/tmp/test2.t3pa", pixet.PX_FTYPE_AUTODETECT, 0)

    pixels.destroy()