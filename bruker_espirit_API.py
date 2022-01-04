import ctypes
import sys
import time
import numpy as np

path_to_dll = r'F:\SharedData\MCEM Data - Staff Only\Bruker API\Esprit API\Bruker.API.Esprit64.dll'
path_to_dll = r'C:\Users\sergeyg\Github\Bruker Nano APIs\Esprit API\Bruker.API.Esprit64.dll'
#path_to_dll = r'\\ad.monash.edu\home\User002\sergeyg\Desktop\Minipix\Bruker Nano APIs\Esprit API\Bruker.API.Esprit64.dll'

AnsiChar = ctypes.c_char * 8
PAnsiChar = ctypes.POINTER(AnsiChar)


# TOpenClientOptions = packed record // structure to describe Quantax start options in ‘OpenClientEx’
# Version: integer; // Version of record structure, should be ‘l’ at the moment
# GUIMode: integer; // ‘0’ = no GUI, ‘1’ = full GUI, ‘2’ = reduced GUI (spectrum chart only)
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
         -201 : 'STATE_WAS_RUNNING_BEFORE'
}

class Bruker_Espirit():
    def __init__(self, path_to_dll):
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

        self.StartNew = True # If true, function starts always a new client instance
        self.GUI      = True # When true client screen is shown, otherwise hidden (only valid at first start of client)

        self.CID = ctypes.c_uint32(123456)       # Identification code for an actual server/client instance
        self.CID_ptr = ctypes.pointer(self.CID)  # Pointer to Identification code for an actual server/client instance
        try:
            self.espirit = ctypes.cdll.LoadLibrary(path_to_dll)
            print(path_to_dll, self.espirit)
        except:
            print(f'path to dll {path_to_dll} does not exist')


    def initialise(self, type='Ex'):
        print('before : Connection identification code = ', self.CID)
        # Starting an application requires a valid password. References to a connection takes place
        # always via an identification code (CID) delivered by the OpenClient function.
        # int32_t OpenClient(   char* pServer, char* pUser, char* pPassword, bool StartNew, bool GUI, uint32_t& CID)
        # int32_t OpenClientTCP(char* pServer, char* pUser, char* pPassword, char* pHost, unsigned  __int16 Port, const TOpenClientOptions Options, uint32_t & CID);
        # int32_t OpenClientEx(char * pServer, char* pUser, char* pPassword, const TOpenClientOptions & Options, uint32_t & CID);
        #
        if type=='direct':
            print('Connecting directly to the client')
            output = self.espirit.OpenClient(self.pServer, self.pUser, self.pPassword, self.StartNew, self.GUI, self.CID_ptr)
        elif type=='Ex':
            print('Connecting to the client : external mode')
            output = self.espirit.OpenClientEx(self.pServer, self.pUser, self.pPassword, self.StartNew, self.GUI, self.CID_ptr)
        elif type == 'TCP':
            print('Connecting to the client : TCP mode')
            output = self.espirit.OpenClientTCP(self.pServer, self.pUser, self.pPassword, self.pHost, self.port, self.Options, self.CID_ptr)
        else:
            print('Connecting to the client : external mode')
            output = self.espirit.OpenClientEx(self.pServer, self.pUser, self.pPassword, self.Options_ptr, self.CID_ptr)
        #
        print('after : Connection identification code = ', self.CID)
        if output==0:
            print('Connection established successfully')
        else:
            print(f'No connection established, ERROR code is {output}, {errors[output]}')

    def close(self):
        self.espirit.CloseClient(self.CID)


    ####################################################################################################################
    ########################################     Getting info     ######################################################
    ####################################################################################################################

    def get_sem_data(self):
        # int32_t GetSEMData(uint32_t CID, double& Magnification, double& HighVoltage, double& WorkingDistance)
        self.mag = ctypes.c_double(0) # magnification
        self.HV  = ctypes.c_double(0) # high voltage in keV
        self.WD  = ctypes.c_double(0) # working ditance in mm
        self.mag_ptr = ctypes.pointer(self.mag)
        self.HV_ptr = ctypes.pointer(self.HV)
        self.WD_ptr = ctypes.pointer(self.WD)
        print(f'before : mag = {self.mag}, HV = {self.HV}, WD = {self.WD}')
        output = self.espirit.GetSEMData(self.CID, self.mag_ptr, self.HV_ptr, self.WD_ptr)
        print(f'after : mag = {self.mag}, HV = {self.HV}, WD = {self.WD}')
        if output==0:
            print('SEM data retrieved successfully')
        else:
            print(f'No SEM data could be fetched, ERROR code is {output}, {errors[output]}')

    def get_sem_bright_and_contrast(self):
        # int32_t GetSEMBCData(uint32_t CID, double& Brightness, double& Contrast)
        self.brightness = ctypes.c_double(0) # magnification
        self.contrast   = ctypes.c_double(0) # high voltage in keV
        self.brightness_ptr = ctypes.pointer(self.mag)
        self.contrast_ptr = ctypes.pointer(self.HV)
        print(f'before : brightness = {self.brightness}, contrast = {self.contrast}')
        output = \
            self.espirit.GetSEMBCData(self.CID, self.brightness_ptr, self.contrast_ptr)
        print(f'after : brightness = {self.brightness}, contrast = {self.contrast}')
        if output==0:
            print('SEM data retrieved successfully')
        else:
            print(f'No SEM data could be fetched, ERROR code is {output}, {errors[output]}')

    def get_sem_probe_current(self):
        # int32_t GetSEMProbeCurrent(uint32_t CID, double& ProbeCurrent)
        self.probe_current = ctypes.c_double(0) # probe current
        self.probe_current_ptr = ctypes.pointer(self.probe_current)
        print(f'before : probe current = {self.probe_current}')
        output = \
            self.espirit.GetSEMProbeCurrent(self.CID, self.probe_current_ptr)
        print(f'after : probe current = {self.probe_current}')
        if output==0:
            print('SEM probe current retrieved successfully')
        else:
            print(f'No SEM probe current could be fetched, ERROR code is {output}, {errors[output]}')

    def get_sem_spot_size(self):
        # int32_t GetSEMSpotSize(uint32_t CID, double& SpotSize)
        self.spot_size = ctypes.c_double(0) # probe current
        self.spot_size_ptr = ctypes.pointer(self.spot_size)
        print(f'before : spot size = {self.spot_size}')
        output = \
            self.espirit.GetSEMSpotSize(self.CID, self.spot_size_ptr)
        print(f'after : spot size = {self.spot_size}')
        if output==0:
            print('SEM spot size retrieved successfully')
        else:
            print(f'No SEM spot size could be fetched, ERROR code is {output}, {errors[output]}')

    def get_sem_stage_data(self):
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
        output = \
            self.espirit.GetSEMStageData(self.CID,
                                         self.x_pos_ptr, self.y_pos_ptr, self.z_pos_ptr,
                                         self.t_pos_ptr, self.r_pos_ptr)
        if output==0:
            print(f'SEM position is: x,y,z: ({self.x_pos}, {self.y_pos}, {self.z_pos}); tilt: {self.t_pos};  rotation: {self.r_pos}')
        else:
            print(f'No SEM stage info could be fetched, ERROR code is {output}, {errors[output]}')

    def get_sem_info(self):
        # int32_t GetSEMInfo(uint32_t CID, char* Info, int32_t BufSize)
        ################################################################
        # Info := '';
        # SetLength(Info, 1000);
        # GetSEMInfo(FCID, PAnsiChar(Info), 999);
        buffer_size = ctypes.c_int32(999)
        info = ' ' * 1000 # block of memory for 1000 characters
        self.Info = info.encode('utf-8') # bytes, reference, char*
        output = \
            self.espirit.GetSEMInfo(self.CID, self.Info, buffer_size)
        if output==0:
            print('SEM Info: ', str(self.Info))
        else:
            print(f'No SEM info could be fetched, ERROR code is {output}, {errors[output]}')


    def get_field_width(self):
        #int32_t ImageGetFieldWidth(uint32_t CID, double & FieldWidth)
        self.field_width = ctypes.c_double(0) #  mm
        self.field_width_ptr = ctypes.pointer(self.field_width)
        output = \
            self.espirit.ImageGetFieldWidth(self.CID, self.field_width_ptr)
        if output==0:
            print(f'Field width = {self.field_width}')
        else:
            print(f'Field width could not be obtained, ERROR code is {output}, {errors[output]}')





    ####################################################################################################################
    ##########################################     Settings     ########################################################
    ####################################################################################################################

    def set_sem_magnification(self, mag=100.):
        # int32_t SetSEMParameter(uint32_t CID, char* Params, char* ValueIDs, double* Values)
        # Result := SetSEMParameter(FCID, '', 'Mag', @ Mag);
        # Result := SetSEMParameter(FCID, '', 'HV', @ HV);
        # Result := SetSEMParameter(FCID, '', 'WD', @ WD);
        MAG = ctypes.c_double(mag)
        MAG_ptr = ctypes.pointer(MAG)
        output = \
            self.espirit.SetSEMParameter(self.CID_ptr, '', 'Mag', MAG_ptr)
        if output==0:
            print(f'SEM magnification successfully set to {MAG}')
        else:
            print(f'No success in setting the SEM magnification, ERROR code is {output}, {errors[output]}')

    def set_sem_high_voltage(self, hv=10.):
        # int32_t SetSEMParameter(uint32_t CID, char* Params, char* ValueIDs, double* Values)
        # Result := SetSEMParameter(FCID, '', 'Mag', @ Mag);
        # Result := SetSEMParameter(FCID, '', 'HV', @ HV);
        # Result := SetSEMParameter(FCID, '', 'WD', @ WD);
        HV = ctypes.c_double(hv)
        HV_ptr = ctypes.pointer(HV)
        output = \
            self.espirit.SetSEMParameter(self.CID_ptr, '', 'HV', HV_ptr)
        if output==0:
            print(f'SEM high voltage successfully set to {HV}')
        else:
            print(f'No success in setting the SEM high voltage, ERROR code is {output}, {errors[output]}')

    def set_sem_probe_current(self, current=1e-10):
        # int32_t SetSEMProbeCurrent(uint32_t CID, double ProbeCurrent)
        # Result := SetSEMProbeCurrent(FCID,PC);
        probe_current = ctypes.c_double(current)
        probe_current_ptr = ctypes.pointer(probe_current)
        output = \
            self.espirit.SetSEMProbeCurrent(self.CID_ptr, probe_current)
        if output==0:
            print(f'SEM probe current successfully set to {probe_current}')
        else:
            print(f'No success in setting the SEM probe current, ERROR code is {output}, {errors[output]}')

    def set_sem_stage_data(self, x=0, y=0, z=0, t=0, r=0):
        # Sets stage position, tilt and rotation
        # int32_t SetSEMStageData(uint32_t CID, double XPos, double YPos, double ZPos, double Tilt, double Rotation)
        self.x_pos = ctypes.c_double(x) # x
        self.y_pos = ctypes.c_double(y) # y
        self.z_pos = ctypes.c_double(z) # z
        self.t_pos = ctypes.c_double(t) # tilt
        self.r_pos = ctypes.c_double(r)  # rotation
        output = \
            self.espirit.SetSEMStageData(self.CID,
                                         self.x_pos, self.y_pos, self.z_pos,
                                         self.t_pos, self.r_pos)
        if output==0:
            print(f'SEM position is: x,y,z: ({self.x_pos}, {self.y_pos}, {self.z_pos}); tilt: {self.t_pos};  rotation: {self.r_pos}')
        else:
            print(f'No SEM stage could be set, ERROR code is {output}, {errors[output]}')


    def set_sem_external(self, external=True):
        # int32_t SetSEMExternalOn(uint32_t CID)
        # int32_t SetSEMExternalOff(uint32_t CID)
        if external==True:
            output = \
                self.espirit.SetSEMExternalOn(self.CID)
        else:
            output = \
                self.espirit.SetSEMExternalOff(self.CID)
        if output==0:
            print(f'SEM external mode is ', external)
        else:
            print(f'External/Internal mode could be set, ERROR code is {output}, {errors[output]}')


    def beam_control(self, beamOn=True):
        # int32_t SwitchSEMOff(uint32_t CID, bool HVOff, bool BeamCurrentOff, bool BeamBlank)
        # SwitchSEMOff(FCID,true,false,false);
        # HVOff: Switches microscopes high voltage off
        # BeamCurrentOff: Switches beam off completely
        # BeamBlank: Blank the electron beam
        output = \
            self.espirit.SwitchSEMOff(self.CID, False, False, beamOn)
        if output==0:
            print(f'Beam is ON = ', beamOn)
        else:
            print(f'Could not turn the beam on/off, ERROR code is {output}, {errors[output]}')


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
        self.width_ptr   = ctypes.pointer(self.width)
        self.height_ptr  = ctypes.pointer(self.height)
        self.average_ptr = ctypes.pointer(self.average)
        self.Ch1_ptr     = ctypes.pointer(self.Ch1)
        self.Ch2_ptr     = ctypes.pointer(self.Ch2)
        self.get_field_width()
        output = \
            self.espirit.ImageGetConfiguration(self.CID,
                                               self.width_ptr, self.height_ptr,
                                               self.average_ptr, self.Ch1_ptr, self.Ch2_ptr)
        if output==0:
            print(f'Image configuration: width {self.width}; height {self.height}; average {self.average}); Ch1 {self.Ch1};  Ch2: {self.Ch2}')
        else:
            print(f'No image configuration could be retrieved, ERROR code is {output}, {errors[output]}')


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
        output = \
            self.espirit.ImageSetConfiguration(self.CID,
                                               self.width, self.height,
                                               self.average, self.Ch1, self.Ch2)
        self.get_field_width() # update field width after magnification change
        if output==0:
            print(f'Image configuration set to: width {self.width}; height {self.height}; average {self.average}); Ch1 {self.Ch1};  Ch2: {self.Ch2}')
        else:
            print(f'No image configuration could be set, ERROR code is {output}, {errors[output]}')


    def set_external_scan_mode(self, external=True):
        # Use external scan engine which triggers scan generator trough an external signal
        # int32_t ImageSetExternalScan(uint32_t CID, bool UseExternalScan)
        # ImageSetExternalScan(FCID,MapExternalScanCheckBox.Checked);
        self.external_scan = ctypes.c_bool(external)
        output = \
            self.espirit.ImageSetExternalScan(self.CID, self.external_scan)
        if output==0:
            print(f'Set external scanning mode to {external} successfully')
        else:
            print(f'Could not set external scanning mode to {external}, ERROR code is {output}, {errors[output]}')


    def acquire_image(self, channel=1, show_progress=False):
        # int32_t ImageAquireImage(uint32_t CID, int32_t Ch, bool ShowProgress, void* Buffer, int32_t& BufSize, PRTImageInfoEx ImgInfo)
        # ImageAquireImageEx(FCID, 2, MemStream.Memory, 0, aSize, @ImgInfo)
        #
        self.image_info = TRTImageInfoEx()
        self.image_info_ptr = ctypes.pointer(self.image_info)
        self.buffer_size = ctypes.c_uint32(self.width.value * self.height.value + 200000) # MemStream.SetSize(W*H+20000); aSize:=MemStream.Size;
        self.buffer_size_ptr = ctypes.pointer(self.buffer_size)

        # version 1
        #self.image_buffer_ptr = ctypes.c_void_p() # void* Buffer

        # version 2 : array
        IntArray = ctypes.c_uint32 * self.buffer_size.value
        #self.image_buffer_ptr = ctypes.POINTER(IntArray)
        self.image_buffer_ptr = IntArray()


        output = \
            self.espirit.ImageAquireImage(self.CID, channel, show_progress, self.image_buffer_ptr, self.buffer_size_ptr, self.image_info_ptr)
        if output==0:
            print(f'image acquired successfully')
        else:
            print(f'Could not acquire image, ERROR code is {output}, {errors[output]}')


        self.image = np.zeros( self.buffer_size.value )
        for ii in range( self.buffer_size.value ):
            self.image[ii] = self.image_buffer_ptr[0]
            #self.image[ii] = self.image_buffer_ptr.contents[ii].value









if __name__ == "__main__":
    bruker = Bruker_Espirit(path_to_dll=path_to_dll)
    bruker.initialise(type='TCP')
    bruker.get_sem_data()

    bruker.set_image_configuration(width=500, height=300, average=1, Ch1=True, Ch2=True)
    bruker.acquire_image(channel=1,show_progress=False)
    # bruker.close()