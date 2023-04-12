import sys, time
import numpy as np
import matplotlib.pyplot as plt

path_to_pixet = r'C:\Program Files\PIXet Pro'
sys.path.append(path_to_pixet)
import pypixet
pixet = pypixet.pixet

pypixet.start()

devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)
print('low level: devices = ', devices)

if devices == []:
    print('No device connected')
    devices = ['no device connected']


device = devices[0]


def get_temperature(device):
    temperature = device.temperature()
    return temperature


full_name = device.fullName()
width = device.width()
pixel_count = device.pixelCount()
chip_count = device.chipCount()
chip_id = device.chipIDs()
detector_info = {'full_name': full_name, 'width': width,
                 'pixel_count': pixel_count, 'chip_count': chip_count,
                 'chip_id': chip_id}
print(detector_info)


mode1 = 'Frames'
if mode1 == 'Frames':
    acquisition_type = pixet.PX_ACQTYPE_FRAMES
if mode1 == 'Test pulses':
    acquisition_type = pixet.PX_ACQTYPE_TESTPULSES
else:
    acquisition_type = pixet.PX_ACQTYPE_FRAMES
print('setting acquisition type to ', mode1, 'pixet = ', acquisition_type)


#mode2 = 'EVENT_iTOT'
mode2 = 'TOATOT'

if mode2 == 'TOATOT' or mode2 == 'TOA & TOT':
    print('Setting detector mode to (1) ', mode2)
    device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
elif mode2 == 'TOA':
    print('Setting detector mode to (2)', mode2)
    device.setOperationMode(pixet.PX_TPX3_OPM_TOA)
elif mode2 == 'EVENT_iTOT':
    print('Setting detector mode to (3)', mode2)
    device.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
elif mode2 == 'TOT_not_OA':
    print('Setting detector mode to (4)', mode2)
    device.setOperationMode(pixet.PX_TPX3_OPM_TOT_NOTOA)
else:
    print('Setting detector mode to (1) ', mode2)
    device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)


print(f'Temperature = {get_temperature(device)}')

# device.setBias(100)  # sets detector bias voltage to 100 V
print(device.bias())  # return device bias volage (set value)


if 0: # SIMPLE ACQUISITION
    number_of_frames = 1
    integration_time = 0.5
    energy_threshold_keV = 2.2
    device.setThreshold(0, energy_threshold_keV, 2)
    rc = device.doSimpleAcquisition(number_of_frames,
                                    integration_time,
                                    pixet.PX_FTYPE_AUTODETECT,
                                    '')


if 1:
    number_of_frames = 5
    integration_time = 0.5
    energy_threshold_keV = 1.5
    device.setThreshold(0, energy_threshold_keV, 2)
    print('Energy threshold = ', device.threshold(0, 2), ' keV')

    rc = device.doSimpleAcquisition(number_of_frames,
                                    integration_time*5,
                                    pixet.PX_FTYPE_AUTODETECT, "")
    print("Acquition: %d" % rc)

    # multi-frame
    # acqCount = device.acqFrameCount() # number of measured acquisitions (frames)
    # print(f'acqCount = {acqCount}')
    # for ii in range(4):
    #     frame = device.acqFrameRefInc(ii) # get frame with index from last acquisition series
    #     data = frame.data()
    #     data = np.reshape(data, (256,256))
    #     plt.subplot(2,2,ii+1)
    #     plt.imshow(data)


    # get last frame
    frame = device.lastAcqFrameRefInc()


    # get frame data to python array/list:
    data = frame.data()

    data = np.reshape(data, (256,256))

    plt.imshow(data)

    frame.destroy() # release the frame






def acqExample6():
    device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)

    energy_threshold_keV = 1.5
    device.setThreshold(0, energy_threshold_keV, 2)
    print('Energy threshold = ', device.threshold(0, 2), ' keV')

    print(f'Temperature = {get_temperature(device)}')

    # device.setBias(100)  # sets detector bias voltage to 100 V
    print(device.bias())  # return device bias volage (set value)


    number_of_frames = 1
    integration_time = 1 # in seconds, 0.1 s
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

    ######################## get tpx3 pixels ########################
    pixels = device.lastAcqPixelsRefInc()
    pixel_count = pixels.totalPixelCount()
    pixel_data = pixels.pixels()
    print("PixelCount: %d " % pixel_count)


    ######################## get first pixel values ########################
    matrix_index = pixel_data[0][0]
    tot = pixel_data[1][0]
    toa = pixel_data[2][0]
    print(matrix_index, tot, toa)

    ######################## get second pixel values ########################
    matrix_index = pixel_data[0][1]
    tot = pixel_data[1][1]
    toa = pixel_data[2][1]
    print(matrix_index, tot, toa)

    # save data to a file
    # pixels.save("test_1_toa_tot.t3pa", pixet.PX_FTYPE_AUTODETECT, 0)

    ####################################################################################################################

    print(max(pixel_data[0]),
          max(pixel_data[1]),
          max(pixel_data[2]),
          max(pixel_data[0]))

    indices = pixel_data[0][:]
    TOA     = pixel_data[1][:]
    TOT     = pixel_data[2][:]

    indices = np.array(indices)
    TOT = np.array(TOT)
    TOA = np.array(TOA)
    print(f'max TOA = {TOA.max()}')
    print(f'max TOT = {TOT.max()}')
    print(f'max time = {TOA.max()/1e9} sec')


    toa_integral = np.zeros(256*256)
    tot_integral = np.zeros(256*256)


    # for ind in indices:
    #     toa_integral[ind] += TOA[ind]
    #     tot_integral[ind] += TOT[ind]
    for ii in range(len(indices)):
        pixel_index = indices[ii]
        toa_integral[pixel_index] += TOA[ii]
        tot_integral[pixel_index] += TOT[ii]

    toa_integral = np.reshape(toa_integral, (256, 256))
    tot_integral = np.reshape(tot_integral, (256, 256))

    plt.subplot(1, 2, 1)
    plt.imshow(toa_integral, cmap='gray')
    plt.colorbar()
    plt.title("TOA")
    #
    plt.subplot(1, 2, 2)
    plt.imshow(np.log(tot_integral), cmap='gray')
    plt.colorbar()
    plt.title("TOT")
    #
    plt.show()



    NN = int(TOT.max())
    n_x, bins_x, patches_x = plt.hist(TOA, NN)




    pixels.destroy()