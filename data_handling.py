import hyperspy.api as hs
import kikuchipy as kp
import h5py
import numpy as np
import matplotlib.pyplot as plt
import os, glob
import utils

#matplotlib.rcParams["backend"] = "Agg"
hs.preferences.GUIs.warn_if_guis_are_missing = False
hs.preferences.save()

class Storage():
    def __init__(self):
        self.stack = []
        self.metadata = ''

    def test_artifical_data(self):
        s = hs.datasets.artificial_data.get_core_loss_eels_signal()
        s.plot()
        plt.show()

    def initialise(self, i=1, j=1, Nx=256, Ny=256):
        #self.data = hs.signals.Signal1D(np.random.random((10, 20, 100)))
        self.stack = hs.signals.Signal2D(np.zeros((i,j, Nx,Ny))) #i,j pixels in the image [Nx,Ny] spectra for each i,j pixel

    def populate_stack(self, new_data, slice_n):
        self.stack.data[slice_n] = new_data

    def save_stack(self, file_name):
        self.stack.save( file_name + '.hspy')

    def load_stack(self, stack):
        pass




if __name__ == '__main__':
    print('data handling')

    print('testing data loading')

    if 0:
        data_dir = r'C:\Users\sergeyg\Github\DATA.minipix_2022.04.14'
        all_h5_files = sorted(glob.glob( os.path.join(data_dir, '*.h5')  ))
        #file_name = r'19_30keV_spot2_mag200kx_perovskite_on_Si.h5'
        #file_name = os.path.join(data_dir, file_name)

        file_name = all_h5_files[4]

        #s = hs.load(file_name)
        #s = kp.load(filename=file_name)
        with h5py.File(file_name, 'r') as f:
           acqTime = list(f['Frame_0']['MetaData']['Acq time'])
           threshold = list(f['Frame_0']['MetaData']['Threshold'])
           data = f['Frame_0']['Data']
           data = np.reshape(data,(256,256))
           plt.imshow(np.log(data), cmap='gray')
           cbar = plt.colorbar()
           plt.text(0, 330, f"Vertical orientation \nAcquistion time: {acqTime} \nThreshold: {threshold}", fontsize=10)

        plt.show()

    if 1:
        print('testing background removal')
        data_dir = r'C:\Users\sergeyg\Github\DATA.minipix_2022.04.28\Si_100\stack_HfLaOsF2_220428.123020'
        stack_files = sorted(glob.glob( os.path.join(data_dir, '*Event.pmf')  ))

        Nx, Ny = utils.get_Nx_Ny_from_indices(data_dir, stack_files)
        print(Nx, Ny)

        stack = hs.signals.Signal2D(np.zeros((Nx, Ny, 256, 256)))  # i,j pixels in the i

        for file_name in stack_files:
            image = np.loadtxt(file_name)
            ii, jj = utils.get_indices_from_file_name(data_dir, file_name)
            stack.data[ii][jj] = image

        # convert hs.signals.Signal2D BaseSignal to EBSD (EBSDMasterPattern or VirtualBSEImage)
        stack.set_signal_type("EBSD")

        stack.remove_dynamic_background(operation="subtract", relative=True)