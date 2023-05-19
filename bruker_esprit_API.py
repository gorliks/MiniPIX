import ctypes
import sys
import time, datetime
import numpy as np
import matplotlib.pyplot as plt
from utils import MicroscopeState

# from importlib import reload  # Python 3.4+
# reload(utils)

#path_to_dll = r'F:\SharedData\MCEM Data - Staff Only\Bruker API\Esprit API\Bruker.API.Esprit64.dll'
path_to_dll = r'C:\Users\sergeyg\Github\Bruker Nano APIs\Esprit API\Bruker.API.Esprit64.dll'

AnsiChar = ctypes.c_char * 8
PAnsiChar = ctypes.POINTER(AnsiChar)

# TOpenClientOptions = packed record // structure to describe Quantax start options in ‘OpenClientEx’
# Version: integer; // Version of record structure, should be 'l' at the moment
# GUIMode: integer; // '0' = no GUI, '1' = full GUI, '2' = reduced GUI (spectrum chart only)
# StartNew: boolean; // start new instance of Quantax end;
# POpenClientOptions = ^ TOpenClientOptions;
class TOpenClientOptions(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Version',  ctypes.c_uint32),
        ('GUIMode',  ctypes.c_uint32),
        ('StartNew', ctypes.c_bool),
        ('IdentifierLength', ctypes.c_int8),
        ('TCPHost', ctypes.c_char * 64),
        ('TCPPort', ctypes.c_uint16)
    ]

class TPoint(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('X', ctypes.c_uint32),
        ('Y', ctypes.c_uint32)
    ]
TPointArray = TPoint * 16382
PPointArray = ctypes.POINTER(TPointArray)


# pixelsize = um/pixel
class TRTImageInfoEx(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Magnification',   ctypes.c_int32),
        ('PixelSizeX',      ctypes.c_double),
        ('PixelSizeY',      ctypes.c_double),
        ('HighVoltage',     ctypes.c_double),
        ('WorkingDistance', ctypes.c_double)
    ]
# typedef TRTImageInfoEx* PRTImageInfoEx;


# Y value of segment
# XStart : x start position on that line
# XCount : number of contiguous pixels
# in Delphi TRTSegment = packed record
class TSegment(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Y'     , ctypes.c_uint32),
        ('XStart', ctypes.c_uint32),
        ('XCount', ctypes.c_uint32)
    ]

# struct TRTSpectrumHeaderRec {
# 	unsigned __int8 IdentifierLength;
# 	char Identifier[25];			// 'Rontec XRay spectrum'
# 	int32_t Version;				// Version information
# 	int32_t Size;					// Size in byte
# 	double DateTime;				// Delphi 5.0 version of date and time
# 	int32_t ChannelCount;			//
# 	int32_t ChannelOffset;			// First channel index
# 	double CalibrationAbs;			// Energy of first channel
# 	double CalibrationLin;          // keV per channel
# 	double SigmaAbs;				// Sigma^2 energy calibration
# 	double SigmaLin;
# 	// additional data compared to normal Roentec header
# 	int32_t RealTime;					// real measure time in ms
# 	int32_t LifeTime;					// life time in ms
# };
# #pragma pack(pop)

id = ' ' * 25  # char Identifier[25];
id = id.encode('utf-8')  # bytes, reference, char*
class TRTSpectrumHeaderRec(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Identifier', ctypes.c_char_p*25),
        ('Version', ctypes.c_uint32),
        ('Size', ctypes.c_uint32),
        ('DateTime', ctypes.c_double),
        ('ChannelCount', ctypes.c_uint32),
        ('ChannelOffset', ctypes.c_uint32),
        ('CalibrationAbs', ctypes.c_double),
        ('CalibrationLin', ctypes.c_double),
        ('SigmaAbs', ctypes.c_double),
        ('SigmaLin', ctypes.c_double),
        ('RealTime', ctypes.c_uint32),
        ('LifeTime', ctypes.c_uint32)
    ]


def print_spectrum_header(spectrum_header : TRTSpectrumHeaderRec):
    print(f'Version: {spectrum_header.Version}')
    print(f'Size   :  {spectrum_header.Size}')
    print(f'ChannelCount   :  {spectrum_header.ChannelCount}')
    print(f'RealTime       :  {spectrum_header.RealTime}')


errors = {-1 : 'IFC_ERROR_IN_EXECUTION',
         -2 : 'IFC_ERROR_WRONG_PARAMETER (execution)',
         -3 : 'IFC_ERROR_SPECTRUM_BUFFER_EMPTY',
         -4 : 'IFC_ERROR_PARAMETER_MISSED',
         -5 : 'IFC_ERROR_TOO_MANY_PARAMETERS',
         -6 : 'IFC_ERROR_USER_TERMINATED',
         -7 : 'IFC_ERROR_TIMEOUT',
         -8 : 'IFC_ERROR_UNKNOWN_VALUE_NAME',
         -9 : 'IFC_ERROR_WRONG_VALUE_TYPE',
         -10 : 'IFC_ERROR_NO_LICENCE',
         -11 : 'IFC_ERROR_RESULT_BUFFER_INSUFFICIENT',
         -12 : 'IFC_ERROR_HARDWARE_LOCKED',
         -51: 'IFS_ERROR_PARAMETER_MISSED',
         -52 : 'IFS_ERROR_FUNCTION_NOT_IMPLEMENTED',
         -21 : 'CONN_ERROR_UNKNOWN',
         -22 : 'CONN_ERROR_INTERFACE_NOT_CONNECTED',
         -23 : 'CONN_ERROR_PARAMETER_MISSED',
         -24 : 'CONN_ERROR_ANSWER_TIMEOUT',
         -25 : 'CONN_ERROR_SERVER_NOT_RESPONDING',
         -26 : 'CONN_ERROR_RESULT_MISSED',
         -27 : 'CONN_ERROR_NO_INTERFACE',
         -28 : 'CONN_ERROR_INVALID_LOGIN',
         -29 : 'CONN_ERROR_NO_CONNECTION_TO_SERVER',
         -30 : 'CONN_ERROR_SERVER',
         -31 : 'CONN_ERROR_ACTION_ABORTED',
         -101 : 'ERROR_WRONG_PARAMETER',
         -102 : 'ERROR_FILE_NOT_EXIST',
         -103 : 'ERROR_INVALID_CONNECTION',
         -104 : 'ERROR_NO_ANSWER',
         -105 : 'ERROR_CAN_NOT_START_PROCESS',
         -106 : 'ERROR_INVALID_RESULT_DATA',
         -107 : 'ERROR_SETTINGS_NOT_FOUND',
         -108 : 'ERROR_INVALID_SERVER_CONNECTION',
         -109 : 'ERROR_IN_EXECUTION',
         -110 : 'ERROR_IFC_BUSY',
         -201 : 'STATE_WAS_RUNNING_BEFORE',
         -232 : 'No Error Description Available',
         +232 : 'No Error Description Available',
}


