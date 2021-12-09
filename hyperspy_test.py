import hyperspy.api as hs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["backend"] = "Agg"

hs.preferences.GUIs.warn_if_guis_are_missing = False
hs.preferences.save()

##################################################################
##################################################################

#s = hs.load("filename")
my_np_array = np.random.random((10,20,100))
s = hs.signals.Signal1D(my_np_array)
s = hs.signals.Signal1D(np.random.random((10, 20 , 100)))
s.axes_manager
s.axes_manager[0].name = "X"

if 0:
    s.axes_manager.gui()

if 1:
    hs.datasets.example_signals.EDS_TEM_Spectrum().plot()
    plt.show()

if 1: #artifical dataset
    s = hs.datasets.artificial_data.get_core_loss_eels_signal()
    s.plot()
    plt.show()

if 1: #function in hs.datasets can directly load spectra from The EELS Database
    hs.datasets.eelsdb(formula="B2O3")

if 1: #image stack  has signal dimension 2 and navigation dimension 1 and is stored in the Signal2D subclass
    im = hs.signals.Signal2D(np.zeros((30, 10, 20)))
    #im   < Signal2D, title:, dimensions: (30 | 20, 10) >


import kikuchipy as kp
kikuchi_dir = r'C:\ProgramData\Anaconda3\envs\py37\Lib\site-packages\kikuchipy'
datadir = kikuchi_dir + '/data/'

if 1: #from HyperSpy signal !!!!
    s_hs = hs.signals.Signal2D(np.random.random((20, 10, 60, 60)))
    s_hs.set_signal_type("EBSD")
    s_hs.set_signal_type("VirtualBSEImage")
    s_hs.set_signal_type("EBSDMasterPattern")

if 1:
    nordif_ebsd = "nordif/Pattern.dat"
    s = kp.load(datadir + nordif_ebsd)
    s_lazy = kp.load(datadir + nordif_ebsd, lazy = True)
    print(s_lazy)
    s_lazy_copy = s_lazy.inav[:2, :].deepcopy()
    s_lazy_copy.compute()

if 1:
    emsoft_master_pattern = (
        "emsoft_ebsd_master_pattern/ni_mc_mp_20kv_uint8_gzip_opts9.h5"
    )
    s_mp = kp.load(filename=datadir + emsoft_master_pattern)

if 1:
    emsoft_ebsd = "emsoft_ebsd/simulated_ebsd.h5"  # Dummy data set
    s_sim = kp.load(filename=datadir + emsoft_ebsd)
    s_sim2 = kp.load(filename=datadir + emsoft_ebsd, scan_size=(2, 5))
    print(s_sim2)
    print(s_sim2.data.shape)

if 1:
    s_test = hs.signals.Signal2D(np.zeros((3, 3, 256, 256)))
    s_test.set_signal_type("EBSD")
    s_test.set_signal_type("VirtualBSEImage")
    s_test.set_signal_type("EBSDMasterPattern")

