TPX3_INDEX = 0
TPX3_TOT = 1
TPX3_TOA = 2

# get first Timepix3 device:
devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)
dev = devices[0]

# set Timepix3 operation mode:
dev.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
#dev.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
#dev.setOperationMode(pixet.PX_TPX3_OPM_TOA)
#dev.setOperationMode(pixet.PX_TPX3_OPM_TOT_NOTOA)


# make 10 frames acquisition, 0.1 s acq time and save it to file:
dev.doSimpleAcquisition(10, 0.1, pixet.PX_FTYPE_AUTODETECT, "/tmp/test1.pmf")

# make integral acquisition 100 frames, 0.1 s and save to file
dev.doSimpleIntegralAcquisition(100, 0.1, pixet.PX_FTYPE_AUTODETECT, "/tmp/test2.pmf")

# make data driven acquisition for 5 seconds and save to file:
dev.doAdvancedAcquisition(1, 1, pixet.PX_ACQTYPE_DATADRIVEN, pixet.PX_ACQMODE_NORMAL, pixet.PX_FTYPE_AUTODETECT, 0, "/tmp/test.t3pa")


# make data driven acquisition and process the pixels in the script. Note: if you want to process
# the data online you cannot save the data in the acquisition function. You can save them later by calling
# pixels.save()
dev.doAdvancedAcquisition(1, 1, pixet.PX_ACQTYPE_DATADRIVEN, pixet.PX_ACQMODE_NORMAL, pixet.PX_FTYPE_AUTODETECT, 0, "")


# get tpx3 pixels:
pixels = dev.lastAcqPixelsRefInc()
pixelCount = pixels.totalPixelCount()
pixelData = pixels.pixels()
print("PixelCount: %d " % pixelCount)

# get first pixel values:
matrixIndex = pixelData[TPX3_INDEX][0]
tot = pixelData[TPX3_TOT][0]
toa = pixelData[TPX3_TOA][0]

# get second pixel values:
matrixIndex = pixelData[TPX3_INDEX][1]
tot = pixelData[TPX3_TOT][1]
toa = pixelData[TPX3_TOA][1]

# save data to a file
pixels.save("/tmp/test2.t3pa", pixet.PX_FTYPE_AUTODETECT, 0)

pixels.destroy()