header = []
for ii in range(255):
    header.append(ii)
    header.append(ii)
    header.append(ii)
    header.append(0)
header = np.array(header)



class Bruker_Esprit():
    def __init__(self, demo):
        self.demo = demo

        self.path_to_dll = path_to_dll

        self.pServer = ''.encode('utf-8') # Pointer to a server name (if empty the local/default server is referenced)

        self.User = 'edx'
        self.pUser = self.User.encode('utf-8')

        self.password = 'edx'
        self.pPassword = self.password.encode('utf-8')

        self.host = '127.0.0.1' # 'local host'
        self.pHost = self.host.encode('utf-8')

        self.port = ctypes.c_uint16(0)

        self.Options = TOpenClientOptions()
        self.Options.Version = 1
        self.Options.GUIMode = 1 # GUIMode: integer; // ‘0’ = no GUI, ‘1’ = full GUI, ‘2’ = reduced GUI (spectrum chart only)
        self.Options.StartNew = True # If true, function starts always a new client instance
        self.Options.IdentifierLength = 8 # ???
        self.Options.TCPHost = self.host.encode('utf-8')
        self.Options.TCPport = self.port
        self.Options_ptr = ctypes.pointer(self.Options)

        self.StartNew = False # If true, function starts always a new client instance
        self.GUI      = True # When true client screen is shown, otherwise hidden (only valid at first start of client)

        self.CID = ctypes.c_uint32(123456)       # Identification code for an actual server/client instance
        self.CID_ptr = ctypes.pointer(self.CID)  # Pointer to Identification code for an actual server/client instance

        self.error_message = ''

        self.beam_x_pos = 0
        self.beam_y_pos = 0

        self.microscope_state = MicroscopeState()

        try:
            self.esprit = ctypes.cdll.LoadLibrary(path_to_dll)
            print(path_to_dll, self.esprit)
        except:
            self.error_message = f'path to dll {path_to_dll} does not exist'
            print(self.error_message + '\n')


    def initialise(self, type='Ex'):
        # Starting an application requires a valid password. References to a connection takes place
        # always via an identification code (CID) delivered by the OpenClient function.
        # int32_t OpenClient(   char* pServer, char* pUser, char* pPassword, bool StartNew, bool GUI, uint32_t& CID)
        # int32_t OpenClientTCP(char* pServer, char* pUser, char* pPassword, char* pHost, unsigned  __int16 Port, const TOpenClientOptions Options, uint32_t & CID);
        # int32_t OpenClientEx(char * pServer, char* pUser, char* pPassword, const TOpenClientOptions & Options, uint32_t & CID);
        #
        if self.demo is not True:
            if type=='direct':
                print('Connecting directly to the client')
                output = \
                    self.esprit.OpenClient(self.pServer, self.pUser, self.pPassword, self.StartNew, self.GUI, self.CID_ptr)
            elif type=='Ex':
                print('Connecting to the client : external mode')
                output = \
                    self.esprit.OpenClientEx(self.pServer, self.pUser, self.pPassword, self.StartNew, self.GUI, self.CID_ptr)
            elif type == 'TCP':
                print('Connecting to the client : TCP mode')
                output = \
                    self.esprit.OpenClientTCP(self.pServer, self.pUser, self.pPassword, self.pHost, self.port, self.Options, self.CID_ptr)
            else:
                print('Connecting to the client : external mode')
                output = self.esprit.OpenClientEx(self.pServer, self.pUser, self.pPassword, self.Options_ptr, self.CID_ptr)
            #
            print(f'after : Connection identification code = {self.CID}')
            if output==0:
                print('Connection established successfully\n')
                self.error_message = ''
                # TODO get all the SEM info, current stage coordinates, beam current, etc
            else:
                self.error_message = f'No connection established, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')


        elif self.demo is True:
            print('This is demo mode: Connection establishment procedure called\n')
            self.error_message = ''
            # TODO get all the SEM info, current stage coordinates, beam current, etc


    def reset_communication(self):
        output = \
            self.esprit.ResetSEMCommunication(self.CID)

        if output==0:
            print('Communication reset successfully\n')
            self.error_message = ''
        else:
            self.error_message = f'Communication reset unsuccessful, ERROR code is {output}, {errors[output]}'
            print( self.error_message + '\n')


    def get_servers_info(self):
        # int32_t QueryInfo(uint32_t CID, char* pInfo, int32_t BufSize);
        # Delivers info about a client/server instance

        if self.demo is not True:
            buffer_size = ctypes.c_int32(999)
            query = ' ' * 1000 # block of memory for 1000 characters
            self.query = query.encode('utf-8') # bytes, reference, char*

            output = \
                self.esprit.QueryInfo(self.CID, self.query, buffer_size)

            if output==0:
                print('SEM servers/client: ', str(self.query), '\n')
                self.error_message = ''
            else:
                self.error_message = f'No SEM servers/clients info could be fetched, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:
            print('This is demo mode: SEM servers/client query ')
            self.error_message = ''


    def close(self):
        if self.demo is not True:
            self.esprit.CloseClient(self.CID)
        else:
            print('This is demo mode: closing client')


    ####################################################################################################################
    ########################################     Getting info     ######################################################
    ####################################################################################################################


    def get_sem_data(self):
        # int32_t GetSEMData(uint32_t CID, double& Magnification, double& HighVoltage, double& WorkingDistance)

        self.mag = ctypes.c_double(0) # magnification
        self.high_voltage  = ctypes.c_double(0) # high voltage in keV
        self.working_distance  = ctypes.c_double(0) # working distance in mm
        # Pointers
        self.mag_ptr = ctypes.pointer(self.mag)
        self.high_voltage_ptr = ctypes.pointer(self.high_voltage)
        self.working_distance_ptr = ctypes.pointer(self.working_distance)

        if self.demo is not True:

            output = \
                self.esprit.GetSEMData(self.CID, self.mag_ptr, self.high_voltage_ptr, self.working_distance_ptr)

            if output==0:
                self.error_message = ''
                print('SEM data retrieved successfully\n')
                print(f'mag = {self.mag.value}, HV = {self.high_voltage.value}, WD = {self.working_distance.value}')
            else:
                self.error_message = f'No SEM data could be fetched, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        else:
            self.error_message = ''
            print('This is demo mode: SEM data retrieve')
            print(f'mag = {self.mag.value}, HV = {self.high_voltage.value}, WD = {self.working_distance.value}')


    def get_sem_info(self):
        # int32_t GetSEMInfo(uint32_t CID, char* Info, int32_t BufSize)
        ################################################################
        # Info := '';
        # SetLength(Info, 1000);
        # GetSEMInfo(FCID, PAnsiChar(Info), 999);
        buffer_size = ctypes.c_int32(999)
        info = ' ' * 1000 # block of memory for 1000 characters
        self.Info = info.encode('utf-8') # bytes, reference, char*

        if self.demo is not True:

            output = \
                self.esprit.GetSEMInfo(self.CID, self.Info, buffer_size)

            if output==0:
                self.error_message = ''
                print('SEM Info: ', str(self.Info), '\n')
            else:
                self.error_message = f'No SEM info could be fetched, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:

            self.error_message = ''
            print('This is demo mode: SEM Info ', str(self.Info), '\n')


    def get_sem_capabilities(self):
        # int32_t GetSEMCapabilities(uint32_t CID, char* Capabilities, int32_t BufSize)
        # Gets the microscope capability of reading and writing of parameters and the available options
        buffer_size = ctypes.c_int32(999)
        capabilities = ' ' * 1000 # block of memory for 1000 characters
        self.capabilities = capabilities.encode('utf-8') # bytes, reference, char*

        if self.demo is not True:

            output = \
                self.esprit.GetSEMCapabilities(self.CID, self.capabilities, buffer_size)

            if output==0:
                self.error_message = ''
                print('SEM Capabilities: ', str(self.capabilities), '\n')
            else:
                self.error_message = f'No SEM capabilities could be fetched, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:

            self.error_message = ''
            print('This is demo mode: SEM Capabilities ', str(self.capabilities), '\n')


    def get_sem_brightness_and_contrast(self):
        # int32_t GetSEMBCData(uint32_t CID, double& Brightness, double& Contrast)
        self.brightness = ctypes.c_double(0.0) # magnification
        self.contrast   = ctypes.c_double(0.0) # high voltage in keV
        self.brightness_ptr = ctypes.pointer(self.brightness)
        self.contrast_ptr = ctypes.pointer(self.contrast)

        if self.demo is not True:

            output = \
                self.esprit.GetSEMBCData(self.CID, self.brightness_ptr, self.contrast_ptr)

            if output==0:
                self.error_message = ''
                print('SEM data retrieved successfully\n')
                print(f'brightness = {self.brightness.value}, contrast = {self.contrast.value}')
            else:
                self.error_message = f'No SEM data could be fetched, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:

            self.error_message = ''
            print('This is demo mode: SEM data retrieve')
            print(f'brightness = {self.brightness.value}, contrast = {self.contrast.value}')


    def get_sem_probe_current(self):
        # int32_t GetSEMProbeCurrent(uint32_t CID, double& ProbeCurrent)
        self.probe_current = ctypes.c_double(0) # probe current
        self.probe_current_ptr = ctypes.pointer(self.probe_current)

        if self.demo is not True:

            output = \
                self.esprit.GetSEMProbeCurrent(self.CID, self.probe_current_ptr)

            if output==0:
                self.error_message = ''
                print('SEM probe current retrieved successfully\n')
                print(f'probe current = {self.probe_current.value}')
            else:
                self.error_message = f'No SEM probe current could be fetched, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:

            self.error_message = ''
            print('This is demo mode: SEM probe current retrieve')
            print(f'probe current = {self.probe_current.value}')




    def get_sem_spot_size(self):
        # int32_t GetSEMSpotSize(uint32_t CID, double& SpotSize)
        self.spot_size = ctypes.c_double(0)
        self.spot_size_ptr = ctypes.pointer(self.spot_size)

        if self.demo is not True:

            output = \
                self.esprit.GetSEMSpotSize(self.CID, self.spot_size_ptr)

            if output==0:
                self.error_message = ''
                print('SEM spot size retrieved successfully\n')
                print(f'spot size = {self.spot_size.value}')
            else:
                self.error_message = f'No SEM spot size could be fetched, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:
            self.error_message = ''
            print('This is demo mdoe: SEM spot size retrieve')
            print(f'spot size = {self.spot_size.value}')



    def get_sem_stage_position(self):
        # int32_t  GetSEMStageData(uint32_t CID, double & XPos, double & YPos, double & ZPos, double & Tilt, double & Rotation)
        self.x_pos = ctypes.c_double(0) # x, mm
        self.y_pos = ctypes.c_double(0) # y, mm
        self.z_pos = ctypes.c_double(0) # z, mm
        self.t_pos = ctypes.c_double(0) # tilt, deg
        self.r_pos = ctypes.c_double(0) # rotation, deg
        self.x_pos_ptr = ctypes.pointer(self.x_pos)
        self.y_pos_ptr = ctypes.pointer(self.y_pos)
        self.z_pos_ptr = ctypes.pointer(self.z_pos)
        self.t_pos_ptr = ctypes.pointer(self.t_pos)
        self.r_pos_ptr = ctypes.pointer(self.r_pos)


        if self.demo is not True:

            output = \
                self.esprit.GetSEMStageData(self.CID,
                                            self.x_pos_ptr, self.y_pos_ptr, self.z_pos_ptr,
                                            self.t_pos_ptr, self.r_pos_ptr)
            if output==0:
                self.error_message = ''
                print(f'SEM position is: x,y,z: ({self.x_pos.value}, {self.y_pos.value}, {self.z_pos.value});'
                      f' tilt: {self.t_pos.value};  rotation: {self.r_pos.value}\n')
            else:
                self.error_message = f'No SEM stage info could be fetched, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:

            self.error_message = ''
            print(f'Demo mode: SEM position is: x,y,z: ({self.x_pos.value}, {self.y_pos.value}, {self.z_pos.value});'
                  f' tilt: {self.t_pos.value};  rotation: {self.r_pos.value}\n')



    def get_sem_stage_range(self):
        # int32_t GetSEMStageRange(uint32_t CID, double& Xmin, double& Xmax, double& Ymin, double& Ymax, double& Zmin, double& Zmax, double& Tmin, double& Tmax, double& Rmin, double& Rmax)
        self.x_min = ctypes.c_double(0) #
        self.x_max = ctypes.c_double(0) #
        self.y_min = ctypes.c_double(0) #
        self.y_max = ctypes.c_double(0) #
        self.z_min = ctypes.c_double(0) #
        self.z_max = ctypes.c_double(0) #
        self.t_min = ctypes.c_double(0) #
        self.t_max = ctypes.c_double(0) #
        self.r_min = ctypes.c_double(0) #
        self.r_max = ctypes.c_double(0) #

        self.x_min_ptr = ctypes.pointer(self.x_min)
        self.x_max_ptr = ctypes.pointer(self.x_max)
        self.y_min_ptr = ctypes.pointer(self.y_min)
        self.y_max_ptr = ctypes.pointer(self.y_max)
        self.z_min_ptr = ctypes.pointer(self.z_min)
        self.z_max_ptr = ctypes.pointer(self.z_max)
        self.t_min_ptr = ctypes.pointer(self.t_min)
        self.t_max_ptr = ctypes.pointer(self.t_max)
        self.r_min_ptr = ctypes.pointer(self.r_min)
        self.r_max_ptr = ctypes.pointer(self.r_max)


        if self.demo is not True:

            output = \
                self.esprit.GetSEMStageRange(self.CID,
                                             self.x_min_ptr, self.x_max_ptr,
                                             self.y_min_ptr, self.y_max_ptr,
                                             self.z_min_ptr, self.z_max_ptr,
                                             self.t_min_ptr, self.t_max_ptr,
                                             self.r_min_ptr, self.r_max_ptr)

            if output==0:
                self.error_message = ''
                print(f'SEM stage limits are '
                      f'X:({self.x_min.value}, {self.x_max.value}); '
                      f'Y:({self.y_min.value}, {self.y_max.value}), '
                      f'Z:({self.z_min.value}, {self.z_max.value}); '
                      f'tilt: ({self.t_min.value}, {self.t_max.value});'
                      f'rotation: ({self.r_min.value}, {self.r_max.value})\n')
            else:
                self.error_message = f'No SEM stage limits could be retrieved, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:

            self.error_message = ''
            print(f'Demo mode: SEM stage limits are '
                  f'X:({self.x_min.value}, {self.x_max.value}); '
                  f'Y:({self.y_min.value}, {self.y_max.value}), '
                  f'Z:({self.z_min.value}, {self.z_max.value}); '
                  f'tilt: ({self.t_min.value}, {self.t_max.value});'
                  f'rotation: ({self.r_min.value}, {self.r_max.value})\n')



    def get_field_width(self):
        #int32_t ImageGetFieldWidth(uint32_t CID, double & FieldWidth)
        # Reads image field width from scan settings and SEM mag.
        self.field_width = ctypes.c_double(0)  # Width of the scanned area in mm
        self.field_width_ptr = ctypes.pointer(self.field_width)

        if self.demo is not True:

            output = \
                self.esprit.ImageGetFieldWidth(self.CID, self.field_width_ptr)

            if output==0:
                self.error_message = ''
                print(f'Field width = {self.field_width.value}\n')
            else:
                self.error_message = f'Field width could not be obtained, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:
            self.error_message = ''
            print(f'demo mode: Field width = {self.field_width.value}\n')



    def get_current_microscope_state(self) -> MicroscopeState:
        """Acquires the current microscope state to store
         if necessary it is possible to return to this stored state later
         Returns the state in MicroscopeState dataclass variable
        Args:
            None
        Returns
        -------
        MicroscopeState
        """
        try:
            self.get_sem_info()
            self.microscope_state.sem_info = self.Info
            #
            self.get_sem_capabilities()
            self.microscope_state.sem_capabilities = self.capabilities
            #
            self.get_sem_data()
            self.microscope_state.hv = self.high_voltage.value
            self.microscope_state.mag = self.mag.value
            self.microscope_state.working_distance = self.working_distance.value
            #
            self.get_sem_brightness_and_contrast()
            self.microscope_state.brightness = self.brightness.value
            self.microscope_state.contrast = self.contrast.value
            #
            self.get_sem_probe_current()
            self.microscope_state.beam_current = self.probe_current.value
            #
            self.get_sem_spot_size()
            self.microscope_state.spot_size = self.spot_size.value
            #
            self.get_sem_stage_position()
            self.microscope_state.x = self.x_pos.value
            self.microscope_state.y = self.y_pos.value
            self.microscope_state.z = self.z_pos.value
            self.microscope_state.t = self.t_pos.value
            self.microscope_state.r = self.r_pos.value
            #
            self.get_field_width()
            self.microscope_state.horizontal_field_width = self.field_width.value
            #
            self.get_image_configuration()
            self.microscope_state.width = self.width.value
            self.microscope_state.height = self.height.value


        except Exception as e:
            print(f"Could not get the microscope state, error {e}")
            self.microscope_state.x = 0
            self.microscope_state.y = 0
            self.microscope_state.z = 0
            self.microscope_state.t = 0
            self.microscope_state.r = 0

        return self.microscope_state



    ####################################################################################################################
    ##########################################     Settings     ########################################################
    ####################################################################################################################


    def set_sem_parameters(self, mag=0, high_voltage=0, working_distance=0):
        #### Result := SetSEMData(FCID,Mag,HV,WD); to set three values simultanelously
        # int32_t SetSEMData(uint32_t CID, double Magnification, double HighVoltage, double WorkingDistance)
        self.get_sem_data() # get current mag, hv, wd
        if mag:
            mag = ctypes.c_double(mag) # if mag parameter provided, use it
        else:
            mag = self.mag # otherwise, use the current value on the machine
        if high_voltage:
            high_voltage = ctypes.c_double(high_voltage)
        else:
            high_voltage = self.high_voltage
        if working_distance:
            working_distance = ctypes.c_double(working_distance)
        else:
            working_distance = self.working_distance

        output = \
            self.esprit.SetSEMData(self.CID, mag, high_voltage, working_distance)

        self.get_sem_data() # get current mag, hv, wd; update the stored values

        if output==0:
            self.error_message = ''
            print(f'SEM set to: mag={self.mag.value}, hv={self.high_voltage.value}, wd={self.working_distance.value}')
        else:
            self.error_message = f'No success in setting the SEM mag, HV, WD; ERROR code is {output}, {errors[output]}'
            print( self.error_message + '\n')


    ### TODO: this function does not work : -2 : 'IFC_ERROR_WRONG_PARAMETER (execution)',
    def set_sem_magnification(self, mag=100.):
        # int32_t SetSEMParameter(uint32_t CID, char* Params, char* ValueIDs, double* Values)
        # Result := SetSEMParameter(FCID, '', 'Mag', @ Mag);
        # Result := SetSEMParameter(FCID, '', 'HV', @ HV);
        # Result := SetSEMParameter(FCID, '', 'WD', @ WD);
        #### Also --> Result := SetSEMData(FCID,Mag,HV,WD); to set three values simultanelously
        MAG = ctypes.c_double(mag)
        MAG_ptr = ctypes.pointer(MAG)

        output = \
            self.esprit.SetSEMParameter(self.CID, '', 'Mag', MAG_ptr)

        if output==0:
            self.error_message = ''
            print(f'SEM magnification successfully set to {MAG}')
        else:
            self.error_message = f'No success in setting the SEM magnification, ERROR code is {output}, {errors[output]}'
            print( self.error_message + '\n')


    ### TODO: this function does not work : -2 : 'IFC_ERROR_WRONG_PARAMETER (execution)',
    def set_sem_high_voltage(self, hv=10.):
        # int32_t SetSEMParameter(uint32_t CID, char* Params, char* ValueIDs, double* Values)
        # Result := SetSEMParameter(FCID, '', 'Mag', @ Mag);
        # Result := SetSEMParameter(FCID, '', 'HV', @ HV);
        # Result := SetSEMParameter(FCID, '', 'WD', @ WD);
        #### Also --> Result := SetSEMData(FCID,Mag,HV,WD); to set three values simultanelously\
        HV = ctypes.c_double(hv)
        HV_ptr = ctypes.pointer(HV)

        output = \
            self.esprit.SetSEMParameter(self.CID, '', 'HV', HV_ptr)

        if output==0:
            self.error_message = ''
            print(f'SEM high voltage successfully set to {HV}\n')
        else:
            self.error_message = f'No success in setting the SEM high voltage, ERROR code is {output}, {errors[output]}'
            print( self.error_message + '\n')


    def set_sem_probe_current(self, current=1e-10):
        # int32_t SetSEMProbeCurrent(uint32_t CID, double ProbeCurrent)
        # Result := SetSEMProbeCurrent(FCID,PC);
        probe_current = ctypes.c_double(current)

        output = \
            self.esprit.SetSEMProbeCurrent(self.CID, probe_current)

        if output==0:
            self.error_message = ''
            print(f'SEM probe current successfully set to {probe_current}')
        else:
            self.error_message = f'No success in setting the SEM probe current, ERROR code is {output}, {errors[output]}'
            print( self.error_message + '\n')


    def move_stage_to_coordinate(self, x=0, y=0, z=0, t=0, r=0):
        # Sets stage position, tilt and rotation
        # int32_t SetSEMStageData(uint32_t CID, double XPos, double YPos, double ZPos, double Tilt, double Rotation)
        self.x_pos = ctypes.c_double(x) # x
        self.y_pos = ctypes.c_double(y) # y
        self.z_pos = ctypes.c_double(z) # z
        self.t_pos = ctypes.c_double(t) # tilt
        self.r_pos = ctypes.c_double(r)  # rotation

        output = \
            self.esprit.SetSEMStageData(self.CID,
                                        self.x_pos, self.y_pos, self.z_pos,
                                        self.t_pos, self.r_pos)

        if output==0:
            self.error_message = ''
            print(f'SEM position is: x,y,z: ({self.x_pos.value}, {self.y_pos.value}, {self.z_pos.value}); '
                  f'tilt: {self.t_pos.value};  rotation: {self.r_pos.value}')
        else:
            self.error_message = f'No SEM stage could be set, ERROR code is {output}, {errors[output]}'
            print( self.error_message + '\n')



    def set_sem_to_external_mode(self, external=True):
        # There is also a function set_external_scan_mode(self, external=True)
        # int32_t SetSEMExternalOn(uint32_t CID)
        # int32_t SetSEMExternalOff(uint32_t CID)


        if self.demo is not True:

            if external==True:
                output = \
                    self.esprit.SetSEMExternalOn(self.CID)
            else:
                output = \
                    self.esprit.SetSEMExternalOff(self.CID)

            if output==0:
                self.error_message = ''
                print(f'SEM external mode is ', external)
            else:
                self.error_message = f'External/Internal mode could be set, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:
            self.error_message = ''
            print(f'demo mode: SEM external mode is ', external)



    def beam_control(self, beamOn=True):
        # int32_t SwitchSEMOff(uint32_t CID, bool HVOff, bool BeamCurrentOff, bool BeamBlank)
        # SwitchSEMOff(FCID,true,false,false);
        # HVOff: Switches microscopes high voltage off
        # BeamCurrentOff: Switches beam off completely
        # BeamBlank: Blank the electron beam
        beamOn = ctypes.c_bool(beamOn)


        if self.demo is not True:

            output = \
                self.esprit.SwitchSEMOff(self.CID, ctypes.c_bool(False), ctypes.c_bool(False), beamOn)

            if output==0:
                self.error_message = ''
                print(f'Beam is ON = ', beamOn.value, '\n')
            else:
                self.error_message = f'Could not turn the beam on/off, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')


        elif self.demo is True:

            self.error_message = ''
            print(f'Beam is ON = ', beamOn.value, '\n')


    ####################################################################################################################
    ###########################################     Imaging     ########################################################
    ####################################################################################################################


    def get_image_configuration(self):
        # int32_t ImageGetConfiguration(uint32_t CID, uint32_t & Width, uint32_t & Height, uint32_t & Average, bool & Ch1, bool & Ch2)
        # ImageGetConfiguration(FCID,w,h,Average,Ch1,Ch2);
        # w,h, Average      : Cardinal;
        # Width: Image  width in pixel
        # Height: Image height in pixel
        # Average: Number of pixel average cycles. Depending on the number of active channels one cycle takes
        # 1 us (for one active channel) or 2 us (for two active channels)
        # Ch1, Ch2: Image channel active or not
        self.width   = ctypes.c_uint32(0) # image width
        self.height  = ctypes.c_uint32(0) # image height
        self.average = ctypes.c_uint32(1)
        self.Ch1     = ctypes.c_bool(False)
        self.Ch2     = ctypes.c_bool(False)
        ################## pointers ##################
        self.width_ptr   = ctypes.pointer(self.width)
        self.height_ptr  = ctypes.pointer(self.height)
        self.average_ptr = ctypes.pointer(self.average)
        self.Ch1_ptr     = ctypes.pointer(self.Ch1)
        self.Ch2_ptr     = ctypes.pointer(self.Ch2)


        if self.demo is not True:

            self.get_field_width() # get the field width as well, good for estimation of pixel size

            output = \
                self.esprit.ImageGetConfiguration(self.CID,
                                                  self.width_ptr, self.height_ptr,
                                                  self.average_ptr, self.Ch1_ptr, self.Ch2_ptr)

            if output==0:
                self.error_message = ''
                print(f'Image configuration: width {self.width.value}; height {self.height.value}; '
                      f'average {self.average.value}); Ch1 {self.Ch1.value};  Ch2: {self.Ch2.value}\n')
            else:
                self.error_message = f'No image configuration could be retrieved, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

        elif self.demo is True:
            self.error_message = ''
            print(f'demo mode: Image configuration: width {self.width.value}; height {self.height.value}; '
                  f'average {self.average.value}); Ch1 {self.Ch1.value};  Ch2: {self.Ch2.value}\n')


    def set_image_configuration(self, width=500, height=300, average=1, Ch1=True, Ch2=True):
        # int32_t ImageSetConfiguration(uint32_t CID, uint32_t Width, uint32_t Height, uint32_t Average, bool Ch1, bool Ch2)
        # ImageSetConfiguration(FCID,StrToInt(WidthEdit.Text),StrToInt(HeightEdit.Text),1,true,true);
        # Width: Image  width in pixel
        # Height: Image height in pixel
        # Average: Number of pixel average cycles. Depending on the number of active channels one cycle takes 1 us (for one active channel) or 2 us (for two active channels)
        # Ch1, Ch2: Image channel active or not
        self.width   = ctypes.c_uint32(width) # image width
        self.height  = ctypes.c_uint32(height) # image height
        self.average = ctypes.c_uint32(average)
        self.Ch1     = ctypes.c_bool(Ch1)
        self.Ch2     = ctypes.c_bool(Ch2)


        if self.demo is not True:

            output = \
                self.esprit.ImageSetConfiguration(self.CID,
                                                  self.width, self.height,
                                                  self.average, self.Ch1, self.Ch2)

            self.get_field_width() # update field width after magnification change

            if output==0:
                self.error_message = ''
                print(f'Image configuration set to: width {self.width.value}; height {self.height.value}; '
                      f'average {self.average.value}); Ch1 {self.Ch1.value};  Ch2: {self.Ch2.value}\n')
            else:
                self.error_message = f'No image configuration could be set, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')


        elif self.demo is True:

            self.error_message = ''
            print(f'Demo mode: Image configuration set to: width {self.width.value}; height {self.height.value}; '
                  f'average {self.average.value}); Ch1 {self.Ch1.value};  Ch2: {self.Ch2.value}\n')


    def set_external_scan_mode(self, external=True):
        # There is also a function set_sem_to_external_mode(self, external=True)
        # Use external scan engine which triggers scan generator trough an external signal
        # int32_t ImageSetExternalScan(uint32_t CID, bool UseExternalScan)
        # ImageSetExternalScan(FCID,MapExternalScanCheckBox.Checked);
        self.external_scan = ctypes.c_bool(external)


        if self.demo is not True:

            output = \
                self.esprit.ImageSetExternalScan(self.CID, self.external_scan)

            if output==0:
                self.error_message = ''
                print(f'Set external scanning mode to {external} successfully\n')
            else:
                self.error_message = f'Could not set external scanning mode to {external}, ERROR code is {output}, {errors[output]}\n'
                print( self.error_message + '\n')

        elif self.demo is True:

            self.error_message = ''
            print(f'Demo mode: Set external scanning mode to {external} successfully\n')


    def acquire_image(self, channel=1, show_progress=False):
        # int32_t ImageAquireImage(uint32_t CID, int32_t Ch, bool ShowProgress, void* Buffer, int32_t& BufSize, PRTImageInfoEx ImgInfo)
        # ImageAquireImageEx(FCID, 2, MemStream.Memory, 0, aSize, @ImgInfo)
        #
        self.image_info = TRTImageInfoEx()
        self.image_info_ptr = ctypes.pointer(self.image_info)

        extra_buffer_for_image = 200000
        self.buffer_size = ctypes.c_uint32(self.width.value * self.height.value + extra_buffer_for_image) # MemStream.SetSize(W*H+20000); aSize:=MemStream.Size;
        self.buffer_size_ptr = ctypes.pointer(self.buffer_size)

        self.channel = ctypes.c_uint32(channel)
        show_progress = ctypes.c_bool(show_progress)

        # version 1 - void pointer
        #self.image_buffer_ptr = ctypes.c_void_p() # void* Buffer

        # version 2 : array
        # the image has 8 bit depth (0..255) hence ctypes.c_uint8
        IntArray = ctypes.c_uint8 * self.buffer_size.value # int8 array the size of width*height+extra for storing the image
        self.image_buffer = IntArray() # initialise the array
        self.image_buffer_ptr = ctypes.pointer(self.image_buffer) # pointer to the image buffer array


        if self.demo is not True:

            output = \
                self.esprit.ImageAquireImage(self.CID,
                                             self.channel, show_progress,
                                             self.image_buffer_ptr, self.buffer_size_ptr, self.image_info_ptr)

            print(f'image info: mag={self.image_info.Magnification}, pixelsize={self.image_info.PixelSizeX}, '
                  f'HV={self.image_info.HighVoltage}, WD={self.image_info.WorkingDistance}')

            if output==0:
                self.error_message = ''
                print(f'image acquired successfully\n')
            else:
                self.error_message = f'Could not acquire image, ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')

            self.buffer = np.zeros( self.buffer_size.value )
            for ii in range( self.buffer_size.value ):
                self.buffer[ii] = self.image_buffer_ptr.contents[ii] # populate the 1D array from the buffer pointer

            buffer_index = self._find_where_header_ends(self.buffer)

            # remove the header
            self.image = self.buffer[ buffer_index + len(header) :
                                      buffer_index + len(header) + self.height.value * self.width.value]

            self.image = np.reshape(self.image, (self.height.value, self.width.value) ) # reshape the 1D array into the image shape

            self.image = np.flipud(self.image) # rearrange the array to match SEM image


        elif self.demo is True:

            print('this is demo mode, image generated')
            self.image = np.random.randint(0, 255, [self.height.value, self.width.value])




    def _find_where_header_ends(self, buffer):
        ind = 0
        for ii in range(0, len(buffer) - len(header)):
            if list(buffer[ii: ii + len(header)]) == list(header):
                ind = ii
                break
        print(f'index = {ind}, end of header = {ind + len(header)}')
        return ind



    ####################################################################################################################
    ########################################     Beam control     ######################################################
    ####################################################################################################################


    def set_beam_to_point(self, x_pos=10, y_pos=10):
        # int32_t ImageSetPoint(uint32_t CID, uint32_t X, uint32_t Y)
        # Pixel X Y value of the current image to set the electron beam to
        X = ctypes.c_uint32(x_pos)
        Y = ctypes.c_uint32(y_pos)

        if self.demo is not True:

            output = \
                self.esprit.ImageSetPoint(self.CID, X, Y)

            if output==0:
                self.error_message = ''
                # print(f'Beam position set to ({X.value}, {Y.value})\n')
                # update the (x,y) beam position coordinates TODO find a function to retrieve the actual beam position
                self.beam_x_pos = X.value
                self.beam_y_pos = Y.value
            else:
                self.error_message = f'Could not position the beam to ({X.value}, {Y.value}), ERROR code is {output}, {errors[output]}'
                print( self.error_message + '\n')


        elif self.demo is True:
            self.error_message = ''
            self.beam_x_pos = X.value
            self.beam_y_pos = Y.value
            print(f'demo mode: setting beam to pos {x_pos}, {y_pos}')



    def beam_blank(self):
        # blank the beam by moving it to a far-away pixel such that
        # it is no longer dwelling on the sample
        # TODO check pixel limits
        self.set_beam_to_point(x_pos=3000, y_pos=3000)


    def set_point_measurement(self, x=0, y=0, dwell_time=2):
        # int32_t StartPointListMeasurement(uint32_t CID, int32_t SPU, uint32_t SegmentCount, PSegmentList LineSegments, uint32_t RealTime);
        # CID: Identification code for an actual server/ client instance
        # SPU: Spectrometer index (1…n)
        # SegmentCount: Description of points to measure
        # RealTime: Acquisition time in ms

        dwell_time = ctypes.c_uint32(dwell_time)
        SPU = ctypes.c_uint32(1) # spectrometer channel, 1 is used here

        segment = TSegment()
        segment.Y      = ctypes.c_uint32(y) # y start
        segment.XStart = ctypes.c_uint32(x) # x start
        segment.XCount = ctypes.c_uint32(1) # single pixel line

        segment_count = 1
        TSegmentList = TSegment * segment_count # array/list of segment with a single element
        list_of_segments = TSegmentList(segment) # populate the array with a segment
        list_of_segments_ptr = ctypes.pointer(list_of_segments) # pointer to the list of segments/list with a single segment

        output = \
            self.esprit.StartPointListMeasurement(self.CID, SPU, ctypes.c_uint32(segment_count),
                                                  list_of_segments_ptr, dwell_time)

        if output==0:
            self.error_message = ''
            print(f'Segment starting at ({x},{y}) exposed during dwell of {dwell_time.value} ms\n')
        else:
            self.error_message = f'Could not expose segment at ({x},{y}) for dwell of {dwell_time.value} ms\n,' \
                                 f'ERROR code is {output}, {errors[output]}'
            print( self.error_message + '\n')


    def set_rectangular_measurement_point_by_point(self, x0=0, y0=0, Nx=0, Ny=0, dwell_time=2, detector=None):
        # int32_t StartPointListMeasurement(uint32_t CID, int32_t SPU, uint32_t SegmentCount, PSegmentList LineSegments, uint32_t RealTime);
        # CID: Identification code for an actual server/ client instance
        # SPU: Spectrometer index (1…n)
        # SegmentCount: Description of points to measure
        # RealTime: Acquisition time in ms
        #########################################################################
        # x0,y0 start corner of the rectangular, Nx,Ny - number of pixels
        # create segment of each point and expose, continue until done
        # collect data with external detector

        dwell_time = ctypes.c_uint32(dwell_time)
        SPU = ctypes.c_uint32(1) # spectrometer channel, 1 is used here

        segment = TSegment()
        segment.Y      = ctypes.c_uint32(y0) # y start
        segment.XStart = ctypes.c_uint32(x0) # x start
        segment.XCount = ctypes.c_uint32(1) # single pixel line

        segment_count = 1
        TSegmentList = TSegment * segment_count # array/list of segment with a single element
        list_of_segments = TSegmentList(segment) # populate the array with a segment
        list_of_segments_ptr = ctypes.pointer(list_of_segments) # pointer to the list of segments/list with a single segment

        for ii in range(Nx):
            for jj in range(Ny):
                # TODO the list pointer does not get updated when the element values are changed....
                # TODO currently reinitialising the pointer every time the element values are changed
                # TODO change the content of the pointer directly!
                segment.XStart = ctypes.c_uint32(x0 + ii)
                segment.Y      = ctypes.c_uint32(y0 + jj)
                list_of_segments = TSegmentList(segment)  # populate the array with a segment
                list_of_segments_ptr = ctypes.pointer(list_of_segments)  # pointer to the list of segments/list with a single segment

                print(f'Exposing point: ({list_of_segments_ptr.contents[0].XStart}, {list_of_segments_ptr.contents[0].Y})')

                # TODO detector ON, start collection of data
                output = \
                    self.esprit.StartPointListMeasurement(self.CID, SPU, ctypes.c_uint32(segment_count),
                                                          list_of_segments_ptr, dwell_time)
                # TODO detector OFF after beam is OFF

                if output==0:
                    self.error_message = ''
                    print(f'Segment starting at ({x0},{y0}) exposed during dwell of {dwell_time.value} ms\n')
                else:
                    self.error_message = f'Could not expose segment at ({x0},{y0}) for dwell of {dwell_time.value} ms\n, ERROR code is {output}, {errors[output]}'
                    print(self.error_message + '\n')
                    break


    def get_point_list_spectrum(self, spectrum_index = 1, dwell_time = 1):
        # // CID		    : connection identifier
        # // Index		    : spectrum index (1..n)
        # // SpectrumBuf	: buffer to hold complete spectrum with header (around 20kB), must be allocated by caller
        # // BufSize		: size of spectrum buffer
        # int32_t GetPointListSpectrum(uint32_t CID, int32_t Index, PRTSpectrumHeaderRec SpectrumBuf, int32_t BufSize)

        spectrum_index = ctypes.c_uint32(spectrum_index)
        dwell_time = ctypes.c_uint32(dwell_time)

        # # allocate 64000 memory for the header
        # TRTSpectrumHeaderRecArray = TRTSpectrumHeaderRec * 64000
        # SpectrumBuf_ptr = ctypes.POINTER(TRTSpectrumHeaderRecArray)

        SpectrumBuf = TRTSpectrumHeaderRec()
        SpectrumBuf_ptr = ctypes.pointer(SpectrumBuf)

        output = \
            self.esprit.GetPointListSpectrum(self.CID, spectrum_index,
                                             SpectrumBuf_ptr, ctypes.c_uint32(64000))

        if output==0:
            self.error_message = ''
            print(f'Retrieved the line scan spectum\n')
        else:
            self.error_message = f'Could not retrieve the line scan data\n, ERROR code is {output}, {errors[output]}'
            print(self.error_message + '\n')


    ####################################################################################################################
    ##########################################       X-RAY       #######################################################
    ####################################################################################################################

    def start_xray_spectrum_measurement(self, real_time = 100):
        # int32_t StartSpectrumMeasurement(uint32_t CID, int32_t Device, uint32_t RealTime)
        # *****
        # // Device: Number of spectrometer ( 1 in most cases )
        # // RealTime: Measure time in ms ( 0 means endless measurement )
        # // Result: Function call sucessful or not ( 0 = success, otherwise error )
        # StartSpectrumMeasurement(FCID,1,0);
        # StartSpectrumMeasurement(FCID,1,TimeSpinEdit.Value);

        device = ctypes.c_int32(1)  # Device: Number of spectrometer ( 1 in most cases )
        real_time = ctypes.c_uint32(real_time)  # #RealTime: Measure time in ms ( 0 means endless measurement )

        output = \
            self.esprit.StartSpectrumMeasurement(self.CID, device, real_time)

        if output == 0:
            self.error_message = ''
            print(f'Started spectrum measurement\n')
        else:
            self.error_message = f'Could not start the spectrum measurement, ERROR code is {output}, {errors[output]}'
            print(self.error_message + '\n')


    def stop_xray_spectrum_measurement(self):
        # int32_t StopSpectrumMeasurement(uint32_t CID, int32_t Device)
        # *****
        # // Device: Number of spectrometer ( 1 in most cases )
        # // Result: Function call sucessful or not ( 0 = success, otherwise error )
        # StopSpectrumMeasurement(FCID,1);

        device = ctypes.c_int32(1)  # Device: Number of spectrometer ( 1 in most cases )

        output = \
            self.esprit.StopSpectrumMeasurement(self.CID, device)

        if output == 0:
            self.error_message = ''
            print(f'Stopping spectrum measurement\n')
        else:
            self.error_message = f'Could not stop the spectrum measurement, ERROR code is {output}, {errors[output]}'
            print(self.error_message + '\n')


    def get_xray_spectrometer_configuration(self):
        # int32_t GetSpectrometerConfiguration(uint32_t CID, int32_t SPU, uint32_t& MaxEnergy, uint32_t& PulseThroughput)
        # *****
        # SPU: Number of spectrometer ("1" in most cases)
        # MaxEnergy: Energy in keV of that last spectrum channel
        # PulseTroughput: Maximum pulse output rate of the selected amplifier in cps (counts per second)

        self.SPU = ctypes.c_int32(1)  # Number of spectrometer ("1" in most cases)
        self.max_energy = ctypes.c_uint32(0)  # Energy in keV of that last spectrum channel
        self.max_energy_ptr = ctypes.pointer(self.max_energy)
        self.pulse_throughput = ctypes.c_uint32(0)  # Maximum pulse output rate of the selected amplifier in cps (counts per second)
        self.pulse_throughput_ptr = ctypes.pointer(self.pulse_throughput)

        output = \
            self.esprit.GetSpectrometerConfiguration(self.CID, self.SPU,
                                                     self.max_energy_ptr,
                                                     self.pulse_throughput_ptr)

        if output == 0:
            self.error_message = ''
            print(f'Successfully received spectrometer parameters:\n')
            print(f'Spectrometer: max energy = {self.max_energy.value}')
            print(f'Spectrometer: pulse_throughput = {self.pulse_throughput.value}, counts per seconsd')
        else:
            self.error_message = f'Could not get the spectrometer configuration, ERROR code is {output}, {errors[output]}'
            print(self.error_message + '\n')


    def read_xray_spectrum_to_buffer(self):
        # int32_t ReadSpectrum(uint32_t CID, int32_t Device)
        # // Read current spectrum from spectrometer to buffer
        # // Device: Number of spectrometer ( 1 in most cases )
        # // Result: Function call sucessful or not ( 0 = success, otherwise error )
        # if (ReadSpectrum(FCID,1)=0)...

        device = ctypes.c_int32(1)  # Device: Number of spectrometer ( 1 in most cases )

        output = \
            self.esprit.ReadSpectrum(CID, device)

        if output == 0:
            self.error_message = ''
            print(f'Spectrum read into the buffer successfully\n')
        else:
            self.error_message = f'Could not read the spectrum into the buffer, ERROR code is {output}, {errors[output]}'
            print(self.error_message + '\n')


    def get_xray_spectrum(self):
        # int32_t GetSpectrum(uint32_t CID, int32_t Buffer, PRTSpectrumHeaderRec pSpectrumBuf, int32_t BufSize)
        # // Buffer: Buffer index ( 0 for loaded spectrum buffer, > 0 for spectrometer buffers )
        # // Result: Function call sucessful or not ( 0 = success, otherwise error )
        # (GetSpectrum(FCID,1,SpectrumBuf,64000)=0)
        # SpectrumBuf : PRTAPISpectrumHeaderRec;
        # PRTSpectrumHeaderRec -> PRTAPISpectrumHeaderRec

        device = ctypes.c_int32(1)  # Device: Number of spectrometer ( 1 in most cases )

        buffer_size = 64000
        buffer_size = ctypes.c_int32(buffer_size)

        buffer = ctypes.c_int32(1)  # Buffer index ( 0 for loaded spectrum buffer, > 0 for spectrometer buffers )

        spectrum_buffer = TRTSpectrumHeaderRec()
        spectrum_buffer_ptr = ctypes.pointer(spectrum_buffer)
        # TRTSpectrumHeaderRecArray = TRTSpectrumHeaderRec * 64000
        # spectrum_buffer_ptr = ctypes.POINTER(TRTSpectrumHeaderRecArray)

        output = \
            self.esprit.GetSpectrum(self.CID, device, buffer, spectrum_buffer_ptr, buffer_size)

        if output == 0:
            self.error_message = ''
            print(f'GetSpectrum is successfull\n')
            print_spectrum_header(spectrum_buffer)
        else:
            self.error_message = f'Could not GetSpectrum, ERROR code is {output}, {errors[output]}'
            print(self.error_message + '\n')


    def save_xray_spectrum_to_file(self, file_name=None):
        # int32_t SaveSpectrum(uint32_t CID, int32_t Buffer, char* pFileName)
        # // Save spectrum buffer to file
        # function SaveSpectrum(CID:LongWord;Buffer:longint;pFileName:PAnsiChar):longint;stdcall;external csAPILibFile;
        #    // pFilename   : Complete filename for spectrum ( normally with *.spx extension )
        #    // Result      : Function call sucessful or not ( 0 = success, otherwise error )

        buffer = ctypes.c_int32(1)  # Buffer index ( 0 for loaded spectrum buffer, > 0 for spectrometer buffers), 0 - reserved for Load

        if file_name is None:
            ts = time.time()
            stamp = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d.%H%M%S')  # make a timestamp for new file
            file_name = "xray_spectrum_" + stamp + '.txt'
            file_name = file_name.encode('utf-8')  # bytes, reference, char*, PAnsiChar equivalent
        else:
            file_name = file_name.encode('utf-8')  # bytes, reference, char*, PAnsiChar equivalent

        output = \
            self.esprit.SaveSpectrum(self.CID, buffer, file_name)

        if output == 0:
            self.error_message = ''
            print(f'Spectrum saved successfully to file {file_name}\n')
        else:
            self.error_message = f'Could not save spectrum, ERROR code is {output}, {errors[output]}'
            print(self.error_message + '\n')





















if __name__ == "__main__":
    bruker = Bruker_Esprit()
    bruker.initialise(type='direct')

    bruker.get_sem_data()
    bruker.get_sem_info()
    bruker.get_sem_capabilities()
    bruker.get_sem_brightness_and_contrast()
    bruker.get_sem_probe_current()
    bruker.get_sem_spot_size()
    bruker.get_sem_stage_position()
    bruker.get_field_width()
    bruker.get_sem_stage_range()

    bruker.set_sem_parameters(mag=100)
    #bruker.move_stage_to_coordinate(x=10e3, y=5e3, z=0)
    bruker.get_image_configuration()
    bruker.set_image_configuration(width=500, height=100, average=1, Ch1=True, Ch2=True)
    bruker.acquire_image(channel=1,show_progress=True, show=True)
    bruker.get_field_width()


    bruker.set_beam_to_point(50,500)
    # bruker.beam_control(beamOn=True)
    # time.sleep(0.005)
    # bruker.beam_control(beamOn=False)

    bruker.set_point_measurement(x=100, y=250, dwell_time=2500)
    bruker.set_rectangular_measurement_point_by_point(x0=100, y0=50, Nx=5, Ny=3, dwell_time=2500, detector=None)


    # bruker.close()