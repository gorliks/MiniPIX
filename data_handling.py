import hyperspy.api as hs
import numpy as np
import matplotlib.pyplot as plt

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