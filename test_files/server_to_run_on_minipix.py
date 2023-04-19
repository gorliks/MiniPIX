import socket
import numpy as np

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)

def parse_command(command): # this functions goes to utils
    # command = "key1=val1 key2=val2"
    #command = dict(s.split("=") for s in command.split()) #{'key': 'val', 'key2': 'val2'}
    try:
        parsed = dict((key, value) for key, value in [i.split('=') for i in command.split()])
    except:
        parsed = str(command)
    return parsed

class Measurement():
    def __init__(self):
        self.frame = []
        self.data = []
        self.device_data = { 'full_name' : 'empty' }
        self.temperature = -273.
        self.settings = {
            'mode' : 'TOATOT',
            'number_of_frames' : 1,
            'integration_time' : 1.0,
            'energy_threshold_keV' : 2.0,
            'file_name' : ''
        }

    def get_device_data(self, device):
        self.full_name = device.fullName()
        self.width = device.width()
        self.pixel_count = device.pixelCount()
        self.chip_count = device.chipCount()
        self.chip_id = device.chipIDs()
        #
        self.device_data['full_name'] = self.full_name
        self.device_data['width'] = self.width
        self.device_data['pixel_count'] = self.pixel_count
        self.device_data['chip_count'] = self.chip_count
        self.device_data['chip_id'] = self.chip_id
        #
        return self.device_data


measurement = Measurement()

devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)  # pixet.devices() #pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)
print(devices)
device = devices[0]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', PORT))
server.listen(1)

while True:
    conn, addr = server.accept()
    data = conn.recv(2048)
    message = str(data)
    message = message[2:-1]
    #print('Received ', message)
    parsed = parse_command(message)
    #print( parsed )
    send_back = bytes(message, 'utf-8')

    if 'temperature?' in parsed:
        temperature = device.temperature()
        print('temperature = ', temperature)
        temperature = round(temperature, 2)
        send_back = bytes( str(temperature), 'utf-8')

    if 'info?' in parsed:
        measurement.get_device_data(device=device)
        send_back = bytes( str(measurement.device_data), 'utf-8')

    if 'mode' in parsed:
        mode = parsed['mode']
        print('mode = ', mode)
        if mode=='TOATOT': device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
        elif mode=='TOA':  device.setOperationMode(pixet.PX_TPX3_OPM_TOA)
        elif mode=='EVENT_iTOT': device.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
        elif mode=='TOT_not_OA': device.setOperationMode(pixet.PX_TPX3_OPM_TOT_NOTOA)
        else:
            print('Setting detector mode to TOATOT')
            device.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
        measurement.settings['mode'] = mode
        send_back = bytes( mode + 'set', 'utf-8')

    if 'number_of_frames' in parsed:
        number_of_frames = parsed['number_of_frames']
        number_of_frames = int(number_of_frames)
        measurement.settings['number_of_frames'] = number_of_frames
        send_back = bytes('no of frames set to' + str(number_of_frames), 'utf-8')

    if 'integration_time' in parsed:
        integration_time = parsed['integration_time']
        integration_time = float(integration_time)
        measurement.settings['integration_time'] = integration_time
        send_back = bytes('integration time set to' + str(integration_time), 'utf-8')

    if 'energy_threshold_keV' in parsed:
        energy_threshold_keV = parsed['energy_threshold_keV']
        energy_threshold_keV = float(energy_threshold_keV)
        device.setThreshold(0, energy_threshold_keV, 2)
        set_value = device.threshold(0, 2)
        print('Energy threshold = ', set_value, ' keV')
        measurement.settings['energy_threshold_keV'] = energy_threshold_keV
        send_back = bytes('energy threshold set to' + str(set_value) + ' keV', 'utf-8')

    if 'acquire' in parsed:
        file_name = parsed['acquire']
        file_name = file_name.replace( '\\\\', '/' )
        measurement.settings['file_name'] = file_name
        print('measurement settings are ', measurement.settings)
        rc = device.doSimpleAcquisition(measurement.settings['number_of_frames'],
                                             measurement.settings['integration_time'],
                                             pixet.PX_FTYPE_AUTODETECT,
                                             file_name)
        acqCount = device.acqFrameCount()
        for index in range(acqCount):
            frame = device.acqFrameRefInc(index)  # get frame with index from last acquisition series
            # get frame data to python array/list:
            data = frame.data()
            data = np.array(data)
            data = data.reshape((256, 256))
            #plt.figure(10+index)
            #plt.imshow(data, cmap='gray')

        # cannot send the matrix over to the client, send the file name instead
        send_back = bytes( str(file_name), 'utf-8')




    if 'EXIT' in message:
        print('Exiting..')
        conn.sendall( bytes('exiting', 'utf-8'))
        break

    conn.sendall(send_back)


