"""
This scripts shows how to measure with the detector with different options and how to get the measured data or save
them to the disk

"""

# first list all Medipix/Timepix devices and use the first one:
devices = pixet.devicesByType(pixet.PX_DEVTYPE_MPX2)
if not devices:
    raise "No devices connected"
device = devices[0] # use  the first device


# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE - SAVING TO FILE
# -----------------------------------------------------------------------------------
def acqExample1():
    #  take 10 frames from the device, 0.5 second long and save to file test.pmf
    for i in range(10):
        acqCount = 1
        acqTime = 0.5 # in seconds, half second
        outputFile = "test.pmf"
        rc = device.doSimpleAcquisition(acqCount, acqTime, pixet.PX_FTYPE_AUTODETECT, outputFile)
        print("Acquition: %d" % rc)

# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE - INTEGRAL ACQUISITION
# -----------------------------------------------------------------------------------
def acqExample2():
    # does integral acquisition of 10 0.1s frames -> sums 10 frames of 0.1s to one and
    # save to file
    acqCount = 10
    acqTime = 0.1 # in seconds, 0.1 s
    outputFile = "test.pmf"
    rc = device.doSimpleIntegralAcquisition(acqCount, acqTime, pixet.PX_FTYPE_AUTODETECT, outputFile)
    print("Acquition: %d" % rc)


# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE - GETTING FRAME DATA
# -----------------------------------------------------------------------------------
def acqExample3():
    # acquisition 1 frame, 0.5 s acq time, no saving to file:
    rc = device.doSimpleAcquisition(1, 0.5, pixet.PX_FTYPE_AUTODETECT, "")
    print("Acquition: %d" % rc)

    # get last frame
    frame = device.lastAcqFrameRefInc()

    # acqCount = device.acqFrameCount() # number of measured acquisitions (frames)
    # frame = device.acqFrameRefInc(index) # get frame with index from last acquisition series

    # get frame data to python array/list:
    data = frame.data()

    # just print first 10 values of frame
    print(data[0:10])

    frame.destroy() # release the frame

# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE - MORE COMPLEX e.g. triggers
# -----------------------------------------------------------------------------------
def acqExample4():
    # acquisition parameters
    acqPars = pixet.MpxAcqParams()
    acqPars.count = 1 # number of frames
    acqPars.time = 0.5 # time of one frame
    acqPars.mode = pixet.PX_ACQMODE_TRG_NO # trigger mode: pixet.PX_ACQMODE_TRG_NO, pixet.PX_ACQMODE_TRG_HWSTART, pixet.PX_ACQMODE_TRG_HWSTOP, pixet.PX_ACQMODE_TRGHWSTARTSTOP; pixet.PX_ACQMODE_TDI - tdi mode, pixet.PX_ACQMODE_COMPRESSED - compression enabled (ModuPIX)
    acqPars.type = pixet.PX_ACQTYPE_FRAMES # or pixet.PX_ACQTYPE_TESTPULSES for test pulses
    acqPars.outputType = pixet.PX_FTYPE_NONE # output file type, PX_FTYPE_XXX constants. For autodetect by file extension: pixet.PX_FTYPE_AUTODETECT
    acqPars.fileName = "" # output file name
    acqPars.spacing = 1 # spacing acquisition, mostly for test pulses
    acqPars.integral = False # if the acquisition is integral -> only one frame created with sum of acqPars.count frames
    acqPars.refreshDacs = False # refresh detector DAC before acquisition
    acqPars.refreshPixCfg = False # refresh detector pixel configuration before acquisition

    # repeat parameters
    repPars = pixet.MpxRepeatParams()
    repPars.count = 1 # number of repetition. 1 = only one acquisition series made
    repPars.delay = 0 # delay in seconds between repetitions
    repPars.outputFlags = 0 # flags (mask of PX_REPEAT_XXX values) for specifing naming of files with repeat (create directories for each repeat PX_REPEAT_DIR, ...)
    repPars.outputDigits = 0 # number of digits for repeat counter in file name, 0 - automatic

    rc = device.doAcquisition(acqPars, repPars, None)
    print("Acquisition: %d" % rc)
    # note : test pulses are not supported at the moment
    pass

# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE - TIME DELAYED INTEGRATION (TDI)
# -----------------------------------------------------------------------------------
def acqExample5():
    # measures two frames in tdi mode
    acqPars = pixet.MpxAcqParams()
    acqPars.count = 2 # number of frames
    acqPars.time = 0.5 # time of one frame
    acqPars.mode = pixet.PX_ACQMODE_TDI
    acqPars.fileName = "" # output file name
    repPars = pixet.MpxRepeatParams()
    rc = device.doAcquisition(acqPars, repPars, None)
    print("Acquisition: %d" % rc)


# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE ADVANCED ACQUISITION
# -----------------------------------------------------------------------------------
def acqExample6():
    acqCount = 10
    acqTime = 0.1 # in seconds, 0.1 s
    acqType = pixet.PX_ACQTYPE_FRAMES # pixet.PX_ACQTYPE_DATADRIVEN, pixet.PX_ACQTYPE_TESTPULSES
    acqMode = pixet.PX_ACQMODE_NORMAL # pixet.PX_ACQMODE_TRG_HWSTART, pixet.PX_ACQMODE_TDI, ...
    fileType = pixet.PX_FTYPE_AUTODETECT
    fileFlags = 0
    outputFile = "test.pmf"
    device.doAdvancedAcquisition(acqCount, acqTime, acqType, acqMode, fileType, fileFlags, outputFile)

# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE ADVANCED ACQUISITION - INTEGRAL
# -----------------------------------------------------------------------------------
def acqExample7():
    acqCount = 10
    acqTime = 0.1 # in seconds, 0.1 s
    acqType = pixet.PX_ACQTYPE_FRAMES # pixet.PX_ACQTYPE_DATADRIVEN, pixet.PX_ACQTYPE_TESTPULSES
    acqMode = pixet.PX_ACQMODE_NORMAL # pixet.PX_ACQMODE_TRG_HWSTART, pixet.PX_ACQMODE_TDI, ...
    fileType = pixet.PX_FTYPE_AUTODETECT
    fileFlags = 0
    outputFile = "test.pmf"
    device.doAdvancedIntegralAcquisition(acqCount, acqTime, acqType, acqMode, fileType, fileFlags, outputFile)

# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE ABORT ACQUISITION
# -----------------------------------------------------------------------------------
def acqExample8():
    device.abortOperation()  # aborts runnign acquisition

# -----------------------------------------------------------------------------------
#                      ACQUISITION EXAMPLE WITH CALLBACK FOR EACH FRAME
# -----------------------------------------------------------------------------------

def callback(value):
    print("Callback " + str(value))
    # frame = dev.lastAcqFrameRefInc()
    # data = frame.data()
    # frame.destroy()

def acqExample9():
    dev.registerEvent(pixet.PX_EVENT_ACQ_FINISHED, callback, callback)
    dev.doSimpleAcquisition(20, 0.1, 0,  "")
    dev.unregisterEvent(pixet.PX_EVENT_ACQ_FINISHED, callback, callback)


# -----------------------------------------------------------------------------------
#                                   MAIN
# -----------------------------------------------------------------------------------
# uncomment the example you want to run
#acqExample1()
#acqExample2()
#acqExample3()
#acqExample4()
#acqExample5()
#acqExample6()
#acqExample7()
#acqExample8()
